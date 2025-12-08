import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time

from catcalculus.terrain.generator import Terrain
from catcalculus.terrain.functions import (
    meadow,
    wavy_mountain,
    meow_volcano,
    infinite_peak,
)
from catcalculus.cats.models import Cat
from catcalculus.cats.shapes import CatShape
from catcalculus.core.state import GameState
from catcalculus.core.engine import GameEngine

# ====================================================================================
#   INIT GLOBAL
# ====================================================================================
if "game_state" not in st.session_state:
    st.session_state.game_state = GameState.initial_state()

if "engine" not in st.session_state:
    st.session_state.engine = GameEngine(initial_state=st.session_state.game_state)

if "running" not in st.session_state:
    st.session_state.running = False

if "terrain_index" not in st.session_state:
    st.session_state.terrain_index = 0

if "max_z_reached" not in st.session_state:
    st.session_state.max_z_reached = -float('inf') # Inicializar con un valor muy bajo

engine = st.session_state.engine
state = st.session_state.game_state
engine.state = state

terrain_options = {
    "MeaDow": Terrain.from_function(meadow, name="MeaDow"),
    "Wavy mountain": Terrain.from_function(wavy_mountain, name="Wavy mountain"),
    "Meow Volcano": Terrain.from_function(meow_volcano, name="Meow Volcano"),
    "Infinite Peak": Terrain.from_function(infinite_peak, name="Infinite Peak"),
}

# ====================================================================================
#   GRAFICOS
# ====================================================================================

def plot_3d(engine):
    terrain = engine.state.terrain
    X, Y, Z = terrain.x, terrain.y, terrain.z

    fig = go.Figure()

    # Terreno
    fig.add_trace(go.Surface(
        x=X, y=Y, z=Z,
        colorscale="Viridis",
        opacity=0.9,
        showscale=False
    ))

    # Gatos, gradient, trails
    for cat in engine.state.cats:
        zc = terrain.f(cat.x, cat.y)

        fig.add_trace(go.Scatter3d(
            x=[cat.x], y=[cat.y], z=[zc],
            mode="markers+text",
            text=[cat.name],
            marker=dict(size=6),
        ))

        # Trail
        if len(cat.trail) > 2:
            xs = [p[0] for p in cat.trail]
            ys = [p[1] for p in cat.trail]
            zs = [terrain.f(x, y) for x, y in cat.trail]

            fig.add_trace(go.Scatter3d(
                x=xs, y=ys, z=zs,
                mode="lines",
            ))

        # Gradient vector
        dfdx, dfdy = engine.gradient_at(cat.x, cat.y)
        scale = 0.5
        fig.add_trace(go.Scatter3d(
            x=[cat.x, cat.x - dfdx * scale],
            y=[cat.y, cat.y - dfdy * scale],
            z=[zc, zc],
            mode="lines",
        ))

    fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
    return fig


def plot_contours(engine):
    terrain = engine.state.terrain
    X, Y, Z = terrain.x, terrain.y, terrain.z
    fig = go.Figure()

    # Contours
    fig.add_trace(go.Contour(
        x=X[0], y=Y[:, 0], z=Z,
        contours_coloring="lines",
        showscale=False
    ))

    # Gatos
    for cat in engine.state.cats:
        fig.add_trace(go.Scatter(
            x=[cat.x], y=[cat.y],
            mode="markers+text",
            text=[cat.name],
            marker=dict(size=12)
        ))

        # Trail
        if len(cat.trail) > 2:
            xs = [p[0] for p in cat.trail]
            ys = [p[1] for p in cat.trail]
            fig.add_trace(go.Scatter(
                x=xs, y=ys,
                mode="lines",
            ))

        # Gradient
        dfdx, dfdy = engine.gradient_at(cat.x, cat.y)
        scale = 0.5
        fig.add_trace(go.Scatter(
            x=[cat.x, cat.x - dfdx * scale],
            y=[cat.y, cat.y - dfdy * scale],
            mode="lines",
        ))

    fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
    return fig


def build_cat_table(engine):
    terrain = engine.state.terrain
    data = [{
        "Gato": cat.name,
        "x": round(cat.x, 4),
        "y": round(cat.y, 4),
        "z": round(terrain.f(cat.x, cat.y), 4),
        "En mínimo": cat.is_at_minimum,
        "Energía": round(cat.energy, 1),
    } for cat in engine.state.cats]
    return pd.DataFrame(data)

