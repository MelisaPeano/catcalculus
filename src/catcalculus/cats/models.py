from .shapes import CatShape
from dataclasses import dataclass
from typing import Tuple

@dataclass
class Cat:
    name: str
    x: float
    y: float
    energy: float = 100.0
    agility: float = 1.0
    shape: CatShape | None = None

    def move(self, dx: float, dy: float) -> None:
        self.x += dx
        self.y += dy

    def grid_indices(self, coord_sys) -> Tuple[int, int]:
        return coord_sys.world_to_grid(self.x, self.y)

    def get_covered_area(self, coord_sys):
        if not self.shape:
            return [self.grid_indices(coord_sys)]

        dx = self.shape.width / coord_sys.world_bounds.width() * (coord_sys.cols - 1)
        dy = self.shape.height / coord_sys.world_bounds.height() * (coord_sys.rows - 1)
        ci, cj = self.grid_indices(coord_sys)

        i_min = max(0, int(round(ci - dy // 2)))
        i_max = min(coord_sys.rows - 1, int(round(ci + dy // 2)))
        j_min = max(0, int(round(cj - dx // 2)))
        j_max = min(coord_sys.cols - 1, int(round(cj + dx // 2)))

        return [(i, j) for i in range(i_min, i_max + 1) for j in range(j_min, j_max + 1)]
