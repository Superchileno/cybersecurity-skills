# SKILL-KAPE.md — Triage forense con KAPE

Fuente: `_src/mukul-anthropic/triaging-windows-with-kape/`.

## Cuándo usarla
Adquisición/triage forense rápido de endpoints Windows (recopilar artefactos clave sin cambiar el equipo).

## Procedimiento resumido
1. KAPE; definir source (directorio/evidencia) y destino.
2. Fases:
   - **Targets** (adquisición): `kape.exe --tsource <host> --tdest <out>` — recoge evtx, prefetch, registry, ShimCache, AmCache, LNK, SRUM, etc.
   - **Modules** (procesado posterior): `--msource` → parse de artefactos (KAPE-Systematic/def).
3. Indicar fuentes por destino (`-t` vs `-m`).
4. Verificar integridad: hashes (`--hash`), report `KAPE.log`.
5. Enviar triage a análisis (Autopsy, Hayabusa, Zimmerman).

## Herramientas
KAPE (Windows; en Kali usar desde máquina Windows o vía wine — recomendable en un Windows forense).

## Guardrails
- Triage sin alterar evidencia (solo lectura si es live); hash a cada artefacto. Autorización del host.