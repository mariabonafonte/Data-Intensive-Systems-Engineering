import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

#PARTE 1 Carga y exploración 
#1.1 carga ficheros y unelos en DataFrame pedidos. Fecha como índice y ordena 
enero = pd.read_csv("datos/viajes_enero.csv")
febrero = pd.read_csv("datos/viajes_febrero.csv")
viajes = pd.concat([enero, febrero])
viajes["fecha"] = pd.to_datetime(viajes["fecha"])
viajes = viajes.set_index("fecha")
viajes =viajes.sort_index()
print(enero.shape, febrero.shape, viajes.shape) #(177, 8) (143, 8) (320, 7)

#1.2  Muestra 5 primeros pedidos, 3 últimos, índice y nombres columnas.
print(viajes.head(5))
# fecha              id_viaje id_linea id_tarjeta  hora  paradas  retraso_min medio_pago                                                                               
#2026-01-01 08:44:00    V0001      L08       T022     8        3          4.5    tarjeta
#2026-01-01 12:58:00    V0002      L05       T026    12       12          7.5    tarjeta
#2026-01-01 13:03:00    V0003      L01       T026    13        8          6.8   efectivo
#2026-01-01 13:44:00    V0004      L05       T031    13        8          8.0      movil
#2026-01-01 15:51:00    V0005      L06       T003    15        5          8.5    tarjeta

print(viajes.tail(3))
#fecha               id_viaje id_linea id_tarjeta  hora  paradas  retraso_min medio_pago                                                                                
#2026-02-27 21:59:00    V0318      L09       T040    21        9          4.9    tarjeta
#2026-02-28 13:05:00    V0319      L05       T027    13        2          7.8    tarjeta
#2026-02-28 22:11:00    V0320      L05       T020    22        6          7.4    tarjeta

print(viajes.index)
print(viajes.columns)

#DatetimeIndex(['2026-01-01 08:44:00', '2026-01-01 12:58:00',
    #           '2026-01-01 13:03:00', '2026-01-01 13:44:00',
    #           '2026-01-01 15:51:00', '2026-01-01 15:53:00',
    #           '2026-01-01 19:04:00', '2026-01-02 06:59:00',
    #           '2026-01-02 10:25:00', '2026-01-02 13:37:00',
    #           ...
    #           '2026-02-26 22:20:00', '2026-02-26 23:44:00',
    #           '2026-02-27 06:26:00', '2026-02-27 09:41:00',
    #           '2026-02-27 15:27:00', '2026-02-27 16:36:00',
    #           '2026-02-27 21:41:00', '2026-02-27 21:59:00',
    #           '2026-02-28 13:05:00', '2026-02-28 22:11:00'],
    #          dtype='datetime64[us]', name='fecha', length=320, freq=None)
#Index(['id_viaje', 'id_linea', 'id_tarjeta', 'hora', 'paradas', 'retraso_min','medio_pago'], dtype='str')

#1.3 Estadísticas y nulos. Escribe  qué problemas ves en los datos.
print(viajes.describe()) 
#             hora     paradas  retraso_min
#count  320.000000  320.000000   312.000000
#mean    14.868750    9.284375     5.430128
#std      5.201425    4.988112    27.101606
#min      6.000000    1.000000     0.000000
#25%     10.000000    5.000000     1.700000
#50%     15.000000    9.000000     3.100000
#75%     19.000000   13.000000     5.925000
#max     23.000000   18.000000   480.000000

print(viajes.isnull().sum()) # todos 0 menos retraso_min que tiene 8 nulos
# Problemas detectados en los datos:
# 1. La columna "retraso_min" tiene 8 valores nulos, lo que podría afectar a los análisis estadísticos y visualizaciones.
# 2. Puede haber presencia de valores atípicos o extremos, como el valor máximo de 480 minutos, que es extremo.

#PARTE 2  Limpieza y columnas nuevas
#2.1 Haz viaje con retraso imposible (+ 60min). Sustituye por Null. Cuantos hay ahora en retraso_min?

#2.2 Crea sin_nulos y compara nº de filas con el de viajes. rellena los nulos de retraso_min,  teniendo en cuenta que cada línea tiene su propio nivel de retraso:


# (Hecho en la pizarra)

