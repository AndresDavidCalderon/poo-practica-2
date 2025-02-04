from ..fecha import Fecha
from ..sede import Sede
from ..venta import Venta
from .area import Area

class Empleado:
    def __init__(self, nombre, area_actual, traslados, areas, sede):
        self.nombre = nombre
        self.area_actual = area_actual
        self.traslados = traslados
        self.areas = areas
        self.sede = sede


    def calcular_rendimiento(self, fecha: Fecha) -> float:
        rendimiento = 0
        match self.area_actual:
            case Area.CORTE:
                if self.prendas_descartadas == 0:
                    rendimiento = 100
                else:
                    rendimiento = (self.prendas_producidas / self.prendas_descartadas) * 100
            case Area.VENTAS:
                ventas_asesoradas = Venta.filtrar_por_mes(Venta.filtrar_por_empleado(self.sede.historial_ventas, self),fecha)
                if ventas_asesoradas:
                    rendimiento = Venta.acumulado(ventas_asesoradas) / len(ventas_asesoradas)
                else:
                    rendimiento = 0
            case Area.OFICINA:
                acumulado_ventas_sede = sum(venta.valor for venta in self.sede.historial_ventas if venta.fecha <= fecha)
                promedio_ventas_sede = acumulado_ventas_sede / self.sede.cantidad_por_area('Oficina')
                ventas_encargadas = sum(venta.valor for venta in self.ventas_encargadas if venta.fecha <= fecha)
                rendimiento = (ventas_encargadas / promedio_ventas_sede) * 100
            case Area.DIRECCION:

                balances_positivos = sum(1.0 for evaluacion in self.evaluaciones if evaluacion.balance > 0)
                balances_negativos = sum(1.0 for evaluacion in self.evaluaciones if evaluacion.balance <= 0)
                if balances_negativos + balances_positivos == 0:
                    rendimiento = 100
                else:
                    rendimiento = (balances_positivos / (balances_negativos + balances_positivos)) * 100
        
        return rendimiento

    # Parte de la interacción 1 de gestion humana
    @classmethod
    def lista_inicial_despedir_empleado(cls, fecha: Fecha):
        lista_a_despedir = []
        mensajes = []
        retorno = [lista_a_despedir, mensajes]
        lista_a_transferir = [[] for _ in sede.get_lista_sedes()]

        for sede in Sede.get_lista_sedes():
            for emp in sede.get_lista_empleados():
                rendimiento = emp.calcular_rendimiento(Fecha)
                se_va_a_despedir = False

                rendimiento_deseado = emp.sede.get_rendimiento_deseado(emp.area_actual, Fecha)
                if rendimiento < rendimiento_deseado:
                    se_va_a_despedir = True
                    lista_a_despedir.append(emp)
                    mensajes.append(f"El empleado {emp.nombre} tiene un rendimiento insuficiente, con un rendimiento de {rendimiento:.2f} y un rendimiento deseado de {rendimiento_deseado:.2f}")

                if se_va_a_despedir and sede.cantidad_por_area(emp.area_actual) == 1:
                    for idx_sede, sede_destino in enumerate(sede.get_lista_sedes()):
                        if sede_destino.get_rendimiento_deseado(emp.area_actual, Fecha) <= rendimiento + 20 and se_va_a_despedir:
                            mensajes.append(f"El empleado {emp.nombre} ha sido transferido a la sede {sede_destino.nombre}")
                            lista_a_despedir.remove(emp)
                            lista_a_transferir[idx_sede].append(emp)
                            se_va_a_despedir = False

                if se_va_a_despedir and emp.area_actual != 'Corte' and emp.traslados < 2 and sede.cantidad_por_area(emp.area_actual) != 1:
                    puede_cambiar_area = True
                    for area_pasada in emp.areas:
                        if area_pasada > emp.area_actual:
                            puede_cambiar_area = False
                            break

        return retorno