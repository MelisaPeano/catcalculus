from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Optional

from .state import GameState
from .movement import move_cat_by_gradient
from catcalculus.cats.models import Cat


class EngineStatus(Enum):
    STOPPED = auto()
    RUNNING = auto()
    PAUSED = auto()


@dataclass
class EngineConfig:
    tick_rate: float = 1 / 5
    max_time_step: float = 0.1
    stop_threshold: float = 1e-2


class GameEngine:

    def __init__(self,
                 initial_state: Optional[GameState] = None,
                 config: Optional[EngineConfig] = None):

        self.state = initial_state or GameState.initial_state()
        self.config = config or EngineConfig()
        self.status = EngineStatus.STOPPED

        self.on_state_updated: Optional[Callable[[GameEngine], None]] = None

    # -----------------------------
    # Control
    # -----------------------------
    def start(self, reset=True):
        if reset:
            self.state = GameState.initial_state(
                terrain=self.state.terrain,
                cats=self.state.cats,
                reset_cats=True
            )
        self.status = EngineStatus.RUNNING

    def pause(self):
        if self.status == EngineStatus.RUNNING:
            self.status = EngineStatus.PAUSED

    def resume(self):
        if self.status == EngineStatus.PAUSED:
            self.status = EngineStatus.RUNNING

    def stop(self):
        self.status = EngineStatus.STOPPED

    # -----------------------------
    # Main loop
    # -----------------------------
    def step(self, dt=None):
        manual = dt is None
        if manual:
            dt = 0.1

        if self.status != EngineStatus.RUNNING and not manual:
            return

        dt = min(dt, self.config.max_time_step)
        self.state.time += dt

        self._update_logic(dt)

        if self.on_state_updated:
            self.on_state_updated(self)

    # -----------------------------
    # Logic
    # -----------------------------
    def _update_logic(self, dt):
        terrain = self.state.terrain
        if not terrain or not self.state.cats:
            return

        for cat in self.state.cats:
            self._move_cat(cat, dt)

    def _move_cat(self, cat: Cat, dt):
        if cat.is_at_minimum:
            return

        mag = move_cat_by_gradient(
            cat,
            self.state.terrain,
            self.state.coordinate_system,
            step_factor=1.0,
            uphill=False
        )

        if mag is not None and mag < self.config.stop_threshold:
            cat.is_at_minimum = True
        else:
            cat.is_at_minimum = False

    def gradient_at(self, x, y):
        terrain = self.state.terrain

        if not terrain:
            return (0, 0)

        return terrain.fx(x, y), terrain.fy(x, y)