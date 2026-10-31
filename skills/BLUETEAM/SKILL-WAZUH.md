---
name: blueteam-wazuh
description: 'Desplegar/operar Wazuh (HIDS/EDR open-source) para detección en endpoints. Keywords: blueteam, wazuh.'
area: BLUETEAM
tags: [blueteam, wazuh]
source: '_src/mukul-anthropic/implementing-endpoint-detection-with-wazuh/'
license: Apache-2.0
---

# SKILL-WAZUH.md — EDR/HIDS con Wazuh

Fuente: `_src/mukul-anthropic/implementing-endpoint-detection-with-wazuh/`.

## Cuándo usarla
Desplegar/operar Wazuh (HIDS/EDR open-source) para detección en endpoints.

## Procedimiento resumido
1. Desplegar servidor Wazuh (manager + indexer/dashboard) y agent en endpoints.
2. Módulos clave: FIM (integridad), SCA (CIS checks), Syscheck, active response, vulnerability scanning (agent).
3. Escribir reglas/decoders personalizados en `/var/ossec/etc/` si hace falta (SODB canonical).
4. Correlar alertas por host/rule level y alimentar SIEM externo (syslog).
5. Investigar alertas y ajustar niveles para reducir ruido.

## Herramientas
Wazuh manager/agent, dashboard alerts.

## Guardrails
- Agentes en endpoints de producción: coordenarse antes de active-response (bloqueos).