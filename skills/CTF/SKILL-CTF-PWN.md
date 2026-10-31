---
name: ctf-pwn
description: 'Explotación de memoria en binarios de CTF: format string con %hn
  posicional, desbordamiento de pila con ret2win, off-by-one sobre puntero de callback,
  SROP cuando no hay función win ni system, y heap/kernel (musl mallocng, Dirty
  Pagetable). Incluye reconocimiento con checksec, cálculo de offsets y validación
  local antes del remoto. Usar cuando el reto entregue un ELF y un servicio nc.
  Keywords: CTF pwn, format string, ROP, SROP, ret2win, heap, kernel, Dirty Pagetable.'
area: CTF
tags: [ctf, pwn, format-string, rop, srop, heap, kernel]
source: _full/exploiting-binary-vulnerabilities-in-ctf
license: Apache-2.0
---

# SKILL-CTF-PWN.md — Explotación de binarios

Fuente: `_full/exploiting-binary-vulnerabilities-in-ctf/`.

## Cuándo usarla
Hay un ELF y un `nc host puerto`; el binario pide un token, imprime direcciones o
el reto incluye un `patch.diff` de kernel.

## Procedimiento resumido
1. Reconocimiento: `ctf-arsenal checksec binario` (PIE, canary, NX, RELRO).
2. Localizar el bug: `read` sobredimensionado, `printf(entrada)`, off-by-one.
3. Offset: `ctf-arsenal offset binario` (barrido de umbral + GDB).
4. Elegir técnica: ret2win → ROP → SROP → format string → heap/kernel.
5. Validar en local con `/tmp/flag` de prueba:
   `ctf-arsenal ret2win --binary ./bin --offset N --win 0x... --local`.
6. Format string: `ctf-arsenal fmtstr --index N --addr 0x... --value 0x...`.
7. SROP: `ctf-arsenal srop` con los gadgets identificados.
8. Repetir contra el remoto y guardar la transcripción.

## Clasificación de hallazgo
- Shell o lectura de flag → L4 (crítico).
- Crash controlado sin control de RIP → L2.

## Herramientas
`ctf-arsenal`, `pwntools`, `gdb`+`pwndbg`, `ROPgadget`, `ropper`, `one_gadget`.

## Guardrails
- Solo contra el servicio del reto.
- Nunca probar el payload directamente en remoto sin validación local.
- Documentar offsets y gadgets usados.
