import streamlit as st
import matplotlib.pyplot as plt

from catcalculus.core.engine import GameEngine, EngineStatus
from catcalculus.core.coordinates import WorldBounds, CoordinateSystem
from catcalculus.terrain.generator import Terrain
from catcalculus.terrain import functions
from catcalculus.core.movement import move_cat_by_gradient


def _get_engine() -> GameEngine:
    """
    Obtiene (o crea) una instancia de GameEngine guardada en session_state.
    Esto es importante porque Streamlit re-evalúa el script en cada interacción.
    """
    if "engine" not in st.session_state:
        st.session_state.engine = GameEngine()
    return st.session_state.engine


def _apply_selected_terrain(engine: GameEngine, level_name: str) -> None:
    """
    Genera un terreno nuevo según el nivel seleccionado y lo aplica al estado.
    """
    func_map = {
        "Prado suave": functions.meadow,
        "Montaña ondulada": functions.wavy_mountain,
        "Volcán del miau": functions.meow_volcano,
        "Pico infinito": functions.infinite_peak,
    }

    func = func_map[level_name]
    terrain = Terrain.from_function(func, name=level_name)

    bounds = WorldBounds(
        x_min=float(terrain.x.min()),
        x_max=float(terrain.x.max()),
        y_min=float(terrain.y.min()),
        y_max=float(terrain.y.max()),
    )
    coord_sys = CoordinateSystem(bounds, terrain.z.shape)

    engine.state.terrain = terrain
    engine.state.coordinate_system = coord_sys
    engine.state.time = 0.0  # reseteamos tiempo lógico al cambiar de mapa


def _render_terrain_3d(terrain: Terrain) -> None:
    """
    Dibuja la superficie del terreno en 3D usando matplotlib y la muestra en Streamlit.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(terrain.x, terrain.y, terrain.z, linewidth=0, antialiased=True)
    ax.set_title(terrain.name)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("f(x,y)")

    st.pyplot(fig)


def main():
    st.set_page_config(page_title="Catcalculus", layout="wide")

    st.title("😼 Catculus – Vista inicial de la montaña")

    engine = _get_engine()

    # ---- Sidebar: controles del engine ----
    st.sidebar.header("Controles de simulación")

    level_name = st.sidebar.selectbox(
        "Terreno",
        ["Prado suave", "Montaña ondulada", "Volcán del miau", "Pico infinito"],
        index=0,
    )

    if st.sidebar.button("Aplicar terreno"):
        _apply_selected_terrain(engine, level_name)

    st.sidebar.markdown("---")

    col_start, col_pause, col_step = st.sidebar.columns(3)

    if col_start.button("Start/Reiniciar"):
        engine.start(reset=True)

    if engine.status == EngineStatus.RUNNING:
        if col_pause.button("Pausar"):
            engine.pause()
    else:
        if col_pause.button("Reanudar"):
            engine.resume()

    if col_step.button("Step"):
        engine.step()

    st.sidebar.markdown("---")
    st.sidebar.write(f"Estado: **{engine.status.name}**")
    st.sidebar.write(f"Tiempo lógico: **{engine.state.time:.2f} s**")
    st.sidebar.write(f"N° de gatitos: **{len(engine.state.cats)}**")

    # ---- Layout principal ----
    col_info, col_plot = st.columns([1, 2])

    with col_info:
        st.subheader("Estado del juego")
        st.write(f"- Terreno actual: `{engine.state.terrain.name}`")
        st.write(f"- Dimensiones grilla: {engine.state.terrain.z.shape}")
        st.write(f"- Modo: `{engine.state.mode}`")

        if engine.state.cats:
            st.subheader("Gatitos")
            for cat in engine.state.cats:
                with st.container(border=True):
                    st.markdown(f"### 🐱 {cat.name}")
                    st.write(f"**Energía:** {cat.energy:.1f}")
                    st.write(f"**Posición:** ({cat.x:.2f}, {cat.y:.2f})")
        else:
            st.info("Todavía no hay gatitos en el estado.")

    with col_plot:
        st.subheader("Terreno 3D")
        _render_terrain_3d(engine.state.terrain)

if __name__ == "__main__":
    main()
