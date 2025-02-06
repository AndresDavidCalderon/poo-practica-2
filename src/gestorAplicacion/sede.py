from .administracion.area import Area
from .fecha import Fecha
from .venta import Venta
from .bodega.maquinaria import Maquinaria
from typing import List

class Sede:
    lista_sedes = []
    def __init__(self):
        Sede.set_lista_sedes(self)
        
    @staticmethod
    def set_lista_sedes(sede: Sede):
        Sede.lista_sedes.append(sede)

    @staticmethod
    def get_lista_sedes():
        return Sede.lista_sedes

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

                                    #PARA LA INTERACCION 2 DE PRODUCCION
    def sobre_cargada(self, fecha: 'Fecha') -> int:
        senal = 0
        produccion_sedes = self.calc_produccion_sedes(fecha)
        modistas = self.modistas_que_hay()

        if modistas[0] > 0 and ((produccion_sedes[0][0] + produccion_sedes[0][1]) / modistas[0]) > 10:
            senal = 5
        if modistas[1] > 0 and ((produccion_sedes[1][0] + produccion_sedes[1][1]) / modistas[1]) > 10:
            senal += 10

        return senal
    
    def calc_produccion_sedes(self, fecha: 'Fecha') -> List[List[int]]:
        prod_sedes_calculada = []
        prod_calculada_sede_p = []
        prod_calculada_sede_2 = []

        prod_calculada_sede_p.append(Venta.predecir_ventas(fecha, Sede.get_lista_sedes()[0], "Pantalon"))
        prod_calculada_sede_p.append(Venta.predecir_ventas(fecha, Sede.get_lista_sedes()[0], "Camisa"))

        prod_calculada_sede_2.append(Venta.predecir_ventas(fecha, Sede.get_lista_sedes()[1], "Pantalon"))
        prod_calculada_sede_2.append(Venta.predecir_ventas(fecha, Sede.get_lista_sedes()[1], "Camisa"))

        prod_sedes_calculada.append(prod_calculada_sede_p)
        prod_sedes_calculada.append(prod_calculada_sede_2)

        return prod_sedes_calculada

    def prod_sede_p(self, fecha: 'Fecha') -> List[int]:
        pantalones_sede_p = self.calc_produccion_sedes(fecha)[0][0] + self.calc_produccion_sedes(fecha)[1][0]
        camisas_sede_p = self.calc_produccion_sedes(fecha)[0][1] + self.calc_produccion_sedes(fecha)[1][1]

        prod_aproximada = [pantalones_sede_p, camisas_sede_p]
        return prod_aproximada

    def prod_sede_2(self, fecha: 'Fecha') -> List[int]:
        pantalones_sede_2 = self.calc_produccion_sedes(fecha)[1][0]
        camisas_sede_2 = self.calc_produccion_sedes(fecha)[1][1]

        prod_aproximada = [pantalones_sede_2, camisas_sede_2]
        return prod_aproximada

    def modistas_que_hay(self) -> List[int]:
        modistas_en_cada_sede = [0, 0]

        for emp_creados in self.lista_empleados_total:
            if emp_creados.get_area_actual().get_nombre().lower() == "corte":
                if emp_creados.get_sede().get_nombre().lower() == "sede principal":
                    modistas_en_cada_sede[0] += 1
                elif emp_creados.get_sede().get_nombre().lower() == "sede 2":
                    modistas_en_cada_sede[1] += 1

        return modistas_en_cada_sede

    def prod_transferida1(self, fecha) -> List[int]:
        produccion_sedes = self.calc_produccion_sedes(fecha)
        return [produccion_sedes[1][0], produccion_sedes[1][1]]

    def prod_transferida2(self, fecha) -> List[int]:
        produccion_sedes = self.calc_produccion_sedes(fecha)
        return [produccion_sedes[0][0], produccion_sedes[0][1]]

    def plan_produccion(self, maq_disponible: List['Maquinaria'], fecha: 'Fecha', scanner: 'int') -> List[List[List[int]]]:
        a_producir_final = []
        a_producir = []
        lista_espera = []

        lista_espera_vacia = []
        lista_de_ceros = [0, 0]
        maq_sede_p = []
        maq_sede_2 = []
        senal = 0

        lista_espera_vacia.append(lista_de_ceros)
        lista_espera_vacia.append(lista_de_ceros)

        # Dividir las máquinas disponibles por sedes
        for tod_maquinas in maq_disponible:
            if tod_maquinas.get_sede().get_nombre().lower() == "sede principal":
                maq_sede_p.append(tod_maquinas)
            else:
                maq_sede_2.append(tod_maquinas)

        # Dividir las máquinas de cada sede por función
        for tod_maq_sede_p in maq_sede_p:
            if tod_maq_sede_p.es_de_produccion():
                Sede.get_lista_sedes()[0].maq_produccion.append(tod_maq_sede_p)
            else:
                Sede.get_lista_sedes()[0].maq_oficina.append(tod_maq_sede_p)

        for tod_maq_sede_2 in maq_sede_2:
            if tod_maq_sede_2.es_de_produccion():
                Sede.get_lista_sedes()[1].maq_produccion.append(tod_maq_sede_2)
            else:
                Sede.get_lista_sedes()[1].maq_oficina.append(tod_maq_sede_2)

        if len(Sede.get_lista_sedes()[0].maq_produccion) >= 3:
            senal = 5
        if len(Sede.get_lista_sedes()[1].maq_produccion) >= 3:
            senal += 10

        if senal == 5:
            Main.prints_int_2(1)
            opcion = 0
            while opcion not in [1, 2]:
                opcion = scanner.next_int()
                if opcion == 1:
                    a_producir.append(self.prod_sede_p(fecha))
                    a_producir.append(lista_de_ceros)

                    a_producir_final.append(a_producir)
                    a_producir_final.append(lista_espera_vacia)
                elif opcion == 2:
                    a_producir.append(self.calc_produccion_sedes(fecha)[0])
                    a_producir.append(lista_de_ceros)

                    lista_espera.append(self.prod_transferida_1(fecha))
                    lista_espera.append(lista_de_ceros)

                    a_producir_final.append(a_producir)
                    a_producir_final.append(lista_espera)
                else:
                    Main.prints_int_2(2)
        
        elif senal == 10:
            Main.prints_int2(3)

            opcion = 0
            while opcion not in [1, 2]:
                opcion = int(input())

                if opcion == 1:
                    # Producir todo en la sede 2
                    a_producir = [[0, 0], self.prod_sede2(fecha)]
                    a_producir_final = [a_producir, []]

                elif opcion == 2:
                    # Pasar producción a lista de espera
                    a_producir = [[0, 0], self.calc_produccion_sedes(fecha)[1]]
                    lista_espera = [[0, 0], self.prod_transferida2(fecha)]
                    a_producir_final = [a_producir, lista_espera]

                else:
                    Main.prints_int2(4)

        elif senal == 15:
            # Se produce todo entre las dos sedes
            senal_rec = self.sobre_cargada(fecha)

            if senal_rec == 5:
                Main.prints_int2(5)

                opciom = 0
                while opciom not in [1, 2]:
                    opciom = int(input())

                    if opciom == 1:
                        nuevos_pant_p = self.calc_produccion_sedes(fecha)[0][0] + -(- (self.calc_produccion_sedes(fecha)[0][0] + self.calc_produccion_sedes(fecha)[1][0]) // 2)
                        nuevos_pant_2 = self.calc_produccion_sedes(fecha)[1][0] + ((self.calc_produccion_sedes(fecha)[0][0] + self.calc_produccion_sedes(fecha)[1][0]) // 2)

                        nuevas_cam_p = self.calc_produccion_sedes(fecha)[0][1] + -(- (self.calc_produccion_sedes(fecha)[0][1] + self.calc_produccion_sedes(fecha)[1][1]) // 2)
                        nuevas_cam_2 = self.calc_produccion_sedes(fecha)[1][1] + ((self.calc_produccion_sedes(fecha)[0][1] + self.calc_produccion_sedes(fecha)[1][1]) // 2)

                        lo_de_la_p = [nuevos_pant_p, nuevas_cam_p]
                        lo_de_la_2 = [nuevos_pant_2, nuevas_cam_2]

                        a_producir = [lo_de_la_p, lo_de_la_2]
                        a_producir_final = [a_producir, []]

                    elif opciom == 2:
                        a_producir = self.calc_produccion_sedes(fecha)
                        a_producir_final = [a_producir, []]

                    else:
                        Main.prints_int2(6)

            elif senal_rec == 10:
                Main.prints_int2(7)

                opciom = 0
                while opciom not in [1, 2]:
                    opciom = int(input())

                    if opciom == 1:
                        nuevos_pant_p = self.calc_produccion_sedes(fecha)[0][0] + ((self.calc_produccion_sedes(fecha)[0][0] + self.calc_produccion_sedes(fecha)[1][0]) // 2)
                        nuevos_pant_2 = self.calc_produccion_sedes(fecha)[1][0] + -(- (self.calc_produccion_sedes(fecha)[0][0] + self.calc_produccion_sedes(fecha)[1][0]) // 2)

                        nuevas_cam_p = self.calc_produccion_sedes(fecha)[0][1] + ((self.calc_produccion_sedes(fecha)[0][1] + self.calc_produccion_sedes(fecha)[1][1]) // 2)
                        nuevas_cam_2 = self.calc_produccion_sedes(fecha)[1][1] + -(- (self.calc_produccion_sedes(fecha)[1][1] + self.calc_produccion_sedes(fecha)[0][1]) // 2)

                        lo_de_la_p = [nuevos_pant_p, nuevas_cam_p]
                        lo_de_la_2 = [nuevos_pant_2, nuevas_cam_2]

                        a_producir = [lo_de_la_p, lo_de_la_2]
                        a_producir_final = [a_producir, []]

                    elif opciom == 2:
                        a_producir = self.calc_produccion_sedes(fecha)
                        a_producir_final = [a_producir, []]

                    else:
                        Main.prints_int2(8)

            elif senal_rec == 15:
                Main.prints_int2(9)

                opciom = 0
                while opciom not in [1, 2]:
                    opciom = int(input())

                    if opciom == 1:
                        p_sede_p_espera = max(0, self.calc_produccion_sedes(fecha)[0][0] - 10 * self.modistas_que_hay()[0])
                        p_sede_p = self.calc_produccion_sedes(fecha)[0][0] - p_sede_p_espera

                        c_sede_p_espera = max(0, self.calc_produccion_sedes(fecha)[0][1] - 10 * self.modistas_que_hay()[0])
                        c_sede_p = self.calc_produccion_sedes(fecha)[0][1] - c_sede_p_espera

                        p_sede_2_espera = max(0, self.calc_produccion_sedes(fecha)[1][0] - 10 * self.modistas_que_hay()[1])
                        p_sede_2 = self.calc_produccion_sedes(fecha)[1][0] - p_sede_2_espera

                        c_sede_2_espera = max(0, self.calc_produccion_sedes(fecha)[1][1] - 10 * self.modistas_que_hay()[1])
                        c_sede_2 = self.calc_produccion_sedes(fecha)[1][1] - c_sede_2_espera

                        el_guarda_p_de_hoy = [p_sede_p, c_sede_p]
                        el_guarda_2_de_hoy = [p_sede_2, c_sede_2]
                        el_guarda_p_de_manana = [p_sede_p_espera, c_sede_p_espera]
                        el_guarda_2_de_manana = [p_sede_2_espera, c_sede_2_espera]

                        a_producir = [el_guarda_p_de_hoy, el_guarda_2_de_hoy]
                        lista_espera = [el_guarda_p_de_manana, el_guarda_2_de_manana]
                        a_producir_final = [a_producir, lista_espera]

                    elif opciom == 2:
                        a_producir = self.calc_produccion_sedes(fecha)
                        a_producir_final = [a_producir, []]

                    else:
                        Main.prints_int2(10)

            elif senal_rec == 0:
                a_producir = self.calc_produccion_sedes(fecha)
                a_producir_final = [a_producir, []]

        else:
            Main.prints_int2(11)

        return a_producir_final

    