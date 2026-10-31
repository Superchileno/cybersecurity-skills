---
name: ctf-misc
description: 'Retos misceláneos de CTF: pyjails y bash jails (evasión de audit hooks,
  normalización NFKC, traversal de objetos), codificaciones exóticas y esteganografía
  Unicode, resolución de restricciones con Z3, RF/SDR e IQ, juegos y VMs, escalada
  local en contenedores y navegación de la plataforma sin navegador. Usar cuando el
  reto no encaje en web, pwn, crypto, forense ni reversing.
  Keywords: CTF misc, pyjail, bash jail, sandbox escape, Z3, encodings, Unicode
  steganography, SDR, IQ, SUID, docker group, CTFd.'
area: CTF
tags: [ctf, misc, pyjail, encodings, z3, sdr, privesc]
source: _src/ljagiello-ctf-skills/ctf-misc
license: MIT
upstream: ljagiello/ctf-skills
---

# SKILL-CTF-MISC.md — Misceláneos, jails y señales

Profundidad en `_src/ljagiello-ctf-skills/ctf-misc/`.

## Cuándo usarla
El reto entrega un intérprete restringido, un archivo sin categoría clara, una
señal de radio, una VM/juego o un acceso SSH de bajo privilegio.

## Procedimiento resumido
1. Clasificar el artefacto: archivo, servicio interactivo, señal o binario SUID.
2. Si hay intérprete restringido, mapear qué builtins y atributos quedan
   accesibles antes de escribir payloads.
3. Si hay entrada codificada, agotar la cadena de decodificaciones y revisar
   Unicode invisible (selectores de variación, bloque de tags).
4. Si hay restricciones matemáticas, modelar con Z3 en lugar de buscar a mano.
5. Si hay acceso a shell, revisar SUID, sudo, ACL, grupos (`docker`, `lxd`) y
   cron antes de intentar exploits.
6. Si es señal, separar I/Q, mirar espectrograma y modulaciones conocidas.

## Enrutado al `_src`
| Tema | Archivo |
|---|---|
| Pyjails y evasión de sandbox | `ctf-misc/pyjails.md` |
| Bash jails y shells restringidas | `ctf-misc/bashjails.md` |
| Codificaciones base | `ctf-misc/encodings.md` |
| Codificaciones avanzadas y Unicode | `ctf-misc/encodings-advanced.md` |
| Juegos y VMs | `ctf-misc/games-and-vms*.md` |
| Audio y espectrogramas | `ctf-misc/audio.md` |
| RF / SDR / IQ | `ctf-misc/rf-sdr.md` |
| DNS | `ctf-misc/dns.md` |
| Escalada local | `ctf-misc/linux-privesc.md` |
| CTFd sin navegador | `ctf-misc/ctfd-navigation.md` |

## Herramientas
`python3`, `z3-solver`, `pwntools`, `GNU Radio`, `inspect`, GTFOBins, `xxd`.

## Guardrails
- Las jails se prueban en local antes de golpear el servicio remoto.
- No ejecutar payloads de escape fuera del contenedor del reto.
- Registrar la carga útil mínima que funcionó, no solo la que falló.
