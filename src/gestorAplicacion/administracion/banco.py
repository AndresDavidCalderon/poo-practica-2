#* Equipo 4 grupo 1
# * Clase Banco
# * Representa un banco con una cuenta y un ahorro, posiblemente deudas.

from typing import List

class Banco:
    lista_bancos: List['Banco'] = []
    cuenta_principal = None

    def __init__(self, cuenta: str, nombre: str, ahorro: int, interes: float):
        self.nombre_entidad = nombre
        self.nombre_cuenta = cuenta
        self.ahorro_banco = ahorro
        self.interes = interes
        Banco.lista_bancos.append(self)

    def actualizar_deuda(self, ndeuda):
        self.deuda.append(ndeuda)

    def transaccion(self, monto: int):
        self.ahorro_banco += monto

    def __str__(self):
        return f"La Cuenta: {self.nombre_cuenta} en: {self.nombre_entidad} tiene un Ahorro de: {self.ahorro_banco:,} y para pedir un préstamo el Banco tiene un interés de: {self.interes * 100}%"

    @staticmethod
    def total_ahorros() -> int:
        total = sum(b.get_ahorro_banco() for b in Banco.lista_bancos)
        return total

    # ------------------- Getters y Setters -------------------
    def get_nombre_entidad(self) -> str:
        return self.nombre_entidad

    def get_nombre_cuenta(self) -> str:
        return self.nombre_cuenta

    def get_deuda(self) -> List:
        return self.deuda

    def get_ahorro_banco(self) -> int:
        return self.ahorro_banco

    def get_interes(self) -> float:
        return self.interes

    @staticmethod
    def get_lista_bancos() -> List['Banco']:
        return Banco.lista_bancos

    def set_nombre_entidad(self, nombre_banco: str):
        self.nombre_entidad = nombre_banco

    def set_nombre_cuenta(self, nombre_cuenta: str):
        self.nombre_cuenta = nombre_cuenta

    def set_ahorro_banco(self, ahorro_banco: int):
        self.ahorro_banco = ahorro_banco

    def set_interes(self, interes: float):
        self.interes = interes

    @staticmethod
    def set_lista_bancos(lista_bancos: List['Banco']):
        if lista_bancos is None:
            raise ValueError("La lista no puede ser nula")
        Banco.lista_bancos = lista_bancos

    @staticmethod
    def get_cuenta_principal():
        return Banco.cuenta_principal

    @staticmethod
    def set_cuenta_principal(cuenta_principal: 'Banco'):
        Banco.cuenta_principal = cuenta_principal
