from ..gestorAplicacion.administracion import Empleado
from ..gestorAplicacion import Persona, Sede
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

    def planRecuperacion(estimated_difference, date, input_scanner):
        if estimated_difference > 0:
            print("\nEl estimado es positivo, las ventas superan las deudas")
            print("Hay dinero suficiente para hacer el pago de algunas Deudas")
            Deuda.compare_debts(date)
        elif estimated_difference <= 0:
            print("\nEl estimado es negativo, la deuda supera las ventas")
            print("No hay Dinero suficiente para cubrir los gastos de la empresa, tendremos que pedir un préstamo")
            index = -1
            bank_name = None
            while index < 0 or index >= len(Banco.get_bank_list()):
                for bank in Banco.get_bank_list():
                    print(bank)
                print("\nIngrese número de 0 a " + str(len(Banco.get_bank_list()) - 1) + " para solicitar el prestamo al Banco de su elección")
                index = next_safe_int(input_scanner)
                bank_name = Banco.get_bank_list()[index].get_entity_name()
            
            installments = 0
            while installments <= 0 or installments > 18:
                print("Ingrese número de 1 a 18 para las cuotas en que se dividirá la deuda")
                installments = next_safe_int(input_scanner)
            
            debt_to_acquire = Deuda(date, estimated_difference, bank_name, "Banco", installments)
        
        print("\nAnalizando posibilidad de hacer descuentos para subir las ventas...")
        discount = Venta.black_friday(date)
        black_friday_string = None
        if discount <= 0.0:
            black_friday_string = "El análisis de ventas realizado sobre el Black Friday arrojó que la audiencia no reacciona tan bien a los descuentos, \npropusimos no hacer descuentos"
            print("\nSegún las Ventas anteriores,  aplicar descuentos no funcionará")
        else:
            black_friday_string = "El análisis de ventas realizado sobre el Black Friday arrojó que la audiencia reacciona bien a los descuentos, \npropusimos un descuento del " + str(discount * 100) + "%"
            print("\nSegún las Ventas anteriores, aplicar descuentos si funcionará")
        
        print("¿Desea Cambiar el siguiente descuento: " + str(discount * 100) + "? marque 1 para Si, 2 para no ")
        choice = next_safe_int(input_scanner)
        new_discount = -0.1
        if choice == 1:
            while new_discount < 0.0 or new_discount > 0.5:
                print("Ingrese descuento entre 0% y 5%")
                new_discount = next_safe_int(input_scanner) / 100.0
        else:
            new_discount = discount
        
        Prenda.preventive_actions(discount, new_discount, date)
        future_analysis = "\n" + black_friday_string + ", sin embargo su desición fue aplicar un descuento de: " + str(new_discount * 100) + "%."
        return future_analysis
    
    def planificar_produccion(fecha):
        # lista_guia = []
        retorno = []

        for sede in Sede.get_lista_sedes():
            print("\n" + "Para la " + sede.get_nombre())
            print("Tenemos un porcentaje de pesimismo: " + str(round(Venta.get_pesimismo() * 100)) + "%")
            print("\n" + "Seleccione una de las siguientes opciones:")
            print("1. Estoy de acuerdo con el porcentaje de pesimismo")
            print("2. Deseo cambiar el porcentaje de pesimismo")

            opcion = next_int_seguro()
            if opcion == 1:
                pass
            elif opcion == 2:
                print("Ingrese el nuevo porcentaje de pesimismo % ")
                new_pesimismo = int(input())
                Venta.set_pesimismo(new_pesimismo / 100.0)
            else:
                print("Esa opción no es valida.")

            lista_x_sede = []
            insumo_x_sede = []
            cantidad_a_pedir = []
            pantalones_predichos = False
            camisas_predichas = False
            prediccion_p = 0
            prediccion_c = 0

            for prenda in sede.get_prendas_inventadas():
                if isinstance(prenda, Pantalon) and not pantalones_predichos:
                    proyeccion = Venta.predecir_ventas(fecha, sede, prenda.get_nombre())
                    prediccion_p = proyeccion * (1 - Venta.get_pesimismo())
                    print("\n" + "La predicción de ventas para " + str(prenda) + " es de " + str(math.ceil(prediccion_p)))

                    for insumo in prenda.get_insumo():
                        insumo_x_sede.append(insumo)
                    for cantidad in Pantalon.get_cantidad_insumo():
                        cantidad_a_pedir.append(int(math.ceil(cantidad * prediccion_p)))
                    pantalones_predichos = True
                
                if isinstance(prenda, Camisa) and not camisas_predichas:
                    proyeccion = Venta.predecir_ventas(fecha, sede, prenda.get_nombre())
                    prediccion_c = proyeccion * (1 - Venta.get_pesimismo())

                    print("\n" + "La predicción de ventas para " + str(prenda) + " es de " + str(math.ceil(prediccion_c)))

                    for i in range(len(prenda.get_insumo())):
                        insumo = prenda.get_insumo()[i]
                        cantidades_por_prenda = Camisa.get_cantidad_insumo()
                        cantidad = int(math.ceil(cantidades_por_prenda[i] * prediccion_c))

                        index = insumo_x_sede.index(insumo) if insumo in insumo_x_sede else -1
                        if index == -1:
                            insumo_x_sede.append(insumo)
                            cantidad_a_pedir.append(cantidad)
                        else:
                            cantidad_a_pedir[index] += cantidad
                    camisas_predichas = True

            lista_x_sede.append(insumo_x_sede)
            lista_x_sede.append(cantidad_a_pedir)
            retorno.append(lista_x_sede)

        return retorno
    
    def coordinar_bodegas(retorno):
        lista_x_sede = []  # Lista extraida de retorno
        lista_insumos = []  # Extraida de listaXSede
        lista_cantidades = []  # Extraida de listaXSede
        lista_a = []

        for sede in retorno:
            insumos_a_pedir = []
            cantidad_a_pedir = []  # Ambas calculadas en este bucle
            lista_sede = []  # Acumula la info de este bucle.
            
            # Convertir cada elemento en una lista correspondiente a una sede
            lista_x_sede = sede

            # Extraer las listas internas: insumos y cantidades
            lista_insumos = lista_x_sede[0]
            lista_cantidades = lista_x_sede[1]

            for s in Sede.get_lista_sedes():
                for i in lista_insumos:
                    producto_en_bodega = Sede.verificar_producto_bodega(i, s)
                    idx_insumo = lista_insumos.index(i)
                    if producto_en_bodega.get_encontrado() == True:
                        lista_cantidades[idx_insumo] = max(lista_cantidades[idx_insumo] - s.get_cantidad_insumos_bodega()[producto_en_bodega.get_index()], 0)  # Quitamos la cantidad de insumos que ya tenemos
                        # Evitamos restar insumos si ya hay suficiente.

                    cantidad_necesaria = lista_cantidades[lista_insumos.index(i)]
                    producto_en_otra_sede = Sede.verificar_producto_otra_sede(i)
                    if producto_en_otra_sede.get_encontrado() == True:
                        print("\n" + "Tenemos el insumo " + i.get_nombre() + " en nuestra " + producto_en_otra_sede.get_sede() + ".")
                        print("El insumo tiene un costo de " + str(producto_en_otra_sede.get_precio()))
                        print("\n" + "Seleccione una de las siguientes opciones:")
                        print("1. Deseo transferir el insumo desde la " + producto_en_otra_sede.get_sede())
                        print("2. Deseo comprar el insumo")

                        opcion = next_int_seguro()  # Assumes this function exists
                        if opcion == 1:
                            restante = Sede.transferir_insumo(i, s, producto_en_otra_sede.get_sede(), cantidad_necesaria)
                            print("\n" + str(i) + " transferido desde " + str(s) + " con éxito")
                            if restante != 0:
                                insumos_a_pedir.append(i)
                                cantidad_a_pedir.append(restante)
                                if i.get_nombre() == "Tela":
                                    print("\n" + "Tenemos una cantidad de " + str(restante) + "cm de tela restantes a pedir ")
                                elif i.get_nombre() == "Boton":
                                    print("\n" + "Tenemos una cantidad de " + str(restante) + " botones restantes a pedir ")
                                elif i.get_nombre() == "Cremallera":
                                    print("\n" + "Tenemos una cantidad de " + str(restante) + " cremalleras restantes a pedir ")
                                else:
                                    print("\n" + "Tenemos una cantidad de " + str(restante) + " cm de hilo restantes a pedir ")
                            else:
                                print("Insumo transferido en su totalidad")
                        elif opcion == 2:
                            insumos_a_pedir.append(i)
                            cantidad_a_pedir.append(cantidad_necesaria)
                        else:
                            print("Esa opción no es valida.")

                lista_sede.append(insumos_a_pedir)
                lista_sede.append(cantidad_a_pedir)
                lista_a.append(lista_sede)

        return lista_a

    def comprar_insumos(fecha: Any, lista_a: List[List[Any]]) -> str:
        sede = []
        insumos = []
        cantidad = []
        proveedores = []
        precios = []
        deudas = []
        
        # Itera por sedes.
        for s in lista_a:
            sede = s
            insumos = sede[0]
            cantidad = sede[1]

            for sedee in Sede.get_lista_sedes():
                for idx_insumo in range(len(insumos)):
                    mejor_proveedor = None
                    mejor_precio = float('inf')
                    cantidad_añadir = 0

                    for proveedor in Proveedor.get_lista_proveedores():
                        if proveedor.get_insumo() == insumos[idx_insumo]:
                            proveedores.append(proveedor)
                            precios.append(Proveedor.costo_de_la_cantidad(insumos[idx_insumo], cantidad[idx_insumo]))

                    for x in proveedores:
                        precio = x.costo_de_la_cantidad(insumos[idx_insumo], cantidad[idx_insumo])
                        if precio != 0 and precio < mejor_precio:
                            mejor_precio = precio
                            mejor_proveedor = x
                            insumos[idx_insumo].set_proveedor(x)

                    print(f"\nTenemos el insumo {insumos[idx_insumo].get_nombre()} con nuestro proveedor {insumos[idx_insumo].get_proveedor().get_nombre()}.")

                    if insumos[idx_insumo].get_precio_individual() < insumos[idx_insumo].get_ultimo_precio():
                        print(f"\nDado que el costo de la venta por unidad es menor al último precio por el que compramos el insumo")
                        print(f"\nDesea pedir más de la cantidad necesaria para la producción? ")
                        print(f"Cantidad: {cantidad[idx_insumo]}")
                        print("1. Si")
                        print("2. No")

                        opcion = next_int_seguro()
                        if opcion == 1:
                            if opcion >= 0:
                                print(f"\n¿Cuánta cantidad más desea pedir del insumo {insumos[idx_insumo].get_nombre()}?")
                                cantidad_añadir = int(input())
                            else:
                                print("Esa opción no es válida.")
                        elif opcion == 2:
                            pass
                        else:
                            print("Esa opción no es válida.")
                    
                    cantidad[idx_insumo] += cantidad_añadir  # Por si el usuario añade extra.

                    Sede.añadir_insumo(insumos[idx_insumo], sedee, cantidad[idx_insumo])
                    print(f"\nInsumo {insumos[idx_insumo]} comprado con éxito")

                    for proveedor in Proveedor.get_lista_proveedores():
                        monto_deuda = 0
                        if insumos[idx_insumo].get_proveedor().get_nombre() == proveedor.get_nombre():
                            monto_deuda += insumos[idx_insumo].get_precio_individual() * cantidad[idx_insumo]
                        deuda = None
                        if monto_deuda > 0:
                            if proveedor.get_deuda() is None:
                                deuda = Deuda(fecha, monto_deuda, proveedor.get_nombre(), "Proveedor",
                                            Deuda.calcular_cuotas(monto_deuda))
                            elif not proveedor.get_deuda().get_estado_de_pago():
                                proveedor.unificar_deudas_x_proveedor(fecha, monto_deuda)
                                deuda = proveedor.get_deuda()
                            deudas.append(deuda)

        return f"Ahora nuestras deudas con los proveedores lucen así:\n{deudas}"

    def create_random_sale(min_products, max_products, date, advisor, manager, quantity, branch):
        for sale_index in range(quantity):
            total_price = 0
            shipping_cost = 0
            product_count = random.randint(min_products, max_products)
            articles = []
            for product_index in range(product_count):
                product_type = random.randint(0, 1)
                if product_type == 0:
                    shirt = Camisa(date, advisor, False, True, branch, branch.get_supplies_by_name(Camisa.get_supply_type()))
                    total_price += 200000
                    shipping_cost += 1000
                    articles.append(shirt)
                if product_type == 1:
                    pants = Pantalon(date, advisor, False, True, branch, branch.get_supplies_by_name(Pantalon.get_supply_type()))
                    total_price += 200000
                    shipping_cost += 1000
                    articles.append(pants)
            client = random.choice(Persona.get_person_list())
            sale = Venta(branch, date, client, advisor, manager, articles, total_price, total_price + shipping_cost)
            advisor.set_bonus_performance(int(total_price * 0.05))
            sale.set_shipping_cost(shipping_cost)

    # para la interaccion 1 de produccion
    def where_to_withdraw():
        print("\n*Seleccione la sede desde donde comprara el Respuesto:\n")
        if Sede.get_branch_list()[0].get_account().get_bank_savings() >= Main.provider_b.get_price():
            print("1. " + Sede.get_branch_list()[0].get_name() + " tiene disponible: " + str(Sede.get_branch_list()[0].get_account().get_bank_savings()))
        if Sede.get_branch_list()[1].get_account().get_bank_savings() >= Main.provider_b.get_price():
            print("2. " + Sede.get_branch_list()[1].get_name() + " tiene disponible: " + str(Sede.get_branch_list()[1].get_account().get_bank_savings()))
        option = 0
        while option != 1 and option != 2:
            option = int(input())
            if option == 1:
                new_branch_balance = (Sede.get_branch_list()[0].get_account().get_bank_savings() - Main.provider_b.get_supply().get_individual_price())
                Sede.get_branch_list()[0].get_account().set_bank_savings(new_branch_balance)

                print("El repuesto se compro exitosamente desde la " + Sede.get_branch_list()[0].get_name() + ", saldo disponible:")
                print(Sede.get_branch_list()[0].get_name() + " = " + str(Sede.get_branch_list()[0].get_account().get_bank_savings()))
                print(Sede.get_branch_list()[1].get_name() + " = " + str(Sede.get_branch_list()[1].get_account().get_bank_savings()))

            elif option == 2:
                new_branch_balance = (Sede.get_branch_list()[1].get_account().get_bank_savings() - Main.provider_b.get_supply().get_individual_price())
                Sede.get_branch_list()[1].get_account().set_bank_savings(new_branch_balance)

                print("El repuesto se compro exitosamente desde la sede " + Sede.get_branch_list()[1].get_name() + ", saldo disponible:")
                print(Sede.get_branch_list()[0].get_name() + " = " + str(Sede.get_branch_list()[0].get_account().get_bank_savings()))
                print(Sede.get_branch_list()[1].get_name() + " = " + str(Sede.get_branch_list()[1].get_account().get_bank_savings()))
            else:
                print("Opcion incorrecta, marque 1 o 2 segun desee")

    def receive_provider_b(provider_b):
        Main.provider_b = provider_b

    def get_provider_b_from_main():
        return Main.provider_b
        
    def next_int_seguro():
        while True:
            respuesta = input()
            if respuesta.isdigit():
                return int(respuesta)
            else:
                print("Por favor ingrese un número entero")