---
name: solving-classical-and-custom-cryptography
description: 'Resuelve retos de criptografía de CTF: cifradores caseros reversibles
  (XOR + rotación + swap de nibbles), XOR con clave repetida y crib-dragging, reutilización
  de keystream (two-time pad), Vigenère directo e inverso con clave que sólo avanza en
  letras, sustitución por catálogo de glifos, y cadenas de codificación (hex, Base64,
  Base45, ASCII85). Incluye validación por round-trip y prefijo de flag para descartar
  señuelos. Usar cuando el reto entregue texto cifrado, un script cifrador, tokens de
  igual longitud o símbolos que no son ASCII.'
domain: cybersecurity
subdomain: ctf
tags:
- ctf
- cryptography
- xor
- vigenere
- caesar
- substitution
- one-time-pad
- crib-drag
- base64
- base45
- encoding
version: '1.0'
author: auditoria-ia-v2
license: Apache-2.0
mitre_attack:
- T1140
- T1027
nist_csf:
- DE.AE-02
---

# Criptografía Clásica y Cifradores Caseros en CTF

Casi ningún reto de CTF usa criptografía fuerte: usa un cifrador mal construido, una
clave reutilizada o una sustitución con catálogo. El trabajo es identificar la
estructura y validar sin ambigüedad.

## When to Use

- El reto entrega hex, Base64, tokens de igual longitud o símbolos exóticos.
- Hay un `cifrador.py` / binario que "cifra" un mensaje conocido.
- Se dispone de un par (texto plano, cifrado) y otro cifrado del mismo esquema.
- El texto decodifica a algo legible pero no es la flag.
- Hay que decidir entre César, Vigenère, XOR o sustitución.

**No usar** para criptografía de producción (TLS, AEAD, curvas elípticas): para eso
usar la skill de evaluación TLS correspondiente. Aquí se rompen implementaciones
docentes o deliberadamente débiles.

## Prerequisites

- Python 3 con `pycryptodome` (opcional), `numpy` (opcional).
- `hashid`, `hashcat`, `john` para hashes.
- CyberChef (opcional, para cadenas visuales).
- Scripts de esta skill.

## Workflow

### 1. Identificar el alfabeto y la longitud

```python
import collections, string
print(set(texto))
print(len(texto), len(texto) % 4, len(texto) % 3)
```

| Alfabeto observado | Hipótesis |
|---|---|
| `0-9a-f` y longitud par | hex → bytes |
| `A-Za-z0-9+/=` | Base64 (validar múltiplo de 4) |
| `A-Za-z0-9-_` | Base64url |
| 45 símbolos (`0-9A-Z $%*+-./:`) | Base45 |
| sólo símbolos Unicode (▽ ▲ …) | sustitución por catálogo |
| sólo `.` y `-` agrupados | binario, no Morse (verificar) |
| dos textos de igual longitud | XOR / keystream |

### 2. Si hay un cifrador provisto

```bash
python cifrador.py          # leer el código completo antes de ejecutar
```

Órdenes posibles: XOR con clave repetida, rotación dependiente del índice, swap de
nibbles, suma modular. Se descifra **en orden inverso** y se valida con round-trip:

```python
assert cifrar(descifrar(x)) == x
```

### 3. Si hay par conocido

```bash
python scripts/xor_tool.py known --plain mi_sesion.txt --cipher mi_token.hex \
    --target token_gerencia.hex
```

El script calcula `keystream = C ⊕ P`, lo aplica al objetivo y reporta si el resultado
es imprimible. Si los dos cifrados comparten keystream, los extremos de `C1 ⊕ C2`
serán cero.

### 4. Si no hay par conocido

- **Crib-dragging:** probar el prefijo de flag conocido (`flag{`, `flag{`) en cada
  offset y derivar la clave.
- **XOR de clave repetida:** estimar longitud por índice de coincidencia, luego
  resolver cada columna como XOR de un byte.
