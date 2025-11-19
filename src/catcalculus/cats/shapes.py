from dataclasses import dataclass
import numpy as np

@dataclass
class CatShape:
    """
    Representa la forma o tamaño de un gatito sobre el terreno.
    La posición x,y del gatito será el centro.
    """
    width: float  # ancho en unidades del mundo
    height: float  # alto en unidades del mundo
    z_profile: np.ndarray | None = None  # perfil de altura opcional
