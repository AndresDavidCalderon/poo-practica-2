from enum import Enum

class Membresia(Enum):
    ORO=0.30
    PLATA=0.15
    BRONCE=0.5
    NULA=0.0
    
    def __init__(self, descuento):
        self.porcentajeDescuento = descuento
	
    def getPorcentajeDescuento(self):
        return self.porcentajeDescuento