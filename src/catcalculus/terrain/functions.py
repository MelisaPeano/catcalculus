import numpy as np
from typing import Callable

TerrainFunction = Callable[[np.ndarray, np.ndarray], np.ndarray]


def meadow(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Prado suave: f(x, y) = 0.2 (x^2 + y^2)
    """
    return 0.2 * (x**2 + y**2)


def wavy_mountain(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Montaña ondulada: f(x, y) = sin(x) * cos(y)
    """
    return np.sin(x) * np.cos(y)


def meow_volcano(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Volcán del miau: f(x,y) = e^{-(x^2+y^2)} - 0.5 (x^2 + y^2)
    """
    r2 = x**2 + y**2
    return np.exp(-r2) - 0.5 * r2


def infinite_peak(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Pico infinito: f(x, y) = ln(x^2 + y^2 + 1)
    """
    r2 = x**2 + y**2
    return np.log(r2 + 1.0)
