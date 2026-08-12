# SKILL-DD-ACQUISICION.md — Adquisición de imagen de disco con dd/dcfldd

Fuente: `_src/mukul-anthropic/acquiring-disk-image-with-dd-and-dcfldd/`.

## Cuándo usarla
Adquirir imagen bit-por-bit de un disco/dispositivo para análisis forense, preservando integridad.

## Procedimiento resumido
1. Identificar el dispositivo (`fdisk -l`, `lsblk`) — NUNCA montar.
2. **dcfldd** (mejor que dd: progreso + hash en tiempo real):
   `dcfldd if=/dev/sdX of=/mnt/out/evidence.dd hash=sha256 hashlog=sha256.log bs=4M status=on`
   - Legacy: `dd if=/dev/sdX of=evidence.dd bs=4M conv=noerror,sync` + `sha256sum` después.
3. Encabezado/colección: anotar make/model, serial, hash del device, fecha, quién (cadena de custodia).
4. Verificación: `sha256sum -c sha256.log`; si dispone, imagen E01 (`ewfacquire`) para metadatos.
5. Write-protect (write-blocker) para el fuente.

## Herramientas
`dd`/`dcfldd`, `lsblk`, `sha256sum`, `ewfacquire`, write-blocker.

## Guardrails
- Sobre dispositivos autorizados (propios/evidencia legal). Cadena de custodia documentada.
- Nunca montar el dispositivo fuente en modo rw.