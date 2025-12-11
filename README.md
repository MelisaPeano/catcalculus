# Catcalculus

Simulador/juego didáctico de cálculo multivariable donde gatitos se mueven sobre campos escalares 2D. Incluye gradientes numéricos, derivadas direccionales y visualizaciones 2D/3D pensadas para explicar conceptos típicos de Cálculo 2 (pendientes, mínimos, curvas de nivel y áreas bajo la curva).

## Características
- **Terrenos parametrizables:** funciones de ejemplo (prado convexo, montaña seno/coseno, volcán, pico gaussiano) definidas en `src/catcalculus/terrain/functions.py`, construidas como mallas `x,y,z` vía `Terrain.from_function`.
- **Cálculo vectorial:** gradiente numérico central, norma del gradiente y derivada direccional disponibles en `src/catcalculus/core/math_tools.py`.
- **Movimiento por gradiente:** los gatos siguen descenso (o ascenso opcional) con paso proporcional a |∇f| y agilidad (`core/movement.py`) gestionado por el motor (`core/engine.py`).
- **Coordenadas continuo↔grilla:** `CoordinateSystem` mantiene la coherencia entre posiciones del mundo y los índices de la malla (`core/coordinates.py`).
- **UI en Streamlit:** dos modos:
  - *Modo Ingeniero*: superficie 3D, curvas de nivel, vectores de gradiente, tabla de gatos.
  - *Modo Juego*: corte 1D de la superficie con recta tangente, área bajo la curva, HUD de pendientes/gradiente y mecánica de energía.

## Requisitos previos
- Python 3.10+ (probado con 3.11)
- `pip` para instalar dependencias listadas en `requirements.txt`

## Instalación
```bash
python -m venv venv
source venv/bin/activate     # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecutar la demo (Streamlit)
```bash
streamlit run src/catcalculus/ui/streamlit_app.py
```

### Qué encontrarás
- **Modo Ingeniero** (sidebar): elige un terreno, inicia/pausa/reinicia la simulación, crea gatos y observa en 3D/contornos cómo descienden hasta mínimos locales.
- **Modo Juego**: explora un corte 1D; muévete con las flechas; la energía depende de la pendiente (subir cuesta); se muestra la recta tangente, el área recorrida y |∇f|; al alcanzar la cota máxima de un terreno pasas al siguiente.

## Estructura rápida
- `src/catcalculus/core/`: motor de simulación (estado, gradientes, movimiento, coordenadas).
- `src/catcalculus/terrain/`: definición y generación de terrenos a partir de funciones.
- `src/catcalculus/cats/`: modelo del gato y tamaño/forma sobre la malla.
- `src/catcalculus/ui/`: interfaz Streamlit (`streamlit_app.py`).

## Extender/experimentar
- Agrega nuevas superficies creando funciones `f(x, y)` en `terrain/functions.py` y añádelas a `terrain_options` en `ui/streamlit_app.py`.
- Ajusta la agilidad del gato (`Cat.agility`) o los parámetros de energía en el modo juego para variar la dificultad.
- Reusa `numeric_gradient`, `directional_derivative` o `gradient_magnitude` para ejercicios de cálculo simbólico/numérico adicionales.

## Pruebas
Hay dependencias para `pytest` en `requirements.txt`. Si agregas tests, ejecútalos con:
```bash
pytest
```

## Troubleshooting rápido
- Asegúrate de activar el entorno virtual antes de correr Streamlit.
- Si el navegador no abre automáticamente, visita `http://localhost:8501`.
- Si una función de terreno falla, revisa que devuelva un `np.ndarray` con la misma forma que las mallas `X, Y` (ver `Terrain.from_function`).

