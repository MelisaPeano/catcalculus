
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from catcalculus.terrain import functions


@dataclass
class Terrain:
    x: np.ndarray
    y: np.ndarray
    z: np.ndarray
    name: str

    @classmethod
    def from_function(
        cls,
        func,
        x_range=(-3.0, 3.0),
        y_range=(-3.0, 3.0),
        resolution: int = 100,
        name: str = "custom",
    ) -> "Terrain":
        x = np.linspace(*x_range, resolution)
        y = np.linspace(*y_range, resolution)
        X, Y = np.meshgrid(x, y)
        Z = func(X, Y)
        return cls(x=X, y=Y, z=Z, name=name)

    @classmethod
    def default(cls) -> "Terrain":
        return cls.from_function(functions.meadow, name="Prado suave")
