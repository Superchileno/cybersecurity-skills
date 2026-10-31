# Catálogo de señuelos y validación

La mayoría de los retos incluyen 2–4 datos que decodifican a algo plausible pero
falso. Confundirlos con la flag cuesta tiempo y credibilidad en el writeup.

## 1. Señuelos observados por categoría

| Categoría | Señuelo típico | Cómo se detecta |
|---|---|---|
| Estego | Lámina/planilla "reimpresa" con valores trocados | La lámina de control decodifica texto conocido sólo con el catálogo auténtico |
| Estego | Chunk `tEXt` con una clave que no abre nada | Probar la clave y verificar CRC; si falla, es cebo |
| Estego | Imagen interna que es copia de la portada | Comparar hashes/perceptual hash |
| Audio | Tomas de "calibración" que decodifican a texto verosímil | La planilla marca cuáles son MAESTRAS |
| Audio | Tono constante al final | No aporta información (FSK/DTMF descartados) |
| Crypto | Boletos que dicen "frío, muy frío", "más suerte la próxima" | No cumplen el formato de flag |
| Crypto | Clave con variante leet (`CLAVE` vs `CLAVE`) | El XOR se rompe en una posición concreta |
| Forense | Archivos con `DataRun` válido pero contenido `deadbeef` | El JSON de cabecera declara `batch: q1-draft` |
| Forense | Flujo de proxy con todos los eventos `REJECT` | "PREPRODUCCION: ensayo descartado" |
| Forense | Sesiones cifradas que validan SHA-256 pero no traen flag | Sólo una trae la flag; el resto son actas de desvío |
| Web | `flag{ejemplo}` en `strings` | Literal en el binario |
| Web | Base64 que decodifica a binario aleatorio | No es texto, no tiene estructura |
| Pwn | Función "win" que imprime un mensaje sin flag | Verificar qué abre realmente |
| Reversing | Segunda etapa con checksum imposible | Código muerto: la condición nunca se cumple |

## 2. Reglas de validación (en orden de fuerza)

1. **La plataforma acepta la flag.** Es la única validación definitiva.
2. **Estructura:** prefijo oficial + cuerpo legible (`flag{...}`, `flag{ejemplo}`).
3. **Integridad criptográfica:** CRC del ZIP, SHA-256 declarado, firma válida.
4. **Round-trip:** `decrypt(encrypt(x)) == x` para cifradores caseros.
5. **Coherencia semántica:** la flag tiene palabras relacionadas con la historia.
   (`bDRz → l4s` encaja con `s3n4l3s`; `PREFIJO` no encaja con `PREFIJO`.)

## 3. Señales de que estás ante un señuelo

- El texto es legible pero **no** tiene el prefijo oficial.
- El prefijo está corrupto en exactamente un carácter (`PREFIJO`).
- La decodificación produce bytes no imprimibles intercalados.
- El artefacto está etiquetado como `draft`, `test`, `ensayo`, `calibración`,
  `preproducción` o `scratch`.
- Hay dos candidatos y uno requiere una suposición adicional no justificada.

## 4. Qué registrar

Para cada señuelo, en el writeup:

```markdown
- `pista_ensayo.txt` → decodifica `PRUEBA DE AUDIO`; descartado porque la bitácora
  de cabina marca esa transmisión como no autorizada (21:40, ensayo).
```

Registrar el descarte **con la razón** es lo que permite a otro analista no repetir
el camino y demuestra que la flag se eligió por criterio, no por suerte.
