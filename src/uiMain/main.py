from ..gestorAplicacion.administracion import Empleado
from gestorAplicacion import Persona, Sede
import locale
from typing import List

locale.setlocale(locale.LC_ALL, 'es_ES')
comparador = locale.strxfrm

class Main:

    @classmethod
    def main(cls):
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

Main.main()

def despedir_empleados(fecha):
    print("Obteniendo lista sugerida de empleados")
    info_despidos : List[List] = Empleado.lista_inicial_despedir_empleado(fecha)
    a_despedir = info_despidos[0]
    mensajes = info_despidos[1]

    for mensaje in mensajes:
        print(mensaje)

    print("\nEsta es una lista de empleados que no estan rindiendo correctamente, ¿que deseas hacer?")

    diferencia_salarios = -Persona.diferencia_salarios()
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
        opcion = next_int_seguro()
        if opcion == 2:
            print("¿De que sede quieres añadir al empleado?")
            for i, sede in enumerate(Sede.get_lista_sedes()):
                print(f"{i}. {sede.get_nombre()}")
            sede = next_int_seguro()
            print("¿Que empleado quieres despedir? Pon su nombre completo o documento, esto lo añadirá a la lista de despedibles.")
            for emp in Sede.get_lista_sedes()[sede].get_lista_empleados():
                print(f"{emp.get_nombre()} {emp.get_area_actual()} {emp.get_documento()}")
            nombre = input().strip()
            for emp in Sede.get_lista_sedes()[sede].get_lista_empleados():
                if comparador(emp.get_nombre()) == comparador(nombre) or (nombre.isdigit() and emp.get_documento() == int(nombre)):
                    a_despedir.append(emp)

    seleccion = []
    print("¿Que empleados quieres despedir? Pon su nombre completo, documento o FIN para terminar.")
    for emp in a_despedir:
        print(f"{emp.get_nombre()} {emp.get_area_actual()} {emp.get_documento()}")
    nombre = input().strip()
    while nombre.lower() != "fin":
        for emp in a_despedir:
            if comparador(emp.get_nombre()) == comparador(nombre) or (nombre.isdigit() and emp.get_documento() == int(nombre)):
                seleccion.append(emp)
        nombre = input().strip()

    print("Despidiendo empleados...")
    Empleado.despedir_empleados(seleccion, True, fecha)
    print("Listo!")
    return seleccion

def next_int_seguro():
    while True:
        respuesta = input()
        if respuesta.isdigit():
            return int(respuesta)
        else:
            print("Por favor ingrese un número entero")