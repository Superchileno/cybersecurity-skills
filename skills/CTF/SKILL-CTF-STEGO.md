---
name: ctf-stego
description: 'Detección y extracción de información oculta en archivos: polyglots
  (PNG+ZIP, JPEG+ZIP), datos tras los marcadores IEND/EOI/EOF, ZIP anidados, LSB en
  imágenes, mosaicos con periodo repetido, documentos OOXML con texto blanco o
  customXml y cadenas de capas Base64/hex/gzip. Usar con imágenes, ZIP, DOCX, PDF o
  binarios con overlay sospechoso.
  Keywords: steganography, polyglot, LSB, carving, zip nested, ooxml, binwalk.'
area: CTF
tags: [ctf, stego, polyglot, lsb, ooxml, carving]
source: _full/analyzing-file-artifacts-for-steganography
license: Apache-2.0
---

# SKILL-CTF-STEGO.md — Esteganografía y artefactos

Fuente: `_full/analyzing-file-artifacts-for-steganography/`.

## Cuándo usarla
El archivo abre correctamente pero no aporta nada; pesa más de lo esperado; hay
sospecha de polyglot o de capas anidadas.

## Procedimiento resumido
1. Caracterizar: `ctf-arsenal triage archivo`, firmas, offsets y entropía.
2. Datos tras el fin lógico: `ctf-arsenal carve archivo` (ojo: `IEND+8`).
3. Contenedores: `ctf-arsenal zip archivo` para desanidar en memoria.
4. OOXML: `ctf-arsenal ooxml documento.docx` (texto blanco, `customXml`, headers).
5. Imágenes: bit 0 interleaved primero; luego bits 1–3; `ctf-arsenal pattern` para
   mosaicos.
6. Cadenas: identificar por alfabeto y longitud, no por intuición.
7. Validar con prefijo de flag, CRC o round-trip antes de aceptar.

## Clasificación de hallazgo
- Payload extraído con estructura válida → confirmado.
- Texto legible sin formato de flag → señuelo, documentar y seguir.

## Herramientas
`ctf-arsenal`, `binwalk`, `foremost`, `exiftool`, `pngcheck`, `zsteg`, `7z`.

## Guardrails
- Trabajar sobre copia; nunca modificar el artefacto original.
- Registrar cada parámetro LSB probado para no repetirlo.
