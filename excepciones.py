# Excepciones personalizadas del sistema


class ProductoNoEncontradoError(Exception):
    def __init__(self, codigo):
        self.codigo = codigo
        super().__init__("Producto con codigo '" + str(codigo) + "' no encontrado")


class StockInsuficienteError(Exception):
    pass
