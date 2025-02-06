from enum import Enum

from src.gestorAplicacion.venta import Venta

class Area(Enum):
    DIRECCION = ["computador","impresora"]
    OFICINA = ["computador","registradora"]
    VENTAS = ["escaner"]
    CORTE = ["maquina de coser","maquina de corte","plancha industrial"]
    
    @classmethod
    def rendimientoDeseadoActual(sede, fecha):
        rendimiento_sede = []
        for area in Area:
            if area == Area.DIRECCION:
                area.rendimientoDeseado = (3 / 5.0) * 100
            elif area == Area.OFICINA:
                cantidadEmpleadosOfi = sede.cantidadPorArea(Area.OFICINA)
                area.rendimientoDeseado = float(len(Venta.filtrar(sede.getHistorialVentas(), fecha))) / cantidadEmpleadosOfi  # Cantidad de ventas por empleado de oficina
            elif area == Area.VENTAS:
                montoTotal = 0
                for venta in Venta.filtrar(sede.getHistorialVentas(), fecha):
                    montoPagado = venta.getMontoPagado()
                    montoTotal += montoPagado
                cantidadVentas = len(Venta.filtrar(sede.getHistorialVentas(), fecha))
                area.rendimientoDeseado = (montoTotal / cantidadVentas) * 0.8
            elif area == Area.CORTE:
                prendasDescartadas = 0
                prendasProducidas = 0

                for empleado in sede.get_lista_empleados():
                    prendasDescartadas += empleado.getPrendasDescartadas()
                    prendasProducidas += empleado.getPrendasProducidas()

                area.rendimientoDeseado = (float(prendasProducidas) / (prendasDescartadas + prendasProducidas)) * 90

            rendimiento_sede.append(area.rendimientoDeseado)

        return rendimiento_sede
    