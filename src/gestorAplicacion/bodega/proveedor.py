from typing import List, Optional

from typing import List
from src.gestorAplicacion.fecha import Fecha
from src.gestorAplicacion.bodega.insumo import Insumo
from src.gestorAplicacion.administracion.deuda import Deuda

class Proveedor:
    lista_proveedores=[]

    def __init__(self, precio: int = 0, nombre: str = "", insumo: Optional[Insumo] = None):
        self.precio = precio
        self.nombre = nombre
        self.descuento = 0.0
        self.deuda = None
        self.tipo_insumo = insumo
        Proveedor.lista_proveedores.append(self)

    @staticmethod
    def buscar_por_nombre_insumo(nombre: str) -> Optional['Proveedor']:
        for proveedor in Proveedor.lista_proveedores:
            if proveedor.tipo_insumo.get_nombre() == nombre:
                return proveedor
        return None

    @staticmethod
    def costo_de_la_cantidad(insumo: Insumo, cantidad: int) -> int:
        precio_total = 0
        for proveedor in Proveedor.lista_proveedores:
            if proveedor.tipo_insumo == insumo:
                bolsa = insumo  # Assuming Insumo is a Bolsa in this context
                precio_total = (proveedor.precio - round(proveedor.precio * proveedor.descuento * bolsa.get_capacidad_maxima())) * cantidad
        return precio_total

    def unificar_deudas_por_proveedor(self, fecha: Fecha, monto_deuda: int):
        cuotas = Deuda.calcular_cuotas(monto_deuda + self.deuda.get_valor_inicial_deuda() - self.deuda.get_capital_pagado())
        if self.deuda.get_entidad() == self.get_nombre() and not self.deuda.get_estado_de_pago():
            self.deuda.actualizar_deuda(fecha, monto_deuda, cuotas)

    @classmethod
    def get_lista_proveedores(cls):
        return cls.lista_proveedores

    @classmethod
    def set_lista_proveedores(cls, lista):
        cls.lista_proveedores = lista

    def get_deuda(self) -> Optional[Deuda]:
        return self.deuda

    def set_deuda(self, deuda: Deuda):
        self.deuda = deuda

    def get_insumo(self) -> Optional[Insumo]:
        return self.tipo_insumo

    def set_insumo(self, insumo: Insumo):
        self.tipo_insumo = insumo

    def get_precio(self) -> int:
        return self.precio

    def set_precio(self, monto: int):
        self.precio = monto

    def get_nombre(self) -> str:
        return self.nombre

    def set_nombre(self, nombre: str):
        self.nombre = nombre

    def get_descuento(self) -> float:
        return self.descuento

    def set_descuento(self, monto: float):
        self.descuento = monto

    def __str__(self):
        return f"El proveedor {self.nombre} vende insumos de tipo {self.tipo_insumo.get_nombre()} y valen {self.precio}"