---
name: analyzing-file-artifacts-for-steganography
description: 'Detecta y extrae información oculta en archivos de un CTF: polyglots
  (PNG+ZIP, JPEG+ZIP), datos anexados tras los marcadores IEND/EOI/EOF, ZIP anidados,
  LSB en imágenes (bit 0 y superiores), mosaicos con periodo repetido, documentos OOXML
  con texto blanco o customXml, y cadenas de capas Base64/hex/gzip/ASCII85. Incluye
  catálogo de señuelos y reglas de validación para no confundir una decodificación
  plausible con la flag real. Usar con cualquier archivo "raro" entregado en un reto:
  imágenes, ZIP, DOCX, PDF o binarios con overlay.'
domain: cybersecurity
subdomain: ctf
tags:
- ctf
- steganography
- polyglot
- lsb
- carving
- ooxml
- docx
- zip
- png
- jpeg
- binwalk
version: '1.0'
author: auditoria-ia-v2
license: Apache-2.0
mitre_attack:
- T1027
- T1140
- T1005
nist_csf:
- DE.AE-02
- DE.CM-01
---

# Análisis de Artefactos y Esteganografía en CTF

Extrae capas ocultas de archivos aparentemente normales, en el orden que menos tiempo
cuesta, y distingue el resultado real de los señuelos que el reto coloca a propósito.

## When to Use

- El reto entrega una imagen, ZIP, DOCX, PDF, WAV o un binario que "no hace nada".
- `file` identifica el archivo pero su contenido visible es coherente y sin pistas.
- Ya se intentó `strings`/`exiftool` y no apareció nada.
- Se sospecha polyglot: el archivo abre bien pero pesa más de lo que debería.
- Hay que validar si un texto decodificado es la flag o un cebo.

**No usar** para análisis de malware real (aquí no hay contención ni sandbox) ni para
archivos fuera del alcance del reto.

## Prerequisites

- `binwalk`, `foremost`, `exiftool`, `pngcheck`, `xxd`, `zsteg` (opcional),
  `steghide` (opcional), Python 3 con `Pillow` y `numpy`.
- Scripts de esta skill (`scripts/`).
- Copia de trabajo: **nunca** modificar el artefacto original; trabajar sobre copia
  en `work/`.

## Workflow

### 1. Caracterizar antes de extraer

```bash
python scripts/ctf_triage.py reto.png          # de la skill de metodología
file reto.*; exiftool reto.*; binwalk reto.*
```

Anotar: tamaño real, tamaño esperado por la cabecera, firmas encontradas y su offset.

### 2. Datos tras el marcador de fin (lo más frecuente)

```bash
python scripts/carve_appended.py reto.png --out work/
```

El script localiza el fin lógico real (ojo: `find(b"IEND")` cae en el **tipo** del
chunk, el fin verdadero es `pos+8`) y extrae lo que haya después. Si la cola es un
ZIP, lo lista y extrae.

### 3. Capas de contenedores

```bash
python scripts/zip_nested.py reto.zip --out work/capas
```

Desanida en memoria (sin llenar el disco) y registra el nombre y tamaño de cada capa.
Si una capa está cifrada, se detiene y reporta la contraseña necesaria.

### 4. Documentos OOXML (DOCX/XLSX/PPTX)

```bash
python scripts/ooxml_scan.py reto.docx --out work/ooxml
```

Busca: texto con `w:color="FFFFFF"`, `w:vanish`, tamaño 1, `customXml`, headers y
footers, comentarios, y blobs Base64/hex dentro de cualquier parte XML.

### 5. Imágenes

Orden de pruebas (registrar cada una para no repetir):

1. LSB bit 0, orden píxel-interleaved (R,G,B), desde offset 0.
2. LSB bits 1–3.
3. Planos por canal / por fila.
4. Periodo de mosaico por autocorrelación.
5. Comparación con un desplazamiento del propio patrón.

```bash
python scripts/lsb_extract.py reto.png --bit 0 --order interleaved
python scripts/reveal_pattern.py reto.png --out work/
```

### 6. Cadenas de codificación

