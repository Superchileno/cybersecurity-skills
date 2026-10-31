---
name: web-thick-client
description: 'Aplicaciones de escritorio (clientes gordos) que se comunican con servidores (bases, APIs) dentro de alcance autorizado. Keywords: client, thick, web.'
area: WEB
tags: [client, thick, web]
source: '_src/mukul-anthropic/performing-thick-client-application-penetration-test/'
license: Apache-2.0
---

# SKILL-THICK-CLIENT.md — Pentest de clientes gordos (thick client)

Fuente: `_src/mukul-anthropic/performing-thick-client-application-penetration-test/`.

## Cuándo usarla
Aplicaciones de escritorio (clientes gordos) que se comunican con servidores (bases, APIs) dentro de alcance autorizado.

## Procedimiento resumido
1. **Enumeración**: binario (strings, imports), instalador, config (conn strings), servicios internos.
2. **Análisis de ejecución**: procesos, red (netstat/ProcMon), DLLs habilitados (hijacking).
3. **Interceptación**: Burp como proxy de la app (system proxy o `HTTPS_PROXY`), o mitm con `responder`/`mitmproxy`.
4. **Autenticación**: crackear hashes locales, secrets en registry/files, creds hardcoded en binario.
5. **Lógica**: parámetros manipulados, SQLi/XXE en payload del cliente, inyección de comandos.
6. **Escalada**: DLL hijack, protocol hijack, config local para auth.

## Herramientas
Burp (proxy), `strings`, `procmon`, `cheat-engine` (test de memoria), `dnspy` (si .NET).

## Guardrails
- Solo clientes autorizados; interceptar tráfico puede implicar certificados de confianza no deseados — advertir al usuario antes de instalar raíz de Burp.