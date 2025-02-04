from src.gestorAplicacion.Bodega import Insumo

class Bolsa(Insumo):
    def __init__(self, nombre, cantidad, proveedor, sede, capacidad_maxima):
        super().__init__(nombre, cantidad, proveedor, sede)
        self.capacidad_maxima = capacidad_maxima

    def __init__(self, nombre, proveedor):
        super().__init__(nombre, proveedor)

    # Calcula el precio de la bolsa, que puede diferir del definido como Insumo.
    def get_precio_individual(self):
        return round(self.precio_x_unidad - (self.precio_x_unidad * self.proveedor.get_descuento() * self.capacidad_maxima))

    def get_capacidad_maxima(self):
        return self.capacidad_maxima

    def set_capacidad_maxima(self, capacidad_maxima):
        self.capacidad_maxima = capacidad_maxima