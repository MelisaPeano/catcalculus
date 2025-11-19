from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Tuple
import numpy as np
from catcalculus.terrain import functions


@dataclass
class Terrain:
    x: np.ndarray
    y: np.ndarray
    z: np.ndarray
    name: str
    x_range: Tuple[float, float] = (-3.0, 3.0)
    y_range: Tuple[float, float] = (-3.0, 3.0)
    resolution: int = 100

    @classmethod
    def from_function(
            cls,
            func: Callable[[np.ndarray, np.ndarray], np.ndarray],
            x_range: Tuple[float, float] = (-3.0, 3.0),
            y_range: Tuple[float, float] = (-3.0, 3.0),
            resolution: int = 100,
            name: str = "custom",
    ) -> "Terrain":
        """
        Crea un terreno a partir de una función f(x, y).
        """
        x = np.linspace(*x_range, resolution)
        y = np.linspace(*y_range, resolution)
        X, Y = np.meshgrid(x, y)

        try:
            Z = func(X, Y)
            if Z.shape != X.shape:
                raise ValueError(f"La función debe devolver un array del mismo tamaño que X,Y. Obtenido: {Z.shape}, esperado: {X.shape}")
        except Exception as e:
            raise ValueError(f"Error al evaluar la función: {e}")

        return cls(
            x=X,
            y=Y,
            z=Z,
            name=name,
            x_range=x_range,
            y_range=y_range,
            resolution=resolution
        )

    @classmethod
    def default(cls) -> "Terrain":
        """
        Terreno por defecto (Prado suave).
        """
        return cls.from_function(functions.meadow, name="Prado suave")
