class Resultado:
    # Resultado de una busqueda de un Insumo en una Sede.

    def __init__(self, encontrado=False, indice=None, sede=None, precio=None):
        self.encontrado = encontrado
        self.index = indice
        self.precio = precio
        self.sede = sede

    def get_precio(self):
        return self.precio

    def set_precio(self, precio):
        self.precio = precio

    def get_encontrado(self):
        return self.encontrado

    def set_encontrado(self, encontrado):
        self.encontrado = encontrado

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index

    def get_sede(self):
        return self.sede

    def set_sede(self, sede):
        self.sede = sede