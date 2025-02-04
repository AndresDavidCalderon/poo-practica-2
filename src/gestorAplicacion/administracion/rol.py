from enum import Enum

class Rol(Enum):
    PRESIDENTE = 3000000
    EJECUTIVO = 2000000
    ASISTENTE = 1000000
    DISEÑADOR = 2000000
    MODISTA = 1000000
    SECRETARIA = 1000000
    PLANTA = 1500000
    VENDEDOR = 1000000

    def __init__(self, initial_salary):
        self.initial_salary = initial_salary

    def get_initial_salary(self):
        return self.initial_salary