- **Vigenère:** probar suma y resta; validar con el prefijo.

```bash
python scripts/crib_drag.py cifrado.bin --crib "flag{" --max-key 32
python scripts/vigenere.py cifrado.txt --crib PREFIJO --invert
```

### 5. Cadenas de codificación

```bash
python scripts/decode_chain.py --text "$(cat mensaje.txt)" --max-depth 8
```

Prueba en cada nivel: hex, Base64, Base64url, Base32, Base85/ASCII85, Base45, URL,
gzip/deflate/zlib, ROT13 y reverso. Se detiene cuando el texto deja de reducirse o
aparece el formato de flag.

### 6. Validación

- Prefijo oficial exacto.
- Round-trip del cifrador cuando exista.
- Coherencia semántica del cuerpo (palabras del relato, no ruido).
- Si hay varias claves candidatas, elegir la que produzca **100% imprimible**.

## Key Concepts

- **Keystream reutilizado:** si dos mensajes usan la misma clave/nonce, `C1 ⊕ C2 =
  P1 ⊕ P2`. Con un par conocido se recupera el otro mensaje completo.
- **Crib:** fragmento de texto plano esperado. Con `flag{` de 9 bytes se recuperan
  9 bytes de keystream por offset.
- **Índice de coincidencia:** mide si una columna de texto cifrado proviene de un solo
  byte de clave (XOR) o de una sustitución.
- **Permutación:** si la posición de entrada es `(k*i) mod n` con `gcd(k,n)=1`, los
  índices se recorren todos; se puede resolver byte a byte sin invertir el algoritmo.
- **Clave que sólo avanza en letras:** en Vigenère, espacios/símbolos se conservan y
  **no consumen** clave. Ignorar esto desplaza todo el mensaje.
- **Polaridad:** un flujo de `.`/`-` puede ser binario con `.`=1 o `-`=1. Probar ambas;
  la incorrecta da `0xFF` repetidos o bytes no imprimibles.

## Tools & Systems

| Tarea | Herramienta |
|---|---|
| XOR / crib / two-time pad | `scripts/xor_tool.py`, `scripts/crib_drag.py` |
| Vigenère / César | `scripts/vigenere.py` |
| Cadenas de codificación | `scripts/decode_chain.py`, CyberChef |
| Hashes | `hashid`, `hashcat -m`, `john` |
| RSA débil | `RsaCtfTool` |
| AES con modo mal usado | `pycryptodome` + análisis de IV/nonce |
| Frecuencia / IC | `numpy`, scripts propios |

## Common Scenarios

### "Dos tokens del mismo tamaño y los extremos se anulan"
Mismo keystream. Con el par conocido se descifra el objetivo sin fuerza bruta. Si no
hay par conocido, usar la crib del prefijo y explotar el inglés/español del resto.

### "El cifrador suma, rota y hace swap"
Aplicar las operaciones inversas en orden inverso. Si el script no es reversible
(pierde información), entonces no es el camino: buscar otro artefacto.

### "El texto es legible pero el prefijo está mal"
Catálogo trocado o clave leet. En un reto, `CLAVE` vs `CLAVE` rompía el XOR
exactamente en la posición 7. Probar variantes sistemáticamente y verificar posición
por posición.

### "Símbolos raros que parecen Base64"
Puede ser Base45 (`set` de 45 caracteres) o una sustitución con catálogo. Validar
`set(texto) ⊆ alfabeto` y longitud múltiplo de 3 antes de decodificar.

## Output Format

```markdown
## Alfabeto y estructura
- longitud, módulo, conjunto de símbolos

## Hipótesis y descartes
| # | Hipótesis | Prueba | Resultado |

## Clave / keystream
- método de recuperación y validación

## Texto recuperado
```
...
```

## Flag
`...`
```

Referencias: `references/xor_y_reutilizacion.md`,
`references/cifradores_caseros.md`, `references/sustitucion_y_polialfabeticos.md`.
