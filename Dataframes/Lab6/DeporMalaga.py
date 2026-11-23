import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

#PARTE 1 Carga y exploración 
#1.1 carga ficheros y unelos en DataFrame pedidos. Fecha como índice y ordena 
septiembre = pd.read_csv("datos/pedidos_septiembre.csv")
octubre = pd.read_csv("datos/pedidos_octubre.csv")
pedidos = pd.concat([septiembre, octubre])
pedidos["fecha"] = pd.to_datetime(pedidos["fecha"])
pedidos = pedidos.set_index("fecha")
pedidos =pedidos.sort_index()
print(septiembre.shape, octubre.shape, pedidos.shape) #(146, 9) (134, 9) (280, 8)

#1.2  Muestra 5 primeros pedidos, 3 últimos, índice y nombres columnas.
print(pedidos.head(5))
print(pedidos.tail(3))
print(pedidos.index)
print(pedidos.columns)

#                     id_pedido id_cliente  ... metodo_pago     estado
#fecha                                     ...                       
#2026-09-01 11:54:00    PD0001       C040  ...     tarjeta  entregado
#2026-09-01 20:23:00    PD0002       C019  ...      paypal  entregado
#2026-09-02 03:51:00    PD0003       C022  ...      paypal  entregado
#2026-09-03 05:38:00    PD0004       C007  ...     tarjeta  entregado
#2026-09-03 10:54:00    PD0005       C003  ...     tarjeta  entregado

#[5 rows x 8 columns]
#                    id_pedido id_cliente  ... metodo_pago     estado
#fecha                                     ...                       
#2026-10-31 08:14:00    PD0278       C039  ...     tarjeta  entregado
#2026-10-31 17:25:00    PD0279       C037  ...     tarjeta  entregado
##2026-10-31 22:39:00    PD0280       C038  ...     tarjeta   devuelto

#[3 rows x 8 columns]
#DatetimeIndex(['2026-09-01 11:54:00', '2026-09-01 20:23:00',
 #              '2026-09-02 03:51:00', '2026-09-03 05:38:00',
  #             '2026-09-03 10:54:00', '2026-09-03 11:51:00',
   #            '2026-09-03 18:28:00', '2026-09-03 19:00:00',
    #           '2026-09-03 19:27:00', '2026-09-03 21:53:00',
     #          ...
      #         '2026-10-30 03:05:00', '2026-10-30 06:06:00',
       #        '2026-10-30 06:26:00', '2026-10-30 12:29:00',
        #       '2026-10-30 12:30:00', '2026-10-30 22:05:00',
         #      '2026-10-31 04:36:00', '2026-10-31 08:14:00',
          #     '2026-10-31 17:25:00', '2026-10-31 22:39:00'],
           #   dtype='datetime64[us]', name='fecha', length=280, freq=None)
#Index(['id_pedido', 'id_cliente', 'id_producto', 'hora', 'unidades',
 #      'descuento', 'metodo_pago', 'estado'],
   #   dtype='str')


#1.3 Estadísticas y nulos. Escribe  qué problemas ves en los datos.
print(pedidos.describe())
print(pedidos.isnull().sum())     # energia_kwh: 6
# Problemas detectados en los datos:
# Hay 7 valores nulos en descuento'
# unidades presenta un valor máximo muy alto (250) con desviación típica ~14.87, lo que sugiere un posible outlier o error de registro.

#PARTE 2  Limpieza y columnas nuevas
#2.1 Muestra  pedido imposible (más de 100). cliente confirma que en realidad pidió 2: corrige y comprueba.
print (pedidos[pedidos["unidades"] > 100])
#                   id_pedido id_cliente  ... metodo_pago    estado
#fecha                                     ...                      
#2026-10-22 06:19:00    PD0237       C032  ...     tarjeta  devuelto
fila = pedidos[pedidos["unidades"] > 100].index[0]
pedidos.at[fila, "unidades"] = 2
print(pedidos.loc[fila, "unidades"])#2