# Calcula el retraso medio de toda la columna y, recorriendo las líneas con un bucle for, el retraso medio de cada línea.
sin_nulos = viajes.dropna()
# Muestra los viajes sin retraso. ¿De qué líneas son? L08, L05, L01 L06, L04, L09
print(sin_nulos)

# Calcula el retraso medio de toda la columna 
print("Media todas las columnas:", viajes["retraso_min"].mean()) #Media todas las columnas: 5.430128205128205

# recorriendo las líneas con un bucle for, el retraso medio de cada línea.
for linea in np.unique(viajes["id_linea"].dropna()):
  media_linea = viajes.loc[viajes["id_linea"] == linea, "retraso_min"].mean()
  print(f"Línea {linea} -> media retraso_min: {media_linea}")
#Línea L01 -> media retraso_min: 2.5524999999999998
#Línea L02 -> media retraso_min: 2.614705882352941
#Línea L03 -> media retraso_min: 2.9617021276595743
#Línea L04 -> media retraso_min: 1.77
#Línea L05 -> media retraso_min: 17.2734693877551
#Línea L06 -> media retraso_min: 8.330000000000002
#Línea L07 -> media retraso_min: 1.6303030303030304
#Línea L08 -> media retraso_min: 2.056756756756757
#Línea L09 -> media retraso_min: 4.883333333333334
#Línea L11 -> media retraso_min: 3.625

# Divide viajes en un trozo por línea, rellena los nulos de cada trozo con la media de su línea vuelve a unir todos los trozos en viajes, ordénalo por fecha y comprueba que ya no quedan nulos.
trozos=[]
for linea in np.unique(viajes["id_linea"]):
    trozo = viajes[viajes["id_linea"] == linea].copy()
    trozo["retraso_min"] = trozo["retraso_min"].fillna(trozo["retraso_min"].mean())
    trozos.append(trozo)

viajes = pd.concat(trozos)
viajes = viajes.sort_index()
# Explica en un comentario por qué es mejor rellenar así que con la media de toda la columna.
# Cada línea tiene características distintas por lo que rellenar con la media de su propia línea respeta mejor el comportamiento real

#2.3 Añade columna puntualidad: "puntual" si retraso<=2min, "leve" 2-5min, y "retrasado" +5 minutos. 
viajes["puntualidad"] = np.where(
    viajes["retraso_min"] <= 2,
    "puntual",
    np.where(viajes["retraso_min"] <= 5, "leve", "retrasado"),
)
print(viajes["puntualidad"].value_counts())
# ¿Cuántos viajes hay decada tipo? leve: 123, puntual: 100 y retrasado: 97

# PARTE 3 · Selección e indexación
#3.1 Muestra columna paradas de  dos formas posibles y solo las columnas id_linea y retraso_min de todos los viajes.
print(viajes["paradas"])
print(viajes.paradas)
#fecha
# 2026-01-01 08:44:00     3
# 2026-01-01 12:58:00    12
# 2026-01-01 13:03:00     8
# 2026-01-01 13:44:00     8
# 2026-01-01 15:51:00     5
#...

print(viajes.loc[:, ["id_linea", "retraso_min"]])
#fecha                 id_linea  retraso_min                                  
#2026-01-01 08:44:00      L08     4.500000
#2026-01-01 12:58:00      L05     7.500000
#2026-01-01 13:03:00      L01     6.800000
#2026-01-01 13:44:00      L05     8.000000
#2026-01-01 15:51:00      L06     8.500000
#...                      ...          ...

#3.2 Muestra los viajes del 20 a 24. ¿Cuántos viajes hubo en la semana del 2 al 8 de febrero? 38
# Muestra la línea y el medio de pago de los viajes del 6 de enero.
print(viajes[20:24])
primera_semana = viajes["2026-02-02":"2026-02-08"]
print(primera_semana.shape) #(38,8)                        
print(viajes.loc["2026-01-6", ["id_linea", "medio_pago"]])

#fecha              id_viaje id_linea id_tarjeta  hora  paradas  retraso_min medio_pago puntualidad                                                                                     
#2026-01-04 12:09:00    V0021      L04       T030    12       10          2.8   efectivo        leve
#2026-01-04 16:24:00    V0022      L08       T999    16       11          2.2      movil        leve
#2026-01-04 22:19:00    V0023      L06       T003    22        3          7.4    tarjeta   retrasado
#2026-01-04 23:40:00    V0024      L01       T029    23       12          1.8    tarjeta     puntual
# fecha              id_linea medio_pago                         
#2026-01-06 12:18:00      L06    tarjeta
#2026-01-06 15:40:00      L05    tarjeta
#2026-01-06 17:45:00      L04    tarjeta
#2026-01-06 19:55:00      L07   efectivo
#2026-01-06 20:14:00      L02    tarjeta
#2026-01-06 22:39:00      L06    tarjeta


