from src.gestorAplicacion.administracion.deuda import Deuda
from src.gestorAplicacion.bodega.prenda import Prenda
from gestorAplicacion import Persona, Sede,Fecha, Venta
from src.gestorAplicacion.administracion import Empleado,Area, Rol, EvaluacionFinanciera

import locale
from typing import List

locale.setlocale(locale.LC_ALL, 'es_ES')
comparador = locale.strxfrm

class Main:
    if __name__ == "__main__":
        print("Ecomoda a la orden, presiona enter para continuar")
        input()
        while True:
            print("1. Despedir/Transferir/Contratar empleados")
            print("2. Adquirir insumos para la produccion")
            print("3, Ver el desglose economico de la empresa")
            print("4. Vender un producto")
            print("5. Producir prendas")
            print("6. Salir")
            option = input("Selecciona una opción: ")
            if option.isdigit():
                match option:
                    case "1":
                        print("Despedir/Transferir/Contratar empleados")
                    case "2":
                        print("Adquirir insumos para la produccion")
                    case "3":
                        print("Ver el desglose economico de la empresa")
                    case "4":
                        print("Vender un producto")
                    case "5":
                        print("Producir prendas")
                    case "6":
                        quit()
            else:
                print("Por favor selecciona una opción válida")

    def ingresar_fecha():
        dia = -1
        mes = -1
        while dia <= 0 or dia > 31:
            dia = int(input("Ingrese día: "))
            while mes <= 0 or mes > 12:
                mes = int(input("Ingrese mes: "))
        año = int(input("Ingrese año: "))
        fecha = Fecha(dia, mes, año)
        return fecha
    
    def avisar_falta_de_insumos(sede, fecha, tipo_prenda):
        print(f"No se pudo producir {tipo_prenda} en la sede {sede.get_nombre()} por falta de insumos en la fecha {fecha}.")
        print(f"Hasta el momento se ha usado {Prenda.get_cantidad_tela_ultima_produccion()} en tela.")

    def despedir_empleados(fecha):
        print("Obteniendo lista sugerida de empleados")
        info_despidos : List[List] = Empleado.lista_inicial_despedir_empleado(fecha)
        a_despedir = info_despidos[0]
        mensajes = info_despidos[1]

        for mensaje in mensajes:
            print(mensaje)

        print("\nEsta es una lista de empleados que no estan rindiendo correctamente, ¿que deseas hacer?")

        diferencia_salarios -= Persona.diferencia_salarios()
        if diferencia_salarios > 0:
            print(f"Tus empleados estan {diferencia_salarios:,} sobre el promedio de salarios")
        elif diferencia_salarios < 0:
            print(f"Tus empleados estan {diferencia_salarios:,} bajo el promedio de salarios")
        else:
            print("Tus empleados estan en el promedio de salarios")

        for emp in a_despedir:
            print(f"Nombre: {emp.get_nombre()}, Área: {emp.get_area_actual()}, Documento: {emp.get_documento()}")

        opcion = 2
        while opcion == 2:
            print("1. Elegir a los despedidos")
            print("2. Añadir a alguien más")
            opcion = Main.next_int_seguro()
            if opcion == 2:
                print("¿De que sede quieres añadir al empleado?")
                for i , sede in enumerate(Sede.get_lista_sedes()):
                    print(f"{i}. {sede.get_nombre()}")
                sede = Main.next_int_seguro()
                print("¿Que empleado quieres despedir? Pon su nombre completo o documento, esto lo añadirá a la lista de despedibles.")
                for emp in Sede.get_lista_sedes()[sede].get_lista_empleados():
                    print(f"{emp.get_nombre()} {emp.get_area_actual()} {emp.get_documento()}")
                nombre = input().strip()
                for emp in Sede.get_lista_sedes().get(sede).get_lista_empleados():
                    if emp.get_nombre() == nombre or (nombre.isdigit() and emp.get_documento() == int(nombre)):
                        a_despedir.append(emp)

        seleccion = []
        print("¿Que empleados quieres despedir? Pon su nombre completo, documento o FIN para terminar.")
        for emp in a_despedir:
            print(f"{emp.get_nombre()} {emp.get_area_actual()} {emp.get_documento()}")
        nombre = input().strip()
        while nombre.lower() != "fin":
            for emp in a_despedir:
                if emp.get_nombre() == nombre or (nombre.isdigit() and emp.get_documento() == int(nombre)):
                    seleccion.append(emp)
            nombre = input().strip()

        print("Despidiendo empleados...")
        Empleado.despedir_empleados(seleccion, True, fecha)
        print("Listo!")
        return seleccion

    def reorganizar_empleados(despedidos: List[Empleado]):
        print(f"Todavía nos quedan {len(despedidos)} empleados por reemplazar, revisamos la posibilidad de transferir empleados.")
        necesidades = Sede.obtener_necesidad_transferencia_empleados(despedidos)
        
        # Desempacamos los datos dados por GestorAplicacion
        roles_a_transferir = necesidades[0]
        transferir_de = necesidades[1]
        a_contratar = necesidades[2]

        # Lista de empleados a transferir de sede, seleccionados por el usuario.
        a_transferir = []

        for rolidx in range(len(roles_a_transferir)):
            rol = roles_a_transferir[rolidx]
            sede = transferir_de[rolidx]
            print(f"Se necesita transferir {rol} de {sede.get_nombre()}, estos son los candidatos: Ingresa su nombre completo para hacerlo.")
            
            for emp in sede.get_lista_empleados():
                if emp.get_rol() == rol:
                    descripcion = f"Nombre: {emp.get_nombre()}, Documento: {emp.get_documento()}"
                    if emp.get_rol() == Rol.VENDEDOR:
                        descripcion += f", Ventas asesoradas: {Venta.acumulado_ventas_asesoradas(emp)}"
                    elif emp.get_rol() == Rol.MODISTA:
                        descripcion += f", Pericia: {emp.get_pericia()}"
                    else:
                        descripcion += f", contratado en {emp.get_fecha_contratacion()}"
                    print(descripcion)

            # Obtenemos la cantidad de empleados a seleccionar
            cantidad = sum(1 for emp in despedidos if emp.get_rol() == rol)
            for _ in range(cantidad):
                nombre = input().strip()
                for emp in sede.get_lista_empleados():
                    if comparador.compare(emp.get_nombre(), nombre) == 0:
                        a_transferir.append(emp)

        Sede.reemplazar_por_cambio_sede(despedidos, a_transferir)

        return a_contratar

    def contratar_empleados(a_reemplazar: List[Empleado], in_stream, fecha: Fecha):
        elecciones = Persona.entrevistar(a_reemplazar)
        aptos = elecciones[0]
        roles_a_reemplazar = elecciones[1]
        cantidad = elecciones[2]

        a_contratar = []
        for i in range(len(roles_a_reemplazar)):
            rol = roles_a_reemplazar[i]
            cantidad_necesaria = cantidad[i]

            print(f"Se necesitan {cantidad_necesaria} {rol}s, estos son los candidatos:")

            for persona in aptos:
                if persona.get_rol() == rol:
                    print(f"Nombre: {persona.get_nombre()}, Documento: {persona.get_documento()}, con {persona.get_experiencia()} años de experiencia.")

            print("Ingresa el nombre de los que quieres contratar.")

            for cantidad_contratada in range(cantidad_necesaria):
                nombre = in_stream.readline().strip()
                for persona in aptos:
                    if comparador.compare(persona.get_nombre(), nombre) == 0:
                        a_contratar.append(persona)
                        print(f"Seleccionaste a {persona.get_nombre()} con {persona.calcular_salario() - persona.valor_esperado_salario()} de diferencia salarial sobre el promedio")

        Persona.contratar(a_contratar, a_reemplazar, fecha)

    def error_de_reemplazo(persona):
        print(f"No se pudo contratar a {persona.get_nombre()}, no sabemos a quien reemplaza.")

    def calcular_balance_anterior(fecha):
        print("\nObteniendo balance entre Ventas y Deudas para saber si las ventas cubren los gastos de la producción de nuestras prendas...")
        balance_costos_produccion = Venta.calcular_balance_venta_produccion(fecha)
        eleccion = 0
        while eleccion <= 0 or eleccion > 3:
            print("\nIngrese las deudas que quiere calcular")
            print("Ingrese 1 para proveedor, 2 para Banco o 3 para ambos")
            eleccion = Main.next_int_seguro()
        
        deuda_calculada = Deuda.calcular_deuda_mensual(fecha, eleccion)
        balance_total = balance_costos_produccion - deuda_calculada
        empleado = None
        elegible_empleados = []
        
        for empleado_actual in Sede.get_lista_empleados_total():
            if empleado_actual.get_area_actual() == Area.DIRECCION:
                elegible_empleados.append(empleado_actual)
        
        indice_empleado = -1
        while indice_empleado < 0 or indice_empleado >= len(elegible_empleados):
            for indice, empleado_en_lista in enumerate(elegible_empleados):
                print(f"{indice} {empleado_en_lista}")
            print(f"\nIngrese número de 0 a {len(elegible_empleados) - 1} según el Directivo que escoja para registrar el balance")
            indice_empleado = Main.next_int_seguro()
            empleado = elegible_empleados[indice_empleado]
        
        nuevo_balance = EvaluacionFinanciera(balance_total, empleado)
        return nuevo_balance

    # Interaccion 2 Sistema Financiero
    def calcular_estimado(fecha, balance_anterior):
        print("\nCalculando estimado entre Ventas y Deudas para ver el estado de endeudamiento de la empresa...")
        porcentaje = -1.0
        while porcentaje < 0.0 or porcentaje > 1:
            print("\nIngrese porcentaje a modificar para fidelidad de los clientes sin membresía, entre 0% y 100%")
            porcentaje = Main.next_int_seguro() / 100.0
        
        diferencia_estimado = EvaluacionFinanciera.estimado_ventas_gastos(fecha, porcentaje, balance_anterior)
        # Un mes se puede dar por salvado si el 80% de los gastos se pueden ver
        # cubiertos por las ventas predichas
        return diferencia_estimado



    def next_int_seguro():
        while True:
            respuesta = input()
            if respuesta.isdigit():
                return int(respuesta)
            else:
                print("Por favor ingrese un número entero")