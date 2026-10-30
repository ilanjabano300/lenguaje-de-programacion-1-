# Procesamiento por lotes:  CodigoProducto | Cantidad | CedulaCliente

from datos import inventario, registro_errores
from excepciones import ProductoNoEncontradoError, StockInsuficienteError
from productos import registrar_venta
from utilidades import formato


def registrar_error(numero, linea, mensaje):
    registro_errores.append({"linea": numero, "contenido": linea, "error": mensaje})
    print("  [ERR] Linea " + str(numero) + ": " + mensaje + "  -> '" + linea + "'")


def procesar_lote(lineas):
    exitosas = 0
    fallidas = 0
    numero = 0

    for linea in lineas:
        numero += 1
        linea = linea.strip()
        if linea == "":
            continue
        try:
            partes = linea.split("|")
            if len(partes) != 3:
                raise ValueError("se esperaban 3 campos separados por '|'")

            codigo = partes[0].strip().upper()
            cantidad_txt = partes[1].strip()
            cedula = partes[2].strip()

            if codigo == "" or cedula == "":
                raise ValueError("codigo o cedula vacios")
            if not cantidad_txt.isdigit():
                raise ValueError("la cantidad '" + cantidad_txt + "' no es un entero valido")
            cantidad = int(cantidad_txt)

            t = registrar_venta(codigo, cantidad, cedula)
            exitosas += 1
            print("  [OK]  Linea " + str(numero) + ": " + t["producto"] + " x"
                  + str(cantidad) + " -> $" + formato(t["total"])
                  + " (stock restante: " + str(inventario[codigo]["stock"]) + ")")

        except ProductoNoEncontradoError as e:
            fallidas += 1
            registrar_error(numero, linea, str(e))
        except StockInsuficienteError as e:
            fallidas += 1
            registrar_error(numero, linea, str(e))
        except ValueError as e:
            fallidas += 1
            registrar_error(numero, linea, "Linea mal formateada: " + str(e))

    print("\nLote finalizado: " + str(exitosas) + " exitosas, "
          + str(fallidas) + " con error.")
