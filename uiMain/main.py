
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