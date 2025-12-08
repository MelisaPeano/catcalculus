from __future__ import annotations

from typing import Callable, Tuple
import numpy as np

# Campo escalar 2D: f(x, y) -> z
ScalarField2D = Callable[[np.ndarray, np.ndarray], np.ndarray]


def numeric_gradient(
        func: ScalarField2D,
        x: np.ndarray,
        y: np.ndarray,
        h: float = 1e-3,
) -> Tuple[np.ndarray, np.ndarray]:

    # Aseguramos arrays
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    # Variaciones en x
    fx_plus = func(x + h, y)
    fx_minus = func(x - h, y)
    gx = (fx_plus - fx_minus) / (2.0 * h)

    # Variaciones en y
    fy_plus = func(x, y + h)
    fy_minus = func(x, y - h)
    gy = (fy_plus - fy_minus) / (2.0 * h)

    return gx, gy


def gradient_magnitude(
        func: ScalarField2D,
        x: np.ndarray,
        y: np.ndarray,
        h: float = 1e-3,
) -> np.ndarray:
    gx, gy = numeric_gradient(func, x, y, h=h)
    return np.sqrt(gx**2 + gy**2)


def directional_derivative(
        func: ScalarField2D,
        x: np.ndarray,
        y: np.ndarray,
        direction: Tuple[float, float],
        h: float = 1e-3,
) -> np.ndarray:
    ux, uy = direction
    norm = np.sqrt(ux**2 + uy**2)
    if norm == 0:
        raise ValueError("La dirección no puede ser el vector cero.")

    ux /= norm
    uy /= norm

    gx, gy = numeric_gradient(func, x, y, h=h)
    return gx * ux + gy * uy
