from .shapes import CatShape
from dataclasses import dataclass, field
from typing import Tuple, Optional


@dataclass
class Cat:
    name: str
    x: float
    y: float

    initial_x: float = field(init=False)
    initial_y: float = field(init=False)

    energy: float = 100.0
    agility: float = 1.0

    is_at_minimum: bool = False
    shape: Optional[CatShape] = None

    trail: list[tuple[float, float]] = field(default_factory=list)

    def __post_init__(self):
        self.initial_x = self.x
        self.initial_y = self.y
        self.trail.append((self.x, self.y))

    # -------------------------
    # Movimiento
    # -------------------------
    def move(self, dx: float, dy: float):
        if self.is_at_minimum:
            return

        self.x += dx
        self.y += dy
        self.update_trail()

    def update_trail(self):
        self.trail.append((self.x, self.y))
        if len(self.trail) > 250:
            self.trail.pop(0)

    # -------------------------
    # Posiciones / Reseteo
    # -------------------------
    def reset_position(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.energy = 100.0
        self.is_at_minimum = False
        self.trail = [(self.x, self.y)]

    def grid_indices(self, coord_sys) -> Tuple[int, int]:
        return coord_sys.world_to_grid(self.x, self.y)

    def get_covered_area(self, coord_sys):
        if not self.shape:
            return [self.grid_indices(coord_sys)]

        dx = self.shape.width / coord_sys.world_bounds.width() * (coord_sys.cols - 1)
        dy = self.shape.height / coord_sys.world_bounds.height() * (coord_sys.rows - 1)
        ci, cj = self.grid_indices(coord_sys)

        i_min = max(0, int(ci - dy // 2))
        i_max = min(coord_sys.rows - 1, int(ci + dy // 2))
        j_min = max(0, int(cj - dx // 2))
        j_max = min(coord_sys.cols - 1, int(cj + dx // 2))

        return [(i, j) for i in range(i_min, i_max + 1)
                for j in range(j_min, j_max + 1)]
