# SKILL-GDPR.md — Controles y derechos de datos GDPR

Fuente: `_src/mukul-anthropic/implementing-gdpr-data-subject-access-request/`.

## Cuándo usarla
Organizaciones que procesan datos personales de residentes UE (RGPD/LOPDGDD): implementar controles y gestionar DSAR.

## Procedimiento resumido
1. **Mapa de datos**: inventario de datos personales, finalidades, bases legales, flujos (procesadores/transferencias).
2. Controles: minimización, seudonimización, cifrado, retention policies, privacidad por diseño, DPO si procede.
3. **DSAR** (derechos del interesado): 
   - Identificar la solicitud (acceso, rectificación, supresión, portabilidad, objeción).
   - Verificar identidad del solicitante; plazos (< 1 mes, extensión excepcional).
   - Localizar todos los repositorios (SI, copias, backups, terceros procesadores).
   - Responder en formato accesible; documentar la respuesta (prueba de cumplimiento).
4. **Breaches**: notificación a autoridad ≤ 72h (si riesgo) e informar al afectado según riesgo.
5. Evaluación de impacto (DPIA) para procesamiento de alto riesgo.

## Referencias
- GDPR (UE 2016/679), LOPDGDD 3/2018 (España), guías EDPB/AEPD.

## Guardrails
- Tratar solicitudes como mínimo privilegio: verificación de identidad antes de revelar datos.