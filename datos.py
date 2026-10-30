# Estructuras de datos compartidas en memoria

inventario = {}        # codigo -> {"nombre", "precio", "stock"}
clientes = {}          # cedula -> categoria (general, afiliado, vip)
historial = []         # lista de transacciones realizadas
registro_errores = []  # errores del procesamiento por lotes

CATEGORIAS = ("general", "afiliado", "vip")
