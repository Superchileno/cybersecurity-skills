# SKILL-BGP-HIJACK.md — Evaluación de hijacking BGP y mitigación RPKI

Fuente: `_src/mukul-anthropic/exploiting-bgp-hijacking-vulnerabilities/`, `implementing-bgp-security-with-rpki`.

## Cuándo usarla
Entender/validar el riesgo de secuestro BGP de rangos de la organización (routing security), y mitCon RPKI (de forma defensiva/auditoría).

## Procedimiento resumido
1. **Auditoría pasiva**: consultar fuentes públicas (bgp.he.net, RIPEstat, RPKI validity via `rpki-client`/routinator) del ASN/rango propio.
2. Verificar RPKI: origin validation (ROA existente), Route Origin Authorization de los prefijos.
3. Detectar anomalías de anuncio (hijack): cambios de AS path inesperados (BGPmon, GreyNoise/Honeypot feeds).
4. **Hijacking test en laboratorio**: emular anuncio en entorno de simulación (no en producción); medir impacto (mopping-trust).
5. **Mitigación**: crear ROA/ROV con tu RIR (RIPE NCC), filtrar con `rpki-client` en routers; mitigación en peers (RPKI ROV en todos).
6. Documentar: BGP is trust model débil; recomendar RPKI y filtrado origen.

## Herramientas
`rpki-client`, `routinator` (RIPE), bgpview/HE, BGPmon.

## Guardrails
- No anunciar prefijos ajenos/en producción; el test es solo en simulador autorizado.