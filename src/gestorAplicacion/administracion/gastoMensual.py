from abc import abstractmethod

from src.gestorAplicacion.administracion.empleado import Empleado
from src.gestorAplicacion.bodega.insumo import Insumo
from src.gestorAplicacion.bodega.maquinaria import Maquinaria

class GastoMensual:
    
    @abstractmethod
    def calcular_gasto_mensual(self):
        pass

    def gasto_mensual_tipo(self, fecha, fecha_objeto, objeto):
        gasto_actual = 0
        gasto_pasado = 0
        gasto_total = [0, 0]
        
        if fecha_objeto.get_año() == fecha.get_año():
            if fecha_objeto.get_mes() == fecha.get_mes():
                gasto_actual += objeto.calcular_gasto_mensual()
                gasto_total[0] = gasto_actual
            if fecha_objeto.get_mes() == fecha.get_mes() - 1:
                gasto_pasado += objeto.calcular_gasto_mensual()
                gasto_total[1] = gasto_pasado
        
        return gasto_total

    @staticmethod
    def gastos_mensuales(fecha):
        gastos_maquinaria = Maquinaria.gasto_mensual_clase(fecha)
        gastos_nomina = Empleado.gasto_mensual_clase()
        gasto_bolsa = Insumo.gasto_mensual_clase(fecha)
        suma = gastos_maquinaria + gastos_nomina + gasto_bolsa
        return suma