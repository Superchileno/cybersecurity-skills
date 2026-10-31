# Checklist de triaje y cierre — CTF

## Al recibir el reto

- [ ] Carpeta `ctf/NN-nombre/` con `CONTEXTO.md`, `solucion/`, `work/`
- [ ] Enunciado **literal** copiado
- [ ] Formato de flag anotado (`flag{}`, `flag{ejemplo}`, otro)
- [ ] Hash SHA-256 de cada artefacto registrado
- [ ] Alcance anotado: hosts/puertos permitidos

## Primer barrido (siempre, en orden)

- [ ] `file` de todos los artefactos
- [ ] `exiftool` de imágenes/documentos
- [ ] `binwalk -eM` de binarios/imágenes
- [ ] `strings -n 6` filtrando ruido
- [ ] Últimos bytes: ¿datos tras IEND / EOI / EOF?
- [ ] Chunks/comentarios (`tEXt`, `Comment`, `customXml`)

## Clasificación

- [ ] Categoría asignada
- [ ] Skill específica cargada
- [ ] Hipótesis escrita como "creo X porque Y; si Z lo descarto"

## Control de señuelos

- [ ] Cada candidato validado por estructura (prefijo, CRC, hash, round-trip)
- [ ] Descartados registrados en `CONTEXTO.md`
- [ ] Si hay catálogo/planilla: validado contra la lámina de control
- [ ] Si hay varias claves: probada la variante leet y la literal

## Cierre

- [ ] `solucion/` ejecuta end-to-end sin pasos manuales
- [ ] `work/` contiene los artefactos intermedios
- [ ] `flag.txt` escrito
- [ ] `CONTEXTO.md` completo (enunciado, análisis, solución, señuelos, lecciones)
- [ ] Entrada nueva en `CONTEXTO_CTF.md` con fecha y backup del índice
- [ ] Flag validada en la plataforma

## Si se abandona

- [ ] Estado `en curso` en el índice
- [ ] Hipótesis vivas y próximo paso concreto anotados
- [ ] Fecha del último intento
