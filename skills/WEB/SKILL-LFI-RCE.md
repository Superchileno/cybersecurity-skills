# SKILL-LFI-RCE.md — LFI / path traversal / RCE

## Cuándo usarla
Parámetros con rutas: `file=`, `page=`, `include=`, `template=`, `path=`, `download=`,
`view=`; apps PHP (`phpinfo-to-rce`), o plataformas con template engines.

## Procedimiento resumido
1. Traversal básico: `../../../../etc/passwd`, con variantes
   `....//`, `..%2f`, `%00` (null byte, PHP <5.3), URL-encoding doble, `c:\windows\win.ini`.
2. LFI a RCE (PHP): wrappers `php://filter/convert.base64-encode/resource=<file>`,
   `data://`, `expect://`, inclusion de logs/`/proc/self/environ`, session files.
3. RCE genérico: plantillas (SSTI) `{{7*7}}`, deserialización, `phpinfo()` + upload
   a temp file (`recon/phpinfo-to-rce`).
4. Confirmar con payload que produce efecto observable (respuesta, timing, deref).

## Clasificación
- Lectura de `/etc/passwd` → L3; ejecución de código → L4.

## Herramientas
`curl`, Burp, `phpinfo`-recon scripts del pack.

## Guardrails
- El `expect://` y `data://` pueden ejecutar comandos: **solo con aprobación** y
  payload no destructivo (id, hostname). Evidencia reproducible.
- Nada destructivo sin autorización escrita.