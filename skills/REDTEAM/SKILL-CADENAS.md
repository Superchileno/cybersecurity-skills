# SKILL-CADENAS.md — Cadenas de ataque

## Cuándo usarla
Cuando varios hallazgos parciales se pueden conectar para un impacto mayor
(ej. subdomain takeover → phish auth → ATO, o upload → LFI → RCE).

## Procedimiento resumido
1. Inventariar hallazgos con su nivel (L1–L4) y clases (OWASP).
2. Construir el grafo: qué primitiva habilita cuál (source→sink).
   Mapearlo con MITRE ATT&CK y OWASP ASVS.
3. Validar cada "arista" con evidencia reproducible (request/response) antes de
   asumir el salto.
4. Probar la cadena completa con autorización y mínimo impacto; testimoniar
   cada paso (`chains/cross-attack-chains`).
5. El impacto de la cadena = severidad agregada (CVSS compuesto si aplica).

## Referencias _src
- `chains/cross-attack-chains`, `chains/wordpress-full-compromise`
- Pares clásicos: `wordpress-cors-xmlrpc-rce-chain`, `cors-credential-wordpress`

## Guardrails
- Cada paso de la cadena requiere su propia evidencia; no encadenar "probablemente".
- Pivot entre hosts = nueva aprobación explícita.