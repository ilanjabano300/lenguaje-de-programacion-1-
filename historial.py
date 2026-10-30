# Buscador sobre el historial de transacciones en memoria

from datos import historial


def buscar_por_codigo(codigo):
    resultados = []
    for t in historial:
        if t["codigo"] == codigo:
            resultados.append(t)
    return resultados


def buscar_por_cedula(cedula):
    resultados = []
    for t in historial:
        if t["cedula"] == cedula:
            resultados.append(t)
    return resultados
