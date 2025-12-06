from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Tuple
import numpy as np

from ..core.math_tools import numeric_gradient, ScalarField2D
from catcalculus.terrain import functions


@dataclass
class Terrain:
    x: np.ndarray
    y: np.ndarray
    z: np.ndarray
    name: str
    func: Callable[[np.ndarray, np.ndarray], np.ndarray]
    x_range: Tuple[float, float] = (-4.0, 4.0)
    y_range: Tuple[float, float] = (-4.0, 4.0)
    resolution: int = 100

    @classmethod
    def from_function(
            cls,
            func: Callable[[np.ndarray, np.ndarray], np.ndarray],
            x_range: Tuple[float, float] = (-4.0, 4.0),
            y_range: Tuple[float, float] = (-4.0, 4.0),
            resolution: int = 100,
            name: str = "custom",
    ) -> "Terrain":
        """
        Crea un terreno a partir de una función escalar f(x, y).

        Requisitos de `func`:
        - Debe aceptar dos np.ndarray (X, Y) con la misma forma.
        - Debe devolver un np.ndarray Z de la misma forma que X e Y.
        """
        x = np.linspace(*x_range, resolution)
        y = np.linspace(*y_range, resolution)
        X, Y = np.meshgrid(x, y)

        try:
            Z = func(X, Y)
        except Exception as e:
            raise ValueError(f"Error al evaluar la función de terreno: {e}")

        if not isinstance(Z, np.ndarray):
            raise TypeError(
                f"La función debe devolver un np.ndarray, se obtuvo: {type(Z)}"
            )

        if Z.shape != X.shape:
            raise ValueError(
                f"La función debe devolver un array del mismo tamaño que X,Y. "
                f"Obtenido: {Z.shape}, esperado: {X.shape}"
            )

        if not np.all(np.isfinite(Z)):
            raise ValueError("La superficie contiene valores no finitos (NaN o inf).")

        return cls(
            x=X,
            y=Y,
            z=Z,
            name=name,
            func=func,
            x_range=x_range,
            y_range=y_range,
            resolution=resolution,
        )

    @classmethod
    def default(cls) -> "Terrain":
        """
        Terreno por defecto (Prado suave).
        """
        return cls.from_function(functions.meadow, name="Prado suave")

    def get_slice_2d(self, y_val: float) -> Tuple[np.ndarray, np.ndarray]:
        """Obtiene el perfil 2D a lo largo de un valor y_val específico."""
        # Encuentra la fila (índice i) más cercana al valor y_val
        y_vals = self.y[:, 0]
        i_slice = np.argmin(np.abs(y_vals - y_val))

        x_profile = self.x[i_slice, :]
        z_profile = self.z[i_slice, :]

        return x_profile, z_profile

    def f(self, x, y):
        if self.func:
            return self.func(np.array(x), np.array(y)).item()
        return 0.0

    def fx(self, x: float, y: float) -> float:
        """Componente X del gradiente (df/dx) en un punto (x, y)."""
        if not self.func:
            return 0.0

        gx, _ = numeric_gradient(self.func, np.array(x), np.array(y))
        return gx.item()

    def fy(self, x: float, y: float) -> float:
        """Componente Y del gradiente (df/dy) en un punto (x, y)."""
        if not self.func:
            return 0.0

        _, gy = numeric_gradient(self.func, np.array(x), np.array(y))
        return gy.item()