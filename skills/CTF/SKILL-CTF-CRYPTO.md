---
name: ctf-crypto
description: 'Criptografía de CTF: cifradores caseros reversibles (XOR, rotación, swap
  de nibbles), XOR con clave repetida y crib-dragging, reutilización de keystream
  (two-time pad), Vigenère directo e inverso, sustitución por catálogo de glifos y
  cadenas de codificación (hex, Base64, Base45, ASCII85). Usar con texto cifrado,
  scripts de cifrado o tokens de igual longitud.
  Keywords: CTF crypto, XOR, two-time pad, crib drag, Vigenere, substitution, base45.'
area: CTF
tags: [ctf, crypto, xor, vigenere, sustitucion, encoding]
source: _full/solving-classical-and-custom-cryptography
license: Apache-2.0
---

# SKILL-CTF-CRYPTO.md — Criptografía clásica y cifradores caseros

Fuente: `_full/solving-classical-and-custom-cryptography/`.

## Cuándo usarla
El reto entrega hex, Base64, tokens del mismo tamaño, símbolos exóticos o un script
que "cifra" un mensaje conocido.

## Procedimiento resumido
1. Identificar alfabeto y longitud (módulo 4, módulo 3, conjunto de símbolos).
2. Con cifrador provisto: leer el código, invertir en orden inverso y validar
   `cifrar(descifrar(x)) == x`.
3. Con par conocido: `ctf-arsenal xor known --plain P --cipher C1 --target C2`.
4. Sin par conocido: `ctf-arsenal xor brute` y `ctf-arsenal vigenere --crib PREFIJO`.
5. Cadenas de codificación: `ctf-arsenal decode archivo`.
6. Catálogos de glifos: validar primero con la lámina de control.
7. Verificar 100% imprimible + prefijo de flag + coherencia semántica.

## Clasificación de hallazgo
- Texto recuperado con formato de flag → confirmado.
- Clave "casi" correcta (variante leet) → revisar posición a posición.

## Herramientas
`ctf-arsenal`, CyberChef, `hashcat`, `john`, `hashid`, `RsaCtfTool`.

## Guardrails
- No aceptar resultados parcialmente legibles: un byte mal indica clave errónea.
- Documentar claves y keystreams recuperados como evidencia.
