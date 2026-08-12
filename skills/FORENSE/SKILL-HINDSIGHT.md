# SKILL-HINDSIGHT.md — Forense de navegador con Hindsight

Fuente: `_src/mukul-anthropic/analyzing-browser-forensics-with-hindsight/`.

## Cuándo usarla
Analizar datos de navegación (Chrome/Edge/Chromium) en imágenes forenses: historial, descargas, cookies, autofill.

## Procedimiento resimido
1. Localizar perfiles del navegador en la imagen (Users/<u>/AppData/Local/Google/Chrome/User Data/Default/...).
2. Ejecutar Hindsight sobre el perfil: `python3 hindsight.py -i <perfile_dir> -o <output.csv>` (Google Takeout export también soportado).
3. Información obtenida: visitas (timestamps), descargas, cookies, autofill, URL predictions, ejevectores históricos.
4. Cruzar con timeline general (Plaso/Hayabusa) y con URLs sospechosas de CTI.
5. Exportar CSV/JSON; filtrar por dominio/usuario/fecha.

## Herramientas
`hindsight` (pip; de obsidianforensics). Necesita SQLite (evitar corromper original: copiar perfil antes).

## Guardrails
- Copiar el perfil antes de abrirlo (SQLite locks); imagen autorizada. PII del usuario redactada.