# Utilidades de entrada / salida por terminal


def formato(valor):
    return "{:,.2f}".format(valor)


def pedir_entero(mensaje, minimo=0):
    while True:
        try:
            valor = int(input(mensaje))
            if valor < minimo:
                print("  Debe ser un numero >= " + str(minimo))
                continue
            return valor
        except ValueError:
            print("  Ingresa un numero entero valido.")


def pedir_decimal(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                print("  El valor no puede ser negativo.")
                continue
            return valor
        except ValueError:
            print("  Ingresa un numero valido (ej. 12.50).")


def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print("  Este campo no puede estar vacio.")


def mostrar_transacciones(lista):
    if len(lista) == 0:
        print("  No se encontraron transacciones.")
        return
    print("  {:<4} {:<8} {:<16} {:>5} {:<12} {:<9} {:>5} {:>12}".format(
        "ID", "Codigo", "Producto", "Cant", "Cedula", "Categoria", "Desc", "Total"))
    print("  " + "-" * 78)
    for t in lista:
        print("  {:<4} {:<8} {:<16} {:>5} {:<12} {:<9} {:>4}% {:>12}".format(
            t["id"], t["codigo"], t["producto"][:16], t["cantidad"], t["cedula"],
            t["categoria"], t["descuento"], formato(t["total"])))
