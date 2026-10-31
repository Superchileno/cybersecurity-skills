---
name: solving-ctf-challenges-systematically
description: 'Metodología completa para resolver desafíos de CTF (Capture The Flag). Cubre
  el triaje del enunciado y de los artefactos entregados, la clasificación por categoría
  (misc, stego, crypto, forense, OSINT, web, pwn, reversing, boot2root), el árbol de
  decisión "si ves X, aplica Y", el control de señuelos y la documentación reproducible
  del writeup. Derivada de 39 desafíos resueltos en competiciones de CTF reales.
  Usar al recibir un reto nuevo, al organizar una carpeta de CTF, o al decidir el siguiente
  paso cuando un desafío está bloqueado.'
domain: cybersecurity
subdomain: ctf
tags:
- ctf
- methodology
- triage
- writeup
- steganography
- forensics
- cryptography
- osint
- pwn
- reversing
- boot2root
version: '1.0'
author: auditoria-ia-v2
license: Apache-2.0
mitre_attack:
- T1592
- T1595
- T1005
- T1140
- T1027
nist_csf:
- ID.AM-05
- ID.RA-05
- DE.AE-02
---

# Resolución Sistemática de Desafíos CTF

Convierte el tiempo de CTF en resultados reproducibles: clasificar rápido, no repetir
callejones sin salida ya conocidos, distinguir señuelos de la flag real y dejar un
writeup que otro analista pueda repetir sin adivinar.

## When to Use

- Llega un reto nuevo y hay que decidir por dónde empezar en los primeros 5 minutos.
- El reto está bloqueado y no se sabe qué técnica descartar a continuación.
- Hay que montar la carpeta del desafío con su estructura y convención de nombres.
- Hay que escribir o revisar un writeup antes de cerrar el reto.
- Se quiere convertir un desafío resuelto en material reutilizable (skill/script).

**No usar** para evaluaciones de seguridad reales: aquí el objetivo es la flag y el
alcance está delimitado por el CTF; para un pentest usar la skill de metodología
correspondiente y el contrato de autorización.

## Prerequisites

- Enunciado literal del reto (copiarlo sin parafrasear: las pistas están en el texto).
- Artefactos entregados (ZIP, imagen, binario, pcap, URL, credenciales).
- Kali Linux o equivalente con: `file`, `exiftool`, `binwalk`, `foremost`,
  `pngcheck`, `strings`, `xxd`, `sqlmap`, `john`, `hashcat`, `radare2`, `gdb`,
  `pwntools`, `nmap`, `ffuf`, `tshark`, `sox`, `tesseract`, `jq`.
- Autorización: en CTF el alcance es el host/servicio indicado. **Nunca** salir del
  alcance (ni atacar infraestructura de la plataforma ni otros jugadores).

## Workflow

### 1. Registro inicial (2 minutos)

1. Crear carpeta `ctf/NN-nombre-desafio/` con `CONTEXTO.md`, `solucion/`, `work/`.
2. Guardar el enunciado **literal** y los datos de entrega (URL, host:puerto,
   credenciales, cookies, token JWT).
3. Calcular hashes de los artefactos y anotarlos: `ctf_triage.py --hash`.
4. Anotar el formato de flag esperado (`flag{...}`, `flag{ejemplo}`, otro).

### 2. Clasificar el artefacto

| Lo que entregan | Categoría probable | Skill a cargar |
|---|---|---|
| ZIP, PNG, JPG, WAV, DOCX, PDF, binario "raro" | Misc / stego | `analyzing-file-artifacts-for-steganography` |
| Texto cifrado, hex, Base64, "cifrador.py" | Crypto | `solving-classical-and-custom-cryptography` |
| `.log`, `.pcap`, audio con voz/música, video | Forense | `performing-ctf-forensics-on-audio-and-logs` |
| Fotos, usuario de red social, coordenadas | OSINT | este mismo skill + `references/triaje_por_artefacto.md` |
| URL + login + API | Web | skills de api-security / web del repo |
| `nc host puerto` + ELF | Pwn | `exploiting-binary-vulnerabilities-in-ctf` |
| ELF sin servicio, "token", passphrase | Reversing | `reversing-obfuscated-binaries-and-vms` |
| OVA/VMDK + "obtén user y root" | Boot2Root | `references/boot2root.md` |

### 3. Barrido de bajo costo (siempre, en este orden)

```bash
file *; exiftool *; strings -n 6 * | sort -u | head -50
binwalk -eM archivo        # carving automático
xxd archivo | tail -20     # ¿hay datos tras el marcador de fin?
```

Si algo de esto ya da la flag, se documenta y se cierra. No escalar complejidad sin
haber descartado lo trivial.

### 4. Hipótesis explícita

