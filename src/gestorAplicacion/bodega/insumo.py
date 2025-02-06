from src.gestorAplicacion.sede import Sede;

class Insumo:
    precio_stock_total = 0

    def __init__(self, nombre, cantidad=None, proveedor=None, sede=None, horas_de_vida_util=None):
        self.nombre = nombre
        self.proveedor = proveedor
        self.sede = sede
        if cantidad is not None and proveedor is not None:
            self.precio_compra = proveedor.get_precio() * round(cantidad)
            self.precio_x_unidad = round(self.precio_compra / cantidad)
            self.ultimo_precio = self.precio_x_unidad
            Insumo.precio_stock_total += self.precio_compra
            sede.get_lista_insumos_bodega().append(self)
            sede.get_cantidad_insumos_bodega().append(round(cantidad))
        elif proveedor is not None:
            self.precio_x_unidad = proveedor.get_precio()
        if horas_de_vida_util is not None:
            self.horas_de_vida_util = horas_de_vida_util

    @staticmethod
    def gasto_mensual_clase(fecha):
        gasto_insumo = 0
        gasto_actual = 0
        gasto_pasado = 0
        for sede in Sede.get_lista_sedes():
            for venta in sede.get_historial_ventas():
                for insumo in venta.get_bolsas():
                    lista = insumo.gasto_mensual_tipo(fecha, venta.get_fecha_venta(), insumo)
                    gasto_actual += lista[0]
                    gasto_pasado += lista[1]
                    if gasto_actual != 0:
                        gasto_insumo = gasto_actual
                    else:
                        gasto_insumo = gasto_pasado
        return gasto_insumo

    def calcular_gasto_mensual(self):
        valor = 0
        for i in range(len(self.sede.get_lista_insumos_bodega())):
            if self.sede.get_lista_insumos_bodega()[i] == self:
                valor = self.get_precio_individual() * self.sede.get_cantidad_insumos_bodega()[i]
        return valor

    @staticmethod
    def get_precio_stock_total():
        return Insumo.precio_stock_total

    @staticmethod
    def set_precio_stock_total(precio_stock_total):
        Insumo.precio_stock_total = precio_stock_total

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre):
        self.nombre = nombre

    def get_proveedor(self):
        return self.proveedor

    def set_proveedor(self, proveedor):
        self.proveedor = proveedor

    def get_sede(self):
        return self.sede

    def set_sede(self, sede):
        self.sede = sede

    def get_precio_compra(self):
        return self.precio_compra

    def set_precio_compra(self, precio):
        self.precio_compra = precio

    def get_precio_individual(self):
        return self.precio_x_unidad

    def set_ultimo_precio(self, precio):
        self.ultimo_precio = precio

    def get_ultimo_precio(self):
        return self.ultimo_precio

    def __str__(self):
        return f"Insumo: {self.nombre}"