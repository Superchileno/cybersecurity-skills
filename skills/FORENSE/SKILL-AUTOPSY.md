# SKILL-AUTOPSY.md — Análisis de imágenes de disco con Autopsy

Fuente: `_src/mukul-anthropic/analyzing-disk-image-with-autopsy/`.

## Cuándo usarla
Análisis forense de imágenes de disco Windows/Linux (filesystem, correo, navegador, borrados).

## Procedimiento resumido
1. Crear case en Autopsy y añadir la imagen (E01/raw).
2. Ingestores: file hashing, keyword search, timeline, extension mismatch, EXIF, email.
3. Explorar: debris (papelera), deleted files, unallocated space, MFT.
4. Timeline del caso; filtros por fecha/usuario.
5. Exportar report HSL/HTML con hallazgos y bookmarks (marcadores).

## Herramientas
Autopsy (GUI). Para CLI triage se prefiere `tsk_recover`/`fls` (Sleuth Kit, ya incluido).

## Guardrails
- Imágenes de disco autorizadas; cadena de custodia documentada (hash al adquirir).
- PII en reportes redactada.