from typing import List
from ..fecha import Fecha
from .insumo import Insumo
from .proveedor import Proveedor

class Repuesto(Insumo):
    listado_repuestos = []

    def __init__(self, nombre: str, horas_de_vida_util: int, proveedor: Proveedor):
        self.nombre = nombre
        self.horas_de_vida_util = horas_de_vida_util
        self.proveedor = proveedor
        self.fechas_compra = []
        self.precios_compra = []
        self.horas_de_uso = 0
        self.estado = True
        Repuesto.listado_repuestos.append(self)

    def get_fechas_compra(self) -> List[Fecha]:
        return self.fechas_compra

    def set_fechas_compra(self, fecha_compra: Fecha):
        self.fechas_compra.append(fecha_compra)

    def get_precios_compra(self) -> List[int]:
        return self.precios_compra

    def set_precios_compra(self, precio: int):
        self.precios_compra.append(precio)

    def get_nombre(self) -> str:
        return self.nombre

    def get_horas_de_vida_util(self) -> int:
        return self.horas_de_vida_util

    def set_horas_de_uso(self, horas: int):
        self.horas_de_uso += horas

    def get_horas_de_uso(self) -> int:
        return self.horas_de_uso

    @staticmethod
    def get_listado_repuestos() -> List['Repuesto']:
        return Repuesto.listado_repuestos

    @staticmethod
    def reemplazar_listado_repuestos(listado_repuestos: List['Repuesto']):
        Repuesto.listado_repuestos = listado_repuestos

    @staticmethod
    def set_listado_repuestos(repa_retirar: 'Repuesto'):
        Repuesto.listado_repuestos.remove(repa_retirar)

    def set_estado(self):
        self.estado = False

    def is_estado(self) -> bool:
        return self.estado

    def copiar(self) -> 'Repuesto':
        return Repuesto(self.nombre, self.horas_de_vida_util, self.proveedor)

    def copiar_con_proveedor(self, prov_barato: 'Proveedor') -> 'Repuesto':
        return Repuesto(self.nombre, self.horas_de_vida_util, prov_barato)

    def calcular_gasto_mensual(self, fecha: Fecha) -> int:
        gasto_mensual = 0
        for i in range(len(self.fechas_compra)):
            if self.fechas_compra[i].year == fecha.year and self.fechas_compra[i].month == fecha.month:
                gasto_mensual += self.precios_compra[i]
        return gasto_mensual

    def usar(self, horas: int):
        self.horas_de_uso += horas


    # Auxiliary to Maquina.usar
    def usar(self, horas):
        self.horas_de_uso += horas
