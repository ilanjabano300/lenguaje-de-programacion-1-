# Programa principal: menu por terminal del sistema de tienda

from datos import inventario, clientes, historial, registro_errores, CATEGORIAS
from excepciones import ProductoNoEncontradoError, StockInsuficienteError
from precios import calcular_total, mostrar_tabla_descuentos
from productos import obtener_producto, agregar_producto, registrar_venta
from historial import buscar_por_codigo, buscar_por_cedula
from lotes import procesar_lote
from utilidades import (formato, pedir_entero, pedir_decimal, pedir_texto,
                        mostrar_transacciones)


def menu_agregar_producto():
    codigo = pedir_texto("Codigo del producto: ").upper()
    nombre = pedir_texto("Nombre: ")
    cantidad = pedir_entero("Cantidad (stock): ", 0)
    precio = pedir_decimal("Precio unitario: ")
    if agregar_producto(codigo, nombre, cantidad, precio):
        print("Producto agregado.")
    else:
        print("El producto ya existia: stock incrementado a "
              + str(inventario[codigo]["stock"]) + ".")


def menu_ver_inventario():
    if len(inventario) == 0:
        print("  Inventario vacio.")
        return
    print("  {:<8} {:<20} {:>12} {:>8}".format("Codigo", "Nombre", "Precio", "Stock"))
    print("  " + "-" * 51)
    for codigo in inventario:
        p = inventario[codigo]
        alerta = "  <- stock bajo" if p["stock"] < 5 else ""
        print("  {:<8} {:<20} {:>12} {:>8}{}".format(
            codigo, p["nombre"][:20], formato(p["precio"]), p["stock"], alerta))


def menu_ajustar_stock():
    codigo = pedir_texto("Codigo del producto: ").upper()
    try:
        producto = obtener_producto(codigo)
    except ProductoNoEncontradoError as e:
        print("  " + str(e))
        return
    print("  Stock actual de " + producto["nombre"] + ": " + str(producto["stock"]))
    nuevo = pedir_entero("Nuevo stock: ", 0)
    producto["stock"] = nuevo
    print("  Stock actualizado.")


def menu_registrar_cliente():
    cedula = pedir_texto("Cedula: ")
    while True:
        categoria = input("Categoria (general / afiliado / vip): ").strip().lower()
        if categoria in CATEGORIAS:
            break
        print("  Categoria invalida.")
    clientes[cedula] = categoria
    print("  Cliente " + cedula + " registrado como " + categoria + ".")


def menu_venta():
    codigo = pedir_texto("Codigo del producto: ").upper()
    cantidad = pedir_entero("Cantidad: ", 1)
    cedula = pedir_texto("Cedula del cliente: ")
    try:
        t = registrar_venta(codigo, cantidad, cedula)
    except ProductoNoEncontradoError as e:
        print("  Error: " + str(e))
        return
    except StockInsuficienteError as e:
        print("  Error: " + str(e))
        return
    print("  Subtotal:  $" + formato(t["subtotal"]))
    print("  Descuento: " + str(t["descuento"]) + "% (cliente " + t["categoria"] + ")")
    print("  TOTAL:     $" + formato(t["total"]))


def menu_cotizar():
    precio = pedir_decimal("Precio unitario: ")
    cantidad = pedir_entero("Cantidad: ", 1)
    categoria = input("Categoria (general / afiliado / vip): ").strip().lower()
    if categoria not in CATEGORIAS:
        print("  Categoria desconocida, se usara 'general'.")
        categoria = "general"
    subtotal, descuento, total = calcular_total(precio, cantidad, categoria)
    print("  Subtotal $" + formato(subtotal) + " - " + str(descuento)
          + "% = TOTAL $" + formato(total))


def menu_lote():
    print("Formato:  CodigoProducto | Cantidad | CedulaCliente")
    print("1) Pegar lineas (termina con una linea vacia)")
    print("2) Leer desde archivo de texto")
    opcion = input("Opcion: ").strip()
    lineas = []
    if opcion == "1":
        while True:
            linea = input("> ")
            if linea.strip() == "":
                break
            lineas.append(linea)
    elif opcion == "2":
        ruta = pedir_texto("Ruta del archivo: ")
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                lineas = f.readlines()
        except OSError as e:
            print("  No se pudo abrir el archivo: " + str(e))
            return
    else:
        print("  Opcion invalida.")
        return
    procesar_lote(lineas)


def menu_historial():
    print("1) Ver todo")
    print("2) Buscar por codigo de producto")
    print("3) Buscar por cedula de cliente")
    opcion = input("Opcion: ").strip()
    if opcion == "1":
        mostrar_transacciones(historial)
    elif opcion == "2":
        mostrar_transacciones(buscar_por_codigo(pedir_texto("Codigo: ").upper()))
    elif opcion == "3":
        mostrar_transacciones(buscar_por_cedula(pedir_texto("Cedula: ")))
    else:
        print("  Opcion invalida.")


def menu_errores():
    if len(registro_errores) == 0:
        print("  No hay errores registrados.")
        return
    for e in registro_errores:
        print("  Linea " + str(e["linea"]) + ": " + e["error"] + "  -> '" + e["contenido"] + "'")


def main():
    opciones = {
        "1": ("Agregar producto", menu_agregar_producto),
        "2": ("Ver inventario", menu_ver_inventario),
        "3": ("Ajustar stock", menu_ajustar_stock),
        "4": ("Registrar cliente", menu_registrar_cliente),
        "5": ("Registrar venta", menu_venta),
        "6": ("Cotizar precio (sin vender)", menu_cotizar),
        "7": ("Procesar lote de transacciones", menu_lote),
        "8": ("Historial / buscador", menu_historial),
        "9": ("Ver errores de lotes", menu_errores),
        "10": ("Tabla de descuentos", mostrar_tabla_descuentos),
    }

    while True:
        print("\n========== TIENDA ==========")
        for clave in opciones:
            print(" " + clave.rjust(2) + ") " + opciones[clave][0])
        print("  0) Salir")
        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "0":
            print("Hasta luego.")
            break
        elif opcion in opciones:
            print()
            opciones[opcion][1]()
        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    main()