#2.2 elimina filas con valores nulos y compara nºfilas con nºpedidos. 
sin_nulos = pedidos.dropna()
print(sin_nulos.shape, pedidos.shape) #(273, 8) (280, 8)
print(pedidos[pedidos["descuento"].isnull()])
pedidos["descuento"] = pedidos["descuento"].fillna(0)
print(pedidos.shape)                                  
print(pedidos.isnull().sum()) #0

# 2.3 Clasificar pedidos según unidades en tipo_pedido
pedidos["tipo_pedido"] = np.where(
    pedidos["unidades"] == 1,
    "individual",
    np.where(pedidos["unidades"].isin([2, 3]), "pequeño", "grande"),
)
print(pedidos["tipo_pedido"].value_counts())
#tipo_pedido ¿Cuántos pedidos hay de cada tipo? individual: 106, pequeño: 96, grande: 78

# PARTE 3 · Selección e indexación
#3.1 Seleccionar columnas 
print(pedidos["metodo_pago"])
print(pedidos.metodo_pago)
print(pedidos.loc[:, ["id_producto", "unidades"]])

# fecha
#2026-09-01 11:54:00    tarjeta
#2026-09-01 20:23:00     paypal
#2026-09-02 03:51:00     paypal
#2026-09-03 05:38:00    tarjeta
#2026-09-03 10:54:00    tarjeta
#2026-10-30 22:05:00     paypal
#2026-10-31 04:36:00     paypal
#2026-10-31 08:14:00    tarjeta
#2026-10-31 17:25:00    tarjeta
#2026-10-31 22:39:00    tarjeta
#Name: metodo_pago, Length: 280, dtype: str
#fecha
#2026-09-01 11:54:00    tarjeta
#2026-09-01 20:23:00     paypal
#2026-09-02 03:51:00     paypal
#2026-09-03 05:38:00    tarjeta
#2026-09-03 10:54:00    tarjeta
#2026-10-30 22:05:00     paypal
#2026-10-31 04:36:00     paypal
#2026-10-31 08:14:00    tarjeta
#2026-10-31 17:25:00    tarjeta
#2026-10-31 22:39:00    tarjeta
#Name: metodo_pago, Length: 280, dtype: str
#                    id_producto  unidades
#fecha                                    
#2026-09-01 11:54:00         P07         1
#2026-09-01 20:23:00         P01         2
#2026-09-02 03:51:00         P03         2
#2026-09-03 05:38:00         P06         1
#2026-09-03 10:54:00         P03         1
#2026-10-30 22:05:00         P09         3
#2026-10-31 04:36:00         P09         2
#2026-10-31 08:14:00         P05         4
#2026-10-31 17:25:00         P01         4
#2026-10-31 22:39:00         P03         2

# 3.2 Muestra posiciones 10 a 14 . ¿Cuántos pedidos hubo en la primera quincena de octubre (del 1 al 15)? Muestra  identificador y  método de pago de los pedidos del fin de semana del 12 y 13 de septiembre.
print(pedidos[10:15])
primera_quincena = pedidos["2026-10-01":"2026-10-15"]
print(primera_quincena.shape)                         
print(pedidos.loc["2026-09-12":"2026-09-13", ["id_pedido", "metodo_pago"]])

#                    id_pedido id_cliente id_producto  ... metodo_pago     estado tipo_pedido
#fecha                                                 ...                                   
#2026-09-04 08:26:00    PD0011       C001         P09  ...     tarjeta  entregado  individual
#2026-09-04 08:50:00    PD0012       C039         P02  ...      paypal  entregado  individual
#2026-09-04 18:36:00    PD0013       C016         P07  ...     tarjeta  entregado      grande
#2026-09-05 00:31:00    PD0014       C024         P10  ...      paypal  entregado      grande
#2026-09-05 00:48:00    PD0015       C018         P10  ...     tarjeta  entregado      grande

