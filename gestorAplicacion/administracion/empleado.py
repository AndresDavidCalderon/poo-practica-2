from ..fecha import Fecha
from ..sede import Sede

class Empleado:
    def __init__(self, nombre, area_actual, traslados, areas, sede):
        self.nombre = nombre
        self.area_actual = area_actual
        self.traslados = traslados
        self.areas = areas
        self.sede = sede

    def calcular_rendimiento(self, fecha: fecha) -> float:
        # Placeholder for actual implementation
        pass

def lista_inicial_despedir_empleado(fecha: fecha):
    lista_a_despedir = []
    mensajes = []
    retorno = [lista_a_despedir, mensajes]
    lista_a_transferir = [[] for _ in sede.get_lista_sedes()]

    for sede in Sede.get_lista_sedes():
        for emp in sede.get_lista_empleados():
            rendimiento = emp.calcular_rendimiento(fecha)
            se_va_a_despedir = False

            rendimiento_deseado = emp.sede.get_rendimiento_deseado(emp.area_actual, fecha)
            if rendimiento < rendimiento_deseado:
                se_va_a_despedir = True
                lista_a_despedir.append(emp)
                mensajes.append(f"El empleado {emp.nombre} tiene un rendimiento insuficiente, con un rendimiento de {rendimiento:.2f} y un rendimiento deseado de {rendimiento_deseado:.2f}")

            if se_va_a_despedir and sede.cantidad_por_area(emp.area_actual) == 1:
                for idx_sede, sede_destino in enumerate(sede.get_lista_sedes()):
                    if sede_destino.get_rendimiento_deseado(emp.area_actual, fecha) <= rendimiento + 20 and se_va_a_despedir:
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