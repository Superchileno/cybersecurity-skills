---
name: ctf-metodologia
description: 'Metodología para resolver retos de CTF: triaje del enunciado y de los
  artefactos, clasificación por categoría (stego, crypto, forense, OSINT, web, pwn,
  reversing, boot2root), control de señuelos y writeup reproducible. Usar al recibir
  un reto nuevo, al organizar la carpeta del desafío o cuando el reto está bloqueado.
  Keywords: CTF methodology, triage, writeup, decoy, flag validation.'
area: CTF
tags: [ctf, metodologia, triaje, writeup]
source: _full/solving-ctf-challenges-systematically
license: Apache-2.0
---

# SKILL-CTF-METODOLOGIA.md — Metodología de resolución de CTF

Fuente: `_full/solving-ctf-challenges-systematically/`.

## Cuándo usarla
Llega un reto nuevo, hay que decidir el primer paso, o el desafío está bloqueado y
no se sabe qué descartar.

## Procedimiento resumido
1. Registrar enunciado literal, formato de flag, artefactos y hashes.
2. Clasificar por artefacto: archivo→stego, texto cifrado→crypto, log/pcap/audio→
   forense, URL+API→web, `nc`+ELF→pwn, ELF con token→reversing, OVA→boot2root.
3. Barrido de bajo costo: `ctf-arsenal triage archivo`, `binwalk -eM`, últimos bytes.
4. Escribir hipótesis explícita: "creo X porque Y; si Z lo descarto".
5. Validar la flag por estructura y por la plataforma; registrar señuelos.
6. Cerrar con `solucion/` reproducible, `work/` auditable y writeup.

## Clasificación de hallazgo
- Reto resuelto con flag validada → cierre.
- Técnica identificada sin flag → documentar como parcial con hipótesis vivas.
- Señuelo confundido con flag → revisar validación estructural.

## Herramientas
`ctf-arsenal`, `binwalk`, `exiftool`, `strings`, `xxd`, `file`.

## Guardrails
- Alcance limitado al host/servicio del reto.
- No atacar infraestructura de la plataforma ni a otros jugadores.
- Registrar descartes con su razón para no repetir pruebas.
