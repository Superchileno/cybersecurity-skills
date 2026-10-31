# LSB, mosaicos y canales — esteganografía visual

## 1. LSB en imágenes

### Esquema más común en retos

- Bit **0** (el menos significativo) de cada componente.
- Orden **interleaved**: R, G, B del píxel 0, luego R, G, B del píxel 1, …
- Desde el offset 0 (no desde el centro ni desde el final).
- Empaquetado **MSB-first**: el primer bit es el bit 7 del primer byte.

```python
bits = []
for y in range(h):
    for x in range(w):
        for c in range(3):                     # R, G, B
            bits.append(pixel[y, x][c] & 1)
bytes_ = bytes(
    sum(bits[i + k] << (7 - k) for k in range(8))
    for i in range(0, len(bits) - 7, 8)
)
```

### Diagnóstico previo

- Media del LSB ≈ 0.5 en los tres canales → hay datos embebidos de forma uniforme.
- Media ≈ 0 → canal plano (posible máscara o imagen sintética).
- Histograma con pares de valores → posible LSB *matching* o *±1*.

### Orden de pruebas (registrar cada una)

| # | Bit | Orden | Canal | Resultado |
|---|---|---|---|---|
| 1 | 0 | interleaved | RGB | |
| 2 | 1 | interleaved | RGB | |
| 3 | 0 | planar | R, luego G, luego B | |
| 4 | 0 | interleaved | sólo el canal con mayor varianza | |
| 5 | 2–3 | interleaved | RGB | |

Si el bit 0 da texto que empieza con un Base64 válido pero se corta, revisar si hay un
terminador (`0x00`) y decodificar sólo hasta él.

## 2. Mosaicos y patrones periódicos

Cuando la imagen repite un patrón (sello, textura, ruido), el secreto está en las
**desviaciones** del patrón.

1. Calcular autocorrelación horizontal/vertical para estimar el periodo `P`.
2. Restar la imagen desplazada: `diff = |img - shift(img, P)|`.
3. Umbralizar: los píxeles fuera del patrón forman las letras.
4. Agrupar por bandas de filas y recortar cada línea para lectura.

En un reto, `P = 164 px` y las dos bandas de texto estaban en las filas 108–179 y
303–374; el resto de la imagen era ruido coherente.

## 3. Espectrogramas (imágenes que en realidad son audio, y viceversa)

- Si el artefacto es una imagen de un espectrograma, el texto está dibujado en
  frecuencias: leerlo visualmente y con OCR.
- Si es audio, generar el espectrograma antes de cualquier otra prueba.

```bash
sox audio.wav -n spectrogram -o spec.png -x 1200 -y 600 -z 90
```

Ajustes útiles: `-z` (rango dinámico), recorte temporal (`trim`), y canales
separados para señales estéreo.

## 4. QR y códigos

```bash
zbarimg -q imagen.png
```

Si el contenido es binario en texto (`01001100 00110000 …`), convertir grupos de 8
bits a ASCII. Si es Base64, decodificar. Si es una URL, no seguirla sin evaluar
(el contenido de un reto puede ser un señuelo o una inyección).

## 5. Estego clásica (probar después de lo anterior)

| Herramienta | Formato | Nota |
|---|---|---|
| `steghide` | JPEG/BMP/WAV | requiere passphrase; probar vacía |
| `stegseek` | JPEG | crackeo rápido de la passphrase |
| `zsteg -a` | PNG/BMP | barrido de combinaciones LSB |
| `exiftool` | todos | metadatos y trailers |
| `outguess` | JPEG | menos común |

## 6. Señuelos visuales típicos

- Planos LSB que dibujan formas pero no contienen texto.
- Chunks `tEXt` con una "pista" que lleva a una contraseña incorrecta.
- Imágenes internas que son copias de la portada.
- Espectrogramas con texto decorativo que no es la clave (probar siempre la cadena
  exacta, incluidos mayúsculas y números).

Validación: la clave/flag debe producir un resultado **estructuralmente** correcto
(abre el ZIP, cumple el formato, verifica el CRC).