def create_and_add_cat():
    # Accedemos al estado global que está en la sesión
    current_state = st.session_state.game_state

    name = st.session_state.new_cat_name_input
    pos_x = st.session_state.new_cat_x_input
    pos_y = st.session_state.new_cat_y_input

    if name:
        cat = Cat(name=name, x=pos_x, y=pos_y, shape=CatShape(width=0.5, height=0.5))

        new_cats_list = current_state.cats[:]
        new_cats_list.append(cat)
        current_state.cats = new_cats_list

        st.session_state.last_message = f"Gato {name} creado en ({pos_x},{pos_y})"
        st.session_state.last_message_type = "success"
    else:
        st.session_state.last_message = "El gato necesita un nombre."
        st.session_state.last_message_type = "error"

    # Limpiar las entradas
    st.session_state.new_cat_name_input = ""
    st.session_state.new_cat_x_input = 0.0
    st.session_state.new_cat_y_input = 0.0


# ====================================================================================
#   UI
# ====================================================================================
st.title("🐱 Catculus — Demo Interactiva")

mode = st.sidebar.selectbox("Selecciona un modo", ["Juego", "Modo Ingeniero"])

# ====================================================================================
#   MODO INGENIERO
# ====================================================================================
if mode == "Modo Ingeniero":
    st.header("🔧 Modo Ingeniero")

    # --- Terreno ---
    selected = st.selectbox("Terreno", list(terrain_options.keys()))
    terrain = terrain_options[selected]
    engine.state.terrain = terrain

    # --- Controles de simulación ---
    st.subheader("Simulación")

    c1, c2, c3 = st.columns(3)
    if c1.button("▶ Start"):
        engine.start(reset=False)
        st.session_state.running = True
        st.rerun()

    if c2.button("⏸ Pausa"):
        engine.pause()
        st.session_state.running = False

    if c3.button("🔄 Reiniciar"):
        engine.stop()
        engine.state = GameState.initial_state(terrain=engine.state.terrain)
        st.session_state.game_state = engine.state
        st.session_state.running = False
        st.rerun()

    # ====================================================================================
    #   LOOP DE VISUALIZACIÓN
    # ====================================================================================

    # Manejar el step del engine si está corriendo
    if st.session_state.running:
        for _ in range(3):
            engine.step(dt=0.1)

    # Mostrar gráficos
    col3d, col2d = st.columns(2)
    col3d.plotly_chart(plot_3d(engine), use_container_width=True, config={})
    col2d.plotly_chart(plot_contours(engine), use_container_width=True, config={})


    # --- Crear gatos ---
    st.subheader("Crear Gatito 🐾")

    # Mostrar mensaje de éxito/error ANTES del botón
    if "last_message" in st.session_state and st.session_state.last_message:
        if st.session_state.last_message_type == "success":
            st.success(st.session_state.last_message)
        else:
            st.error(st.session_state.last_message)
        st.session_state.last_message = None

    c_name, c_x, c_y, c_button = st.columns([1, 1, 1, 1])

    with c_name:
        st.text_input("Nombre", key="new_cat_name_input", label_visibility="collapsed", placeholder="Nombre")
    with c_x:
        st.number_input("x", value=0.0, key="new_cat_x_input", label_visibility="collapsed")
    with c_y:
        st.number_input("y", value=0.0, key="new_cat_y_input", label_visibility="collapsed")
    with c_button:
        st.button("Crear gato", on_click=create_and_add_cat, use_container_width=True)

    # --- Tabla de Gatos ---
    st.dataframe(build_cat_table(engine))

    # --- Bucle de Simulación ---
    if st.session_state.running:
        time.sleep(0.08)
        st.rerun()


