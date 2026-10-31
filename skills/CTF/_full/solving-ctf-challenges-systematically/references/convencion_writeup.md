# Convención de carpetas, documentación y backups

Regla de trabajo: **ningún cambio queda sin copia local
y sin registro en el contexto**. Aplicada a CTF significa que el writeup es parte
del entregable, no un extra.

## Estructura

```
ctf/
├── CONTEXTO_CTF.md          # índice + historial (fuente de verdad)
├── _PLANTILLA_WRITEUP.md    # plantilla
├── backups/                 # copias antes de modificar archivos del índice
└── NN-nombre-desafio/
    ├── CONTEXTO.md          # writeup (enunciado, análisis, solución, flag)
    ├── flag.txt             # la flag, sola
    ├── solucion/            # scripts reproducibles end-to-end
    └── work/                # artefactos intermedios (evidencia auditable)
```

Convenciones:

- Si el usuario ya creó una carpeta con otro nombre (`casaembrujada/`,
  `punto ciego/`), **se respeta**; no renombrar.
- Nada de archivos sueltos en la raíz de `ctf/` ni en la raíz del proyecto.
- El nombre del script describe la acción: `decodificar_coro.py`, `exploit_turno.py`,
  `resolver_puertas.py`. Evitar `test.py`, `prueba.py`, `script1.py`.

## Ciclo por desafío

1. **Antes de tocar un archivo existente** (índice, contexto de otro reto):
   ```bash
   cp CONTEXTO_CTF.md backups/CONTEXTO_CTF.md.$(date +%Y%m%d-%H%M%S)
   ```
2. Trabajar en `work/`. Nada de sobrescribir el artefacto original: se copia y se
   modifica la copia (`fragmento_reparado.png`, no `fragmento.bin`).
3. Mover el resultado final a `solucion/` y dejarlo ejecutable con argumentos
   explícitos (sin rutas absolutas del equipo del autor).
4. Actualizar `CONTEXTO.md` del desafío y añadir entrada al historial de
   `CONTEXTO_CTF.md` con: fecha, evidencia (tamaño + hash), técnica, flag y
   backup previo del índice.

## Entrada de historial (formato)

```markdown
### 2026-10-24 — Desafío 42 «El Susurro del Conde» resuelto
- Evidencia: `reto/audio.wav` (640.044 B, SHA256 `7CCD2A90…896011`).
- Hallazgo: <técnica en una línea>.
- Cadena: <paso → paso → flag>.
- Señuelos: <qué se descartó y por qué>.
- Herramienta: `susurro/solucion/descifrar_susurro.py`; artefactos en `susurro/work/`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261024-182942`.
```

## Reglas de oro del writeup

- **Reproducible:** otro analista ejecuta `solucion/` y obtiene la flag.
- **Con evidencia:** hash del artefacto, offsets, tamaños y salidas clave.
- **Con descartes:** lo que se probó y no funcionó, con la razón. Es la parte más
  útil para el siguiente reto.
- **Sin secretos innecesarios:** no pegar credenciales reales fuera del alcance
  del CTF; sí las del reto (son parte de la evidencia).
- **Español**, salvo nombres técnicos y rutas.

## Cierre

Checklist en `assets/checklist_triaje.md`. Si el reto no se resolvió, se documenta
igual: estado `en curso`, hipótesis vivas y fecha de último intento.
