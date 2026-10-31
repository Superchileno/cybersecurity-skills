---
name: ctf-ai-ml
description: 'Retos de IA y machine learning en CTF: ejemplos adversariales (FGSM, PGD,
  C&W), evasión de clasificadores, ataques a LLM (prompt injection, jailbreak y fuga
  de system prompt), extracción e inversión de modelos, análisis de pesos
  (safetensors, LoRA, HuggingFace) y envenenamiento de datos. Usar cuando el reto
  entregue un modelo, un notebook, pesos o un endpoint de LLM.
  Keywords: CTF AI, ML, adversarial examples, FGSM, PGD, model extraction, prompt
  injection, jailbreak, poisoning, safetensors, LoRA.'
area: CTF
tags: [ctf, ai, ml, adversarial, llm, prompt-injection]
source: _src/ljagiello-ctf-skills/ctf-ai-ml
license: MIT
upstream: ljagiello/ctf-skills
---

# SKILL-CTF-AI-ML.md — IA y machine learning

Profundidad en `_src/ljagiello-ctf-skills/ctf-ai-ml/`.

## Cuándo usarla
El reto entrega un modelo entrenado, pesos, un notebook, un clasificador remoto
o un endpoint de LLM con un objetivo que hay que cumplir.

## Procedimiento resumido
1. Identificar el artefacto: `.pt`/`.pth`, `.safetensors`, `.onnx`, `LoRA`,
   `pickle` o API remota.
2. Inspeccionar formato y arquitectura antes de cargarlo; un `pickle` puede
   ejecutar código al deserializar.
3. Definir el objetivo real: ¿cambiar la clase predicha, extraer pesos, leer un
   secreto del prompt o provocar una salida concreta?
4. Elegir familia: evasión (adversarial), extracción (queries), inversión
   (reconstruir entradas) o ataque lingüístico (LLM).
5. Medir con la métrica del reto; ajustar épsilon, pasos y restricciones.
6. Comparar pesos entre modelos cuando se busca un fine-tune malicioso.

## Enrutado al `_src`
| Tema | Archivo |
|---|---|
| Ejemplos adversariales y gradientes | `ctf-ai-ml/adversarial-ml.md` |
| Ataques a LLM y prompt injection | `ctf-ai-ml/llm-attacks.md` |
| Extracción, inversión y pesos | `ctf-ai-ml/model-attacks.md` |

## Herramientas
`torch`, `numpy`, `scikit-learn`, `onnx`, `safetensors`, `transformers`,
`adversarial-robustness-toolbox`, `fickling` para inspeccionar pickles.

## Guardrails
- Cargar modelos ajenos en entorno aislado y sin red.
- No usar `torch.load` sobre archivos no confiables sin `weights_only`.
- Documentar la perturbación mínima que cambia la decisión.
