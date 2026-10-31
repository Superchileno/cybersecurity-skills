# Sustitución, Vigenère y catálogos

## 1. César

Desplazamiento fijo. Se detecta comparando el prefijo esperado con el observado:

```
PREFIJOX{...}   →   flag{ejemplo}     desplazamiento −3
```

Si no se conoce el prefijo, probar los 26 desplazamientos y puntuar por frecuencia de
letras del idioma (espacio, `e`, `a`, `o` en español).

## 2. Vigenère

`C = P + K (mod 26)` o `C = P − K (mod 26)`. En retos aparecen variantes:

- **Inversa:** el cifrador resta en vez de sumar; hay que probar ambos signos.
- **Clave que sólo avanza en letras:** espacios, dígitos y símbolos se conservan y
  **no consumen** clave. Si se aplica ingenuamente, todo el mensaje se desplaza.
- **Alfabeto reducido:** a veces sólo `a-z`, sin mayúsculas.

```python
def vigenere(texto, clave, signo=+1, solo_letras=True):
    salida, k = [], 0
    for ch in texto:
        if ch.isalpha() and ch.isascii():
            base = ord('A') if ch.isupper() else ord('a')
            desplaz = ord(clave[k % len(clave)].lower()) - ord('a')
            salida.append(chr((ord(ch) - base + signo * desplaz) % 26 + base))
            k += 1
        else:
            salida.append(ch)
    return "".join(salida)
```

Validación: aplicar con el prefijo conocido en las dos polaridades y comprobar que el
cuerpo es legible. En un reto, sólo la resta daba texto coherente.

## 3. Sustitución por catálogo de glifos

Estructura típica:

```
catalogo_glifos.txt    →  16 glifos ↔ valores hex (0..F)
lamina_PROMO.txt       →  lámina de control (texto conocido)
lamina_objetivo.txt    →  lámina con la flag
```

Regla: **2 glifos por byte** (hex). El catálogo define el mapeo.

Trampa real: existía un segundo catálogo "reimpreso" con dos valores intercambiados
(`▽` y `▲`, 9↔2). Con el catálogo falso, la lámina de control daba basura y la flag
salía plausible pero corrupta (`PREFIJO{...}`).

Procedimiento obligatorio:

1. Decodificar la lámina de **control** con el catálogo candidato.
2. Si el control no produce el texto conocido, el catálogo es falso.
3. Sólo entonces decodificar la lámina objetivo.

## 4. Sustituciones numéricas y binarias

| Esquema | Identificación | Inverso |
|---|---|---|
| Morse aparente (`.`/`-`) | Sólo 2 tokens distintos; longitud total múltiplo de 8 | Bits → bytes → ASCII |
| Binario enmascarado | Grupos de 8 símbolos | Igual |
| Códigos de 5 bits (Baudot/ITA2) | Longitud múltiplo de 5 | Tabla ITA2 |
| Nibbles duales | Dos frecuencias por símbolo | `byte = (alto<<4) | bajo` |
| Base45 | 45 símbolos, longitud múltiplo de 3 | `base45.b45decode` |

Polaridad: en un flujo de `.`/`-`, probar `'.'=1` y `'-'=1`. La incorrecta produce
`0xFF` repetidos o bytes no imprimibles.

## 5. Cadenas de codificación (identificación por alfabeto)

| Codificación | Alfabeto | Longitud |
|---|---|---|
| Hex | `0-9a-fA-F` | par |
| Base32 | `A-Z2-7=` | múltiplo de 8 |
| Base64 | `A-Za-z0-9+/=` | múltiplo de 4 |
| Base64url | `A-Za-z0-9-_` | múltiplo de 4 |
| Base45 | `0-9A-Z $%*+-./:` | múltiplo de 3 |
| Ascii85 | `!` a `u` | múltiplo de 5 (aprox.) |
| Ook! | palabras `Ook.` `Ook?` `Ook!` | — |
| Brainfuck | `+-<>[].,` | — |

Un reto real encadenó: hex → ASCII → Base45 → Base64 → Ook! → Brainfuck. La clave fue
comprobar `set(texto) ⊆ alfabeto` y `len % 3 == 0` en cada nivel, en vez de asumir que
el texto era una modulación binaria.

## 6. Señuelos en criptografía

- Mensajes que decodifican a frases motivacionales o de burla.
- Claves "casi" correctas (variante leet) que fallan en una posición.
- Catálogos reimpresos con un valor alterado.
- Texto que parece Base64 pero decodifica a binario aleatorio.

Criterio: la flag correcta cumple formato **y** coherencia semántica **y** (si aplica)
integridad criptográfica.
