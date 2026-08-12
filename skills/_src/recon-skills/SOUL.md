# Operating Principles

This library turns offensive-security knowledge into portable, reviewable, and
repeatable procedures.

> These skills are for authorized security testing only. Only test targets you
> own or have explicit written permission to test.

## Scope Before Technique

Authorization, target boundaries, permitted test classes, rate limits, and stop
conditions are prerequisites. A technically valid probe outside scope is still
an invalid test.

## Reconnaissance Is a Pipeline

Discovery creates hypotheses. Enumeration adds context. Validation tests one
hypothesis at a time. Attack-path analysis combines only verified facts.
Reporting preserves the evidence and the limits of what was demonstrated.

Each stage should reduce uncertainty and determine the next stage. A checklist
that generates requests without changing a decision is noise.

## Evidence Before Severity

Do not infer impact from a product name, version string, status code, open port,
or permissive-looking header. Confirm the behavior required by the finding and
record the negative controls that distinguish it from a false positive.

State observations separately from inference:

```text
Observed: exact request, response, and environment
Inferred: likely cause or reachable attack path
Confirmed: reproduced security impact
Not tested: action excluded by scope or safety
```

## Minimal Side Effects

Prefer passive and read-only checks. Before any request that creates, changes,
deletes, sends, purchases, publishes, authenticates as another user, or affects
availability, stop and obtain explicit authorization for that action.

Proof should use the least data and the smallest state change necessary.

## Portable Skills

A skill is durable knowledge, not an environment snapshot. It must declare its
tools and privileges, accept portable inputs, write beneath
`${OUTPUT_DIR:-./output}`, and remain useful whether executed by a person, an
agent, CI, a container, or a dedicated testing host.

The runtime owns orchestration, scheduling, isolation, credentials, networking,
and resource limits. This repository owns methodology.

## Focused Loading

Load the smallest set of skills that explains the observed surface. Large
context dumps reduce precision and make stale instructions harder to detect.
Cross-reference shared procedures instead of copying them.

## Concurrency Is a Risk Control

Concurrency is not a performance default. Derive it from scope, target
stability, rate limits, and the cost of a false positive. Start low, measure,
and increase only when evidence supports it.

## Reproducible Output

Every material finding should include:

- target and scope context;
- UTC timestamp;
- sanitized request and response evidence;
- tool and relevant version;
- expected and observed behavior;
- reproduction steps;
- impact demonstrated;
- limitations and untested assumptions.

Store private evidence outside the public skill library. Promote only reusable,
redacted methodology back into a skill.

## Technical Writing

Use direct language. Remove marketing claims, unsupported absolutes, personal
narration, and environment folklore. Commands should be bounded and copyable.
Verification should explain what proves the claim and what does not.

The library improves when procedures become safer, narrower, more portable, and
easier to falsify.
