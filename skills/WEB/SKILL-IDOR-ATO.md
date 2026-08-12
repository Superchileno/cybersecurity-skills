# SKILL-IDOR-ATO.md — IDOR / Auth flaws / ATO

## Cuándo usarla
Endpoints con IDs secuenciales/adivinables (`/user/1`, `/order?id=100`), APIs REST,
lambda auth, broken function-level auth.

## Procedimiento resumido
1. Recoger IDs reales con **dos** cuentas propias (A y B).
2. Probar `A` accediendo al recurso de `B` cambiando el ID (probar `1`, `2`, `next`).
3. Bypass de auth: métodos alternativos (`POST/GET`), `X-Original-URL`, `X-Rewrite-URL`,
   quitar headers, mass assignment en body, cookies/sesión manipulada.
4. ATO: password reset flow (token en respuesta/URL/header), OAuth state/hostheader,
   MFA bypass (`hunt-mfa-bypass`, `hunt-ato`).
5. Confirmar con cambio observable del estado del objeto (L3) o acceso a datos de
   otra cuenta (L4).

## Clasificación
- Acceso a objeto de otro usuario → L3; escalada a admin/otra cuenta → L4.

## Herramientas
Burp, `curl`, scripts de enumeración sencillos (`seq 1 100` + jq).

## Guardrails
- Solo con cuentas de test propias; no tocar datos reales de terceros.
- No truncar/mutar inventario de la BD objetivo sin aprobación.