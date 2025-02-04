from enum import Enum

class Area(Enum):
    DIRECCION = "Direccion", ["gerente","subgerente","director","subdirector"],3
    OFICINA = "Oficina", ["computador","registradora"],2
    VENTAS = "Ventas", ["escaner"],1
    CORTE = "Corte", ["maquina de coser","maquina de corte","plancha industrial"],0