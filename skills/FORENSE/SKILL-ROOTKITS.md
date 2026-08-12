# SKILL-ROOTKITS.md — Análisis de bootkits y rootkits

Fuente: `_src/mukul-anthropic/analyzing-bootkit-and-rootkit-samples/`.

## Cuándo usarla
Investigar muestras de rootkits/bootkits (kernel, UEFI, boot sector) en laboratorio autorizado.

## Procedimiento resumido
1. Entorno aislado (VM con snapshots, sin red saliente).
2. **Static first** (nunca ejecutar así): strings, imports, firmas, firmwares.
3. UEFI/bootkits: `chipsec` (audit firmware), `binwalk`/`uefi-firmware-parser` para extraer módulos UEFI.
4. Rootkits kernel Linux: comparar System.map, verificar `/dev/mem`, módulos ocultos; en Windows: MBR/VBR, hooks SSDT/IDT.
5. Dinámica en sandbox: observar comportamiento (ocultación, descifrado, persistencia UEFI/ESP).
6. Documentar IOCs (hashes, cápsulas, técnicas de persistencia).

## Herramientas
Ghidra, `chipsec`, `binwalk`, Volatility (detección rootkit), Cuckoo/sandbox.

## Guardrails
- Sampoes/EV en la muestra: ningún ejecutable fuera de sandbox; autorización del laboratorio.