# Localizar `main`, entender tablas y detectar código muerto

## 1. De `_start` a `main` en un binario stripped

En x86-64 dinámico:

```asm
_start:
  xor  ebp, ebp
  mov  r9, rdx              ; rtld_fini
  pop  rsi                  ; argc
  mov  rdx, rsp             ; argv
  and  rsp, -16
  ...
  lea  rdi, [rip+0x...]     ; <-- main
  call __libc_start_main@plt
```

Procedimiento:

1. `readelf -h` → entry point.
2. Desensamblar desde el entry.
3. Buscar la llamada a `__libc_start_main`.
4. El `lea rdi, [rip+X]` anterior es `main`.
5. En estáticos: `__libc_start_main` está dentro del binario; buscar la referencia
   directa a `main` en el `_start`.

Atajo con GDB:

```bash
gdb -q ./binario -ex 'b *0x401040' -ex run -ex 'info registers rdi' \
    -ex 'x/40i $rdi'
```

## 2. Tablas en `.rodata`

Patrones típicos:

| Patrón | Interpretación |
|---|---|
| 16 valores 0..15 | catálogo de nibbles |
| Permutación de 0..n-1 | tabla de índices (`tabla_B`) |
| 32/64 bytes aleatorios | clave XOR |
| Array de direcciones (8 B cada una) | tabla de saltos de VM |
| Cadenas cortas separadas por `\0` | alfabeto o nombres de opcode |

Extracción:

```bash
objdump -s -j .rodata ./binario | head -40
python scripts/extract_tables.py ./binario --offset 0x21a0 --length 32
```

Verificación: una tabla de índices debe ser una permutación exacta (sin repetidos)
para que el algoritmo recorra todos los elementos.

## 3. Permutaciones y orden de lectura

Si el índice de entrada es `(k*i) mod n`:

- Comprobar `gcd(k, n) == 1`; si no, el bucle no cubre todos los índices.
- El resultado se construye en orden de `i`, pero se lee en el orden permutado.
- No hace falta invertir: se resuelve por posición.

Ejemplo: `(7*i) mod 36` con `gcd(7,36)=1` → 36 posiciones distintas, una solución por
posición.

## 4. División mágica

`div`/`idiv` por constante se compila como multiplicación por un inverso y shift:

```asm
movabs rax, 0xAAAAAAAAAAAAAAAB
mul  rcx
shr  rdx, 1
```

Al emular, replicar exactamente:

- El multiplicador y el shift deben tomarse del binario.
- Para negativos, el redondeo es hacia cero (`idiv`), no hacia −∞.
- Validar con GDB: poner un breakpoint después del cálculo y comparar.

En un reto, la emulación fallaba por un `add esi, edi` omitido antes de la primera
rotación; la traza de GDB lo reveló.

## 5. Código muerto

Antes de invertir una etapa, comprobar:

| Pregunta | Cómo |
|---|---|
| ¿La rama es alcanzable? | ¿Hay un `jmp` que la salte siempre? ¿La condición es posible? |
| ¿El checksum puede coincidir? | Calcularlo con los datos reales |
| ¿El valor comparado es imprimible? | Volcarlo; si incluye `0x0a` y la entrada es `fgets`, es imposible |
| ¿La variable cambió alguna vez? | Buscar escrituras; si nace con un valor y nunca se modifica, la comparación es decorativa |

Ejemplos reales:

- Comparación con `999` sobre una variable inicializada en `0x54` y nunca modificada.
- Checksum que da `0xf5` y exige `0x24`.
- Tabla de 36 bytes con `0x0a` que `fgets` no puede introducir.

## 6. Overlay

```bash
readelf -SW binario | awk '{print $6}' | tail -5
stat -c %s binario
```

Si el archivo es mucho mayor que la última sección, hay overlay. Comprobar con
`binwalk`; si no hay firma conocida ni entropía alta, es relleno.

## 7. Checklist

- [ ] `main` localizado y confirmado en GDB
- [ ] Tablas extraídas y clasificadas
- [ ] Permutación verificada (`gcd`, sin repetidos)
- [ ] Operaciones anotadas con su dependencia
- [ ] Código muerto identificado y documentado
- [ ] Emulación validada contra el binario real
- [ ] Resultado verificado ejecutando el programa
