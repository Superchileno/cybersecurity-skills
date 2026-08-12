# WEB — Subskills de pentest web

Área: enumeración web, clases de vulnerabilidad (OWASP Top 10), frameworks,
WordPress e APIs. Fuente completa: `skills/_src/recon-skills/redteam/hunt-*`,
`skills/_src/recon-skills/recon/*`, `skills/_src/hermes-security/web-pentest`,
`skills/_src/mukul-anthropic/*`.

## Subskills destiladas

| Subskill | Cuándo usarla | Fuente |
|---|---|---|
| `SKILL-WEBPENTEST.md` | Metodología completa faseada (autorización→recon→análisis→exploit→reporte) | `hermes-security/web-pentest/SKILL.md` (oficial) |
| `SKILL-ENUM-WEB.md` | Enumeración web: paths, ficheros, tecnología, source maps | `recon/web-enumeration`, `recon/js-secrets-extraction` |
| `SKILL-SQLI.md` | SQL injection (todos los tipos + bypass) | `redteam/hunt-sqli` |
| `SKILL-XSS.md` | XSS reflejado/almacenado/DOM (+ DOM advanced) | `redteam/hunt-xss`, `redteam/hunt-dom` |
| `SKILL-SSRF.md` | Server-Side Request Forgery | `redteam/hunt-ssrf` |
| `SKILL-LFI-RCE.md` | LFI, RCE, phpinfo→RCE | `redteam/hunt-lfi`, `redteam/hunt-rce`, `recon/phpinfo-to-rce` |
| `SKILL-UPLOAD.md` | File upload bypass | `redteam/hunt-file-upload` |
| `SKILL-IDOR-ATO.md` | IDOR / Account Takeover / auth bypass | `redteam/hunt-idor`, `redteam/hunt-ato`, `redteam/hunt-auth-bypass` |
| `SKILL-WPSCAN.md` | WordPress: plugins, XMLRPC, REST auth bypass (wpscan) | `recon/wordpress-plugin-hunt`, `recon/xmlrpc-exploitation`, `recon/wp-*` |
| `SKILL-API.md` | APIs: no-auth, GraphQL, misconfig | `redteam/hunt-graphql`, `redteam/hunt-api-misconfig`, `recon/api-noauth-hunt` |
| `SKILL-THICK-CLIENT.md` | Pentest de clientes gordos (escritorio) | `mukul-anthropic/performing-thick-client-application-penetration-test` |
| `SKILL-XML-INJECTION.md` | XXE / XML injection | `mukul-anthropic/testing-for-xml-injection-vulnerabilities` |
| `SKILL-HPP.md` | HTTP Parameter Pollution | `mukul-anthropic/performing-http-parameter-pollution-attack` |
| `SKILL-PROMPT-LEAK.md` | Fuga de system prompt en LLM | `mukul-anthropic/testing-for-system-prompt-leakage` |

## Enrutado al _src (para detalle por clase)

- Auth y SSO: `redteam/hunt-oauth`, `redteam/hunt-saml`, `recon/jwt-attack`, `auth/saml-sso-attack`
- Redirección/Smuggling/Prototype: `hunt-open-redirect`, `hunt-http-smuggling`, `hunt-prototype-pollution`
- Frameworks: `hunt-aspnet`, `hunt-django`, `hunt-fastapi`, `hunt-nodejs`, `hunt-nestjs`, `hunt-nextjs`, `hunt-springboot`, `hunt-laravel`, `hunt-sharepoint`
- Cloud/DevOps: `hunt-cicd`, `hunt-k8s`, `hunt-cloud-misconfig`, `hunt-firebase`
- Misc high-value: `hunt-deserialization`, `hunt-race-condition`, `hunt-ssti`, `hunt-xxe`, `hunt-nosqli`, `hunt-csrf`, `hunt-cors`, `hunt-host-header`, `hunt-session`, `hunt-grpc`, `hunt-ldap`, `hunt-ntlm-info`, `hunt-websocket`, `hunt-mfa-bypass`, `hunt-cache-poison`, `hunt-source-leak`, `hunt-information-disclosure`, `hunt-brute-force`, `hunt-business-logic`, `hunt-misc`

## Recuerda (guardrails)

- Todo payload activo: solo sobre targets autorizados.
- Stored XSS: no `alert(1)` en entornos compartidos; usar witness propio.
- Bypass WAF/filtros: agotar el set de bypass antes de declarar falso positivo.