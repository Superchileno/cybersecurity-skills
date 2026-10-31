# Triaje por artefacto — "si ves X, aplica Y"

Tabla destilada de 39 desafíos resueltos (una competición de CTF) y 8 retos una competición de CTF.
Cada fila indica la **primera** prueba a ejecutar, no la única.

## 1. Archivos contenedores

| Señal observada | Primera prueba | Herramienta |
|---|---|---|
| ZIP dentro de ZIP, nombres numéricos o Fibonacci | Desanidar en memoria hasta el final | `scripts/zip_nested.py` |
| ZIP anexado tras PNG/JPEG/GIF | Carving desde el marcador de fin | `scripts/carve_appended.py` |
| ZIP cifrado + contraseña "visible" en otro artefacto | Probar la cadena tal cual (espectrograma, `tEXt`, EXIF) | `7z`, `python zipfile` |
| ZIP cifrado sin pista | Diccionario / known-plaintext con prefijo de flag | `zip2john`+`john`, `bkcrack` |
| Un archivo "imposible" (PNG que también es ZIP) | Polyglot: validar ambas firmas y extraer por offset | `binwalk -eM` |
| DOCX/XLSX/PPTX | Es un ZIP: descomprimir y buscar texto blanco, `vanish`, `customXml` | `scripts/ooxml_scan.py` |
| PDF | `pdf-parser`, objetos con `/JS`, texto invisible, capas | `pdfid`, `pdf-parser` |
| Binario con overlay enorme (ej. 8 MB y `.text` de 3 KB) | Ignorar el overlay; es cebo | `readelf -SW` |

## 2. Imágenes

| Señal | Prueba | Nota |
|---|---|---|
| Firma dañada (`00 50 4E 47` en vez de `89 50 4E 47`) | Restaurar byte y validar CRC | Dos retos se resolvieron así |
| Firma OK pero `file` dice `data` | Verificar últimos bytes y tamaño real | |
| `exiftool`: "Trailer data after IEND/EOI" | Carving inmediato | |
| Chunk `tEXt` con `pista=` o `clave=` | Leerlo: puede ser la contraseña de la capa siguiente | |
| Imagen con patrón repetido (mosaico/sello) | Autocorrelación para el periodo + máscara de diferencias | `scripts/reveal_pattern.py` |
| Sospecha de LSB | Extraer **bit 0** primero, orden píxel-interleaved, desde offset 0 | `scripts/lsb_extract.py` |
| LSB bit 0 sin resultado | Probar bits 1–3 y planar por canal, **registrando** lo probado | |
| QR visible | `zbarimg`; si el contenido son grupos de 8 bits, convertir binario→ASCII | |

## 3. Audio

| Señal | Prueba |
|---|---|
| "Música" o "voz" sin contenido útil | Espectrograma (`sox ... spectrogram`) — el texto suele estar dibujado |
| Tomas cortas y repetidas | FFT por ventana; dos picos = dos nibbles = un byte |
| PCM 16-bit mono | LSB del bit 0 de cada muestra, empaquetado MSB-first |
| Tono constante al final | Descartar FSK/DTMF; probablemente sea relleno |
| Morse aparente | Verificar si es flujo binario (`.=1`) antes de decodificar Morse |

## 4. Logs y red

| Señal | Prueba |
|---|---|
| `.log` con CEF/LEEF | Parsear `cs1=`, `cn1=`; ordenar por índice y decodificar Base64 |
| `.pcap` pequeño | `tshark -r` por stream; seguir TCP y reconstruir credenciales |
| Tráfico FTP | Buscar `USER`/`PASS`, contar fallos, `RETR` de archivos |
| Log de proxy + log de backend | Unir por `rid`, filtrar `OK`, ordenar por `(flow, seq)`, **concatenar** el Base64 antes de decodificar |
| Log de aplicaciones/sensores | Corregir desfase horario declarado antes de cruzar eventos |
| CSV de MFT + USN + `unalloc.raw` | `DataRun × tamaño_clúster` → offset; buscar magic |

