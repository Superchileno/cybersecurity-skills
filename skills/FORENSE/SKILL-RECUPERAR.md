---
name: forense-recuperar
description: 'Force-push borró un commit, PR/issue fue eliminado, o necesitas reconstruir el historial (dentro de una investigación forense autorizada). Keywords: forense, recuperar.'
area: FORENSE
tags: [forense, recuperar]
license: Apache-2.0
---

# SKILL-RECUPERAR.md — Recuperación de commits/PR/issues borrados

## Cuándo usarla
Force-push borró un commit, PR/issue fue eliminado, o necesitas reconstruir el
historial (dentro de una investigación forense autorizada).

## Procedimiento
1. **Local git** (si tienes el repo): 
   - `git fsck --lost-found --unreachable | grep commit` → SHAs huérfanos.
   - `git reflog --all` → historial reescrito.
   - `git branch -a -v` y `git log --show-signature`.
2. **GitHub API**: un commit force-pushed a veces 404 en `/commits/SHA` pero
   responde en `/git/commits/SHA`; probar también `/commits/SHA.patch`.
3. **Wayback CDX**: `curl -s "https://web.archive.org/cdx/search/cdx?url=github.com/OWNER/REPO/..."` 
   para snapshots de issues/PR/releases eliminados.
4. **GH Archive / BigQuery**: eventos PushEvent/DeleteEvent con ventanas de tiempo
   → reconstruir la secuencia (force-push = `distinct_size=0` con `size>0`).
5. Reordenar y, si es pertinente, reconstruir el diff (git checkout de un SHA).

## Referencias _src
- `oss-forensics` → `references/recovery-techniques.md`, `github-archive-guide.md`.

## Guardrails
- Solo en investigación de repos autorizados. Doble fuente para cada SHA/URL
  antes de marcarlo `[VERIFIED]`.