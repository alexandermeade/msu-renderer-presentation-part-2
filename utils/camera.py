import math
from pydantic.dataclasses import dataclass
import numpy as np
from pydantic import Field

class Camera: 
    fov: float
    zfar: float
    znear: float
    width: float
    height: float
    pos: np.ndarray 

    def __init__(self, fov: float, zfar: float, znear: float, width: float, height: float, pos:np.ndarray | None =None):
        self.fov = fov
        self.zfar = zfar
        self.znear = znear
        self.width = width
        self.height = height

        self.pos = np.zeros(3) if pos is None else np.asarray(pos)

    def aspect_ratio(self) -> float:
        return self.width/self.height

