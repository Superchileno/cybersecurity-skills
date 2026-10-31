---
name: ctf-orquestacion
description: 'Orquestación de retos CTF: triaje inicial, clasificación de categoría,
  enrutado a la skill especializada, criterios de pivote cuando el reto se bloquea,
  búsqueda de writeups similares por palabras clave y generación del writeup
  estandarizado de entrega. Usar al recibir un reto nuevo, al no saber qué skill
  aplica o al cerrar el reto para documentarlo.
  Keywords: CTF orchestration, triage, routing, pivot, writeup, similar search,
  challenge handoff.'
area: CTF
tags: [ctf, orquestacion, triaje, writeup, routing]
source: _src/ljagiello-ctf-skills/solve-challenge, _src/ljagiello-ctf-skills/ctf-writeup, _src/ljagiello-ctf-skills/ctf-similar-search
license: MIT
upstream: ljagiello/ctf-skills
---

# SKILL-CTF-ORQUESTACION.md — Triaje, pivote y writeup

Profundidad en `_src/ljagiello-ctf-skills/{solve-challenge,ctf-writeup,ctf-similar-search}/`.

## Cuándo usarla
Al empezar un reto, cuando el primer enfoque falla dos veces seguidas o cuando
hay que entregar el writeup.

## Procedimiento resumido
1. Triaje: inventariar artefactos, leer el enunciado dos veces y anotar la
   pregunta exacta que se responde.
2. Clasificar por señal dominante: URL, ELF+puerto, archivo, texto cifrado,
   binario ofuscado, muestra maliciosa, pista pública.
3. Elegir una sola skill y ejecutar su primer paso; no abrir cinco frentes.
4. Pivote: si dos intentos fallan, cambiar de categoría, no de payload.
5. Búsqueda por similitud con 2–3 palabras clave o una cadena única del reto.
6. Cerrar con writeup: resumen, pasos reproducibles, evidencia y flag.

## Enrutado al `_src`
| Necesidad | Archivo |
|---|---|
| Flujo de resolución y rutas por dificultad | `solve-challenge/SKILL.md`, `solve-challenge/difficulty-routing.md` |
| Formato de writeup de entrega | `ctf-writeup/SKILL.md` |
| Búsqueda de writeups similares (Tavily) | `ctf-similar-search/SKILL.md`, `search.py`, `search.sh` |

## Enrutado interno
| Categoría | Skill |
|---|---|
| Metodología y control de señuelos | `solving-ctf-challenges-systematically` |
| Web | `ctf-web` |
| Misc, jails y señales | `ctf-misc` |
| IA/ML | `ctf-ai-ml` |
| Malware | `ctf-malware` |
| OSINT | `ctf-osint` |
| Archivos y estego | `analyzing-file-artifacts-for-steganography` |
| Criptografía | `solving-classical-and-custom-cryptography` |
| Audio, logs, pcap, disco | `performing-ctf-forensics-on-audio-and-logs` |
| Pwn | `exploiting-binary-vulnerabilities-in-ctf` |
| Reversing | `reversing-obfuscated-binaries-and-vms` |

## Herramientas
`ctf-arsenal triage`, `ctf-arsenal verify`, plantilla `templates/writeup.md`,
API de Tavily para búsqueda por similitud (requiere clave propia).

## Guardrails
- Una hipótesis a la vez, con su criterio de falsación anotado.
- No copiar writeups ajenos sin adaptar y entender cada paso.
- El writeup no publica flags de eventos activos; se sanea antes de compartir.
