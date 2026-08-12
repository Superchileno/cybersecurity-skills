# SKILL-YARA.md — Desarrollo de reglas YARA para detección

Fuente: `_src/mukul-anthropic/performing-yara-rule-development-for-detection/`.

## Cuándo usarla
Crear reglas YARA para detectar/identificar malware por metadatos (strings, bytes, imports, comportamientos).

## Procedimiento resimido
1. Definir objetivo: muestra específica, familia, indicador genérico.
2. Extraer características sólidas (strings únicas, byte patterns en `.text`, imports, tamaño).
3. Escribir la regla:
   ```
   rule Familia_Alert {
     meta: description/author/tlp/attck
     strings:
       $s1 = "payload" ascii wide nocase
       $b1 = { 4D 5A ... }
     condition:
       uint16(0)==0x5A4D and 2 of them and filesize < 300KB
   }
   ```
4. Validar: `yara rule.yar <samples>` (TP), contra corpus benigno (FN/FP).
5. Usar `yarGen`/`yara-analyzer` para run inicial.
6. Integrar en pipelines (strings en intel, detección endpoint).

## Herramientas
`yara` (yara-python), `yarGen`, `strings`. En Kali: `apt install yara`.

## Guardrails
- Reglas testeadas contra corpus benigno antes de desplegar (evitar FP masivos).