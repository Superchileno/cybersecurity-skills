# SKILL-HAYABUSA.md — Forense de Windows con Hayabusa

Fuente: `_src/mukul-anthropic/generating-forensic-timelines-with-hayabusa/`.

## Cuándo usarla
Timelines forenses rápidos de eventos Windows (evtx) con detección reglas Sigma/YARA integradas.

## Procedimiento resumido
1. Ejecutar: `hayabusa csv-timeline -d <dir_evtx> -o timeline.csv` (o `json-timeline`).
2. Reglas: include/exclude por nivel; `--no-wizard` para auto-detección.
3. Flags útiles: `-f` para key-value extra, `-M` (increase), orientación por alert level.
4. Filtrar por level high/critical y correlacionar (usuarios, hosts, tiempos).
5. Detección de alerta: `hayabusa logon-summary`, `-D` para dynamic profiles.
6. Exportar a CSV/JEQL para SIEM.

## Herramientas
`hayabusa` (descargar release), reglas/es incluidos. En Linux corre con wine (Windows evtx analysis) — en Kali preferir binario `.tar.gz` con `wine` o ejecutar en Windows.

## Guardrails
- Copias de evtx; no tocar originales. Evidencia redactada.