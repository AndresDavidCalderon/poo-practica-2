
from src.gestorAplicacion.bodega.insumo import Insumo


class Repuesto(Insumo):  # Implements serializable for Repuesto
    listado_repuestos = []  # Static variable to hold all Repuesto instances

    def __init__(self, nombre, horas_de_vida_util, proveedor, p=None):
        super().__init__(nombre, horas_de_vida_util, proveedor)
        self.fechas_compra = []  # List to store purchase dates
        self.precios_compra = []  # List to store purchase prices
        self.horas_de_uso = 0
        self.estado = True
        Repuesto.listado_repuestos.append(self)

        if p is not None:
            self.horas_de_uso = 100000  # Special constructor to damage Repuesto

    def get_fechas_compra(self):
        return self.fechas_compra

    def set_fechas_compra(self, fecha_compra):
        self.fechas_compra.append(fecha_compra)

    def get_precios_compra(self):
        return self.fechas_compra

    def set_precios_compra(self, precio):
        self.precios_compra.append(precio)

    def get_nombre(self):
        return self.nombre

    def get_horas_de_vida_util(self):
        return self.horas_de_vida_util

    def set_horas_de_uso(self):
        # Here we will modify the hours of use for each Repuesto
        pass

    def get_horas_de_uso(self):
        return self.horas_de_uso

    @staticmethod
    def get_listado_repuestos():
        return Repuesto.listado_repuestos

    @staticmethod
    def reemplazar_listado_repuestos(nuevo_listado_repuestos):
        Repuesto.listado_repuestos = nuevo_listado_repuestos

    @staticmethod
    def set_listado_repuestos(repuesto_a_retirar):
        Repuesto.listado_repuestos.remove(repuesto_a_retirar)

    def set_estado(self):
        self.estado = False

    def is_estado(self):
        return self.estado

    def copiar(self):
        return Repuesto(self.nombre, self.horas_de_vida_util, self.proveedor)

    def copiar_proveedor(self, proveedor_barato):
        return Repuesto(self.nombre, self.horas_de_vida_util, proveedor_barato)

    def calcular_gasto_mensual(self, fecha):
        gasto_mensual = 0
        for i in range(len(self.fechas_compra)):
            if (self.fechas_compra[i].get_año() == fecha.get_año() and
                    self.fechas_compra[i].get_mes() == fecha.get_mes()):
                gasto_mensual += self.precios_compra[i]
        return gasto_mensual

    # Auxiliary to Maquina.usar
    def usar(self, horas):
        self.horas_de_uso += horas