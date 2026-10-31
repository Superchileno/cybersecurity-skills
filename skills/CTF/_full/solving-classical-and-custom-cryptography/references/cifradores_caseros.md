# Cifradores caseros — cómo invertirlos sin adivinar

## 1. Procedimiento general

1. **Leer el código completo** (o descompilar la función de cifrado). No ejecutar a
   ciegas un binario que puede pedir red.
2. Anotar cada operación por byte y su dependencia: índice, byte anterior, clave.
3. Verificar si es **inyectivo** (reversible). Si dos entradas distintas dan la misma
   salida, no es el camino.
4. Escribir el inverso en orden inverso.
5. Validar con round-trip sobre un mensaje de prueba, y luego sobre el artefacto.

```python
assert cifrar(descifrar(x)) == x
```

## 2. Ejemplo real: XOR + rotación + swap de nibbles

Cifrado por byte `b` en posición `i`:

```
b ^= clave[i % len(clave)]
b = rotl(b, (i % 7) + 1)
b = swap_nibbles(b)
```

Descifrado:

```
b = swap_nibbles(b)                      # el swap es su propia inversa
b = rotr(b, (i % 7) + 1)
b ^= clave[i % len(clave)]
```

Notas:

- El swap de nibbles es involutivo: aplicarlo dos veces deja el byte igual.
- La rotación debe usar el mismo `(i % 7) + 1` calculado sobre el **índice del byte**,
  no sobre el índice del carácter del texto cifrado (si hay hex, cada byte son dos
  caracteres).
- Validación adicional: si el resultado es 100% imprimible y contiene el prefijo de
  flag, es correcto.

## 3. Ejemplo real: token con tabla de índices

```
token[i] = "CLAVE"[ tabla[i % 5] ] ^ clave[i]
tabla = [3, 1, 4, 0, 2]
```

El texto índice resultante no es `CLAVE` sino `EVALC` (lectura permutada). La flag del
reto era literalmente `indices_que_nadie_miro`.

Lección: si el algoritmo construye una cadena a partir de una tabla, **el resultado
está en el orden de la tabla**, no en el orden del literal.

## 4. Ejemplo real: ofuscación aritmética con división mágica

Bucle de `n` iteraciones con:

- índice de entrada `(7*i) mod n` (permutación si `gcd(7,n)=1`)
- rotaciones dependientes de `i`
- XOR con constantes lineales (`0x41 + 0x13*i`)
- comparación final de un registro

Estrategia: como la condición es byte a byte y los índices se recorren todos, se
prueban los 256 valores por índice (256·n evaluaciones) en vez de invertir las
rotaciones. Si el binario usa divisiones mágicas, validar la emulación con GDB
(breakpoints en las comparaciones) antes de confiar en el resultado.

## 5. Ejemplo real: cifrador con dos etapas, una muerta

Un binario tenía una segunda etapa (checksum de una tabla + comparación con 36 bytes
no imprimibles) que **nunca podía ejecutarse**: el checksum daba `0xf5` y exigía
`0x24`, y la entrada se leía con `fgets` (imposible teclear `0x0a`).

Regla: antes de romper una etapa, comprobar si es alcanzable. En varios retos la
mitad del binario era código muerto.

## 6. Cifradores por bloque "de juguete"

| Esquema | Ataque típico |
|---|---|
| ECB | Bloques repetidos → patrón visible |
| CBC con IV fijo | XOR del bloque anterior conocido |
| CTR con nonce reutilizado | Igual que two-time pad |
| Feistel casero con pocas rondas | Fuerza bruta / diferencial |
| Sustitución + permutación con clave corta | Índice de coincidencia y frecuencia |

## 7. Checklist

- [ ] Código leído completo (no sólo la función `main`)
- [ ] Operaciones anotadas con su dependencia (índice / clave / byte previo)
- [ ] Reversibilidad comprobada
- [ ] Round-trip pasa
- [ ] Resultado 100% imprimible
- [ ] Prefijo de flag presente
- [ ] Señuelos (mensajes "casi" correctos) descartados por estructura
