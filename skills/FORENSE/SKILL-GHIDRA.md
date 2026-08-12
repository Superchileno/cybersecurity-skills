# SKILL-GHIDRA.md — Reversing de malware con Ghidra

Fuente: `_src/mukul-anthropic/reverse-engineering-malware-with-ghidra/`.

## Cuándo usarla
Análisis estático de binarios maliciosos (funciones, strings, C2, técnicas) con Ghidra.

## Procedimiento resumido
1. Importar el binario en Ghidra (Headless o GUI); auto-analyze.
2. Buscar strings relevantes (`Ctrl+Shift+F`), imports suspicious, URLs/IP/dominios.
3. Localizar funciones clave (entry, main, WinMain) y sinks (VirtualAlloc, CreateProcess, WinExec).
4. Deobfuscación básica: renombrar funciones/variables, resolver calls indirectos.
5. Exportar report: TTPs, indicadores, hashes, imports, control flow.
   - Criptografía: identificar algoritmos (constantes, BCrypt).

## Herramientas
Ghidra (headless: `analyzeHeadless`), `strings`, `objdump`/`radare2` como apoyo.

## Guardrails
- Manejar el sample en máquina/entorno aislado; no ejecutarlo. Uso autorizado (laboratorio).