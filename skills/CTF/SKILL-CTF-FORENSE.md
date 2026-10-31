---
name: ctf-forense
description: 'Forense de CTF sobre audio, logs, capturas de red y artefactos de sistema
  de archivos: espectrogramas, tonos duales por FFT, LSB en muestras PCM, eventos CEF,
  sesiones FTP en pcap, correlación proxy+backend por rid/flow/seq con inflado y
  recuperación de archivos borrados con MFT+USN. Usar con WAV/MP3, .log, .pcap, CSV
  de MFT o volcados de disco parciales.
  Keywords: CTF forensics, spectrogram, FFT, pcap, CEF, MFT, USN, timeline.'
area: CTF
tags: [ctf, forense, audio, pcap, logs, mft]
source: _full/performing-ctf-forensics-on-audio-and-logs
license: Apache-2.0
---

# SKILL-CTF-FORENSE.md — Forense de audio, logs y red

Fuente: `_full/performing-ctf-forensics-on-audio-and-logs/`.

## Cuándo usarla
El reto entrega audio, logs de seguridad, un pcap pequeño o artefactos de disco, y
pide reconstruir qué ocurrió.

## Procedimiento resumido
1. Audio: `ctf-arsenal spectrogram audio.wav` antes de cualquier otra prueba.
2. Tonos: `ctf-arsenal tones audio.wav --low 520 --high 1400 --step 40`.
3. Muestras: `ctf-arsenal pcm-lsb audio.wav --bit 0`.
4. Logs: `ctf-arsenal logs cef eventos.log` y contar por entidad antes de leer.
5. Proxy+backend: unir por `rid`, filtrar `OK`, ordenar por `(flow, seq)`,
   concatenar el Base64 y luego inflar.
6. pcap: `tshark -r captura.pcap -q -z follow,tcp,ascii,<stream>`.
7. Disco: `ctf-arsenal mft --mft mft.csv --raw unalloc.raw --magic FBLK`.
8. Corregir desfases horarios antes de cruzar fuentes.

## Clasificación de hallazgo
- Sujeto/actor identificado con dos fuentes independientes → confirmado.
- Un solo indicador sin corroboración → parcial.

## Herramientas
`ctf-arsenal`, `sox`, `ffmpeg`, `tesseract`, `tshark`, `zeek`, `sleuthkit`.

## Guardrails
- No ejecutar muestras de audio/video con reproductores vulnerables.
- Redactar PII y credenciales en el writeup.
