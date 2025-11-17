from dataclasses import dataclass


@dataclass
class Cat:
    name: str
    energy: float = 100.0
    agility: float = 1.0
    x: float = 0.0
    y: float = 0.0

    def move(self, dx: float, dy: float) -> None:
        self.x += dx
        self.y += dy
        # Más adelante: consumir energía según la pendiente, etc.
