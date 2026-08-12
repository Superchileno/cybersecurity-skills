# SKILL-HUNTING-ELASTIC.md — Threat hunting con Elastic SIEM

Fuente: `_src/mukul-anthropic/performing-threat-hunting-with-elastic-siem/`.

## Cuándo usarla
Hunting estructurado de amenazas sobre Elastic Stack (potencialmente WELK ya desplegado).

## Procedimiento resumido
1. Definir hipótesis (ver `SKILL-HUNTING.md` / MITRE ATT&CK).
2. Buscar con KQL/Lucene en Discover; o usar EQL para correlación de eventos.
3. Enrichment: joins con logs de contexto (usuarios activos, sessions).
4. Visualizar en Kibana; guardar como saved search + alert rule.
5. Documentar hallazgos con evidencia (tickets, timeline).

## Herramientas
Elastic Stack (Kibana/Discover), consultas EQL/KQL.

## Guardrails
- Hunting sobre datos reales de producción: solo lectura; no abrir artefactos maliciosos.
- Evidencia redactada (PII) en el informe de hunting.