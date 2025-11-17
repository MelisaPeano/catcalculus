from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from catcalculus.core.coordinates import CoordinateSystem, WorldBounds
from catcalculus.terrain.generator import Terrain
from catcalculus.cats.models import Cat


@dataclass
class GameState:
    """
    Representa el estado completo del juego en un instante de tiempo.
    """
    terrain: Terrain
    coordinate_system: CoordinateSystem
    cats: List[Cat] = field(default_factory=list)
    mode: str = "engineer"  # más adelante: Enum o Literal["engineer", "challenge"]
    time: float = 0.0       # tiempo lógico del juego, en segundos

    @classmethod
    def initial_state(
        cls,
        terrain: Optional[Terrain] = None,
        cats: Optional[List[Cat]] = None,
    ) -> "GameState":
        """
        Crea un estado inicial razonable: terreno y dos gatitos.
        """
        if terrain is None:
            terrain = Terrain.default()

        bounds = WorldBounds(
            x_min=float(terrain.x.min()),
            x_max=float(terrain.x.max()),
            y_min=float(terrain.y.min()),
            y_max=float(terrain.y.max()),
        )
        coord_sys = CoordinateSystem(
            world_bounds=bounds,
            grid_shape=terrain.z.shape,  # (rows, cols)
        )

        if cats is None:
            cats = [
                Cat(name="Euler"),
                Cat(name="Gauss"),
            ]

        return cls(
            terrain=terrain,
            coordinate_system=coord_sys,
            cats=cats,
            mode="engineer",
            time=0.0,
        )
