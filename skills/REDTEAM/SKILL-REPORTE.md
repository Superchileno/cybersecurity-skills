# SKILL-REPORTE.md — Escritura de reportes

## Cuándo usarla
Generar el informe final de un engagement (fuente: `redteam/report-writing`,
`redteam/redteam-report-template`, `skills/_src/.../web-pentest` templates).

## Estructura (plantilla)
1. Resumen ejecutivo (lenguaje preciso: "no se encontraron issues explotables en
   alcance X, tiempo T, métodos Y" — nunca "la app es segura").
2. Alcance del engagement (`scope.txt`).
3. Autorización (`authorization.md`).
4. Hallazgos (solo L3/L4 con prueba): título, severidad **CVSS 3.1 + CWE**,
   endpoint(s), prueba (request+response), reproducción, impacto, remediación.
5. No-explotados (L1/L2 con nota de qué los bloqueó).
6. Observaciones fuera de alcance.
7. Metodología/herramientas.
8. Limitaciones y qué NO se probó.

## Reglas
- CVSS solo para L3/L4 (ver `AGENTS.md`).
- Evidencias redactadas (ver `SKILL-EVIDENCIA.md`).
- Idioma: español (salvo petición del cliente).

## Guardrails
- Reporte = assessment, no "PASS". Mantener el lenguaje de limitaciones.