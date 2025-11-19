# src/catcalculus/core/engine.py

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Optional

from catcalculus.core.state import GameState
from catcalculus.core.movement import move_cat_by_gradient



class EngineStatus(Enum):
    STOPPED = auto()
    RUNNING = auto()
    PAUSED = auto()


@dataclass
class EngineConfig:
    tick_rate: float = 1.0 / 30.0
    max_time_step: float = 0.1  # evita saltos de simulación


class GameEngine:
    """
    Motor lógico del juego.
    Se encarga del tiempo, estados y ciclo de simulación.
    """

    def __init__(
            self,
            initial_state: Optional[GameState] = None,
            config: Optional[EngineConfig] = None,
    ) -> None:
        self.config = config or EngineConfig()
        self.state: GameState = initial_state or GameState.initial_state()
        self.status: EngineStatus = EngineStatus.STOPPED

        # callback: on_state_updated(engine)
        self.on_state_updated: Optional[Callable[[GameEngine], None]] = None

    # ---------------------------
    # Ciclo de vida
    # ---------------------------

    def start(self, reset: bool = True) -> None:
        if reset:
            self.state = GameState.initial_state(
                terrain=self.state.terrain,
                cats=self.state.cats,
            )
        self.status = EngineStatus.RUNNING

    def pause(self) -> None:
        if self.status == EngineStatus.RUNNING:
            self.status = EngineStatus.PAUSED

    def resume(self) -> None:
        if self.status == EngineStatus.PAUSED:
            self.status = EngineStatus.RUNNING

    def stop(self) -> None:
        self.status = EngineStatus.STOPPED

    def toggle_pause(self) -> None:
        if self.status == EngineStatus.RUNNING:
            self.pause()
        elif self.status == EngineStatus.PAUSED:
            self.resume()

    # ---------------------------
    # Bucle principal
    # ---------------------------

    def step(self, dt: float | None = None) -> None:
        if self.status != EngineStatus.RUNNING:
            return

        if dt is None:
            dt = self.config.tick_rate

        dt = min(dt, self.config.max_time_step)

        # avanzar tiempo global
        self.state.time += dt

        # actualizar lógica
        self._update_logic(dt)

        # notificar a UI
        if self.on_state_updated:
            self.on_state_updated(self)

    # ---------------------------
    # Lógica interna
    # ---------------------------

    def _update_logic(self, dt: float) -> None:
        """
        Hook de lógica. Aquí movemos gatitos por gradiente.
        """
        # seguridad: si no hay terreno o no hay gatos, no hacemos nada
        if not self.state.cats or self.state.terrain is None:
            return

        # mover cada gato según gradiente
        for cat in self.state.cats:
            move_cat_by_gradient(
                cat,
                self.state.terrain,
                step=dt,
                uphill=False
            )