#[5 rows x 9 columns]
#(62, 9)
#                   id_pedido metodo_pago
#fecha                                    
#2026-09-12 09:07:00    PD0048      paypal
#2026-09-12 20:14:00    PD0049      paypal
#2026-09-13 02:39:00    PD0050     tarjeta
#2026-09-13 04:56:00    PD0051     tarjeta
#2026-09-13 08:40:00    PD0052     tarjeta
#2026-09-13 08:46:00    PD0053       bizum
#2026-09-13 14:01:00    PD0054      paypal
#2026-09-13 16:43:00    PD0055     tarjeta
#2026-09-13 23:38:00    PD0056     tarjeta

#3.3 Selección por posición
print(pedidos.iloc[00]) # muestra el primer pedido 
print(pedidos.iloc[270:280, 1:4]) #los 10 últimos, solo las columnas de posiciones 1 a 3.

#id_pedido          PD0001
#id_cliente           C040
#id_producto           P07
#hora                   11
#unidades                1
#descuento             0.0
#metodo_pago       tarjeta
#estado          entregado
#tipo_pedido    individual
#Name: 2026-09-01 11:54:00, dtype: object
#                   id_cliente id_producto  hora
#fecha                                           
#2026-10-30 03:05:00       C011         P07     3
#2026-10-30 06:06:00       C024         P06     6
#2026-10-30 06:26:00       C018         P09     6
#2026-10-30 12:29:00       C018         P08    12
#2026-10-30 12:30:00       C013         P02    12
#2026-10-30 22:05:00       C028         P09    22
#2026-10-31 04:36:00       C039         P09     4
#2026-10-31 08:14:00       C039         P05     8
#2026-10-31 17:25:00       C037         P01    17
#2026-10-31 22:39:00       C038         P03    22

# 3.4 Cambiar el índice, at y ordenar 
por_id = pedidos.reset_index()
por_id = por_id.set_index("id_pedido") #rea por_id, una copia de pedidos con id_pedido como índice 
print(por_id.loc["PD0100"]) # Muestra todos los datos del pedido PD0100
print(por_id.at["PD0100", "metodo_pago"])#y, aparte, solo su método de pago. 
print(pedidos.sort_index(axis=1).head(3))# Muestra las 3 primeras filas de pedidos con las columnas ordenadas alfabéticamente
print(pedidos.sort_values(by="unidades", ascending=False).head(5))# los 5 pedidos con más unidades


#fecha          2026-09-21 20:04:00
#id_cliente                    C009
#id_producto                    P01
#hora                            20
#unidades                         1
#descuento                     10.0
#metodo_pago                tarjeta
#estado                   entregado
#tipo_pedido             individual
#Name: PD0100, dtype: object
#tarjeta
#                     descuento     estado  hora  ... metodo_pago tipo_pedido  unidades
#fecha                                            ...                                  
#2026-09-01 11:54:00        0.0  entregado    11  ...     tarjeta  individual         1
#2026-09-01 20:23:00       15.0  entregado    20  ...      paypal     pequeño         2
#2026-09-02 03:51:00        0.0  entregado     3  ...      paypal     pequeño         2
#[3 rows x 9 columns]
#                    id_pedido id_cliente id_producto  ... metodo_pago     estado tipo_pedido
#fecha                                                 ...                                   
#2026-09-07 21:03:00    PD0030       C039         P10  ...     tarjeta  entregado      grande
#2026-09-12 09:07:00    PD0048       C030         P07  ...      paypal  entregado      grande
#2026-09-30 11:59:00    PD0145       C014         P09  ...       bizum  entregado      grande
#2026-09-07 07:17:00    PD0025       C030         P09  ...       bizum  entregado      grande
#2026-09-07 13:50:00    PD0026       C028         P11  ...      paypal  entregado      grande
#[5 rows x 9 columns]

