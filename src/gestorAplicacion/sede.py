from .administracion.area import Area
from .fecha import Fecha
from .venta import Venta

class Sede:
    @staticmethod
    def get_lista_sedes():
        # Placeholder for actual implementation
        pass

    def getListaEmpleados(self):
        # Placeholder for actual implementation
        return self.listaEmpleados

    def get_rendimiento_deseado(self, area:Area, fecha: Fecha) -> float:
        rendimiento = 0.0; # Este valor siempre se va a retornar
        # Meramente que en este caso no es muy lejible poner returns dentro de la funcion.
        match area:
            case Area.DIRECCION:
                rendimiento = (3.0/5.0)*100.0;
            case Area.OFICINA:
                cantidadEmpleadosOficina = self.cantidad_por_area(Area.OFICINA)
                renidimento = len(Venta.filtrar(self.historialVentas, fecha))/cantidadEmpleadosOficina
            case Area.VENTAS:
                montoTotal = 0
                for venta in Venta.filtrar_por_fecha(self.historialVentas, fecha):
                    montoTotal += venta.monto_pagado
                cantidadVentas = Venta.filtrar(self.historialVentas, fecha)
                rendimiento = montoTotal/cantidadVentas
            case Area.CORTE:
                prendasProducidas = 0.0
                prendasDescartadas = 0.0

                for emp in self.getListaEmpleados():
                    prendasProducidas += emp.prendasProducidas
                    prendasDescartadas += emp.prendasDescartadas
                
                rendimiento = prendasProducidas/(prendasProducidas + prendasDescartadas)*0.9
        return rendimiento

    def cantidad_por_area(self, area_actual) -> int:
        cantidad = 0
        for emp in self.getListaEmpleados():
            if emp.area_actual == area_actual:
                cantidad +=1
        return cantidad

