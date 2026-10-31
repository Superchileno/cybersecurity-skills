---
name: reversing-obfuscated-binaries-and-vms
description: 'Ingeniería inversa de binarios de CTF ofuscados: localización de main
  desde _start en binarios stripped, extracción de tablas en .rodata, resolución de
  permutaciones de índices, emulación de ofuscación aritmética con divisiones mágicas
  validada en GDB, análisis de máquinas virtuales de bytecode con dispatch por tabla de
  saltos, y uso de oráculos (conteo de instrucciones, longitud de ejecución, comparación
  de registros) para recuperar passphrases. Usar cuando el reto entregue un ELF sin
  símbolos que pide un token, vector o contraseña, o cuando el binario contenga un
  intérprete propio.'
domain: cybersecurity
subdomain: ctf
tags:
- ctf
- reversing
- obfuscation
- vm
- bytecode
- gdb
- radare2
- ghidra
- x86-64
- static-analysis
version: '1.0'
author: auditoria-ia-v2
license: Apache-2.0
mitre_attack:
- T1027
- T1140
- T1480
nist_csf:
- DE.AE-02
---

# Reversing de Binarios Ofuscados y VMs

Recuperar el secreto sin ejecutar el binario a ciegas: entender la estructura, aislar
la transformación y verificarla con el propio programa.

## When to Use

- ELF stripped que pide un "token", "vector" o "passphrase".
- El binario contiene un intérprete (VM) y un programa embebido.
- Hay tablas de bytes en `.rodata` que se usan como claves o permutaciones.
- El tamaño del archivo no cuadra con sus secciones (overlay).
- Se necesita un oráculo cuando la comparación es opaca.

**No usar** para malware real (requiere sandbox y contención) ni para binarios sin
autorización.

## Prerequisites

- `radare2`/`rizin`, `ghidra`, `objdump`, `readelf`, `strings`.
- `gdb` con `pwndbg`/`gef`, `strace`/`ltrace`.
- Python 3 con `pyelftools` (opcional), `capstone` (opcional).
- Scripts de esta skill.

## Workflow

### 1. Reconocimiento

```bash
python ../exploiting-binary-vulnerabilities-in-ctf/scripts/checksec_summary.sh ./binario
readelf -SW ./binario
readelf -sW ./binario | head -20
```

Comprobar:

- `.text` pequeño respecto al archivo → overlay (posible cebo).
- Secciones `rwx` o `W+X` → probable VM o shellcode.
- Entradas dinámicas (`printf`, `fopen`) → hay I/O que aprovechar.

### 2. Localizar `main` sin símbolos

```bash
python scripts/find_main.py ./binario
```

Heurística: `_start` → `__libc_start_main(main, ...)` → primer argumento en `rdi`.
En binarios estáticos, buscar la llamada a `__libc_start_main` y el `lea rdi, [rip+...]`
anterior.

### 3. Identificar la transformación

Leer el bucle principal y anotar:

- Índice de entrada: ¿lineal, permutado (`(k*i) mod n`), invertido?
- Clave: ¿en `.rodata`, construida en pila, derivada del índice?
- Operaciones por byte: XOR, rotación, suma, tabla.
- Condición de éxito: comparación byte a byte, checksum, o retorno de la VM.

### 4. Buscar código muerto

Antes de invertir una segunda etapa:

- ¿La condición es alcanzable con la entrada permitida (`fgets`, longitud fija)?
- ¿El checksum puede coincidir? (calcularlo)
- ¿El valor comparado es imprimible?

En un reto, la segunda etapa exigía 36 bytes no imprimibles y el checksum nunca
coincidía: era código muerto.

### 5. Resolver sin invertir

Si la condición es byte a byte y los índices se recorren todos:

```python
for i in range(n):
    for v in range(256):
        if eval_etapa(entrada_con(v, i)):
            solucion[i] = v
```

Esto evita invertir rotaciones y divisiones mágicas. Complejidad `256·n`.

### 6. Validar con GDB

Cuando la emulación no coincide, instrumentar:

```bash
gdb -q ./binario \
  -ex 'b *0x1380' -ex 'b *0x13af' -ex 'b *0x13c6' \
  -ex 'run < /tmp/entrada' \
  -ex 'info registers' -ex 'x/8i $pc'
```

En un caso, esto reveló un `add esi, edi` que faltaba antes de la primera rotación.

### 7. VM de bytecode

1. Localizar el intérprete: un bucle con `switch` compilado a **tabla de saltos**
   (`jmp [rax*8 + tabla]`).
2. Identificar el fetch: `op = code[pc]`, `pc += 1`.
3. Mapear los opcodes: `mov reg, imm16`, `xor reg, reg`, `cmp`, `jcc`, `store`.
4. Extraer el programa embebido (offset y longitud suelen ser constantes en `main`).
5. Decodificar los pares XOR de la sección de comparación.

### 8. Oráculo de ejecución (VM)

Si no se puede invertir la validación:

- Poner un breakpoint en el fetch del intérprete.
- Contar instrucciones ejecutadas para cada entrada candidata.
- La entrada correcta ejecuta **más** instrucciones (avanza más en el programa).
- Fuerza bruta del último carácter sobre el alfabeto permitido.

Ejemplo real: `aaaaaaaaaa` → 56 instrucciones, `passphrase9` → completa y muestra el
token.

## Key Concepts

- **`_start` → `main`:** el entry point pasa `main` como primer argumento a
  `__libc_start_main`.
- **Permutación de índices:** `(k*i) mod n` con `gcd(k,n)=1` recorre todos los índices;
  permite resolver por posición.
- **División mágica:** el compilador reemplaza `div` por multiplicación y shift; la
  emulación debe replicar el redondeo exacto.
- **Tabla de saltos:** `jmp qword [base + rax*8]` con un array de direcciones en
  `.rodata` identifica un dispatcher de VM.
- **Oráculo:** cualquier observable (conteo, tiempo, salida parcial) que revela
  información sobre bytes correctos.
- **Código muerto:** ramas inalcanzables que parecen la "etapa final".
- **Overlay:** bytes después del final de la última sección; suele ser relleno.

## Tools & Systems

| Tarea | Herramienta |
|---|---|
| Estructura ELF | `readelf`, `scripts/find_main.py` |
| Desensamblado | `objdump -d`, `r2 -A`, Ghidra |
| Emulación | `unicorn`, `qiling`, o script propio |
| Depuración | `gdb` + `pwndbg` |
| Extracción de tablas | `scripts/extract_tables.py` |
| Fuerza bruta con oráculo | `scripts/oracle_bruteforce.py` |

## Common Scenarios

### "El archivo pesa 8 MB y `.text` mide 3 KB"
Overlay. Ignorarlo salvo que `binwalk` encuentre algo. En un reto era cebo.

### "Pide un vector de 36 bytes"
Bucle con índice permutado y condición por byte. Resolver con fuerza bruta por índice
(36×256) en vez de invertir las rotaciones.

### "El token se construye con una tabla de índices"
`token[i] = "CLAVE"[tabla[i%5]] ^ clave[i]` produce `EVALC`, no `CLAVE`. La flag era
`indices_que_nadie_miro`.

### "Hay un intérprete y un programa embebido"
Mapear opcodes, extraer el programa, y decodificar los pares XOR de la sección de
comparación. Si hace falta la passphrase, usar el oráculo de conteo.

### "El programa dice 'Trayectoria perdida' y no hay más pistas"
Buscar la cadena de comparación y trabajar hacia atrás: qué debe valer cada registro
en el momento del `cmp`.

## Output Format

```markdown
## Binario
- formato, protecciones, SHA-256, tamaño de secciones

## Estructura
- main en 0x..., bucle de N iteraciones, tabla en .rodata:0x...

## Transformación
```python
# emulación comentada
```

## Validación
- GDB: breakpoints y registros observados
- ejecución real: salida

## Flag
`...`
```

Referencias: `references/localizar_main_y_tablas.md`, `references/vm_y_oraculos.md`.
