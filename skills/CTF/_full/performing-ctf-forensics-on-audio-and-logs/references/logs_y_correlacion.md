# Logs, pcap y artefactos de sistema de archivos

## 1. Método general

1. **Inventario:** ¿qué fuentes hay y qué representa cada una?
2. **Formato:** identificar el parser real (CEF, JSON lines, CSV, syslog).
3. **Normalización:** hora a UTC, campos comunes (`host`, `src`, `dst`, `user`).
4. **Conteo:** agrupar por entidad antes de leer en detalle.
5. **Correlación:** unir por clave, filtrar por estado, ordenar por secuencia.
6. **Conclusión:** una frase con sujeto, acción y evidencia.

## 2. CEF (Common Event Format)

```
CEF:0|Ubiqui|UniFi|6.0|OUTBOUND.C2.Beacon|C2 Beacon|8|src=... dst=... cs1=<b64> cn1=3
```

- `cs1..cs4`: campos string personalizados.
- `cn1..cn4`: campos numéricos; `cn1` muchas veces es el **índice de orden**.
- `severity` es el último campo antes de las extensiones.

Regla práctica: si varios eventos traen `cs1` en Base64 y `cn1` incremental, ordenar
por `cn1` y concatenar **antes** de decodificar. Cada fragmento puede decodificar a
basura por separado.

## 3. Correlación proxy + backend

Escenario: el proxy registra la petición del cliente y el backend registra el
resultado real; ninguno de los dos tiene la historia completa.

1. Unir por identificador de petición (`rid`).
2. Quedarse con las filas cuyo resultado en el backend sea exitoso (`OK`); descartar
   `REPLAY`/`REJECT` (si se incluyen, el siguiente paso se corrompe).
3. Ordenar por `(flow, seq)` — el flujo identifica la sesión, `seq` el orden interno.
4. Concatenar el campo `p` como **texto** (Base64url) y sólo entonces decodificar.
5. Si el resultado es deflate/zlib, inflar.

Detalle crítico: el Base64 puede venir **partido** en trozos de 5 caracteres. Decodificar
cada trozo por separado falla; hay que concatenar primero.

## 4. Línea de tiempo y desfases

- Un mismo evento puede estar registrado con relojes distintos (cámara, bitácora,
  servidor). El enunciado o una nota del log puede declarar el desfase.
- Corregir a una base común (UTC) **antes** de cruzar fuentes.
- Si dos candidatos caen en la misma hora pero distinto minuto, el desfase decide.

## 5. pcap

```bash
capinfos captura.pcap
tshark -r captura.pcap -q -z io,phs
tshark -r captura.pcap -q -z conv,tcp
tshark -r captura.pcap -Y "ftp || ftp-data" -T fields \
    -e frame.number -e ip.src -e ip.dst -e ftp.request.command -e ftp.request.arg
```

Preguntas que suele hacer el reto:

- IP de origen del atacante.
- Servicio y puerto objetivo.
- Número de intentos fallidos y credencial válida.
- Archivo exfiltrado y su contenido.

Seguir el stream relevante:

```bash
tshark -r captura.pcap -q -z follow,tcp,ascii,14
```

## 6. MFT + USN + espacio no asignado

| Artefacto | Aporta |
|---|---|
| `mft.csv` | nombre, estado de borrado, secuencia, timestamps, `DataRun` |
| `usn.csv` | `FILE_CREATE`, `DATA_OVERWRITE`, `FILE_DELETE` con hora |
| `unalloc.raw` | contenido residual de los clústeres liberados |

Procedimiento:

1. Identificar el archivo de interés por nombre y por cronología coherente
   (create → overwrite → delete).
2. Convertir `DataRun` a offset: `clúster × tamaño_clúster` (4096 típico).
3. Verificar que en ese offset hay una firma válida (`FBLK`, `PK`, etc.).
4. Parsear el artefacto y aplicar la decodificación que él mismo declare.
5. Contrastar con los homónimos: los señuelos tienen el mismo nombre o formato pero
   `DataRun` distinto y contenido trivial (`deadbeef`, `cafebabe`).

Con sleuthkit sobre una imagen completa:

```bash
mmls imagen.dd
fls -r -p imagen.dd
icat imagen.dd <inode> > recuperado.bin
```

## 7. Señales de ruido deliberado

- Alertas de severidad alta en hosts que no participan en la historia.
- Un evento repetido 4 veces (el incidente) frente a uno de cada tipo en otros hosts.
- Archivos con nombres relacionados pero `batch`/`draft`/`tmp` en la cabecera.
- Sesiones que descifran correctamente pero cuyo contenido es un acta administrativa.

La conclusión debe apoyarse en **dos fuentes independientes** cuando el reto las
ofrece (p. ej. cámara + manifiesto, o proxy + backend).
