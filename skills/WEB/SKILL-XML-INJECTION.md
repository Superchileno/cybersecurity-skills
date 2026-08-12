# SKILL-XML-INJECTION.md — Inyección XML (XXE/XPATH)

Fuente: `_src/mukul-anthropic/testing-for-xml-injection-vulnerabilities/`.

## Cuándo usarla
Aplicaciones que procesan XML (SOAP, import docs, WebDAV) — probabilidad de XXE/XXE-XPath en `data:` tags.

## Procedimiento resumido
1. Detectar entrada XML: subir docs .xml, SOAP, `Content-Type: application/xml`.
2. XXE básico:
   ```xml
   <!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]><foo>&xxe;</foo>
   ```
3. Blind (sin salida): parametrizar con entidad en URL externa (callback) o usar errores (via `docb` / entidades malformadas).
4. SSRF vía XXE: `SYSTEM "http://<tu-host>/x"` → confirmar con callback propio.
5. XPath injection en filtros XML (si aplica): payload en XPath.
6. Aislo parses: deshabilitar `<!DOCTYPE>` (librerías secure parsing).

## Herramientas
`curl`, Burp, listas de payload XXE (OWASP cheat sheet).

## Guardrails
- `file:///etc/passwd` es acto de lectura (L3/L4); solo targets autorizados, callback en host propio.