#PARTE 4 · Consultas con y sin query
# %% 4.1 Pedidos devueltos
a = pedidos[pedidos.estado == "devuelto"]
b = pedidos.query("estado == 'devuelto'")
print(a.shape, b.shape) 

# 4.2 Pedidos pagados con bizum de más de 2 unidades
bizum = pedidos[pedidos.metodo_pago == "bizum"]
a = bizum[bizum.unidades > 2]
bizum_q = pedidos.query("metodo_pago == 'bizum'")
b = bizum_q.query("unidades > 2")
print(a.shape, b.shape)
print(b.loc[:, ["id_pedido", "id_producto", "unidades"]])

print("Pedidos con bizum y más de 2 unidades:")
print(pedidos[(pedidos.metodo_pago == "bizum") & (pedidos.unidades > 2)][["id_pedido", "id_producto", "unidades"]])
print("con query")
print(pedidos.query("metodo_pago == 'bizum' and unidades > 2").loc[:, ["id_pedido", "id_producto", "unidades"]])

#[5 rows x 9 columns]
#(23, 9) (23, 9)
#(27, 9) (27, 9)
#                    id_pedido id_producto  unidades
#fecha                                              
#2026-09-03 18:28:00    PD0007         P02         5
#2026-09-05 21:56:00    PD0021         P05         4
#2026-09-06 07:08:00    PD0023         P09         4
#2026-09-07 07:17:00    PD0025         P09         5
#2026-09-09 04:27:00    PD0036         P02         3
#2026-09-14 08:57:00    PD0058         P01         3
#2026-09-14 20:05:00    PD0061         P10         3
#2026-09-14 20:22:00    PD0062         P07         3
#2026-09-19 09:30:00    PD0092         P04         4
#2026-09-21 22:30:00    PD0101         P02         3
#2026-09-23 06:04:00    PD0110         P06         4
#2026-09-25 17:06:00    PD0120         P04         5
#2026-09-26 07:00:00    PD0122         P07         5
#2026-09-26 13:23:00    PD0123         P05         4
#2026-09-27 00:14:00    PD0126         P03         4
#2026-09-30 11:19:00    PD0143         P01         4
#2026-09-30 11:59:00    PD0145         P09         5
#2026-10-04 00:53:00    PD0161         P04         3
#2026-10-04 01:51:00    PD0162         P03         5
#2026-10-12 10:37:00    PD0200         P01         5
#2026-10-17 03:50:00    PD0214         P01         3
#2026-10-17 20:19:00    PD0217         P02         5
#2026-10-19 18:31:00    PD0226         P07         5
#2026-10-20 05:17:00    PD0229         P02         5
#2026-10-27 22:19:00    PD0261         P10         3
#2026-10-28 02:04:00    PD0262         P04         5
#2026-10-29 16:59:00    PD0268         P02         4
#Pedidos con bizum y más de 2 unidades:
#                    id_pedido id_producto  unidades
#fecha                                              
#2026-09-03 18:28:00    PD0007         P02         5
#2026-09-05 21:56:00    PD0021         P05         4
#2026-09-06 07:08:00    PD0023         P09         4
#2026-09-07 07:17:00    PD0025         P09         5
#2026-09-09 04:27:00    PD0036         P02         3
#2026-09-14 08:57:00    PD0058         P01         3
#2026-09-14 20:05:00    PD0061         P10         3
#2026-09-14 20:22:00    PD0062         P07         3
#2026-09-19 09:30:00    PD0092         P04         4
#2026-09-21 22:30:00    PD0101         P02         3
#2026-09-23 06:04:00    PD0110         P06         4
#2026-09-25 17:06:00    PD0120         P04         5
#2026-09-26 07:00:00    PD0122         P07         5
#2026-09-26 13:23:00    PD0123         P05         4
#2026-09-27 00:14:00    PD0126         P03         4
#2026-09-30 11:19:00    PD0143         P01         4
#2026-09-30 11:59:00    PD0145         P09         5
#2026-10-04 00:53:00    PD0161         P04         3
#2026-10-04 01:51:00    PD0162         P03         5
#2026-10-12 10:37:00    PD0200         P01         5
#2026-10-17 03:50:00    PD0214         P01         3
#2026-10-17 20:19:00    PD0217         P02         5
#2026-10-19 18:31:00    PD0226         P07         5
#2026-10-20 05:17:00    PD0229         P02         5
#2026-10-27 22:19:00    PD0261         P10         3
#2026-10-28 02:04:00    PD0262         P04         5
#2026-10-29 16:59:00    PD0268         P02         4
#con query
#                    id_pedido id_producto  unidades
#fecha                                              
#2026-09-03 18:28:00    PD0007         P02         5
#2026-09-05 21:56:00    PD0021         P05         4
#2026-09-06 07:08:00    PD0023         P09         4
#2026-09-07 07:17:00    PD0025         P09         5
#2026-09-09 04:27:00    PD0036         P02         3
#2026-09-14 08:57:00    PD0058         P01         3
#2026-09-14 20:05:00    PD0061         P10         3
#2026-09-14 20:22:00    PD0062         P07         3
#2026-09-19 09:30:00    PD0092         P04         4
#2026-09-21 22:30:00    PD0101         P02         3
#2026-09-23 06:04:00    PD0110         P06         4
#2026-09-25 17:06:00    PD0120         P04         5
#2026-09-26 07:00:00    PD0122         P07         5
#2026-09-26 13:23:00    PD0123         P05         4
#2026-09-27 00:14:00    PD0126         P03         4
#2026-09-30 11:19:00    PD0143         P01         4
#2026-09-30 11:59:00    PD0145         P09         5
#2026-10-04 00:53:00    PD0161         P04         3
#2026-10-04 01:51:00    PD0162         P03         5
#2026-10-12 10:37:00    PD0200         P01         5
#2026-10-17 03:50:00    PD0214         P01         3
#2026-10-17 20:19:00    PD0217         P02         5
#2026-10-19 18:31:00    PD0226         P07         5
#2026-10-20 05:17:00    PD0229         P02         5
#2026-10-27 22:19:00    PD0261         P10         3
#2026-10-28 02:04:00    PD0262         P04         5
#2026-10-29 16:59:00    PD0268         P02         4

