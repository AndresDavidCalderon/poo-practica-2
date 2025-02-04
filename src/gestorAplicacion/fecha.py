class Fecha:
    def __init__(self, dia=1, mes=1, año=2000):
        self.dia = dia
        self.mes = mes
        self.año = año

    @property
    def get_dia(self):
        return self.dia

    @get_dia.setter
    def set_dia(self, dia):
        self.dia = dia

    @property
    def get_mes(self):
        return self.mes

    @get_mes.setter
    def set_mes(self, mes):
        self.mes = mes

    @property
    def get_año(self):
        return self.año

    @get_año.setter
    def set_año(self, año):
        self.año = año


    def restar_meses(self, meses):
        mes = self.mes - meses
        año = self.año
        if mes <= 0:
            mes += 12
            año -= 1
        return Fecha(self.dia, mes, año)

    @staticmethod
    def comparar_fecha(fecha1, fecha2):
        return (Fecha.comparar_año(fecha1.año, fecha2.año) and
                Fecha.comparar_mes(fecha1.mes, fecha2.mes) and
                Fecha.comparar_dia(fecha1.dia, fecha2.dia))

    def dias_hasta(self, hasta):
        dias = (hasta.año - self.año) * 365
        dias += (hasta.mes - self.mes) * 30
        dias += hasta.dia - self.dia
        return dias

    def dia_siguiente(self):
        nueva_fecha = Fecha(self.dia, self.mes, self.año)
        nueva_fecha.dia += 1
        if nueva_fecha.dia > 31:
            nueva_fecha.dia = 1
            nueva_fecha.mes += 1
            if nueva_fecha.mes > 12:
                nueva_fecha.mes = 1
                nueva_fecha.año += 1
        return nueva_fecha

    def __str__(self):
        return f"Día: {self.dia} Mes: {self.mes} Año: {self.año}"