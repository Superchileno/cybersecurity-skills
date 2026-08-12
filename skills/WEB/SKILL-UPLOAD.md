# SKILL-UPLOAD.md — File Upload

## Cuándo usarla
Formularios/API de subida de archivos (avatar, docs, import, editor).

## Procedimiento resumido
1. Probar extensiones bloqueadas: doble extensión `shell.php.jpg`, `shell.pHp`, `.phtml`,
   `.svg` (stored XSS), `.htaccess`, espacios/`%00`, `shell.php%00.png`.
2. Content-Type spoof; polyglot (imagen+PHP); análisis del servidor (Apache .htaccess,
   Nginx misconfig).
3. Detectar almacenamiento: probar acceso `/<ruta>/shell.png` y si es ejecutado.
4. Si no hay ejecución local, valorar impacto (overwrite, LFI via `../`, almacenado XSS).

## Clasificación
- Script subido y ejecutado → L4 (RCE). Solo lectura/fuga de ruta → L3.

## Herramientas
Burp (Intercept/Repeater), `curl -F "file=@payload.png"`.

## Guardrails
- Subir webshells solo en labs/entornos de prueba propios del engagement, con
  aprobación; retirarlas tras la prueba. Evidencia request+response.