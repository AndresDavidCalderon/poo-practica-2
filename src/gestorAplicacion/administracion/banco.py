#* Equipo 4 grupo 1
# * Clase Banco
# * Representa un banco con una cuenta y un ahorro, posiblemente deudas.

from typing import List

class Banco:
    listaBancos= []
    cuenta_principal = None

    def __init__(self, cuenta: str, nombre: str, ahorro: int, interes: float):
        self.nombreEntidad = nombre
        self.nombreCuenta = cuenta
        self.ahorroBanco = ahorro
        self.interes = interes
        self.deuda= []
        Banco.listaBancos.append(self)

    def actualizarDeuda(self, ndeuda):
        self.deuda.append(ndeuda)

    def transaccion(self, monto: int):
        self.ahorroBanco += monto

    def __str__(self):
        return f"La Cuenta: {self.nombreCuenta} en: {self.nombreEntidad} tiene un Ahorro de: {self.ahorroBanco:,} y para pedir un préstamo el Banco tiene un interés de: {self.interes * 100}%"

    @staticmethod
    def totalAhorros(cls):
        total=0
        for b in Banco.listaBancos:
            total+=b.getAhorroBanco()
        return total

    # ------------------- Getters y Setters -------------------
    def getNombreEntidad(self) -> str:
        return self.nombreEntidad

    def getNombreCuenta(self) -> str:
        return self.nombreCuenta

    def getDeuda(self) -> List:
        return self.deuda

    def getAhorroBanco(self) -> int:
        return self.ahorroBanco

    def getInteres(self) -> float:
        return self.interes

    @staticmethod
    def getListaBancos():
        return Banco.listaBancos

    def setNombreEntidad(self, nombreBanco: str):
        self.nombreEntidad = nombreBanco

    def setNombreCuenta(self, nombreCuenta: str):
        self.nombreCuenta = nombreCuenta

    def setAhorroBanco(self, ahorroBanco: int):
        self.ahorroBanco = ahorroBanco

    def setInteres(self, interes: float):
        self.interes = interes

    @staticmethod
    def setListaBancos(listaBancos):
        if listaBancos is None:
            raise ValueError("La lista no puede ser nula")
        Banco.listaBancos = listaBancos

    @staticmethod
    def getCuentaPrincipal():
        return Banco.cuenta_principal

    @staticmethod
    def setCuentaPrincipal(cuentaPrincipal):
        Banco.cuentaPrincipal = cuentaPrincipal