# ==========================
#     🎮 MODO JUEGO
# ==========================
else:

    st.header("🎮 Modo Juego — Desafío 2D")

    # --- DEFINICIÓN DEL CORTE Y PLOTEO ---
    SLICE_COORD = 0.0
    # Selecciona si el corte es a lo largo del eje 'x' o 'y'.
    SLICE_AXIS = 'x' # Corte horizontal (mueve en X, Y=0 fijo)
    terrain_keys = list(terrain_options.keys())

    # Jugador
    if "player" not in st.session_state:
        if st.session_state.terrain_index == 2 or st.session_state.terrain_index == 3:
            start_coord = -4
        else:
            start_coord = 0

        initial_x = SLICE_COORD if SLICE_AXIS == 'y' else start_coord
        initial_y = SLICE_COORD if SLICE_AXIS == 'x' else start_coord

        st.session_state.player = Cat(
            name="Jugador",
            x=initial_x,
            y=initial_y,
            shape=CatShape(width=0.5, height=0.5)
        )
        st.session_state.energy = 100
        st.session_state.selected_terrain = terrain_keys[st.session_state.terrain_index]
    player = st.session_state.player

    # Lógica de cambio de terreno
    if st.session_state.get("goal_reached", False):
        current_index = st.session_state.terrain_index

        if current_index == len(terrain_keys) - 1: # Final del juego
            st.balloons()
            st.success("🏆 ¡FELICIDADES, COMPLETÓ CATCÁLCULUS! 🏆")
            st.session_state.goal_reached = False
            st.stop()

        next_index = (current_index + 1) % len(terrain_keys) # Siguiente terreno, vuelve al inicio

        st.session_state.terrain_index = next_index
        st.session_state.energy = 100

        # REINICIAMOS EL MÁXIMO Z ALCANZADO PARA EL NUEVO TERRENO
        st.session_state.max_z_reached = -float('inf')

        if next_index == 2 or next_index == 3:
            start_coord = -4
        else:
            start_coord = 0

        st.session_state.player.x = SLICE_COORD if SLICE_AXIS == 'y' else start_coord
        st.session_state.player.y = SLICE_COORD if SLICE_AXIS == 'x' else start_coord
        st.session_state.goal_reached = False
        st.rerun()

    current_terrain_key = terrain_keys[st.session_state.terrain_index]

    # El usuario todavía puede cambiarlo si quiere explorar
    # Usamos la clave actual del índice como valor predeterminado
    st.session_state.selected_terrain = st.selectbox("Terreno", terrain_keys, index=st.session_state.terrain_index)

    # Si el usuario cambia manualmente el selectbox, actualizamos el índice para que sea consistente
    if st.session_state.selected_terrain != current_terrain_key:
        st.session_state.terrain_index = terrain_keys.index(st.session_state.selected_terrain)


    terrain = terrain_options[st.session_state.selected_terrain]

    # ----------------------------------------------------------------------
    #   NUEVA FUNCIÓN DE PLOTEO PARA EL CORTE 1D
    # ----------------------------------------------------------------------
    def plot_slice_2d(terrain, cat, slice_axis, slice_coord):
        """Genera el gráfico 2D del corte de la función y la posición del gato."""
        fig = go.Figure()

        if slice_axis == 'x':
            axis_values = terrain.x[0]
            z_values = np.array([terrain.f(x, slice_coord) for x in axis_values])
            cat.y = slice_coord
            axis_label = "Posición X"
            slice_label = f"Corte en Y = {slice_coord:.2f}"
            cat_coord_to_plot = cat.x
        else:
            axis_values = terrain.y[:, 0]
            z_values = np.array([terrain.f(slice_coord, y) for y in axis_values])
            cat.x = slice_coord
            axis_label = "Posición Y"
            slice_label = f"Corte en X = {slice_coord:.2f}"
            cat_coord_to_plot = cat.y

        min_val = axis_values.min()
        max_val = axis_values.max()

        # Plotear la función
        fig.add_trace(go.Scatter(
            x=axis_values,
            y=z_values,
            mode='lines',
            name=terrain.name,
            line=dict(color='orange', width=4),
            fill='tozeroy',
            fillcolor='rgba(255, 165, 0, 0.3)'
        ))

        # Gatito
        cat_z = terrain.f(cat.x, cat.y)

        fig.add_trace(go.Scatter(
            x=[cat_coord_to_plot],
            y=[cat_z],
            mode='text+markers',
            text=["🐱"],
            name=cat.name,
            textfont=dict(size=24),
            marker=dict(size=1, color='red'),
        ))

        # Actualizar diseño y límites
        fig.update_xaxes(
            title_text=axis_label,
            range=[min_val, max_val],
            showgrid=True
        )
        fig.update_yaxes(
            title_text="Altura Z",
            showgrid=True
        )

        fig.update_layout(
            title=f"Ascenso en {terrain.name} ({slice_label})",
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='#f0f2f6'
        )

        # Lógica de "Llegada a la cima"
        MAX_Z_TERRAIN = z_values.max()
        TOLERANCE = 0.05 * MAX_Z_TERRAIN # Tolerancia del 5% del máximo

        current_max_z = st.session_state.max_z_reached

        if current_max_z >= MAX_Z_TERRAIN - TOLERANCE:

            fig.add_shape(type="line", x0=min_val, y0=MAX_Z_TERRAIN, x1=max_val, y1=MAX_Z_TERRAIN,
                          line=dict(color="green", width=2, dash="dash"),
                          name="Meta")

            st.session_state.goal_reached = True
            st.success(f"🎉 ¡Felicidades, {cat.name} encontró la cima (Z máx ≈ {MAX_Z_TERRAIN:.2f})! Presiona el botón de mover para pasar al siguiente terreno.")

        if current_max_z > -float('inf'):
            st.markdown(f"**Altura Máxima Alcanzada:** {current_max_z:.2f} / {MAX_Z_TERRAIN:.2f}")


        return fig

    # Mostrar el nuevo gráfico de corte 2D
    st.plotly_chart(plot_slice_2d(terrain, st.session_state.player, SLICE_AXIS, SLICE_COORD), use_container_width=True)

    st.subheader("Movimiento del gato")

    col1, col2, col3 = st.columns(3)

    step_size = 0.5
    MIN_COST_UP = 2
    RECHARGE_DOWN = 3
    GRADIENT_FACTOR = 10

    # Función de movimiento general
    def handle_move(dx, dy):
        if st.session_state.get("goal_reached", False):
            st.rerun()
            return

        # Calcular la posición y altura actual (Z_old)
        old_x, old_y = player.x, player.y
        z_old = terrain.f(old_x, old_y)

        # Calcular la posición y altura futura (Z_new)
        new_x = old_x + dx * step_size
        new_y = old_y + dy * step_size
        z_new = terrain.f(new_x, new_y)

        # Determinar el cambio de energía
        energy_change = 0

        if z_new > z_old:
            # --- LÓGICA DE COSTE BASADA EN PENDIENTE ---
            dfdx, dfdy = engine.gradient_at(old_x, old_y)
            gradient_magnitude = np.sqrt(dfdx**2 + dfdy**2)
            # El costo aumenta con la magnitud del gradiente
            cost_up = MIN_COST_UP + int(gradient_magnitude * GRADIENT_FACTOR)
            # Subiendo: Gasta energía, solo si tiene
            if st.session_state.energy >= cost_up:
                energy_change = -cost_up
            else:
                st.session_state.last_game_message = f"🥵 ¡Necesitas {cost_up} energía para subir aquí! (Pendiente: {gradient_magnitude:.2f})"
                st.rerun()
                return # No movemos si intenta subir sin energía
        else:
            # Bajando o moviéndose lateralmente/descansando: Recarga
            energy_change = RECHARGE_DOWN

        # Aplicar el movimiento y el cambio de energía
        player.move(dx * step_size, dy * step_size)
        st.session_state.energy += energy_change

        # Asegurar límites de energía
        st.session_state.energy = int(np.clip(st.session_state.energy, 0, 100))

        # Actualizar el máximo Z alcanzado
        if z_new > st.session_state.max_z_reached:
            st.session_state.max_z_reached = z_new

        st.rerun()


    # Arriba / Abajo
    if SLICE_AXIS == 'y': # Si el corte es en Y, el movimiento "arriba/abajo" es en Y
        if col2.button("⬆️"):
            handle_move(0, 1) # Mueve Y
        if col2.button("⬇️"):
            handle_move(0, -1) # Mueve Y

    # Izquierda / Derecha
    if SLICE_AXIS == 'x': # Si el corte es en X, el movimiento "izq/der" es en X
        col1.button("⬅️", on_click=lambda: handle_move(-1, 0)) # Mueve X
        col3.button("➡️", on_click=lambda: handle_move(1, 0)) # Mueve X

    # Barra de energía
    display_energy = int(np.clip(st.session_state.energy, 0, 100))

    st.progress(display_energy)

    if st.session_state.energy <= 0:
        st.error("💤 El gatito está agotado. Necesita descansar…")

    # Muestra el mensaje si existe
    if "last_game_message" in st.session_state and st.session_state.last_game_message:
        st.warning(st.session_state.last_game_message)
        st.session_state.last_game_message = None