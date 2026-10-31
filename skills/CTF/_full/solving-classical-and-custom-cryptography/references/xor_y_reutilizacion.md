# XOR, keystream reutilizado y crib-dragging

## 1. Propiedades que se explotan

| Propiedad | Consecuencia |
|---|---|
| `C = P ⊕ K` | `P = C ⊕ K` |
| `C1 ⊕ C2 = P1 ⊕ P2` | Con dos cifrados del mismo keystream, la clave desaparece |
| `P ⊕ P = 0` | Los bytes iguales en la misma posición se anulan |
| `crib ⊕ C = K` | Un fragmento conocido recupera el keystream en ese offset |

## 2. Two-time pad con par conocido

Datos: `P1` (texto plano), `C1` (su cifrado), `C2` (otro cifrado del mismo esquema).

```
K  = C1 ⊕ P1
P2 = C2 ⊕ K
```

Condiciones para que funcione:

- `C1` y `C2` tienen la **misma longitud** (o el keystream se reutiliza desde el inicio).
- El keystream no depende de un contador por mensaje.
- Validación: `C1 ⊕ C2` debe tener **ceros en los extremos** (donde `P1 == P2`, típico
  en cabeceras y pies estructurados como `usuario=...` / `region=cl;mfa=on`).

Detección temprana en un reto real: ambos tokens medían 128 B y `C1 ⊕ C2` empezaba y
terminaba en ceros → mismo keystream confirmado antes de intentar nada más.

## 3. Crib-dragging

Cuando no hay par conocido pero se conoce el formato esperado:

```python
for offset in range(len(C) - len(crib) + 1):
    keystream = bytes(c ^ p for c, p in zip(C[offset:offset+len(crib)], crib))
    # si el keystream se repite o es texto, es candidato
```

Aplicaciones:

- Recuperar la clave de un XOR repetido (el crib cubre al menos un periodo completo).
- Verificar la longitud de la clave: si el keystream extraído tiene periodo `L`, ese es
  el largo de la clave.
- Confirmar un descifrado: el resultado debe ser texto coherente en **todo** el mensaje.

## 4. XOR con clave repetida sin crib

1. Estimar `L` minimizando la entropía media de las columnas:

```python
for L in range(1, 65):
    columnas = [C[i::L] for i in range(L)]
    score = sum(entropia(c) for c in columnas) / L
```

2. Resolver cada columna como XOR de un byte: el byte de clave que maximiza la
   proporción de caracteres imprimibles / la frecuencia de espacio (`0x20`).

3. Unir las columnas y validar.

## 5. Vector de ataque típico en CTF

Un reto entregó 10 boletos en Base64 y una pista: la marca `clave_de_ejemplo` estaba
"presente en todos los registros y era necesaria para revisarlos". Es decir: Base64 →
XOR con `clave_de_ejemplo` repetida. Los 10 decodificaban a frases; sólo uno tenía
estructura de flag. Los otros nueve eran señuelos ("frío, muy frío").

Lección: **la pista del enunciado suele ser literal**. Si dice "la marca está presente
en todos los registros", se prueba esa cadena como clave antes que cualquier fuerza
bruta.

## 6. Errores frecuentes

- Aplicar el XOR sobre la representación hex (texto) en vez de sobre los bytes.
- Olvidar que un keystream de 8 bytes sólo es válido si la longitud del mensaje es
  múltiplo de 8; si no, la última vuelta se trunca.
- Confundir `C1 ⊕ C2` con `P1 ⊕ P2` cuando los mensajes tienen longitudes distintas.
- Aceptar un resultado "casi legible": un solo byte mal indica clave incorrecta o
  índice desplazado.
