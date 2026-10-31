---
name: ctf-reversing
description: 'Ingeniería inversa de binarios de CTF ofuscados: localizar main en
  stripped, extraer tablas de .rodata, resolver permutaciones de índices, emular
  ofuscación aritmética validada en GDB, analizar VMs de bytecode con tablas de salto
  y usar oráculos para recuperar passphrases. Usar cuando el binario pide token,
  vector o contraseña, o contiene un intérprete propio.
  Keywords: CTF reversing, obfuscation, VM bytecode, oracle, gdb, rodata tables.'
area: CTF
tags: [ctf, reversing, ofuscacion, vm, gdb, oraculo]
source: _full/reversing-obfuscated-binaries-and-vms
license: Apache-2.0
---

# SKILL-CTF-REVERSING.md — Reversing de binarios ofuscados y VMs

Fuente: `_full/reversing-obfuscated-binaries-and-vms/`.

## Cuándo usarla
ELF stripped que pide un token, vector o passphrase; hay tablas en `.rodata`; el
archivo pesa mucho más que sus secciones; existe un intérprete embebido.

## Procedimiento resumido
1. Estructura: `ctf-arsenal find-main binario` y `readelf -SW`.
2. Tablas: `ctf-arsenal tables binario --section .rodata --classify`.
3. Identificar la transformación: índice (lineal o permutado), clave, operaciones.
4. Descartar código muerto antes de invertir una segunda etapa.
5. Resolver por posición cuando el índice es una permutación (256·n pruebas).
6. Validar la emulación con GDB en las comparaciones.
7. VM: mapear opcodes desde la tabla de saltos y extraer el bytecode.
8. Oráculo: `ctf-arsenal oracle --mode insn --breakpoint 0x... --length N`.
9. Verificar ejecutando el binario con la entrada recuperada.

## Clasificación de hallazgo
- Entrada aceptada y token impreso → confirmado.
- Token extraído estáticamente sin ejecución → confirmar con round-trip.

## Herramientas
`ctf-arsenal`, `r2`, `ghidra`, `objdump`, `gdb`+`pwndbg`, `capstone`.

## Guardrails
- Analizar en entorno aislado; no ejecutar binarios desconocidos como root.
- Documentar breakpoints y registros observados.
