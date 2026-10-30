[README.md](https://github.com/user-attachments/files/34185164/README.md)
# Sistema de Inventario y Ventas para Comercio Minorista

Programa en **Python puro** que funciona en la terminal y sirve para:

- Registrar productos por **código, nombre, cantidad y precio**.
- Gestionar el **stock** (entradas, salidas y ajustes).
- Aplicar **precios escalonados** según la cantidad comprada y la categoría del cliente (general, afiliado, VIP).
- Guardar un **historial de transacciones** en memoria y buscar en él por **código de producto** o por **cédula del cliente**.
- **Procesar lotes** de transacciones con el formato `CodigoProducto | Cantidad | CedulaCliente`.
- **Manejar errores** sin detener el programa, con una excepción personalizada `ProductoNoEncontradoError`.

> **No usa ninguna librería**, ni externa (no hay que instalar nada con `pip`) ni de la biblioteca estándar (no hay `import os`, `import sys`, etc.).
> Los únicos `import` que aparecen son **entre los propios archivos del proyecto**.

---

## Índice

1. [Requisitos](#1-requisitos)
2. [Cómo ejecutarlo](#2-cómo-ejecutarlo)
3. [Estructura del proyecto](#3-estructura-del-proyecto)
4. [Cómo se conectan los archivos (imports)](#4-cómo-se-conectan-los-archivos-imports)
5. [Explicación archivo por archivo](#5-explicación-archivo-por-archivo)
6. [La política de precios escalonados](#6-la-política-de-precios-escalonados)
7. [Procesamiento por lotes](#7-procesamiento-por-lotes)
8. [Manejo de errores](#8-manejo-de-errores)
9. [Guía de uso del menú (paso a paso)](#9-guía-de-uso-del-menú-paso-a-paso)
10. [Ejemplo completo de una sesión](#10-ejemplo-completo-de-una-sesión)
11. [Conceptos de Python que se aplican](#11-conceptos-de-python-que-se-aplican)
12. [Limitaciones](#12-limitaciones)

---

## 1. Requisitos

- **Python 3** instalado (cualquier versión 3.6 o superior).
- Nada más. No hay dependencias.

Para comprobar que tienes Python:

```bash
python --version
```

---

## 2. Cómo ejecutarlo

1. Asegúrate de que **los 8 archivos `.py` estén en la misma carpeta**. Si falta uno, Python dará un error del tipo `ModuleNotFoundError`.
2. Abre una terminal en esa carpeta.
3. Ejecuta:

```bash
python main.py
```

Aparecerá el menú principal:

```
========== TIENDA ==========
  1) Agregar producto
  2) Ver inventario
  3) Ajustar stock
  4) Registrar cliente
  5) Registrar venta
  6) Cotizar precio (sin vender)
  7) Procesar lote de transacciones
  8) Historial / buscador
  9) Ver errores de lotes
 10) Tabla de descuentos
  0) Salir
Selecciona una opcion:
```

Escribe el número de la opción y presiona **Enter**.

---

## 3. Estructura del proyecto

```
ss/
├── main.py          ← Punto de entrada. Contiene el menú.
├── datos.py         ← Diccionarios y listas donde se guarda todo en memoria.
├── excepciones.py   ← Excepciones personalizadas.
├── precios.py       ← Cálculo del total con descuentos escalonados.
├── productos.py     ← Agregar productos, buscar productos, registrar ventas.
├── historial.py     ← Buscador del historial (por código y por cédula).
├── lotes.py         ← Procesamiento de transacciones por lotes.
├── utilidades.py    ← Funciones para pedir datos por teclado y mostrar tablas.
└── README.md        ← Este documento.
```

La idea de dividirlo así es que **cada archivo tenga una sola responsabilidad**. Así es más fácil de leer, de corregir y de explicar.

---

## 4. Cómo se conectan los archivos (imports)

Este diagrama muestra **quién importa a quién**. La flecha `A ──► B` significa "A importa algo de B".

```
main.py
 ├──► datos.py
 ├──► excepciones.py
 ├──► precios.py
 ├──► utilidades.py
 ├──► historial.py ──► datos.py
 ├──► productos.py ──► datos.py
 │                 ├─► excepciones.py
 │                 └─► precios.py
 └──► lotes.py ─────► datos.py
                   ├─► excepciones.py
                   ├─► productos.py
                   └─► utilidades.py
```

Los archivos que **no importan nada** (`datos.py`, `excepciones.py`, `precios.py`, `utilidades.py`) son la base. Los demás se construyen encima de ellos.

Dicho en palabras:

| Archivo | Importa de... | ¿Por qué? |
|---|---|---|
| `main.py` | **todos** | Es el menú: necesita llamar a todas las funciones. |
| `productos.py` | `datos`, `excepciones`, `precios` | Guarda productos en `inventario`, lanza errores si el producto no existe y calcula el total de cada venta. |
| `historial.py` | `datos` | Recorre la lista `historial` para buscar. |
| `lotes.py` | `datos`, `excepciones`, `productos`, `utilidades` | Registra ventas una por una, atrapa los errores, los guarda y da formato al dinero. |
| `datos.py` | nada | Solo define las estructuras. |
| `excepciones.py` | nada | Solo define las clases de error. |
| `precios.py` | nada | Es una función matemática pura. |
| `utilidades.py` | nada | Solo usa `input()` y `print()`, que vienen con Python. |

### ¿Cómo se comparten los datos entre archivos?

Todos los módulos importan **los mismos objetos** desde `datos.py`:

```python
from datos import inventario, historial
```

En Python, cuando importas un diccionario o una lista, **no se copia**: todos los archivos apuntan al **mismo objeto en memoria**. Por eso, si `lotes.py` registra una venta, el stock baja también en lo que muestra `main.py`.

> ⚠️ Esto funciona porque el código **modifica** los diccionarios y listas (`inventario[codigo] = ...`, `historial.append(...)`) y **nunca los reasigna** (`inventario = {}`). Si alguno los reasignara, ese archivo quedaría con un objeto distinto y se perdería la conexión.

---

## 5. Explicación archivo por archivo

### 5.1 `datos.py`: la "base de datos" en memoria

```python
inventario = {}        # codigo -> {"nombre", "precio", "stock"}
clientes = {}          # cedula -> categoria (general, afiliado, vip)
historial = []         # lista de transacciones realizadas
registro_errores = []  # errores del procesamiento por lotes

CATEGORIAS = ("general", "afiliado", "vip")
```

Así se ven los datos después de usar el programa un rato:

```python
inventario = {
    "A1": {"nombre": "Arroz",  "precio": 2.5, "stock": 75},
    "B2": {"nombre": "Azucar", "precio": 3.0, "stock": 10},
}

clientes = {
    "123": "vip",
    "456": "afiliado",
}

historial = [
    {"id": 1, "codigo": "A1", "producto": "Arroz", "cantidad": 120,
     "cedula": "123", "categoria": "vip", "subtotal": 300.0,
     "descuento": 25, "total": 225.0},
    ...
]
```

- **`inventario`** es un **diccionario**: la clave es el código del producto y el valor es otro diccionario con nombre, precio y stock. Se usa un diccionario porque buscar por clave es inmediato.
- **`clientes`** relaciona cada cédula con su categoría.
- **`historial`** es una **lista**, porque las transacciones tienen un orden (la primera, la segunda...).
- **`CATEGORIAS`** es una **tupla** (no se puede modificar) con las categorías válidas.

---

### 5.2 `excepciones.py`: errores personalizados

```python
class ProductoNoEncontradoError(Exception):
    def __init__(self, codigo):
        self.codigo = codigo
        super().__init__("Producto con codigo '" + str(codigo) + "' no encontrado")


class StockInsuficienteError(Exception):
    pass
```

- Una **excepción personalizada** es una clase que **hereda de `Exception`**.
- `ProductoNoEncontradoError` recibe el código que no se encontró y arma un mensaje claro. `super().__init__(...)` le pasa ese mensaje a la clase padre, para que `str(error)` lo muestre.
- `StockInsuficienteError` no necesita nada especial, así que solo tiene `pass`. El mensaje se le pasa al lanzarla.

Se usan así:

```python
raise ProductoNoEncontradoError("ZZ")
# -> Producto con codigo 'ZZ' no encontrado
```

---

### 5.3 `precios.py`: el cálculo del total

Contiene la función principal del requisito:

```python
def calcular_total(precio_unitario, cantidad, categoria):
```

- **Recibe:** el precio unitario, la cantidad y la categoría del cliente.
- **Devuelve:** una tupla `(subtotal, porcentaje_descuento, total)`.

Se explica en detalle en la [sección 6](#6-la-política-de-precios-escalonados).

También tiene `mostrar_tabla_descuentos()`, que imprime la tabla de descuentos (opción 10 del menú).

---

### 5.4 `productos.py`: productos, stock y ventas

#### `obtener_producto(codigo)`

```python
def obtener_producto(codigo):
    if codigo not in inventario:
        raise ProductoNoEncontradoError(codigo)
    return inventario[codigo]
```

Busca un producto. Si no existe, **lanza** `ProductoNoEncontradoError`. Todas las demás funciones usan esta, así el error se lanza siempre en un único lugar.

#### `agregar_producto(codigo, nombre, cantidad, precio)`

- Si el código **no existe**, crea el producto y devuelve `True`.
- Si el código **ya existe**, **suma** la cantidad al stock actual, actualiza nombre y precio, y devuelve `False`.

Ejemplo: si `A1` tiene stock 50 y lo agregas otra vez con cantidad 30, el stock queda en **80**. Funciona como una "entrada de mercancía".

#### `registrar_venta(codigo, cantidad, cedula)`

Es el corazón del sistema. Paso a paso:

1. Busca el producto con `obtener_producto` (si no existe → `ProductoNoEncontradoError`).
2. Verifica que la cantidad sea mayor que 0 (si no → `ValueError`).
3. Verifica que haya stock suficiente (si no → `StockInsuficienteError`).
4. Busca la categoría del cliente con `clientes.get(cedula, "general")`. Si la cédula no está registrada, se usa **"general"** por defecto.
5. Llama a `calcular_total(...)` para obtener el monto con descuento.
6. **Descuenta el stock**: `producto["stock"] -= cantidad`.
7. Crea un diccionario con todos los datos de la transacción y lo agrega al `historial`.
8. Devuelve la transacción.

> 💡 El stock solo se descuenta **después** de pasar todas las validaciones. Así, si algo falla, el inventario queda intacto.

---

### 5.5 `historial.py`: el buscador

```python
def buscar_por_codigo(codigo):
    resultados = []
    for t in historial:
        if t["codigo"] == codigo:
            resultados.append(t)
    return resultados
```

`buscar_por_cedula(cedula)` es igual, pero compara `t["cedula"]`.

Recorre **todas** las transacciones con un bucle `for` y se queda con las que coinciden. Devuelve una lista: vacía si no encontró nada, o con todas las coincidencias.

---

### 5.6 `lotes.py`: procesamiento por lotes

Tiene dos funciones:

- **`procesar_lote(lineas)`** recibe una lista de líneas de texto y las procesa una por una.
- **`registrar_error(numero, linea, mensaje)`** guarda el error en `registro_errores` y lo muestra en pantalla.

Se explica en detalle en la [sección 7](#7-procesamiento-por-lotes).

---

### 5.7 `utilidades.py`: entrada y salida

| Función | Qué hace |
|---|---|
| `formato(valor)` | Convierte un número a texto con 2 decimales y separador de miles: `1234.5` → `"1,234.50"`. |
| `pedir_entero(mensaje, minimo)` | Pide un número entero. **Repite la pregunta** hasta que el usuario escriba un número válido mayor o igual que `minimo`. |
| `pedir_decimal(mensaje)` | Igual, pero acepta decimales (`12.50`) y no permite negativos. |
| `pedir_texto(mensaje)` | Pide texto y no acepta que quede vacío. |
| `mostrar_transacciones(lista)` | Imprime una lista de transacciones en forma de tabla. |

Ejemplo de cómo `pedir_entero` evita que el programa se caiga:

```python
def pedir_entero(mensaje, minimo=0):
    while True:                     # repite para siempre...
        try:
            valor = int(input(mensaje))
            if valor < minimo:
                print("  Debe ser un numero >= " + str(minimo))
                continue            # ...vuelve a preguntar
            return valor            # ...hasta que el dato es válido
        except ValueError:          # si escribió "abc", int() falla
            print("  Ingresa un numero entero valido.")
```

---

### 5.8 `main.py`: el menú

- Importa todo lo necesario de los demás archivos.
- Tiene una función `menu_...()` por cada opción del menú. Cada una pide los datos al usuario y llama a la lógica correspondiente.
- La función `main()` guarda las opciones en un **diccionario** que relaciona cada número con su texto y su función:

```python
opciones = {
    "1": ("Agregar producto", menu_agregar_producto),
    "2": ("Ver inventario", menu_ver_inventario),
    ...
}
```

Luego, en un bucle `while True`, muestra el menú, lee la opción y ejecuta la función con `opciones[opcion][1]()`. Así no hace falta una cadena enorme de `if/elif`.

- La línea final:

```python
if __name__ == "__main__":
    main()
```

significa: "ejecuta `main()` solo si este archivo se corrió directamente con `python main.py`, y no cuando otro archivo lo importa".

---

## 6. La política de precios escalonados

### La tabla

El descuento depende de **dos cosas a la vez**: cuántas unidades se compran y qué tipo de cliente es.

| Cantidad comprada | General | Afiliado | VIP |
|---|:---:|:---:|:---:|
| 1 a 9 | 0% | 5% | 10% |
| 10 a 49 | 5% | 10% | 15% |
| 50 a 99 | 10% | 15% | 20% |
| 100 o más | 15% | 20% | 25% |

Regla general: **mientras más compras, más descuento**, y **cada nivel de cliente suma 5% extra**.

### Cómo está programado (condicionales anidados)

```python
if cantidad >= 100:              # ← 1er nivel: ¿cuántas unidades?
    if categoria == "vip":       # ← 2do nivel: ¿qué cliente es?
        descuento = 25
    elif categoria == "afiliado":
        descuento = 20
    else:
        descuento = 15
elif cantidad >= 50:
    if categoria == "vip":
        descuento = 20
    ...
elif cantidad >= 10:
    ...
else:
    ...
```

- El `if` **de afuera** decide el **rango de cantidad**.
- El `if` **de adentro** decide la **categoría**.
- El orden importa: se pregunta primero por `>= 100`, luego `>= 50`, luego `>= 10`. Si se preguntara primero `>= 10`, una compra de 150 unidades entraría ahí y nunca llegaría al rango de 100.

### Las operaciones aritméticas

```python
subtotal        = precio_unitario * cantidad        # multiplicación
monto_descuento = subtotal * descuento / 100        # porcentaje
total           = subtotal - monto_descuento        # resta
return subtotal, descuento, round(total, 2)         # redondeo a 2 decimales
```

### Ejemplos calculados a mano

**Ejemplo 1:** Arroz a $2.50, 120 unidades, cliente VIP.

```
subtotal        = 2.50 × 120     = 300.00
rango           = 100 o más, VIP → 25%
monto_descuento = 300 × 25 / 100 =  75.00
total           = 300 − 75       = 225.00
```

**Ejemplo 2:** Azúcar a $3.00, 15 unidades, cliente afiliado.

```
subtotal        = 3.00 × 15      =  45.00
rango           = 10 a 49, afiliado → 10%
monto_descuento = 45 × 10 / 100  =   4.50
total           = 45 − 4.50      =  40.50
```

**Ejemplo 3:** Arroz a $2.50, 5 unidades, cédula no registrada.

```
categoria       = "general" (por defecto)
rango           = 1 a 9, general → 0%
total           = 2.50 × 5       =  12.50
```

> Para probar la función sin vender nada (y sin tocar el stock), usa la **opción 6: Cotizar precio**.

---

## 7. Procesamiento por lotes

### Formato de cada línea

```
CodigoProducto | Cantidad | CedulaCliente
```

Ejemplos válidos:

```
A1 | 120 | 123
B2|20|999
a1 | 5 | 777
```

- Los espacios alrededor de `|` se ignoran.
- El código se convierte a **mayúsculas** automáticamente (`a1` = `A1`).
- La cantidad debe ser un **entero positivo**.

### Dos formas de ingresar un lote

Entra a la **opción 7** y elige:

**1) Pegar líneas en la terminal.** Escribe o pega las líneas, una por renglón, y deja una **línea vacía** (presiona Enter sin escribir nada) para terminar.

**2) Leer desde un archivo de texto.** Crea un archivo, por ejemplo `ventas.txt`:

```
A1 | 120 | 123
B2 | 20 | 999
ZZ | 1 | 5
linea rota
A1 | abc | 1
A1 | 5 | 777
```

Luego escribe su ruta cuando el programa la pida (`ventas.txt` si está en la misma carpeta). Para leer el archivo se usa `open()`, que es una **función integrada de Python**, no una librería.

### Qué hace el programa con cada línea

Este es el bucle principal de `procesar_lote`, simplificado:

```python
for linea in lineas:                     # recorre TODAS las líneas
    try:
        partes = linea.split("|")        # "A1 | 120 | 123" -> ["A1 ", " 120 ", " 123"]
        if len(partes) != 3:
            raise ValueError("se esperaban 3 campos separados por '|'")

        codigo = partes[0].strip().upper()
        cantidad_txt = partes[1].strip()
        cedula = partes[2].strip()

        if not cantidad_txt.isdigit():
            raise ValueError("la cantidad no es un entero valido")
        cantidad = int(cantidad_txt)

        registrar_venta(codigo, cantidad, cedula)   # descuenta el stock
        exitosas += 1

    except ProductoNoEncontradoError as e:   # el código no existe
        registrar_error(...)
    except StockInsuficienteError as e:      # no hay suficiente
        registrar_error(...)
    except ValueError as e:                  # la línea está mal escrita
        registrar_error(...)
```

**Lo más importante:** el `try/except` está **dentro** del `for`. Si una línea falla, el `except` atrapa el error, lo registra y el `for` **continúa con la siguiente línea**. Si el `try` estuviera afuera del `for`, el primer error detendría todo el lote.

### Resultado del ejemplo anterior

Suponiendo que `A1` tiene 200 unidades a $2.50, `B2` tiene 10 unidades y la cédula `123` es VIP:

```
  [OK]  Linea 1: Arroz x120 -> $225.00 (stock restante: 80)
  [ERR] Linea 2: Stock insuficiente para 'B2' (disponible: 10, solicitado: 20)  -> 'B2|20|999'
  [ERR] Linea 3: Producto con codigo 'ZZ' no encontrado  -> 'ZZ|1|5'
  [ERR] Linea 4: Linea mal formateada: se esperaban 3 campos separados por '|'  -> 'linea rota'
  [ERR] Linea 5: Linea mal formateada: la cantidad 'abc' no es un entero valido  -> 'A1|abc|1'
  [OK]  Linea 6: Arroz x5 -> $12.50 (stock restante: 75)

Lote finalizado: 2 exitosas, 4 con error.
```

Fíjate en que **la línea 6 sí se procesó** aunque las líneas 2 a 5 fallaron. Ese es el comportamiento que pide el requisito.

---

## 8. Manejo de errores

### Tipos de errores que se atrapan

| Error | Cuándo ocurre | Ejemplo de línea |
|---|---|---|
| `ProductoNoEncontradoError` *(personalizada)* | El código no está en el inventario. | `ZZ \| 1 \| 5` |
| `StockInsuficienteError` *(personalizada)* | Se piden más unidades de las que hay. | `B2 \| 20 \| 999` (y solo hay 10) |
| `ValueError` | Faltan o sobran campos. | `linea rota` |
| `ValueError` | La cantidad no es un número. | `A1 \| abc \| 1` |
| `ValueError` | El código o la cédula están vacíos. | ` \| 5 \| 123` |

### El registro de errores

Cada error se guarda en la lista `registro_errores` de `datos.py` con esta forma:

```python
{"linea": 4, "contenido": "linea rota", "error": "Linea mal formateada: ..."}
```

Puedes consultar todos los errores acumulados con la **opción 9: Ver errores de lotes**.

### Errores fuera de los lotes

En el resto del menú también se atrapan los errores para que el programa **nunca se cierre de golpe**:

- Si en una venta individual (opción 5) el producto no existe o no hay stock, se muestra el mensaje y se vuelve al menú.
- Si escribes letras donde se pide un número, el programa vuelve a preguntar.
- Si el archivo del lote no existe, se muestra "No se pudo abrir el archivo" y se vuelve al menú.

---

## 9. Guía de uso del menú (paso a paso)

### Opción 1: Agregar producto

```
Codigo del producto: A1
Nombre: Arroz
Cantidad (stock): 200
Precio unitario: 2.5
Producto agregado.
```

Si el código ya existía, se suma la cantidad: `El producto ya existia: stock incrementado a 250.`

### Opción 2: Ver inventario

```
  Codigo   Nombre                     Precio    Stock
  ---------------------------------------------------
  A1       Arroz                        2.50      200
  B2       Azucar                       3.00        3  <- stock bajo
```

Los productos con **menos de 5 unidades** se marcan con `<- stock bajo`.

### Opción 3: Ajustar stock

Sirve para corregir el stock manualmente, por ejemplo después de contar la mercancía físicamente:

```
Codigo del producto: B2
  Stock actual de Azucar: 3
Nuevo stock: 40
  Stock actualizado.
```

### Opción 4: Registrar cliente

```
Cedula: 123
Categoria (general / afiliado / vip): vip
  Cliente 123 registrado como vip.
```

Los clientes que no registres se tratan como **general**.

### Opción 5: Registrar venta

```
Codigo del producto: A1
Cantidad: 120
Cedula del cliente: 123
  Subtotal:  $300.00
  Descuento: 25% (cliente vip)
  TOTAL:     $225.00
```

El stock baja automáticamente y la venta queda en el historial.

### Opción 6: Cotizar precio

Calcula el total **sin vender** y **sin tocar el stock**. Sirve para probar la función `calcular_total`:

```
Precio unitario: 10
Cantidad: 60
Categoria (general / afiliado / vip): afiliado
  Subtotal $600.00 - 15% = TOTAL $510.00
```

### Opción 7: Procesar lote

Ver la [sección 7](#7-procesamiento-por-lotes).

### Opción 8: Historial / buscador

```
1) Ver todo
2) Buscar por codigo de producto
3) Buscar por cedula de cliente
```

Ejemplo buscando por código `A1`:

```
  ID   Codigo   Producto          Cant Cedula       Categoria  Desc        Total
  ------------------------------------------------------------------------------
  1    A1       Arroz              120 123          vip         25%       225.00
  2    A1       Arroz                5 777          general      0%        12.50
```

### Opción 9: Ver errores de lotes

Muestra todos los errores registrados durante los lotes procesados.

### Opción 10: Tabla de descuentos

Muestra la tabla de la [sección 6](#6-la-política-de-precios-escalonados).

### Opción 0: Salir

Cierra el programa. **Se pierden todos los datos** (ver [Limitaciones](#12-limitaciones)).

---

## 10. Ejemplo completo de una sesión

Sigue estos pasos en orden para probar todo el sistema:

1. **Opción 1:** agrega `A1`, `Arroz`, cantidad `200`, precio `2.5`.
2. **Opción 1:** agrega `B2`, `Azucar`, cantidad `10`, precio `3`.
3. **Opción 4:** registra la cédula `123` como `vip`.
4. **Opción 7 → 1:** pega estas líneas y termina con una línea vacía:
   ```
   A1 | 120 | 123
   B2 | 20 | 999
   ZZ | 1 | 5
   linea rota
   A1 | abc | 1
   A1 | 5 | 777
   ```
5. Observa que hay **2 exitosas y 4 con error**, y que el lote no se detuvo.
6. **Opción 2:** comprueba que `A1` bajó de 200 a **75** (200 − 120 − 5) y que `B2` sigue en 10.
7. **Opción 8 → 3:** busca la cédula `123`. Aparece la compra de 120 unidades con 25% de descuento.
8. **Opción 8 → 2:** busca el código `A1`. Aparecen las 2 ventas.
9. **Opción 9:** revisa los 4 errores registrados.
10. **Opción 0:** salir.

---

## 11. Conceptos de Python que se aplican

| Concepto | Dónde se usa |
|---|---|
| **Módulos e `import`** | Todos los archivos se importan entre sí (`from datos import inventario`). |
| **Diccionarios** | `inventario`, `clientes`, cada transacción, el menú de opciones. |
| **Listas** | `historial`, `registro_errores`, los resultados de búsqueda. |
| **Tuplas** | `CATEGORIAS` y el valor que devuelve `calcular_total`. |
| **Bucle `for`** | Recorrer las líneas del lote y el historial en las búsquedas. |
| **Bucle `while`** | El menú principal y las funciones que repiten la pregunta hasta tener un dato válido. |
| **Condicionales anidados** | `calcular_total` (rango de cantidad → categoría). |
| **Operadores aritméticos** | `*`, `/`, `-`, `+=`, `-=` en precios y stock. |
| **Operadores de comparación y pertenencia** | `>=`, `<`, `==`, `in`, `not in`. |
| **Funciones con parámetros y retorno** | Toda la lógica está dividida en funciones. |
| **Clases y herencia** | Las excepciones heredan de `Exception`. |
| **`raise`** | Lanzar errores cuando algo no es válido. |
| **`try / except`** | Atrapar errores sin que el programa se detenga. |
| **Métodos de texto** | `split("|")`, `strip()`, `upper()`, `lower()`, `isdigit()`, `format()`. |
| **Funciones integradas** | `input`, `print`, `int`, `float`, `str`, `len`, `round`, `open`. |
| **`if __name__ == "__main__"`** | Para que `main()` solo se ejecute al correr `main.py` directamente. |

---

## 12. Limitaciones

- **Todo se guarda en memoria:** al cerrar el programa se pierden los productos, clientes, historial y errores. Así lo pide el requisito ("historial de transacciones realizadas en memoria").
- Los precios se manejan con `float`, así que en cálculos muy grandes podría haber pequeños errores de redondeo. Para un ejercicio académico esto es aceptable, y el total se redondea a 2 decimales.
- No hay usuarios ni contraseñas: cualquiera que abra el programa puede usarlo.
- Los porcentajes de descuento están escritos directamente en `precios.py`. Para cambiarlos, hay que editar esa función.
# lenguaje-de-programacion-1
# lenguaje-de-programacion-1-
