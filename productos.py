# Gestion de productos, stock y ventas

from datos import inventario, clientes, historial
from excepciones import ProductoNoEncontradoError, StockInsuficienteError
from precios import calcular_total


def obtener_producto(codigo):
    if codigo not in inventario:
        raise ProductoNoEncontradoError(codigo)
    return inventario[codigo]


def agregar_producto(codigo, nombre, cantidad, precio):
    if codigo in inventario:
        # Si ya existe, se suma el stock y se actualiza nombre/precio
        inventario[codigo]["stock"] += cantidad
        inventario[codigo]["nombre"] = nombre
        inventario[codigo]["precio"] = precio
        return False
    inventario[codigo] = {"nombre": nombre, "precio": precio, "stock": cantidad}
    return True


def registrar_venta(codigo, cantidad, cedula):
    producto = obtener_producto(codigo)
    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor que cero")
    if producto["stock"] < cantidad:
        raise StockInsuficienteError(
            "Stock insuficiente para '" + codigo + "' (disponible: "
            + str(producto["stock"]) + ", solicitado: " + str(cantidad) + ")"
        )

    categoria = clientes.get(cedula, "general")
    subtotal, descuento, total = calcular_total(producto["precio"], cantidad, categoria)
    producto["stock"] -= cantidad

    transaccion = {
        "id": len(historial) + 1,
        "codigo": codigo,
        "producto": producto["nombre"],
        "cantidad": cantidad,
        "cedula": cedula,
        "categoria": categoria,
        "subtotal": subtotal,
        "descuento": descuento,
        "total": total,
    }
    historial.append(transaccion)
    return transaccion
