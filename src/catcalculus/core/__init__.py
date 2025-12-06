# catcalculus/core/__init__.py
from .engine import GameEngine, EngineStatus, EngineConfig
from .state import GameState
from .coordinates import CoordinateSystem, WorldBounds
from .math_tools import numeric_gradient, gradient_magnitude, directional_derivative # <-- Asegúrate que math_tools esté expuesto si es usado por otros módulos

__all__ = [
    "GameEngine",
    "EngineStatus",
    "EngineConfig",
    "GameState",
    "CoordinateSystem",
    "WorldBounds",
    "numeric_gradient", # Añadir según necesidad
    "gradient_magnitude",
    "directional_derivative",
]