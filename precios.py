# Politica de precios escalonados


def calcular_total(precio_unitario, cantidad, categoria):
    """Devuelve (subtotal, porcentaje_descuento, total) segun cantidad y categoria."""
    categoria = categoria.lower()
    subtotal = precio_unitario * cantidad

    # Descuento por volumen (escalonado) combinado con la categoria del cliente
    if cantidad >= 100:
        if categoria == "vip":
            descuento = 25
        elif categoria == "afiliado":
            descuento = 20
        else:
            descuento = 15
    elif cantidad >= 50:
        if categoria == "vip":
            descuento = 20
        elif categoria == "afiliado":
            descuento = 15
        else:
            descuento = 10
    elif cantidad >= 10:
        if categoria == "vip":
            descuento = 15
        elif categoria == "afiliado":
            descuento = 10
        else:
            descuento = 5
    else:
        if categoria == "vip":
            descuento = 10
        elif categoria == "afiliado":
            descuento = 5
        else:
            descuento = 0

    monto_descuento = subtotal * descuento / 100
    total = subtotal - monto_descuento
    return subtotal, descuento, round(total, 2)


def mostrar_tabla_descuentos():
    print("  Cantidad      General  Afiliado  VIP")
    print("  1 - 9           0%       5%      10%")
    print("  10 - 49         5%      10%      15%")
    print("  50 - 99        10%      15%      20%")
    print("  100 o mas      15%      20%      25%")
