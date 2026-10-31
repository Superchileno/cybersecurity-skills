---
name: performing-ctf-forensics-on-audio-and-logs
description: 'Análisis forense para CTF sobre audio, logs, capturas de red y artefactos
  de sistema de archivos. Cubre espectrogramas (texto dibujado en frecuencias), decodificación
  de tonos duales por FFT (nibbles), LSB en muestras PCM, correlación de logs CEF/UniFi,
  reconstrucción de sesiones FTP desde pcap, unión de proxy+backend por rid/flow/seq con
  inflado posterior, y recuperación de archivos borrados vía MFT + USN + espacio no asignado.
  Usar cuando el reto entregue WAV/MP3, archivos .log, .pcap, CSV de MFT/USN o un volcado
  de disco parcial.'
domain: cybersecurity
subdomain: ctf
tags:
- ctf
- forensics
- audio
- spectrogram
- fft
- pcap
- tshark
- logs
- cef
- mft
- usn
- timeline
version: '1.0'
author: auditoria-ia-v2
license: Apache-2.0
mitre_attack:
- T1005
- T1070
- T1071
- T1041
nist_csf:
- DE.AE-02
- DE.CM-01
- RS.AN-03
---

# Forense de Audio y Logs en CTF

Reconstruir qué pasó a partir de señales y registros: el secreto suele estar en una
capa que el formato no muestra por defecto (frecuencia, orden de eventos, campos
ocultos).

## When to Use

- El reto entrega audio y el enunciado habla de "mensaje oculto", "susurro", "señal".
- Hay `.log` con eventos de seguridad, o un `.pcap` pequeño.
- Se entregan varios registros que deben **cruzarse** para responder una pregunta.
- Hay un volcado de sistema de archivos (MFT, USN, `unalloc.raw`, imagen de disco).
- El reto pide reconstruir una línea de tiempo o identificar un actor.

**No usar** para análisis de malware (requiere contención) ni para audios de vigilancia
reales sin autorización.

## Prerequisites

- `sox`, `ffmpeg`, `python3` con `numpy` y `scipy` (opcional), `tesseract`.
- `tshark`/`wireshark`, `zeek` (opcional).
- `sleuthkit` (`fls`, `icat`, `mmls`), `analyzeMFT` (opcional).
- Scripts de esta skill.

## Workflow

### 1. Audio: caracterizar primero

```bash
soxi audio.wav            # sample rate, canales, bits, duración
sox audio.wav -n stat     # estadísticas
```

Calcular: duración total, número de segmentos si hay pausas, y si la longitud es
múltiplo de un patrón (p. ej. 30 tomas × 0,35 s = 10,5 s).

### 2. Audio: espectrograma antes que cualquier otra prueba

```bash
python scripts/spectrogram.py audio.wav --out work/ --width 1400
```

Si aparece texto dibujado, esa cadena suele ser una contraseña (de un ZIP) o la propia
flag. Ajustar rango dinámico (`-z`) y recortar la banda de interés.

### 3. Audio: tonos duales por FFT

```bash
python scripts/tone_nibbles.py audio.wav --segments 30 \
    --low 520 --high 1400 --step 40 --out work/
```

Cada segmento tiene dos picos: grave = nibble alto, agudo = nibble bajo. Reordenar
según la planilla si el reto la entrega.

### 4. Audio: LSB en muestras PCM

```bash
python scripts/pcm_lsb.py audio.wav --bit 0 --msb-first
```

Empaquetar el bit 0 de cada muestra, MSB-first. Si el resultado empieza con Base64,
decodificar; puede requerir XOR con una clave obtenida del espectrograma.

### 5. Logs: normalizar y contar

```bash
python scripts/correlate_logs.py --help
```

Reglas:

- Parsear el formato real (CEF: `CET`/`cs1=`/`cn1=`), no asumir CSV.
- Contar por entidad (host, IP, usuario) antes de leer en detalle.
- Ordenar por **índice del evento**, no por aparición en el archivo.
- Verificar desfases horarios declarados antes de cruzar fuentes.

### 6. pcap: seguir el flujo, no los paquetes

