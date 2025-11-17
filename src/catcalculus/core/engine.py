# src/catcalculus/core/engine.py
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Optional

from catcalculus.core.state import GameState


class EngineStatus(Enum):
    STOPPED = auto()
    RUNNING = auto()
    PAUSED = auto()


@dataclass
class EngineConfig:
    """
    Configuración básica del engine.

    tick_rate: frecuencia lógica de actualización (ej. 30 FPS -> 1/30 s).
    max_time_step: paso máximo permitido por update, para evitar saltos bruscos.
    """
    tick_rate: float = 1.0 / 30.0
    max_time_step: float = 0.1  # 100 ms


class GameEngine:
    """
    Núcleo del juego.

    Se encarga de:
    - Mantener el GameState
    - Avanzar el tiempo lógico con step(dt)
    - Gestionar inicio, pausa y reinicio
    - Notificar cambios a un callback opcional (para UI/render)
    """

    def __init__(
        self,
        initial_state: Optional[GameState] = None,
        config: Optional[EngineConfig] = None,
    ) -> None:
        self.config = config or EngineConfig()
        self.state: GameState = initial_state or GameState.initial_state()
        self.status: EngineStatus = EngineStatus.STOPPED

        # Callback opcional que puede usar la UI para “escuchar” cambios
        # firma: on_state_updated(engine: GameEngine) -> None
        self.on_state_updated: Optional[Callable[[GameEngine], None]] = None

    # ---------------------------
    # Gestión de ciclo de vida
    # ---------------------------

    def start(self, reset: bool = True) -> None:
        """
        Inicia el juego. Si reset=True, reinicia el estado a valores iniciales.
        """
        if reset:
            self.state = GameState.initial_state(
                terrain=self.state.terrain,
                cats=self.state.cats,
            )
        self.status = EngineStatus.RUNNING

    def pause(self) -> None:
        """Pone el juego en pausa (no avanza el tiempo lógico)."""
        if self.status == EngineStatus.RUNNING:
            self.status = EngineStatus.PAUSED

    def resume(self) -> None:
        """Reanuda el juego desde PAUSED."""
        if self.status == EngineStatus.PAUSED:
            self.status = EngineStatus.RUNNING

    def stop(self) -> None:
        """Detiene el juego completamente."""
        self.status = EngineStatus.STOPPED

    def toggle_pause(self) -> None:
        """Conveniencia para alternar entre RUNNING y PAUSED."""
        if self.status == EngineStatus.RUNNING:
            self.pause()
        elif self.status == EngineStatus.PAUSED:
            self.resume()

    # ---------------------------
    # Bucle de actualización
    # ---------------------------

    def step(self, dt: float | None = None) -> None:
        """
        Avanza el estado del juego dt segundos lógicos.

        Si dt es None, usa el tick_rate de configuración.
        No hace nada si el engine no está en RUNNING.
        """
        if self.status != EngineStatus.RUNNING:
            return

        if dt is None:
            dt = self.config.tick_rate

        # Limitar dt para evitar saltos gigantes
        dt = min(dt, self.config.max_time_step)

        # 1) Actualizar tiempo global
        self.state.time += dt

        # 2) Actualizar lógica del juego (gatos, eventos, etc.)
        self._update_logic(dt)

        # 3) Notificar a la UI (si hay callback)
        if self.on_state_updated is not None:
            self.on_state_updated(self)

    # ---------------------------
    # Lógica interna (placeholder por ahora)
    # ---------------------------

    def _update_logic(self, dt: float) -> None:
        """
        Lógica de actualización del mundo.

        Por ahora, dejamos el hook vacío para Epic 4 (gatitos) y Epic 2/3.
        Acá más adelante:
        - mover gatos según gradiente
        - aplicar consumo de energía
        - manejar eventos
        """
        # TODO: implementar cuando esté Epic 2 y 4
        pass
