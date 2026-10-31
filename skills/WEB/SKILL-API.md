---
name: web-api
description: 'APIs REST/GraphQL/gRPC, flujos sin auth, misconfigs de endpoints, schema enum. Keywords: api, web.'
area: WEB
tags: [api, web]
license: Apache-2.0
---

# SKILL-API.md — API security hunting

## Cuándo usarla
APIs REST/GraphQL/gRPC, flujos sin auth, misconfigs de endpoints, schema enum.

## Procedimiento resumido
1. Mapear superficie: `recon/api-noauth-hunt`, `redteam/hunt-api-misconfig`.
   Buscar `/swagger`, `/openapi.json`, Postman collections, JS source maps.
2. Auth: probar endpoints sin token, enviar tokens de cuenta propia ajenos,
   `X-Api-Key` trivial, JWT attacks (`recon/jwt-attack`).
3. GraphQL: introspection, queries arbitradas, field-level auth (`hunt-graphql`).
4. gRPC: reflection + probar métodos (`hunt-grpc`).
5. Bcance/parámetros: métodos alternativos (GET→POST), query vs body, fuzzy ids,
   mass assignment, response splitting (el `hunt-*` correspondiente).

## Clasificación
- Procedimiento: mismo esquema L1→L4. Fuga de datos via API → L4.

## Herramientas
`curl`, `jq`, `ffuf` (fuzz endpoints), Burp, `nuclei` (templates HTTP).

## Guardrails
- No abusar de endpoints de datos masivos; respetar rate limit.
- Evidencia con request/response y reproducer `curl`.