from src.gestorAplicacion.Administracion import Empleado
from src.gestorAplicacion.Fecha import Fecha
from src.gestorAplicacion.Sede import Sede
from typing import List, Optional
import random
from src.gestorAplicacion.bodega.prenda import Prenda
from src.gestorAplicacion.bodega.insumo import Insumo

class Camisa(Prenda):
    serial_version_uid = 1
    cantidad_insumo = []
    tipo_insumo = []
    paso_actual = 1

    maquinaria_necesaria = ["Maquina de Corte", "Bordadora Industrial", "Maquina de Coser Industrial", "Maquina de Termofijado", "Plancha Industrial"]

    def __init__(self, fecha: Fecha, modista: Empleado, descartada: bool, terminada: bool, sede: Sede, insumos: List[Insumo]):
        super().__init__(fecha, sede, "Camisa", modista, descartada, terminada, insumos)

    def calcular_gasto_mensual(self) -> int:
        gasto = 0
        for i in range(len(self.insumo)):
            tipo = self.insumo[i]
            cantidad = self.cantidad_insumo[i]
            gasto += round(tipo.get_precio_individual() * cantidad)
        return gasto

    @staticmethod
    def precio_venta() -> int:
        precios = 0
        cantidades = 0
        precio_venta = 0
        for camisa in Sede.get_prendas_inventadas_total():
            if isinstance(camisa, Camisa):
                precios += camisa.calcular_precio()
                cantidades += 1
        if cantidades > 0:
            precio_venta = round(precios / cantidades)
        # Se promedian todos los "precios por los que se deberían vender las prendas para que todas las camisas se vendan al mismo"
        return precio_venta

    def siguiente_paso(self) -> List[Optional[int]]:
        retorno = []
        if self.paso_actual == 1:
            retorno.extend(["Maquina de Corte", 5])
        elif self.paso_actual == 2:
            retorno.extend(["Maquina de Coser Industrial", 10])
        elif self.paso_actual == 3:
            retorno.extend(["Plancha Industrial", 5])
        elif self.paso_actual == 4:
            retorno.extend(["Bordadora Industrial", 5])
        elif self.paso_actual == 5:
            retorno.extend(["Maquina de Termofijado", 10])
        else:
            retorno.append("LISTO")

        self.ultimo_paso = retorno
        return retorno

    def realizar_paso(self, modista: Empleado) -> str:
        self.modista = modista
        probabilidad_de_exito = modista.get_pericia()
        if self.paso_actual == 2:
            probabilidad_de_exito *= 0.9
        elif self.paso_actual == 3:
            probabilidad_de_exito *= 0.8
        elif self.paso_actual == 5:
            probabilidad_de_exito *= 0.9

        retorno = "CONTINUAR"
        self.paso_actual += 1
        suerte = random.random()
        if self.paso_actual > 4:
            return "LISTO"
        if suerte > probabilidad_de_exito:
            retorno = "DESCARTAR"
            self.descartada = True
        return retorno

    @staticmethod
    def get_tipo_insumo() -> List[str]:
        return Camisa.tipo_insumo

    @staticmethod
    def get_cantidad_insumo() -> List[int]:
        return Camisa.cantidad_insumo

    @staticmethod
    def set_tipo_insumo(tipos: List[str]):
        Camisa.tipo_insumo = tipos

    @staticmethod
    def set_cantidad_insumo(cantidades: List[int]):
        Camisa.cantidad_insumo = cantidades

    @staticmethod
    def get_maquinaria_necesaria() -> List[str]:
        return Camisa.maquinaria_necesaria