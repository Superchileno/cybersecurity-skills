# Polyglots, carving y capas de contenedores

## 1. Por qué funciona

Los formatos de archivo son estructuras **delimitadas**: tienen cabecera, cuerpo y un
marcador de fin. Nada impide que después del fin venga otro archivo completo, o que
un mismo prefijo sea válido en dos formatos. Los retos explotan exactamente eso.

## 2. Marcadores de fin reales

| Formato | Fin lógico | Trampa |
|---|---|---|
| PNG | chunk `IEND` completo: `pos(IEND) + 8` | `find(b"IEND")` devuelve el inicio del **tipo**; hay que sumar longitud y CRC (4+4) |
| JPEG | `FF D9` (EOI) | Puede haber miniaturas EXIF antes; usar el **último** `FFD9` |
| GIF | `0x3B` | Puede aparecer dentro de los datos; validar con parser |
| ZIP | fin de directorio central `PK\x05\x06` | El tamaño del comentario final se suma |
| PDF | `%%EOF` | Puede haber varios por actualizaciones incrementales; el último es el válido |
| WAV/RIFF | tamaño declarado en cabecera (`RIFF` + 4 bytes) | Comparar con el tamaño real del archivo |

## 3. Polyglot PNG + ZIP (patrón más común)

Estructura típica:

```
[0x0000] 89 50 4E 47 0D 0A 1A 0A   cabecera PNG
...
[0x3554] 00 00 00 00 49 45 4E 44   chunk IEND (tipo en +4)
[0x355C] 50 4B 03 04 ...           ZIP anexado
```

Extracción:

```python
fin = data.rfind(b"IEND") + 8
cola = data[fin:]
abrir(cola como zipfile.BytesIO)
```

Si el ZIP no abre, probar también `find(b"PK\x03\x04")` directo: a veces hay relleno
entre el IEND y el ZIP.

## 4. Cadenas de capas reales (para calibrar expectativas)

- `nivel1.zip` → `nivel2.gz` → gunzip → texto ASCII85 → `a85decode` → `nivel3.zip`
  → `flag.txt` cifrado con contraseña que estaba en un chunk `tEXt`.
- JPEG → ZIP anexado → `secreto.txt` con texto cifrado César → flag.
- PNG → QR → grupos de 8 bits → ASCII → flag.
- DOCX → `customXml/item1.xml` con Base64 → ZIP → `.dat` con payload hex → flag.

Patrón: **cada capa cambia el formato o el alfabeto**. Si una transformación no cambia
ninguno de los dos, probablemente no es una capa.

## 5. ZIP: detalles que rompen scripts

- Un ZIP puede tener entradas cifradas y otras no.
- `zipfile` de Python lee bien ZipCrypto; AES-256 requiere `pyzipper`.
- El CRC del `ZipInfo` permite **verificar** que la contraseña es correcta sin mirar
  el contenido: si el CRC del descifrado coincide con el declarado, la clave es buena.
- Para known-plaintext, `bkcrack` necesita al menos 12 bytes conocidos continuos
  (el prefijo `flag{` o `flag{` suele bastar) y el método `stored` o `deflate`.

## 6. Overlay en ejecutables

Un ELF puede pesar 8 MB con `.text` de 3 KB: el resto es relleno. Comprobar:

```bash
readelf -SW binario        # tamaño de secciones
stat -c %s binario         # tamaño real
```

Si el tamaño real supera con creces el final de la última sección, hay overlay. En un
reto el overlay era **cebo** y el secreto estaba en el bytecode de `.rodata`.

## 7. Regla de oro

Antes de asumir cifrado, verificar que el archivo **no esté dañado**. Un solo byte
reparado (firma PNG o `PK\x03\x04`) resolvió dos retos completos y evitó horas de
criptoanálisis inútil.