# 4.3 Pedidos con un 15 % de descuento de los productos P03 o P07. Muestra el
#identificador, el producto, las unidades y el descuento. ¿Cuántos son?
descuento15 = pedidos.query("descuento == 15")
p03 = descuento15.query("id_producto == 'P03'")
p07 = descuento15.query("id_producto == 'P07'")
c = pd.concat([p03, p07])                             # el "o" se resuelve uniendo los dos resultados
print(c.loc[:, ["id_pedido", "id_producto", "unidades", "descuento"]])     # 9 pedidos (4 de P03 y 5 de P07)
print(c.shape)
print("Número de pedidos:", len(c))

#                    id_pedido id_producto  unidades  descuento
#fecha                                                         
#2026-09-10 01:04:00    PD0040         P03         1       15.0
#2026-10-05 11:25:00    PD0167         P03         4       15.0
#2026-10-08 00:46:00    PD0180         P03         2       15.0
#2026-10-08 00:57:00    PD0181         P03         2       15.0
#2026-10-08 13:55:00    PD0182         P03         1       15.0
#2026-10-26 16:07:00    PD0255         P03         1       15.0
#2026-09-13 14:01:00    PD0054         P07         3       15.0
#2026-09-14 20:22:00    PD0062         P07         3       15.0
#2026-10-09 11:59:00    PD0189         P07         2       15.0
#2026-10-19 18:31:00    PD0226         P07         5       15.0
#Número de pedidos: 10

#4.4 ¿Cuántos pedidos hizo el cliente C999? ¿Cuántos pedidos son del producto P13? (Más adelanteverás por qué son especiales.)
print(pedidos.query("id_cliente == 'C999'").shape)    # 3
print(pedidos[pedidos.id_producto == "P13"].shape)  # 5

