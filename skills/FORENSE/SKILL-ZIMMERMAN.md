# SKILL-ZIMMERMAN.md — Análisis de artefactos Windows (Eric Zimmerman Tools)

Fuente: `_src/mukul-anthropic/performing-windows-artifact-analysis-with-eric-zimmerman-tools/`.

## Cuándo usarla
Análisis forense rápido y estandarizado de artefactos Windows (soluciones de Zimmerman, gratuitas).

## Procedimiento resumido
1. Desplegar las herramientas (se distinguen por `.exe`).
2. Artefactos y tool:
   - **JumpLists** → `JLECmd`: `JLECmd.exe -d <AppData>\Microsoft\Windows\Recent\AutomaticDestinations -r`.
   - **Prefetch** → `PECmd`: `PECmd.exe -d C:\Windows\Prefetch -o per-host.csv`.
   - **ShellBags** → `SBECmd: <usuario>\AppData\Local\...\BagMRU`.
   - **AmCache** → `AmcacheParser -f C:\Windows\AppCompat\Programs\Amcache.hve -o out`.
   - **Browser hist** → `BECmd` (Chrome/Firefox/Edge).
   - **Key (registry)** → `RECmd`/`Registry Explorer`.
   - **MFT** → `MFTECmd`.
3. Combinar outputs en timeline master (`JCmd` o pandas) para correlación tiempo-usuario.
4. Exportar CSV para análisis central.

## Herramientas
Suite EZTools (descargar desde GitHub ericzimmerman).

## Guardrails
- Ejecutar sobre copias de artefactos (no el original); autorización de la imagen.