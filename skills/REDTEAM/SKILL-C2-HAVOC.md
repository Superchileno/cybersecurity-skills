# SKILL-C2-HAVOC.md — Operar C2 con Havoc

Fuente: `_src/mukul-anthropic/operating-havoc-c2/`.

## Cuándo usarla
Operar un C2 Havoc (teamserver + cliente) en red team autorizado.

## Procedimiento resumido
1. Configurar teamserver (config `teamserver/config.yaoi`), levantar con `./teamserver`.
2. Conectar el cliente Havoc (`havoc`), manejar listeners (HTTP/SMB).
3. Generar agent/payload (Shellcode de STIENT, beacon). Ajustar demonio/payload (molesto = SOC killer).
4. Operar: command line en el agent (commands, modules/heel), técnicas de post-explotación (mimikatz, dumping, lateral Via SMB).
5. Integrar con evidencia: capturar screenshoots, credenciales etc. (solo alcance).
6. Cleanup de agents al final.

## Herramientas
Havoc C2 (teamserver/client). Servidor Linux dedicado recomendado.

## Guardrails
- C2 dentro de alcance; no desplegar en producción sin autorización; eliminar agentes y listeners al cerrar el engagement.