Cuando el contenido extraído es texto: identificar por **alfabeto y longitud**, no por
intuición. Hex → ASCII → Base45 → Base64 → Ook! → Brainfuck fue una cadena real.
Regla práctica: si `set(texto)` cabe en el alfabeto de una codificación y la longitud
es múltiplo de su unidad, probarla.

### 7. Validación

- La flag debe cumplir el formato oficial y tener palabras legibles.
- Si el texto es "casi" la flag (un carácter cambiado, prefijo corrupto), sospechar
  de catálogo trocado o polaridad invertida — no de un error de tipeo.

## Key Concepts

- **Polyglot:** archivo válido en dos formatos. La parte 2 empieza exactamente donde
  termina la 1; se localiza por firma (`PK\x03\x04`, `\x1f\x8b`, etc.).
- **Carving:** extraer un objeto embebido usando su firma y su estructura, sin
  depender de un parser que puede rechazar el contenedor.
- **Fin lógico:** el marcador de fin del formato (IEND, EOI, `%%EOF`, fin de
  directorio ZIP). Todo lo que sigue es candidato.
- **LSB interleaved:** el bit menos significativo de cada componente de color, en
  orden R,G,B por píxel, fila a fila. Es el esquema más común en retos.
- **Periodo de mosaico:** si la imagen repite un patrón cada N píxeles, restar la
  imagen desplazada N deja visible lo que no sigue el patrón.
- **Señuelo:** capa que decodifica a texto plausible. Se descarta por estructura
  (prefijo, CRC, longitud), no por gusto.

## Tools & Systems

| Tarea | Comando |
|---|---|
| Firmas y offsets | `binwalk -eM`, `scripts/ctf_triage.py` |
| Carving genérico | `foremost -i archivo -o work/` |
| ZIP anidado | `scripts/zip_nested.py`, `7z l -slt` |
| ZIP cifrado | `zip2john` + `john --wordlist=rockyou.txt` |
| ZIP known-plaintext | `bkcrack -C x.zip -c flag.txt -p known.txt` |
| PNG estructura | `pngcheck -v`, `scripts/carve_appended.py` |
| LSB | `scripts/lsb_extract.py`, `zsteg -a` |
| Mosaico | `scripts/reveal_pattern.py` |
| OOXML | `scripts/ooxml_scan.py`, `unzip -o docx -d work/` |
| Estego clásica | `steghide extract -sf img.jpg`, `stegseek` |

## Common Scenarios

### "Tras el IEND hay basura"
Casi siempre es un ZIP. Extraerlo por offset (`data[pos:]`) y listar con `zipfile`.
Si el primer intento falla, revisar el offset: `IEND` + 4 bytes de tipo + 4 de CRC
es el fin real del chunk.

### "La imagen pesa el doble de lo que debería"
Comparar el tamaño declarado en la cabecera (ancho × alto × canales + overhead) con
el tamaño real. Un exceso grande indica payload anexado u overlay.

### "El DOCX sólo tiene el texto del acta"
El cuerpo no es donde está. Revisar `word/header*.xml`, `word/footer*.xml`,
`customXml/`, `docProps/` y `word/comments.xml`. Texto en blanco (`FFFFFF`) o con
`w:vanish` es invisible en el visor y visible en el XML.

### "El LSB no da nada"
Puede estar en bits 1–3, en un solo canal, o con orden planar. También puede no haber
LSB: en varios retos el secreto era el **tamaño/periodo** (mosaico) o un chunk
`tEXt`. Registrar los parámetros probados evita repetirlos.

### "Hay un QR pero el contenido son ceros y unos"
Convertir grupos de 8 bits a ASCII antes de buscar la flag.

## Output Format

```markdown
## Evidencia
- archivo, tamaño, SHA-256
- firmas encontradas y offsets
- fin lógico: 0x... ; bytes posteriores: N

## Capas
1. <contenedor> → <extracción> → <resultado>
2. ...

## Señuelos descartados
- <artefacto> → <texto> ; descartado por <razón estructural>

## Flag
`...`
```

Referencias: `references/polyglots_y_carving.md`, `references/ooxml_y_documentos.md`,
`references/lsb_y_visual.md`.
