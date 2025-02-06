
from abc import ABC
from typing import List

from src.gestorAplicacion.administracion.area import Area
from src.gestorAplicacion.administracion.empleado import Empleado
from src.gestorAplicacion.sede import Sede

class Prenda(ABC):
    serial_version_uid = 1
    maquinaria = []  # List to hold machinery objects
    cantidad_insumo = []  # List to hold quantity of supplies
    porcentaje_ganancia = 0.40  # Profit percentage affecting production quantity

    def __init__(self, fecha_fabricacion, sede, nombre, modista, descartada, terminada, insumos):
        self.fecha_fabricacion = fecha_fabricacion
        self.sede = sede
        self.nombre = nombre
        self.modista = modista
        self.descartada = descartada
        self.terminada = terminada
        self.insumo = []  # List of supplies
        self.en_stock = []  # Represents inventory by location
        self.costo_insumos = 0.0
        self.cantidad_ultima_produccion = 0
        self.cantidad_tela_ultima_produccion = 0
        self.costo_produccion = 0
        self.precio = 0  # Price of the clothing item
        self.ultimo_paso = []  # Last step rewritten to use siguientePaso()

        for insumo_item in insumos:
            self.insumo.append(insumo_item)
            self.costo_insumos += insumo_item.get_precio_individual()

        mano_obra = 0
        modistas = 0
        for emp in Empleado.get_emp_creados():
            if emp.get_area_actual() == Area.CORTE:
                mano_obra += emp.calcular_salario()
                modistas += 1

        self.costo_produccion = round((mano_obra / modistas) * 0.08)
        Sede.get_prendas_inventadas_total().append(self)
        sede.get_prendas_inventadas().append(self)
        if descartada:
            modista.set_prendas_descartadas(modista.get_prendas_descartadas() + 1)
        elif terminada:
            modista.set_prendas_producidas(modista.get_prendas_producidas() + 1)
    
    def produce_clothing_items(production_plan, today):
        last_production_fabric_quantity = 0
        last_production_quantity = 0
        production_day = today
        sufficient_supplies = True
        
        for dia in production_plan:
            for index in range(len(dia)):
                location = Sede.get_list_of_locations()[index]
                if not producirListaPrendas(dia[index], location, production_day):
                    sufficient_supplies = False
            production_day = production_day.next_day()
        
        return sufficient_supplies
    
    def producirListaPrendas(production_plan, location, production_date):
        sufficient_supplies = True
        pants_quantity = production_plan[0]
        shirts_quantity = production_plan[1]
        garments = []

        pants_supplies = location.get_supplies_by_name(Pant.get_supply_type())
        for _ in range(pants_quantity):
            if location.remove_supplies(pants_supplies, Pant.get_supply_quantity()):
                global last_production_fabric_quantity
                last_production_fabric_quantity += Pant.get_supply_quantity()[Pant.get_supply_type().index("Fabric")]
                pant = Pant(production_date, None, False, False, location, pants_supplies)
                garments.append(pant)
            else:
                sufficient_supplies = False
                Main.notify_insufficient_supplies(location, production_date, "Pant")
                break

        shirts_supplies = location.get_supplies_by_name(Shirt.get_supply_type())
        for _ in range(shirts_quantity):
            if location.remove_supplies(shirts_supplies, Shirt.get_supply_quantity()):
                last_production_fabric_quantity += Shirt.get_supply_quantity()[Shirt.get_supply_type().index("Fabric")]
                shirt = Shirt(production_date, None, False, False, location, shirts_supplies)
                garments.append(shirt)
            else:
                sufficient_supplies = False
                Main.notify_insufficient_supplies(location, production_date, "Shirt")
                break

        batch_index = 0
        while True:
            if len(garments) == 0:
                break

            batches = []
            cut_batch = []
            trimming_batch = []
            sewing_batch = []
            embroidery_batch = []
            thermal_fixing_batch = []
            ironing_batch = []
            embroidery_machine_batch = []

            for garment in garments:
                next_step = garment.next_step()
                step_name = str(next_step[0]).lower()
                if step_name == "cutting machine":
                    cut_batch.append(garment)
                elif step_name == "trimming machine":
                    trimming_batch.append(garment)
                elif step_name == "industrial sewing machine":
                    sewing_batch.append(garment)
                elif step_name == "embroidery machine":
                    embroidery_batch.append(garment)
                elif step_name == "thermal fixing machine":
                    thermal_fixing_batch.append(garment)
                elif step_name == "industrial iron":
                    ironing_batch.append(garment)
                elif step_name == "industrial embroidery":
                    embroidery_machine_batch.append(garment)

            batches.append(thermal_fixing_batch)
            batches.append(embroidery_batch)
            batches.append(ironing_batch)
            batches.append(cut_batch)
            batches.append(trimming_batch)
            batches.append(sewing_batch)
            batches.append(embroidery_machine_batch)

            dressmaker = Main.request_dressmaker(len(garments), location, batch_index)
            for batch in batches:
                if len(batch) == 0:
                    continue  # No garments for this machinery
                machine = Machine.select_by_type(location, str(batch[0].last_step[0]))
                for garment in batch:
                    machine.use(int(garment.last_step[1]))
                    result = garment.perform_step(dressmaker)
                    if result == "DISCARD":
                        garment.discarded = True
                        dressmaker.set_discarded_garments(dressmaker.get_discarded_garments() + 1)
                        garments.remove(garment)
                    elif result == "READY":
                        garment.finished = True
                        dressmaker.set_produced_garments(dressmaker.get_produced_garments() + 1)
                        garments.remove(garment)
                        global last_production_quantity
                        last_production_quantity += 1
            batch_index += 1

        return sufficient_supplies
    
    def siguientePaso(self):
        pass

    def realizarPaso(self, modista):
        pass

    @staticmethod
    def gastoMensualClase(fecha):
        gastoPrenda = 0
        gastoActual = 0
        gastoPasado = 0
        for prenda in Sede.getPrendasInventadasTotal():
            lista = prenda.gastoMensualTipo(fecha, prenda.fechaFabricacion, prenda)
            gastoActual += lista[0]
            gastoPasado += lista[1]
        gastoPrenda = gastoActual if gastoActual != 0 else gastoPasado
        return gastoPrenda

    # Retorna el pesimismo
    @staticmethod
    def prevenciones(descuento, nuevoDescuento, fecha):
        for sede in Sede.getlistaSedes():
            for prenda in sede.getPrendasInventadas():
                if descuento > 0.0 or nuevoDescuento > 0.0:
                    if nuevoDescuento > 0.0:
                        Prenda.porcentajeGanancia -= Prenda.porcentajeGanancia * (1 - nuevoDescuento)
                    Venta.setPesimismo(Venta.getPesimismo() - 0.05)
                else:
                    Venta.setPesimismo(Venta.getPesimismo() + 0.1)
        return Venta.getPesimismo()

    # -------------------Getters y Setters-------------------
    def getPrendasDescartadas(self):
        return self.descartada

    def getNombre(self):
        return self.nombre

    def getInsumo(self):
        return self.insumo

    @staticmethod
    def getCantidadInsumo():
        return ClothingItem.cantidadInsumo

    def getCostoInsumos(self):
        return self.costoInsumos

    def getPrecio(self):
        return self.precio

    def __str__(self):
        return f"La prenda de tipo {self.nombre}"

    @staticmethod
    def getCantidadUltimaProduccion():
        return 0  # Placeholder for actual implementation

    @staticmethod
    def getCantidadTelaUltimaProduccion():
        return 0  # Placeholder for actual implementation

    def calcularCostoInsumos(self):
        self.costoInsumos = 0
        for i in range(len(self.insumo)):
            insumoI = self.insumo[i]
            cantidad = 0
            if isinstance(self, Pantalon):
                cantidad = Pantalon.getCantidadInsumo()[i]
            elif isinstance(self, Camisa):
                cantidad = Camisa.getCantidadInsumo()[i]
            self.costoInsumos += insumoI.precioXUnidad * cantidad
        return self.costoInsumos

    def calcularCostoProduccion(self):
        sumSalarios = 0
        for empleado in sede.getlistaEmpleados():
            if empleado.getRol() == Rol.MODISTA:
                sumSalarios += empleado.getRol().getSalarioInicial()
        self.costoProduccion = round(sumSalarios * 0.01)
        return self.costoProduccion

    def calcularPrecio(self):
        costoTotal = self.costoInsumos + self.costoProduccion
        gananciaDeseada = costoTotal + (costoTotal * Prenda.porcentajeGanancia)
        self.precio = round(gananciaDeseada)
        return self.precio