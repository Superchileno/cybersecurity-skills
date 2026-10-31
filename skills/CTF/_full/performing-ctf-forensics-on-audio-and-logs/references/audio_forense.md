# Forense de audio

## 1. Orden de pruebas

1. **Espectrograma** (lo primero, siempre). Es barato y resuelve la mayoría.
2. **Estructura**: ¿cuántos segmentos?, ¿hay silencios?, ¿la duración es múltiplo de
   un patrón?
3. **LSB en muestras PCM** (bit 0, MSB-first, hasta `0x00`).
4. **Tonos / frecuencias** (FFT por ventana, picos, nibbles).
5. **Estego clásica** (`steghide`, `stegseek`) si es WAV/MP3.
6. **Descartar explícitamente**: DTMF, FSK, Morse, SSTV.

## 2. Espectrograma

```bash
sox audio.wav -n spectrogram -o spec.png -x 1200 -y 600 -z 90
# recortar 0–5 s y ampliar
sox audio.wav -n trim 0 5 spectrogram -o spec_zoom.png -x 1600 -y 800 -z 110
```

Parámetros:

- `-x` ancho, `-y` alto: subirlos si el texto es pequeño.
- `-z` rango dinámico: más alto = más contraste de señales débiles.
- Canales separados: `sox audio.wav -c 1 -n spectrogram` por canal.

Lectura: el texto aparece como trazos claros sobre fondo oscuro, normalmente entre
1 y 4 kHz. Si el texto es tenue, convertir a escala de grises, aplicar autocontraste y
ampliar ×10 antes de OCR.

OCR:

```bash
tesseract spec.png salida --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_
```

`--psm 7` trata la imagen como una sola línea; `--psm 6` como bloque. Validar el
resultado a mano: OCR confunde `5`/`2`, `0`/`O`, `1`/`l`.

## 3. Tonos duales (nibbles)

Esquema observado: cada toma de 0,35 s contiene **dos** tonos puros; uno grave (nibble
alto) y uno agudo (nibble bajo), con un paso de 40 Hz entre valores 0..15.

```
f_grave = 520 + 40*k_alto
f_agudo = 1400 + 40*k_bajo
byte    = (k_alto << 4) | k_bajo
```

Procedimiento:

1. Segmentar por silencios o por duración fija.
2. Ventana de análisis: 0,05–0,28 s dentro de cada toma (evita ataques y colas).
3. FFT con ventana Hann de 32768 puntos.
4. Pico en la banda grave y pico en la banda aguda.
5. `k = round((f - base) / step)`; descartar si el error supera medio paso.
6. Reordenar por la columna `orden` de la planilla.
7. Filtrar tomas no maestras.

## 4. LSB en PCM

```python
import wave, numpy as np
with wave.open("audio.wav") as w:
    n, sw, ch = w.getnframes(), w.getsampwidth(), w.getnchannels()
    data = np.frombuffer(w.readframes(n), dtype="<i2")
bits = (data & 1).astype(np.uint8)
# MSB-first
bytes_ = np.packbits(bits).tobytes()
```

Notas:

- Empaquetado MSB-first es lo habitual; si sale basura, probar LSB-first.
- Hay un terminador `0x00` antes del relleno: cortar ahí.
- Si el resultado es Base64, decodificar; puede requerir XOR con una clave del
  espectrograma (`CLAVE` vs `CLAVE` en un caso real).
- Probar bits 1–3 sólo después de descartar el bit 0, y registrar lo probado.

## 5. Lo que se descarta y por qué

| Señal | Prueba | Conclusión típica |
|---|---|---|
| Tono constante al final | FFT | Relleno, no información |
| Pulsos periódicos | Intervalo regular | Son los glifos del texto, no Morse |
| Dos frecuencias alternas | DTMF (697/770/852/941 y 1209/1336/1477/1633) | Sólo si coinciden exactamente |
| Ráfagas cortas | Morse | Descartar si el texto ya está en el espectrograma |

## 6. Video y streams

- El manifiesto HLS es una **ventana deslizante**: sólo lista los últimos minutos.
- Los segmentos suelen ser accesibles por índice (`/sq/N/`), lo que permite recuperar
  el DVR completo aunque `ffmpeg -ss` no llegue.
- Para texto en pantalla: extraer frames, recortar la región, aumentar contraste del
  canal de color dominante y aplicar OCR con whitelist.