## 5. Texto y criptografía

| Señal | Prueba |
|---|---|
| Solo hex | `xxd -r -p`; si el resultado es ASCII imprimible, seguir decodificando |
| Base64 que no decodifica | Puede ser **Base64url** o Base45; validar alfabeto y longitud múltiplo de 3 |
| Capas exóticas | Identificar por alfabeto: Base45 → Base64 → Ook! → Brainfuck |
| Dos mensajes cifrados del mismo largo | XOR entre ellos: si hay ceros en los extremos, mismo keystream |
| Texto plano + cifrado disponible | `keystream = C⊕P`, aplicar al otro cifrado (two-time pad) |
| "Cifrador casero" provisto | Descifrar en orden inverso y validar round-trip |
| Sustitución por símbolos/glifos | Buscar el **catálogo** y una lámina de control |
| Texto legible pero desplazado | César; validar con el prefijo de flag conocido |
| Clave = palabra del enunciado | Vigenère, probar suma y **resta**, y si la clave avanza solo en letras |

## 6. Web

| Señal | Prueba |
|---|---|
| Todo 403 | Cookie de sesión de la plataforma, `User-Agent`, o lanzar la instancia |
| Formulario de búsqueda | SQLi: `ORDER BY n` para columnas, `UNION SELECT` con marcador propio |
| SQLite | `sqlite_master`, `group_concat()`, `char()` (evitar comas en el `UNION`) |
| Cookie/JWT editable | `alg:none`, rol en el payload, firma vacía |
| Cookie de alcance (`access_scope=vendor`) | Probar valores de alcance superiores (`internal`) |
| IDOR en `PUT` | Probar modificar otro `id`; incluir campos sensibles (`password`) |
| API con `version` | Buscar `engine`/`mode` que delaten parser inseguro (`yaml` + `load`) |

## 7. Binarios y servicios

| Señal | Prueba |
|---|---|
| `nc` + banner mínimo | Barrido de longitud: encontrar el umbral de crash |
| Crash con mensaje de bash | `stderr` llega al socket: revela rutas y usuario |
| Sin canary, sin PIE | `ret2win` o ROP directo |
| `%p` / `%s` reflejados | Format string: `%n` posicional para escribir |
| Sin función win ni `system` | SROP (`rt_sigreturn`) o syscalls con gadgets |
| Bug de un byte sobre un puntero | Redirigir el puntero a un NOP-sled / rutina útil |
| Kernel + `patch.diff` | Diff del parche → primitiva → Dirty Pagetable |
| VM de bytecode | Decodificar pares XOR en `.rodata`; oráculo de instrucciones en GDB |

## 8. OSINT

| Señal | Prueba |
|---|---|
| "La cuenta ya no existe" | Metadatos (EXIF `Artist`, `UserComment`) + perfiles archivados |
| Fotos con nombres regenerados | Ordenar por `DateTimeOriginal` y `GPS` |
| Repo de GitHub | Historial de commits (`git log -p`), ramas y tags; la flag vieja suele estar en un commit anterior |
| Charla/stream | Localizar el video, y usar segmentos `/sq/N/` del DVR si el manifiesto es ventana deslizante |
| Texto en video | Canal de color + autocontraste + `tesseract` con whitelist |

## 9. Boot2Root

| Señal | Prueba |
|---|---|
| OVA que no arranca en el hipervisor disponible | `tar -xf` el OVA, convertir disco con `qemu-img`, `.vmx` manual |
| VM sin red | Revisar `netplan`: el nombre de NIC cambia entre hipervisores (`enp0s3` → `ens33`) |
| WSL no alcanza la VM | Relay TCP en espacio de usuario o pivote SOCKS |
| Credenciales filtradas | Buscar backups públicos, scripts con `-p'clave'`, `.git` |
| `sudo -l` con script escribible | Inyectar en el script o en variables que use sin comillas |
