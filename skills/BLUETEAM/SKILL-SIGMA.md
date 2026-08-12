# SKILL-SIGMA.md — Building detection rules with Sigma

Fuente: `_src/mukul-anthropic/building-detection-rules-with-sigma/`.

## Cuándo usarla
Crear reglas de detección portable/SIEM-agnóstico, o convertir entre Sigma ↔ Splunk/Elastic/QRadar.

## Procedimiento resumido
1. Identificar la técnica a detectar (MITRE ATT&CK) y los datos concretos (log source, fields).
2. Escribir la regla YAML Sigma:
   - `title`, `id`, `status`, `description`, `author`, `date`, `tags` (mitre), `logsource` (category/product/service), `detection` (selección + condición), `falsepositives`, `level` (informational/low/medium/high/critical).
3. Validar sintaxis: `sigmac --lists` / `sigmac -t splunk -p` (pipeline).
4. Convertir: `sigmac -t splunk rule.yml` o herramienta `sigma-cli`.
5. Testear contra datos reales; ajustar la condición para reducir falsos positivos.

## Herramientas Kali
`sigma-cli` / `sigmac` (pip). No están instaladas → instalarlas antes.

## Guardrails
- Reglas validadas y testeadas; documentar técnica/false positives en el campo `description`.