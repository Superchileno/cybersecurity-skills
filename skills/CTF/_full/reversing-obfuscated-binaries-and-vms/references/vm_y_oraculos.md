# VMs de bytecode y oráculos

## 1. Anatomía de una VM en un binario

Un intérprete embebido suele tener:

```c
void vm(uint8_t *state, uint8_t *code, size_t len) {
    size_t pc = 0;
    while (pc < len) {
        uint8_t op = code[pc++];
        switch (op) {
            case 0x10: /* mov reg, imm16 */ ...
            case 0x11: /* avanza índice */ ...
            case 0x12: /* store */ ...
            case 0x22: /* xor */ ...
            case 0x30: /* cmp */ ...
            case 0x41: /* jcc */ ...
        }
    }
}
```

Compilado, el `switch` aparece como **tabla de saltos**:

```asm
lea  rax, [rip+0x20ac]     ; tabla de direcciones
movzx rdx, byte [rcx]      ; opcode
jmp  qword [rax + rdx*8]
```

Identificación: array de punteros consecutivos en `.rodata` que apuntan dentro de
`.text`, con varios destinos cercanos entre sí.

## 2. Mapear los opcodes

1. Volcar la tabla de saltos y sus destinos.
2. Para cada destino, leer las primeras instrucciones: qué operandos consume.
3. Nombrar los opcodes por función, no por número.
4. Verificar con el programa embebido: las secuencias deben tener sentido.

Formato típico de instrucción (variable):

```
op  reg/idx  imm16
```

o `op imm16` para saltos.

## 3. Extraer el programa embebido

En `main`, el intérprete se invoca con constantes:

```asm
lea rsi, [rip+0x2300]      ; bytecode
mov edx, 0x2d7             ; longitud
call vm
```

Extraer exactamente esos bytes y desensamblar el bytecode con el mapa de opcodes.

## 4. Secciones típicas del bytecode

| Sección | Contenido |
|---|---|
| A | validación de longitud y caracteres (comparaciones por byte) |
| B | construcción del token/flag en memoria (`store` de pares XOR) |
| C | salto de fallo / éxito |

Si B es independiente de la entrada, la flag se puede extraer **estáticamente**
(decodificando los pares XOR). Si depende de la entrada, hace falta el oráculo.

## 5. Oráculo de instrucciones

Cuando la validación es opaca:

1. Breakpoint en el fetch del intérprete (la instrucción que incrementa `pc`).
2. Contar cuántas veces se ejecuta para una entrada dada.
3. Más instrucciones ⇒ la entrada avanzó más ⇒ prefijo correcto.
4. Fuerza bruta carácter a carácter.

Ejemplo de tabla observada:

| Entrada | Instrucciones | Lectura |
|---|---|---|
| `aaaaaaaaaa` | 56 | falla en el 1.er carácter |
| `npassphrase` | 68 | 2 caracteres correctos |
| `passphrase0` | 164 | 9 caracteres correctos |
| `passphrase9` | completa | ✅ |

Con `[a-z0-9]` y longitud fija, la fuerza bruta es 36 candidatos por posición.

## 6. Otros oráculos

| Observable | Uso |
|---|---|
| Longitud de ejecución (tiempo) | Comparación no constante |
| Número de iteraciones | Avance en un bucle |
| Salida parcial (`puts` antes del `cmp`) | Byte correcto confirmado |
| Código de retorno | Éxito/fracaso binario |
| Crash vs no crash | Límite de un buffer |
| `ptrace` + comparación de registros | Estado esperado |

## 7. Validación final

- Ejecutar el binario con la entrada recuperada y comprobar la salida.
- Comparar con la flag extraída estáticamente (deben coincidir).
- Si no coincide, revisar: orden de la planilla, mayúsculas, longitud exacta,
  terminador `\n`.

## 8. Trampas comunes

- Confundir el bytecode con datos: verificar que el intérprete lo consume.
- Asumir que la sección B se ejecuta siempre (puede estar tras la validación).
- Olvidar que la VM puede escribir en `state+0x100` y no en `state`.
- Interpretar el conteo de instrucciones sin fijar la longitud de entrada: longitudes
  distintas producen conteos no comparables.
