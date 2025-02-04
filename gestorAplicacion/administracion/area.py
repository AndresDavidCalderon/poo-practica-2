from enum import Enum

class Area(Enum):
    DIRECCION = "Direccion", ["computador","impresora"]
    OFICINA = "Oficina", ["computador","registradora"]
    VENTAS = "Ventas", ["escaner"]
    CORTE = "Corte", ["maquina de coser","maquina de corte","plancha industrial"]