```bash
tshark -r captura.pcap -q -z conv,tcp
tshark -r captura.pcap -Y "ftp" -T fields -e ftp.request.command -e ftp.request.arg
tshark -r captura.pcap -z follow,tcp,ascii,14
```

Preguntas típicas: ¿cuántos intentos fallidos?, ¿qué usuario entró?, ¿qué archivo se
descargó?

### 7. Sistema de archivos: MFT + USN + no asignado

1. Leer `mft.csv`: nombre, estado de borrado, `DataRun`, timestamps.
2. Leer `usn.csv`: `CREATE` → `DATA_OVERWRITE` → `DELETE` con horas.
3. Convertir `DataRun` (clúster) a offset: `clúster × tamaño_clúster`.
4. Buscar la firma del formato en `unalloc.raw` en esos offsets.
5. Cruzar: el artefacto válido coincide exactamente con un `DataRun`; los señuelos no.

## Key Concepts

- **Espectrograma:** representación tiempo-frecuencia. Texto "dibujado" en el audio
  aparece como bandas horizontales/curvas en la imagen.
- **Nibble dual:** dos frecuencias por símbolo; `byte = (alta<<4) | baja`.
- **Tomas maestras vs calibración:** si hay planilla, sólo algunas tomas cuentan; el
  resto decodifica a basura plausible.
- **CEF:** formato de log `CEF:0|vendor|product|...|ext`. Los campos `cs1..cs4`/`cn1..`
  transportan datos personalizados; `cn1` suele ser el índice de orden.
- **Correlación por clave:** unir tablas por un identificador (`rid`), filtrar por
  estado (`OK`) y ordenar por la secuencia declarada, no por timestamp.
- **DataRun:** ubicación del contenido en clústeres. Es la prueba objetiva que
  distingue el archivo real del señuelo homónimo.
- **Ventana deslizante (HLS):** el manifiesto sólo lista los últimos minutos, pero los
  segmentos suelen ser direccionables por índice (`/sq/N/`), lo que permite recuperar
  el pasado.

## Tools & Systems

| Tarea | Herramienta |
|---|---|
| Info de audio | `soxi`, `ffprobe` |
| Espectrograma | `sox ... spectrogram`, `scripts/spectrogram.py` |
| FFT y picos | `scripts/tone_nibbles.py`, `numpy.fft` |
| LSB PCM | `scripts/pcm_lsb.py` |
| OCR de espectrograma | `tesseract` con `--psm 7` y whitelist |
| Logs | `awk`, `jq`, `scripts/correlate_logs.py` |
| pcap | `tshark`, `zeek`, `tcpflow` |
| Disco | `fls`, `icat`, `mmls`, `analyzeMFT`, `scripts/mft_dat` |

## Common Scenarios

### "El audio no tiene voz ni música"
Espectrograma. Si dibuja texto, es la clave. Si no, revisar LSB de las muestras.

### "Hay 30 tomas y una planilla"
La planilla dice el orden y cuáles son maestras. Ignorar las calibraciones: decodifican
a texto verosímil pero incorrecto (`_ 1 m _ p u a u` en un caso real).

### "El log tiene muchas alertas"
Contar por tipo y por host. El incidente real suele ser una repetición (4 beacons) y el
resto ruido (una alerta de cada tipo en otros hosts).

### "Los eventos no cuadran en el tiempo"
Buscar en el enunciado o en el log una nota de reloj adelantado/atrasado. Corregir el
desfase antes de cruzar; en un reto, 11 minutos de desfase cambiaban el barco
responsable.

### "El archivo borrado no está"
El borrado lógico no destruye datos. Con `DataRun` + `unalloc.raw` se recupera el
contenido completo; los homónimos suelen ser señuelos.

## Output Format

```markdown
## Evidencia
- archivo(s), tamaño, SHA-256
- formato real y parámetros (sample rate, clúster, etc.)

## Línea de tiempo / correlación
| hora | fuente | evento | interpretación |

## Hallazgo
- sujeto / host / usuario responsable
- artefacto que lo confirma

## Señuelos
- ...

## Flag
`...`
```

Referencias: `references/audio_forense.md`, `references/logs_y_correlacion.md`.
