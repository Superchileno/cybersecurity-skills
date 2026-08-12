# SKILL-WPSCAN.md — WordPress security

## Cuándo usarla
Se detecta WordPress (whatweb/nmap) y toca evaluar plugins, themes, XMLRPC, REST.

## Procedimiento resumido
1. Escaneo base: `wpscan --url <url> --enumerate ap,at,tt,vt, cb`
   (con token API para matching avanzado: `--api-token <TW>`, opcional).
2. Plugins vulnerables → cazar CVEs (`redteam/wp-plugin-cve-hunt`, `wordpress-plugin-hunt`).
3. XMLRPC: `wp.getUsersBlogs` para user enum / brute; `system.multicall` para
   amplificación de brute-force (`xmlrpc-exploitation`).
4. REST auth bypass (`wp-plugin-rest-auth-bypass`), CORS+X(MLRPC) chains
   (`cors-credential-wordpress`, `wordpress-cors-xmlrpc-rce-chain`).
5. Post: subir tema/plugin con PHP, `wp-config.php` leak via LFI.

## Clasificación
- Plugin vulnerable confirmado (payload) → L3/L4 según impacto. User enum → L2/L3.

## Herramientas
`wpscan`, `curl`, `hydra` (solo con wordlists acotadas y autorización).

## Guardrails
- Brute-force: respetar límite y evitar bloqueos de cuenta reales.
- No instalar/deploy loads sin aprobación. Evidencia con request+response.