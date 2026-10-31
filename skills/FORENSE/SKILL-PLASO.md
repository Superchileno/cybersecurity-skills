---
name: forense-plaso
description: 'Construir timeline forense integral a partir de múltiples fuentes (filesystem, registro, eventos, navegadores, logs). Keywords: forense, plaso.'
area: FORENSE
tags: [forense, plaso]
source: '_src/mukul-anthropic/building-super-timelines-with-plaso/'
license: Apache-2.0
---

# SKILL-PLASO.md — Super timelines con Plaso (log2timeline)

Fuente: `_src/mukul-anthropic/building-super-timelines-with-plaso/`.

## Cuándo usarla
Construir timeline forense integral a partir de múltiples fuentes (filesystem, registro, eventos, navegadores, logs).

## Procedimiento resumido
1. Parsear el fuente con `log2timeline` (Plaso):
   `log2timeline.py --storage_file evidence.plaso <imagen>` (parsers por default; filtrar con `--parsers`).
2. Completar con artefactos extra (eventos, registry) si aplica.
3. Generar timelines:
   - `psort.py -o l2tcsv evidence.plaso > timeline.csv` (línea CSV).
   - `-o elastic` para indexar en Elastic.
4. Filtrar tiempos intrritos/ataque; buscar artefactos sospechosos (ejecución de binarios, cuentas).
5. Combinar con body file de MFT (`fls -m` + `mactime`).

## Herramientas
Plaso (`log2timeline.py`, `psort.py`), `fls`, `mactime`.

## Guardrails
- Imágenes autorizadas; evidencia con cadena de custodia.