#PARTE 5 · Combinar tablas con merge
#5.1 Carga productos.csv y clientes.csv. 
# ¿Cuántos pedidos tienen un producto que no está en el catálogo? 5
# ¿Qué producto es? P013
productos = pd.read_csv("datos/productos.csv")
clientes = pd.read_csv("datos/clientes.csv")
ped = pedidos.reset_index()
completo = ped.merge(productos, how="left", on="id_producto", indicator=True)

print(completo["_merge"].value_counts())
no_catalogo = completo[completo["_merge"] == "left_only"]
print(no_catalogo.loc[:, ["id_pedido", "id_producto", "unidades"]])
print("Producto(s) fuera del catálogo:", no_catalogo["id_producto"].unique())
#_merge
#both          275
#left_only       5
#right_only      0
#Name: count, dtype: int64
#    id_pedido id_producto  unidades
#85     PD0086         P13         3
#138    PD0139         P13         1
#158    PD0159         P13         4
#177    PD0178         P13         2
#253    PD0254         P13         2
#Producto(s) fuera del catálogo: <StringArray>
#['P13']
#Length: 1, dtype: str

#5.2 Añade a completo los datos de su cliente, también conservando todos los pedidos. 
# ¿Cuántos pedidos se quedan sin tipo de cliente? 3
# Rellena esos valores con "invitado". 
# Añade la columna importe (unidades × precio, aplicando el descuento) y vuelve a poner la fecha como índice.

completo = pd.merge(completo, clientes, on="id_cliente", how="left")
print(completo.isnull().sum())                       
completo["tipo_cliente"] = completo["tipo_cliente"].fillna("invitado")
completo["importe"] = completo["unidades"] * completo["precio"] * (1 - completo["descuento"] / 100)
completo = completo.set_index("fecha")
print(completo.head())

#                    id_pedido id_cliente id_producto  ... tipo_cliente provincia  importe
#fecha                                                 ...                                
#2026-09-01 11:54:00    PD0001       C040         P07  ...      premium   Sevilla    19.90
#2026-09-01 20:23:00    PD0002       C019         P01  ...     estandar    Málaga   203.83
#2026-09-02 03:51:00    PD0003       C022         P03  ...     estandar    Málaga    49.80
#2026-09-03 05:38:00    PD0004       C007         P06  ...     estandar   Granada    49.90
#2026-09-03 10:54:00    PD0005       C003         P03  ...     estandar   Granada    24.90

#5.3 Con otra combinación, averigua qué producto del catálogo no se ha vendido ni una vez.
derecha = pd.merge(ped, productos, on="id_producto", how="right", indicator=True)
print(derecha[derecha["_merge"] == "right_only"].loc[:, ["id_producto", "nombre", "precio"]]) 
#Es P12: Bastones trekking (precio 39.9)

#PARTE 6 · Dividir, unir, agrupar y resumir
# %% 6.1 Dividir en trozos y volver a unir 
trozos = [completo[:100], completo[100:200], completo[200:]]
print(trozos[0].shape, trozos[1].shape, trozos[2].shape)
reunido = pd.concat(trozos)
print(reunido.shape == completo.shape)             

completadas = completo.query("estado == 'entregado'")
interrumpidas = completo.query("estado == 'devuelto'")
por_estado = pd.concat([completadas, interrumpidas])
print(completadas.shape, interrumpidas.shape, por_estado.shape)  


#6.2 Calcula las unidades vendidas y el importe total por categoría,
print(completo.loc[:, ["categoria", "unidades", "importe"]].groupby("categoria").sum())
#categoria         unidades    importe                
#ciclismo        172   7303.220
#montaña          21   1398.000
#natacion        188   3898.230
#running         291  28320.005

