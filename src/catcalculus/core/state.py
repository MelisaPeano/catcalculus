from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from catcalculus.core.coordinates import CoordinateSystem, WorldBounds
from catcalculus.cats.models import Cat
from catcalculus.cats.shapes import CatShape
import random


@dataclass
class GameState:
    """
    Representa el estado completo del juego en un instante de tiempo.
    """
    terrain: 'Terrain'
    coordinate_system: CoordinateSystem
    cats: List[Cat] = field(default_factory=list)
    mode: str = "engineer"
    time: float = 0.0

    @classmethod
    def initial_state(
            cls,
            terrain: Optional['Terrain'] = None,
            cats: Optional[List[Cat]] = None,
            reset_cats: bool = False, # Nuevo parámetro para forzar el reinicio de posición
    ) -> "GameState":
        """
        Crea un estado inicial razonable: terreno y dos gatitos.
        """
        from catcalculus.terrain.generator import Terrain

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
            # Gatitos iniciales por defecto
            cats = [
                Cat(
                    name="Euler",
                    x=0.0,
                    y=0.0,
                    shape=CatShape(width=0.5, height=0.5)
                ),
                Cat(
                    name="Gauss",
                    x=1.0,
                    y=1.0,
                    shape=CatShape(width=0.5, height=0.5)
                ),
            ]

        if reset_cats:
            for cat in cats:
                cat.reset_position()

        return cls(
            terrain=terrain,
            coordinate_system=coord_sys,
            cats=cats,
            mode="engineer",
            time=0.0,
        )

    def add_random_cat(self) -> Cat:
        """
        Agrega un nuevo gato en una posición aleatoria dentro de los límites del mundo.
        """
        x_range = self.coordinate_system.world_bounds

        # Generar coordenadas aleatorias que no estén en los bordes exactos
        x = random.uniform(x_range.x_min + 0.5, x_range.x_max - 0.5)
        y = random.uniform(x_range.y_min + 0.5, x_range.y_max - 0.5)

        new_cat_name = f"Cat-{len(self.cats) + 1}"

        new_cat = Cat(
            name=new_cat_name,
            x=x,
            y=y,
            shape=CatShape(width=0.5, height=0.5)
        )
        self.cats.append(new_cat)
        return new_cat