# 3.3 
print(viajes.iloc[100]) # Muestra el viaje de la posición 100
#id_viaje: V0101, id_linea: L05, id_tarjeta: T999, hora: 9, paradas:7, retraso_min:9.4, medio_pago:tarjeta, puntualidad:retrasado
print(viajes.iloc[0:10, 2:5]) #los 10 primeros, solo las columnas de posiciones 2 a 4.
#fecha                id_tarjeta  hora  paradas                                
#2026-01-01 08:44:00       T022     8        3
#2026-01-01 12:58:00       T026    12       12
#2026-01-01 13:03:00       T026    13        8
#2026-01-01 13:44:00       T031    13        8
#2026-01-01 15:51:00       T003    15        5
#2026-01-01 15:53:00       T043    15       11
#2026-01-01 19:04:00       T014    19       12
#2026-01-02 06:59:00       T002     6       10
#2026-01-02 10:25:00       T036    10        9
#2026-01-02 13:37:00       T036    13       13

# 3.4 Crea por_id
por_id = viajes.reset_index()
por_id = por_id.set_index("id_viaje") #una copia de viajes con id_viaje como índice 
print(por_id.loc["V0200"]) # Muestra todos los datos del pedido V0200: 
#fecha:2026-02-05 21:42:00, idd_linea:L03 id_tarjeta:T028, hora:21, paradas:12, 
# retraso_min:2.7, medio_pago:tarjeta, puntualidad:leve, Name: V0200, dtype: object

print(por_id.at["V0200", "id_linea"])#y, aparte, solo su linea : L03

print(por_id.sort_values(by="retraso_min", ascending=False).head(5))# los 5 viajes con más retraso
# id_viaje   fecha            id_linea id_tarjeta  hora  paradas  retraso_min medio_pago puntualidad                                                                                      
#V0030    2026-01-05 20:48:00      L05       T047    20       17   480.000000    tarjeta   retrasado
#V0193    2026-02-04 14:56:00      L05       T025    14        8    17.273469      movil   retrasado
#V0097    2026-01-18 17:23:00      L06       T039    17        8    11.500000   efectivo   retrasado
#V0013    2026-01-03 08:05:00      L06       T041     8       10    11.400000    tarjeta   retrasado
#V0180    2026-02-01 18:56:00      L05       T049    18        1    11.400000    tarjeta   retrasado



# PARTE 5 · Combinar tablas con merge (hecho en clase completo )
#5.1 (En el examen no entra - muy complejo)
#lineas = pd.read_csv("datos/lineas.csv")
#tarjetas = pd.read_csv("datos/tarjetas.csv")
#via = viajes.reset_index()
#completo = pd.merge(via, lineas, on="id_linea",
#                    how="left", indicator=True)
#print("Completo:")
#print(completo.head(10))
#print("Número de viajes de líneas que no están en el catálogo")
#print(completo("_merge").value_counts())
#print("Lineas que no estan en el catálogo")
#print(completo[completo["_merge"]=="left_only"].
# loc[:,["id_viaje", "id_linea", "recorrido"]])

#5.2 Añadir datos de la tarjeta e importe (mas tipico, mas sencillito)
#completo = pd.merge(Completo,tarjetas, on="id_tarjeta", how="left")
#print(completo.isnull().sum())
#completo["tipo_tarjeta"] = completo["tipo_tarjeta"].fillna("turista")
#completo["descuento"] = completo["descuento"].fillna(0)
#completo["importe"] = completo["tarifa"]*(1-completo["descuento"])
#completo = completo.set_index("fecha")
#completo = completo.sort_index()

#5.3 (en el examen no cae nada de utilizar indicato, demasiado complejo)
# (CAE PARECIDO AL 5.2: hacer merge y rellenar datos)
#derecha = pd.merge(via, linea, on="id_linea", how="right", indicator=True)
#print(derecha[derecha["_merge"] == "right_only"].loc[:, ["id_linea", "numero", "recorrido"]])