# Skill Quality Baseline (STYLE.md)

Minimum quality bar for every SKILL.md in this repository. Reviewers: reject PRs that fail any of these.

---

## Required Sections

Every SKILL.md must have:

1. **`## When to Use`** — trigger conditions, bullet list.
2. **`## Prerequisites`** — what the agent needs before running.
3. **`## How to Run`** — quick copy-paste command(s).
4. **`## Procedure`** — step-by-step with full bash commands.
5. **`## Pitfalls`** — false positives, edge cases, rate limits, misleading results.
6. **`## Verification`** — how to confirm success. Every finding type must have a verification step.

---

## Command Quality Rules

### Keep execution portable

- Do not assume an agent framework, container name, private host, or control API.
- List required tools and privileges in `Prerequisites`.
- Write generated artifacts beneath `${OUTPUT_DIR:-./output}`.
- When root or raw sockets are optional, include an unprivileged fallback.
- Keep target-specific evidence and credentials outside this repository.

### Use `--max-time` on every curl
```bash
# BAD
curl -sk "https://$target/path"

# GOOD
curl -sk --max-time 10 "https://$target/path"
```

### Rate-limit shell loops
```bash
# BAD
for t in $(cat targets.txt); do
  curl -sk "https://$t/path"
done

# GOOD
for t in $(cat targets.txt); do
  curl -sk --max-time 10 "https://$t/path"
  sleep 2
done
```

### Suppress stderr where appropriate
```bash
# GOOD
curl -sk --max-time 10 "https://$target/..." 2>/dev/null
```

### Prefer batch tools over loops for DNS resolution
```bash
# BAD — dig in a while-read loop (slow, sequential)
while read -r sub; do dig +short "$sub" A; done < subs.txt

# GOOD — dnsx batch resolution
dnsx -silent -a -resp-only -l subs.txt
```

---

## Content Rules

### No placeholder content
- If `output/` is empty, do not claim `report_count: N` in frontmatter.
- If a finding has never been confirmed on a real target, say so. Do not fabricate.

### Cross-references must be intentional
- Use `related_skills` for a concrete next step, prerequisite, or companion
  technique.
- References may be directional. Do not add a reverse reference unless it also
  helps an operator navigate from the other skill.

### No broken references
- Any script path referenced in a skill must exist in the repo.
- Run `ls scripts/` before referencing a script.

### Verification before claiming a finding
- **CORS**: Must have BOTH `ACAO: <reflected origin>` AND `ACAC: true`. `ACAO: *` alone is not a finding.
- **Debug log**: Must contain actual PII patterns (emails, phones, SQL queries). Empty 200 is not a finding.
- **XMLRPC**: Must return `methodResponse` in body. HTTP 200 alone is not confirmation.
- **Directory listing**: Must show `Index of` in body. 200 alone is not confirmation.
- **Source leak**: Must contain sensitive content (`DB_`, `APP_`, `_KEY`, `_SECRET` patterns). Empty accessible path is not a finding.
- **Parked domains**: Check `/robots.txt` and `/.env` — if both return 200 with identical body, domain is parked.

---

## Frontmatter Rules

```yaml
---
name: skill-name
description: One sentence, <=60 chars, ends with period. No marketing words.
version: 1.0.0
author: uphiago
license: MIT
platforms: [linux]
compatibility: Requires <tools>
metadata:
  tags: [tag1, tag2]
  category: <recon|redteam|meta|chains|auth|infra>
  related_skills:
    - other-skill-name
---
```

---

## No Template Duplication

If two skills differ only by a sector name, platform name, or target filename, collapse them into one parameterized skill. See `recon-sector` for an example of 25 skills collapsed into 1 parameterized skill with a `sectors.yaml` database.

## State-Changing Tests

Default to passive or read-only validation. Any example that creates, modifies,
deletes, sends, publishes, purchases, uploads, or changes authentication state
must clearly require explicit authorization immediately before the command.

---

## Authorization Disclaimer

Every root-level doc (README.md, SOUL.md) must include:
> These skills are for authorized security testing only. Only test targets you own or have explicit written permission to test.