#  las unidades vendidas por categoría y método de pago, 
print(completo.loc[:, ["categoria", "metodo_pago","unidades"]].groupby(["categoria", "metodo_pago"]).sum())
                       
# categoria metodo_pago    unidades  
#ciclismo  bizum              33
#          paypal             55
#          tarjeta            84
#montaña   bizum               4
#          paypal             10
#          tarjeta             7
#natacion  bizum              31
#          paypal             55
#          tarjeta           102
#running   bizum              81
#          paypal             56
#          tarjeta           154

# y cuántos pedidos hay de cada tipo de cliente.
print(completo["tipo_cliente"].value_counts())

#tipo_cliente
#estandar    184
#premium      93
#invitado      3


#6.3 Escribe una función que clasifique un pedido según su importe. 

def nivel(importe):
    if importe < 30: #"bajo" (menos de 30 €)
        return "bajo"
    elif importe < 100: #"medio" (de 30 a 100 €)
        return "medio"
    else:
        return "alto" #"alto" (100 € o más)
#Aplícala para crear la columna gasto y cuenta cuántos pedidos hay de cada nivel.
completo["nivel"] = completo["importe"].apply(nivel)
print(completo["nivel"].value_counts())               # alto 111, medio 109, bajo 60

#6.4 Calcula la media de las unidades, el descuento y el importe. Muestra también las estadísticas
#básicas de esas tres columnas, con las columnas en filas y las estadísticas en columnas.
cols_64 = ["unidades", "descuento", "importe"]
print(completo.loc[:, cols_64].mean())
print(completo.loc[:, cols_64].describe().T)
#           count        mean         std    min    25%     50%     75%     max
#unidades   280.0    2.442857    1.467797  1.000   1.00   2.000    4.00     5.0
#descuento  280.0    4.660714    5.435437  0.000   0.00   5.000   10.00    15.0
#importe    275.0  148.798018  200.628815  8.415  35.64  75.905  179.82  1245.0

#PARTE 7 · Consultas SQL con DataFrame
#7.1 consultas sobre una tabla
#a) SELECT UPPER(nombre), precio FROM productos WHERE categoria = 'running' ORDER BY precio
a = productos["categoria"] == "running"
r = productos.loc[a, ["nombre", "precio"]].sort_values("precio")
r["nombre"] = r["nombre"].str.upper()
print(r)
#               nombre  precio
#2    CAMISETA TÉCNICA    24.9
#1  ZAPATILLAS ASFALTO    99.9
#0    ZAPATILLAS TRAIL   119.9
#3           RELOJ GPS   249.0

#b )SELECT id_pedido, TO_CHAR(fecha, 'DD/MM/YYYY HH24:MI') AS momento, id_cliente, unidades FROM pedidos WHERE metodo_pago = 'paypal' AND estado = 'devuelto'
b = pedidos.query("metodo_pago == 'paypal' and estado == 'devuelto'").loc[:, ["id_pedido", "id_cliente", "unidades"]].copy()
b["momento"] = b.index.strftime("%d/%m/%Y")
print(b[["id_pedido", "momento", "id_cliente", "unidades"]])        

#fecha               id_pedido   momento      id_cliente   unidades                                                     
#2026-09-12 20:14:00    PD0049  12/09/2026       C007         2
#2026-09-18 22:13:00    PD0086  18/09/2026       C010         3
#2026-09-19 08:45:00    PD0091  19/09/2026       C001         1
#2026-10-20 19:40:00    PD0230  20/10/2026       C017         1
#2026-10-27 02:44:00    PD0256  27/10/2026       C038         4                                                                       # 6 recargas

#c) SELECT * FROM clientes WHERE provincia IN ('Granada', 'Sevilla')
c = clientes["provincia"].isin(['Granada', 'Sevilla'])
print(clientes.loc[c, :])

