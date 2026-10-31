#!/usr/bin/env python3
"""Revela texto oculto en imágenes con patrón periódico (mosaico/sello).

Uso:
    python reveal_pattern.py placa.png --out work/
    python reveal_pattern.py placa.png --period 164 --out work/
    python reveal_pattern.py placa.png --axis both --threshold 24

Método:
  1. Estima el periodo P por autocorrelación (si no se indica).
  2. Calcula la diferencia contra la imagen desplazada P píxeles.
  3. Umbraliza y guarda la máscara; recorta bandas de filas con contenido.
Requiere Pillow y numpy.
"""
from __future__ import annotations

import argparse
import os
import sys

try:
    import numpy as np
    from PIL import Image
except ImportError:
    sys.exit("faltan dependencias: pip install pillow numpy")


def gris(img: Image.Image) -> np.ndarray:
    return np.asarray(img.convert("L"), dtype=np.float32)


def estimar_periodo(arr: np.ndarray, eje: int) -> int:
    """Autocorrelación 1-D sobre el promedio del eje."""
    serie = arr.mean(axis=1 if eje == 0 else 0)
    serie = serie - serie.mean()
    if serie.size < 16 or not np.any(serie):
        return 0
    corr = np.correlate(serie, serie, mode="full")[serie.size - 1:]
    corr /= corr[0] if corr[0] else 1
    # Buscar el primer máximo local significativo después de 8 px
    for i in range(8, min(len(corr) - 1, 4096)):
        if corr[i] > 0.5 and corr[i] >= corr[i - 1] and corr[i] >= corr[i + 1]:
            return i
    return 0


def mascara(arr: np.ndarray, periodo: int, eje: int, umbral: float) -> np.ndarray:
    if periodo <= 0:
        return np.zeros_like(arr, dtype=np.uint8)
    if eje == 0:
        diff = np.abs(arr[:, periodo:] - arr[:, :-periodo])
        m = np.zeros_like(arr, dtype=np.uint8)
        m[:, periodo:] = (diff > umbral).astype(np.uint8) * 255
    else:
        diff = np.abs(arr[periodo:, :] - arr[:-periodo, :])
        m = np.zeros_like(arr, dtype=np.uint8)
        m[periodo:, :] = (diff > umbral).astype(np.uint8) * 255
    return m


def bandas(m: np.ndarray, minimo: int = 4) -> list[tuple[int, int]]:
    filas = (m > 0).sum(axis=1)
    activas = filas > (m.shape[1] * 0.002)
    salida, inicio = [], None
    for i, activa in enumerate(activas):
        if activa and inicio is None:
            inicio = i
        elif not activa and inicio is not None:
            if i - inicio >= minimo:
                salida.append((inicio, i))
            inicio = None
    if inicio is not None and len(activas) - inicio >= minimo:
        salida.append((inicio, len(activas)))
    return salida


def main() -> int:
    ap = argparse.ArgumentParser(description="Revela mosaicos periódicos")
    ap.add_argument("imagen")
    ap.add_argument("--out", default="work")
    ap.add_argument("--period", type=int, default=0)
    ap.add_argument("--axis", default="x", choices=["x", "y", "both"])
    ap.add_argument("--threshold", type=float, default=18.0)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    img = Image.open(args.imagen)
    arr = gris(img)
    print(f"imagen: {args.imagen} {img.size[0]}x{img.size[1]}")

    ejes = [0, 1] if args.axis == "both" else ([0] if args.axis == "x" else [1])
    for eje in ejes:
        etiqueta = "horizontal" if eje == 0 else "vertical"
        p = args.period or estimar_periodo(arr, eje)
        print(f"\n[{etiqueta}] periodo estimado: {p} px")
        if p <= 0:
            print("  [!] sin periodo claro; probar --period manualmente")
            continue
        m = mascara(arr, p, eje, args.threshold)
        ruta = os.path.join(args.out, f"mascara_{etiqueta}.png")
        Image.fromarray(m).save(ruta)
        print(f"  máscara: {ruta} ({int((m > 0).sum())} px fuera de patrón)")

        for i, (a, b) in enumerate(bandas(m)):
            recorte = Image.fromarray(m[a:b, :])
            escala = max(1, int(1200 / max(1, recorte.size[0])))
            recorte = recorte.resize(
                (recorte.size[0] * escala, max(12, recorte.size[1] * escala)),
                Image.NEAREST,
            )
            ruta_b = os.path.join(args.out, f"linea_{etiqueta}_{i+1}.png")
            recorte.save(ruta_b)
            print(f"  banda {i+1}: filas {a}-{b} → {ruta_b}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