Escribir en `CONTEXTO.md`: *"Creo que X porque Y; si Z entonces lo descarto"*.
Cada intento fallido se registra con la razón del descarte. Esto evita repetir
pruebas (fue el error más caro en varios retos: reintentar LSB en bits ya probados).

### 5. Validación de la flag (obligatoria)

- Confirmar el prefijo/formato oficial.
- Si la flag "parece" correcta pero tiene caracteres raros, sospechar de:
  catálogo trocado, polaridad invertida, orden de filas/columnas equivocado,
  clave leet (`CLAVE` vs `CLAVE`), o calibraciones incluidas por error.
- Preferir una validación objetiva: round-trip del cifrador, prefijo conocido,
  CRC/firma, o la propia plataforma.

### 6. Cierre del reto

1. `solucion/` con el script reproducible end-to-end (no pasos manuales sueltos).
2. `work/` con los artefactos intermedios que permiten auditar el resultado.
3. `flag.txt`.
4. Entrada en `CONTEXTO.md` / índice con fecha, evidencia, técnica y señuelos.

## Key Concepts

- **Señuelo (decoy):** dato que decodifica a algo plausible pero falso. Es la norma,
  no la excepción: casi todos los retos tienen 2–4. Se detecta validando estructura
  (prefijo de flag, CRC, SHA-256, longitud) no "legibilidad".
- **Capas (layers):** la flag suele estar a 3–5 transformaciones de distancia. Cada
  capa debe reducir entropía o aumentar estructura; si una transformación no hace
  ninguna de las dos, es un callejón.
- **Oráculo:** cualquier salida del sistema (mensaje, tiempo, longitud, conteo de
  instrucciones) que permite inferir bytes correctos. Es la técnica central en
  reversing y pwn.
- **Presupuesto de tiempo:** 20 minutos por hipótesis. Si no avanza, se anota el
  descarte y se cambia de eje (no de detalle).
- **Reproducibilidad:** si el writeup necesita "y luego moví esto a mano", no está
  terminado.

## Tools & Systems

| Necesidad | Herramienta |
|---|---|
| Identificación y hashes | `file`, `sha256sum`, `scripts/ctf_triage.py` |
| Metadatos | `exiftool`, `identify -verbose` |
| Carving / capas | `binwalk -eM`, `foremost`, `scripts/carve_appended.py` |
| Hex / estructura | `xxd`, `pngcheck`, `zipinfo`, `7z l` |
| Cripto clásica | `scripts/xor_tool.py`, `scripts/vigenere.py`, CyberChef |
| Fuerza bruta de ZIP | `zip2john` + `john`, `bkcrack` (known-plaintext) |
| Web | `ffuf`, `sqlmap`, `jwt_tool`, `curl` |
| Pwn | `checksec`, `pwntools`, `gdb` + `pwndbg` |
| Reversing | `r2`, `objdump`, `ghidra`, `gdb` |
| Forense | `tshark`, `zeek`, `sox`, `tesseract`, `sleuthkit` |

## Common Scenarios

### "El archivo está corrupto / no abre"
Reparar la firma antes de asumir cifrado. Casos reales: PNG con primer byte a `0x00`
en vez de `0x89`; DOCX que empieza en `50 15 78 04` en vez de `PK\x03\x04`. Un byte
reparado abrió el reto completo en dos desafíos distintos.

### "El servicio responde 403 a todo"
No siempre es bypass de cabeceras: en varios retos la puerta era una **cookie de
sesión** (`session_id`) que entrega la plataforma al lanzar la instancia, o el
`User-Agent` del cliente oficial. Leer el enunciado y el HTML antes de fuzzear.

### "Nada funciona y el archivo parece normal"
Comprobar en este orden: datos tras el marcador de fin (IEND/EOI/EOF), chunks
`tEXt`/comentarios, LSB en bit 0 (y solo después bits 1–3), y periodo de mosaico.
En un reto, el `find("IEND")` caía en el *tipo* del chunk: el fin real era `iend+8`.

### "La flag decodifica pero no la acepta"
Sospechar de un catálogo/planilla trocado. Validar con la lámina de control
(la que decodifica un texto conocido) y recién entonces aplicar al objetivo.

## Output Format

```markdown
# Desafío NN — <nombre>
| Campo | Valor |
|---|---|
| Categoría | ... |
| Dificultad | ... |
| Estado | resuelto |
| Flag | `...` |

## Enunciado (literal)
## Reconocimiento (evidencia + hashes)
## Análisis (hipótesis y descartes)
## Solución reproducible
## Señuelos encontrados
## Lecciones
```

Checklist de cierre: `assets/checklist_triaje.md`.
Plantilla: `assets/plantilla_writeup.md`.
Árbol de decisión detallado: `references/triaje_por_artefacto.md`.
Convención de carpetas y backups: `references/convencion_writeup.md`.
