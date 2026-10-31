# Documentos OOXML y PDF — dónde se esconde el texto

Un `.docx`/`.xlsx`/`.pptx` es un ZIP con partes XML. El visor muestra una fracción de
lo que contiene el paquete.

## 1. Mapa de partes relevantes

| Parte | Qué buscar |
|---|---|
| `word/document.xml` | texto con `w:color="FFFFFF"`, `w:vanish`, `w:sz` muy pequeño |
| `word/header*.xml` | **muy usado**: la flag en la cabecera que nadie mira |
| `word/footer*.xml` | igual que la cabecera |
| `word/comments.xml` | comentarios del revisor |
| `word/settings.xml` | `w:trackChanges`, revisiones |
| `customXml/item*.xml` | cachés propietarias, blobs Base64/hex |
| `docProps/core.xml`, `app.xml` | metadatos, autor, títulos |
| `word/media/` | imágenes embebidas (aplicarles todo el pipeline de imágenes) |
| `word/embeddings/` | objetos OLE incrustados (pueden ser ZIP o ejecutables) |

Verificación rápida de la firma antes de descomprimir:

```bash
xxd -l 8 documento.docx     # debe ser 50 4B 03 04
```

Un reto tenía `50 15 78 04`: reparar los 4 primeros bytes a `PK\x03\x04` abrió el
paquete y dejó ver el texto blanco.

## 2. Texto invisible: variantes

```xml
<w:r><w:rPr><w:color w:val="FFFFFF"/></w:rPr><w:t>flag{...}</w:t></w:r>
<w:r><w:rPr><w:vanish/></w:rPr><w:t>flag{...}</w:t></w:r>
<w:r><w:rPr><w:sz w:val="2"/></w:rPr><w:t>flag{...}</w:t></w:r>
```

También puede estar en un `w:instrText` (campo), en `w:fldSimple` o dentro de un
`w:del` (texto borrado con control de cambios).

Extracción robusta: recorrer **todos** los `w:t` con su estilo y marcar los que sean
blancos, ocultos o de tamaño < 6.

## 3. `customXml` y cachés propietarias

Patrón observado:

```xml
<cache xmlns="urn:organizacion:cache:v1" channel="VF-12" encoding="base64">
  UEsDBBQAAAAI...
</cache>
```

`UEsDBBQ` es Base64 de `PK\x03\x04`: un ZIP dentro del XML. Dentro había un `.dat`
con `encoding=hex` y el payload de la flag.

Regla: cualquier atributo `encoding=` es una instrucción de decodificación; respetarla.

## 4. PDF

```bash
pdfid documento.pdf            # /JS /JavaScript /OpenAction /AA /EmbeddedFile
pdf-parser -a documento.pdf    # objetos y streams
```

- Texto invisible: mismo truco de color de relleno igual al fondo.
- Capas (OCG): contenido en capas desactivadas.
- Streams comprimidos: `pdf-parser --decompress`.
- Adjuntos: `/EmbeddedFile`.

## 5. Metadatos que valen oro

`exiftool` sobre el documento y sobre las imágenes internas. En un reto OSINT, el
`Artist` y el `UserComment` de una foto revelaron el nombre de un perfil espejo que
contenía la flag.

Campos a revisar siempre: `Artist`, `Copyright`, `UserComment`, `ImageDescription`,
`XPComment`, `XPAuthor`, `DateTimeOriginal`, `GPS*`, `Software`.

## 6. Checklist OOXML

- [ ] Firma correcta (reparar si no)
- [ ] `unzip -l` completo: ¿partes inesperadas?
- [ ] `document.xml`: runs blancos / ocultos / tamaño mínimo
- [ ] `header*.xml` y `footer*.xml`
- [ ] `comments.xml`
- [ ] `customXml/`
- [ ] `docProps/`
- [ ] `media/` (pipeline de imágenes)
- [ ] `embeddings/`
- [ ] Base64/hex en cualquier parte
