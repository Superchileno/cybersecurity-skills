# CTF — Arsenal de retos y explotación

Área: resolución de CTF (Capture The Flag) con técnicas de esteganografía,
criptografía clásica, forense de audio/logs/red, explotación de binarios, reversing
de código ofuscado y defensa frente a prompt injection dirigida a agentes de IA.

A diferencia del resto de áreas, cada tarjeta tiene una **skill completa ejecutable**
en `_full/`, con `references/`, `scripts/` y `assets/`. El CLI `bin/ctf-arsenal`
despacha a esos scripts.

## Subskills destiladas

| Subskill | Cuándo usarla | Fuente |
|---|---|---|
| `SKILL-CTF-METODOLOGIA.md` | Punto de entrada: triaje, clasificación, writeup y control de señuelos | `_full/solving-ctf-challenges-systematically/` |
| `SKILL-CTF-STEGO.md` | Archivos raros: polyglots, datos tras el fin, LSB, OOXML, mosaicos | `_full/analyzing-file-artifacts-for-steganography/` |
| `SKILL-CTF-CRYPTO.md` | Texto cifrado, cifradores caseros, XOR reutilizado, Vigenère, catálogos | `_full/solving-classical-and-custom-cryptography/` |
| `SKILL-CTF-FORENSE.md` | Audio, logs CEF, pcap, MFT/USN y correlación temporal | `_full/performing-ctf-forensics-on-audio-and-logs/` |
| `SKILL-CTF-PWN.md` | ELF + `nc`: format string, ret2win, SROP, heap y kernel | `_full/exploiting-binary-vulnerabilities-in-ctf/` |
| `SKILL-CTF-REVERSING.md` | Binarios stripped, tablas, permutaciones, VMs y oráculos | `_full/reversing-obfuscated-binaries-and-vms/` |
| `SKILL-CTF-PROMPT-INJECTION.md` | Directivas ocultas dirigidas a agentes de IA | `_full/defending-against-prompt-injection-in-ctf-agents/` |

## Arsenal ejecutable

```bash
skills/CTF/bin/ctf-arsenal --list
skills/CTF/bin/ctf-arsenal triage reto.png
skills/CTF/bin/ctf-arsenal carve reto.png
skills/CTF/bin/ctf-arsenal xor known --plain p.txt --cipher c1.hex --target c2.hex
skills/CTF/bin/ctf-arsenal spectrogram audio.wav
skills/CTF/bin/ctf-arsenal checksec binario
skills/CTF/bin/ctf-arsenal find-main binario
```

## Enrutado al `_full`

- Detalle de una técnica concreta → `references/` de la skill correspondiente.
- Script parametrizable → `scripts/`; el CLI solo es un despachador.
- Plantilla de writeup → `templates/writeup.md`.
- Checklist de cierre → `checklists/triaje.md`.

## Recuerda (guardrails)

- Alcance limitado al host y servicio declarados por el reto.
- No atacar infraestructura de la plataforma ni a otros participantes.
- Nunca publicar flags de eventos activos; los writeups se sanean antes de compartir.
- Trabajar sobre copias de los artefactos; conservar hashes como evidencia.
