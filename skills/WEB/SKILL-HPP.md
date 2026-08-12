# SKILL-HPP.md — HTTP Parameter Pollution

Fuente: `_src/mukul-anthropic/performing-http-parameter-pollution-attack/`.

## Cuándo usarla
Frameworks/backends que no tratan igual parámetros duplicados (primero/último/array) — deriva en lógica rota, auth bypass, SSRF/redirect.

## Procedimiento resimido
1. Identificar endpoints con parámetros controlados; enviar el mismo param dos veces:
   ```
   /search?q=admin&q=value2
   /api/user?id=1&id=2
   ```
2. Confirmar cuál gana (último/primero/concatenado) probando respuesta.
3. Explotación: bypass de auth (`role=user&role=admin`), bypass filtros WAF (uno sanitizado otro no), cambiar lógica (pricing), redirect/host header `redirect=http://evil&redirect=/ok`.
4. Ver cómo lo tratan los proxies (request smuggling de params).
5. Documentar con request+response.

## Herramientas
Burp (Repeater/Intruder), curl.

## Guardrails
- Solo targets autorizados; payload no destructivo.