# SKILL-FOREMOST.md — File carving con foremost

Fuente: `_src/mukul-anthropic/performing-file-carving-with-foremost/`.

## Cuándo usarla
Recuperar ficheros borrados sin metadatos (solo cabeceras) desde imágenes de disco o almacenamiento.

## Procedimiento resumido
1. `foremost -i <imagen> -o <outdir>` (por defecto carving de imágenes, docs, zip, exe, etc.).
2. Flags: `-t` tipo concreto (jpg,png,pdf,...), `-q` (quick, saltar footer validado), `-b` bloques.
3. Analizar resultados: archivos no-tamaño0 en `out/<tipo>/`.
4. Verificar integridad (cabecera/footer, validar apertura) e identificar contenido.
5. Para MFT/deleted específicos usar también `photorec` (recuperación de datos) y `extundelete`.

## Herramientas
`foremost` (Kali incluye), `photorec`/`testdisk`, `binwalk` (firmware).

## Guardrails
- Solo sobre imágenes autorizadas; los ficheros recuperados pueden ser malware → analizar en sandbox o aislados.