#    id_cliente tipo_cliente provincia
#2        C003     estandar   Granada
#4        C005      premium   Sevilla
#5        C006     estandar   Granada
#6        C007     estandar   Granada
#10       C011      premium   Sevilla
#13       C014     estandar   Sevilla
#16       C017      premium   Sevilla
#20       C021      premium   Granada
#25       C026     estandar   Sevilla
#30       C031      premium   Granada
#35       C036     estandar   Granada
#37       C038     estandar   Granada
#39       C040      premium   Sevilla

#d)SELECT * FROM productos ORDER BY precio DESC LIMIT 3
d = productos.sort_values("precio", ascending=False).head(3)
print(d)
#  id_producto              nombre categoria  precio
#3         P04           Reloj GPS   running   249.0
#0         P01    Zapatillas trail   running   119.9
#1         P02  Zapatillas asfalto   running    99.9

#e) SELECT id_cliente, SUM(unidades) FROM pedidos GROUP BY id_cliente HAVING SUM(unidades) > 30
e = completo.groupby("id_cliente")["unidades"].sum().reset_index()
e = e[e["unidades"] > 30]
print(e)
#   id_cliente  unidades
#6        C007        32
#11       C012        31
#29       C030        39
#37       C038        31

#7.2 Consultas con varias tablas.
#a) SELECT p.id_pedido, pr.nombre, p.unidades FROM pedidos p JOIN productos pr ON p.id_producto = pr.id_producto
# WHERE pr.nombre LIKE 'Zapatillas%'
a2 = completo[completo["nombre"].str.startswith("Zapatillas")].loc[:, ["id_pedido", "nombre", "unidades"]]
print(a2)
#PEGO LOS PRIMEROS QUE ES MUY LARGO
# fecha               id_pedido              nombre  unidades                                                     
#2026-09-01 20:23:00    PD0002    Zapatillas trail         2
#2026-09-03 18:28:00    PD0007  Zapatillas asfalto         5
#2026-09-04 08:50:00    PD0012  Zapatillas asfalto         1
#2026-09-05 11:15:00    PD0017  Zapatillas asfalto         1
#...

#b) SELECT c.provincia, COUNT(*) FROM pedidos p JOIN clientes c ON p.id_cliente = c.id_cliente
# GROUP BY c.provincia
b2 = completo.groupby("provincia").size().reset_index(name="count")
print(b2)
#  provincia  count
#0     Cádiz     13
#1   Córdoba     37
#2   Granada     58
#3    Málaga    131
#4   Sevilla     38

#c) SELECT c.tipo_cliente, ROUND(AVG(p.unidades), 2) 
# FROM pedidos p JOIN clientes c ON p.id_cliente = c.id_cliente GROUP BY c.tipo_cliente
c2 = completo.groupby("tipo_cliente")["unidades"].mean().round(2).reset_index(name="avg_unidades")
print(c2)
#  tipo_cliente  avg_unidades
#0     estandar          2.45
#1     invitado          2.33
#2      premium          2.44

#d) SELECT nombre FROM productos pr WHERE EXISTS (SELECT 1 FROM pedidos p
# WHERE p.id_producto = pr.id_producto AND p.estado = 'devuelto' AND p.unidades >= 3)
d2 = completo[(completo["estado"] == "devuelto") & (completo["unidades"] >= 3)]["nombre"].unique()
print(d2)
#<StringArray>
#[                nan, 'Zapatillas asfalto',          'Luces LED',
#   'Camiseta técnica',     'Gorro silicona',            'Culotte']
#Length: 6, dtype: str

#e) SELECT id_cliente, provincia FROM clientes WHERE id_cliente NOT IN (SELECT p.id_cliente
# FROM pedidos p JOIN productos pr ON p.id_producto = pr.id_producto
#WHERE pr.categoria = 'running')
e2 = clientes[~clientes["id_cliente"].isin(completo[completo["categoria"] == "running"]["id_cliente"])]
print(e2)
#   id_cliente tipo_cliente provincia
#23       C024     estandar    Málaga
#24       C025     estandar    Málaga
#30       C031      premium   Granada