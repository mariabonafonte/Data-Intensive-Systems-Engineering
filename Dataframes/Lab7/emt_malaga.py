#MARIA BONAFONTE SANCHEZ

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

#PARTE 4 · Consultas con y sin query

#En 4.1 y 4.2 resuelve cada consulta de las dos formas: con una condición entre corchetes y con
#4.1 Viajes pagados en efectivo. ¿Cuántos hay? 25
efectivo = viajes[viajes.medio_pago == "efectivo"]
efectivo_q = viajes.query("medio_pago == 'efectivo'")
print(efectivo.shape, efectivo_q.shape) 

#4.2 Viajes de la línea L03 de más de 10 paradas. 
# Muestra solo su identificador, la tarjeta y las paradas.
l03 = viajes[viajes.id_linea == "L03"]
paradas = l03[l03.paradas > 10]
l03_q = viajes.query("id_linea == 'L03'")
paradas_q = l03_q.query("paradas > 10")
print(paradas_q.loc[:, ["id_viaje", "id_tarjeta", "paradas"]])
#fecha                 id_viaje id_tarjeta  paradas                                                                 
#2026-01-03 11:00:00    V0014       T004       17
#2026-01-05 22:41:00    V0033       T049       13
#2026-01-08 07:30:00    V0045       T012       13
#2026-01-09 15:07:00    V0052       T044       14
#2026-01-13 16:10:00    V0073       T026       15
#...
#2026-02-26 18:26:00    V0309       T008       17

#4.3 Con query: viajes con un retraso de más de 6 minutos en las líneas L01 o L05.
#  Muestra el identificador, la línea, la hora y el retraso. ¿Cuántos son? 44
linea_l01 = viajes.query("id_linea == 'L01'")
linea_l05 = viajes.query("id_linea == 'L05'")
l01_l05 = pd.concat([linea_l01,linea_l05])   
retraso = l01_l05.query("retraso_min > 6")
print(retraso.loc[:, ["id_viaje", "id_linea", "hora", "retraso_min"]])
 #fecha              id_viaje id_linea  hora  retraso_min                                              
#2026-01-01 13:03:00    V0003      L01    13     6.800000
#2026-01-01 12:58:00    V0002      L05    12     7.500000
#2026-01-01 13:44:00    V0004      L05    13     8.000000
#2026-01-04 09:32:00    V0019      L05     9     9.500000
#...
#2026-02-28 22:11:00    V0320      L05    22     7.400000
print(retraso.shape) #(44,8) => 44 viajes

#4.4 ¿Cuántos viajes se hicieron con la tarjeta T999? 4
t_999 = viajes.query("id_tarjeta == 'T999'")
print(t_999.shape)

# ¿Cuántos viajes son de la línea L11? 4
l11 = viajes.query("id_linea == 'L11'")
print(l11.shape)

# PARTE 5 · Combinar tablas con merge (hecho en clase completo )
#5.1 (En el examen no entra - muy complejo)
lineas = pd.read_csv("datos/lineas.csv")
tarjetas = pd.read_csv("datos/tarjetas.csv")
via = viajes.reset_index()
completo = pd.merge(via, lineas, on="id_linea",
                    how="left", indicator=True)
print("Completo:")
print(completo.head(10))
print("Número de viajes de líneas que no están en el catálogo")
print(completo["_merge"].value_counts())
print("Lineas que no estan en el catálogo")
print(completo[completo["_merge"]=="left_only"].
     loc[:,["id_viaje", "id_linea", "recorrido"]])

#5.2 Añadir datos de la tarjeta e importe (mas tipico, mas sencillito)
completo = pd.merge(completo,tarjetas, on="id_tarjeta", how="left")
print(completo.isnull().sum())
completo["tipo_tarjeta"] = completo["tipo_tarjeta"].fillna("turista")
completo["descuento"] = completo["descuento"].fillna(0)
completo["importe"] = completo["tarifa"]*(1-completo["descuento"])
completo = completo.set_index("fecha")
completo = completo.sort_index()

#5.3 (en el examen no cae nada de utilizar indicato, demasiado complejo)
# (CAE PARECIDO AL 5.2: hacer merge y rellenar datos)
derecha = pd.merge(via, lineas, on="id_linea", how="right", indicator=True)
print(derecha[derecha["_merge"] == "right_only"].loc[:, ["id_linea", "numero", "recorrido"]])



#PARTE 6 · Dividir, unir, agrupar y resumir
#6.1 Divide completo en tres trozos(las 110 primeras, de la 110 a la 219 y el resto) y vuelve a unirlos. 


trozos = [completo[:110], completo[110:219], completo[219:]]
print(trozos[0].shape, trozos[1].shape, trozos[2].shape) #(110, 17) (109, 17) (101, 17)
reunido = pd.concat(trozos)
# Comprueba que el resultado tiene el mismo tamaño que completo. 
print(reunido.shape == completo.shape)   #TRUE  

# Divide después completo en los viajes de enero y los de febrero seleccionando por fechas, 
# únelos y comprueba que suman todos los viajes.
enero = completo.query("fecha >= '2026-01-01' and fecha < '2026-02-01'") #177
febrero = completo.query("fecha >= '2026-02-01' and fecha < '2026-03-01'") #143
por_mes = pd.concat([enero, febrero])
print(enero.shape, febrero.shape, por_mes.shape)  #320


#6.2 Calcula las paradas recorridas y el importe total por tipo de línea, 
print(completo.loc[:, ["id_linea", "paradas", "importe"]].groupby("id_linea").sum())

# id_linea  paradas  importe                id_linea  paradas  importe 
#L01           382  -1426.6                 #L02           341  -1407.0
#L03           503  -1656.2                 #L04           192   -586.6
#L05           413  -1890.0                 #L06           257  -1316.0
#L07           330  -1703.8                 #L08           314   -771.4
#L09           196  -2240.0                 #L11            43      0.0

# el importe total por tipo de línea y tipo de tarjeta, 
print(completo.loc[:, ["id_linea", "tipo_tarjeta", "importe"]].groupby(["id_linea", "tipo_tarjeta"]).sum())
# id_linea tipo_tarjeta  importe         
#L01      estudiante     -686.0             L02      estudiante     -754.6          L07      estudiante     -754.6
#         general          32.2                         general       23.8                   general          16.8
#         jubilado       -772.8                        jubilado     -676.2                   jubilado       -966.0

#L03      estudiante     -823.2             L04      estudiante     -411.6          L08      estudiante     -617.4
#         general          35.0                      general          18.2                   general          37.8
#         jubilado       -869.4                      jubilado       -193.2                   jubilado       -193.2
#         turista           1.4                                                              turista           1.4

#L05      estudiante     -960.4             L06      estudiante     -754.6          L09      estudiante    -1176.0
#         general          35.0                      general          16.8                   general          40.0
#         jubilado       -966.0                      jubilado       -579.6                   jubilado      -1104.0
#         turista           1.4                      turista           1.4  

#L11      estudiante        0.0
#         general           0.0
#         jubilado          0.0


# y cuántos viajes hay de cada tipo de tarjeta.
print(completo["tipo_tarjeta"].value_counts())
#tipo_tarjeta: general: 166, estudiante:91, jubilado:59, turista:4


#6.3 Escribe una función que clasifique según paradas: "corto" (<5), "medio" (5-11) o "largo" (>=12). 
def trayecto(paradas):
    if paradas <5: 
        return "corto"
    elif paradas < 11: 
        return "medio"
    else:
        return "largo" 
    
# Aplícala para crear la columna trayecto y cuenta cuántos viajes hay de cada tipo.    
completo["trayecto"] = completo["paradas"].apply(trayecto)
print(completo["trayecto"].value_counts())  # largo 130, medio 119, corto 71

#6.4 Calcula la media de las paradas, el retraso y el importe de todos los viajes. 
print(completo.loc[:, ["paradas", "retraso_min", "importe"]].mean())
#paradas: 9.284375, retraso_min: 5.413409, importe: -41.131646

# Calcula también el retraso medio de los viajes de la hora punta de la mañana 
hora_punta = completo.query("hora >= 7 and hora <= 9") # (de las 7 a las 9, ambas incluidas).
print(hora_punta.loc[:, ["retraso_min"]].mean()) #retraso_min    5.244231

#PARTE 7 · Consultas SQL con DataFrame
#7.1 Consultas sobre una tabla.

#a) SELECT numero, UPPER(recorrido) FROM lineas WHERE recorrido LIKE '%Alameda%' ORDER BY recorrido
condicion_a = lineas["recorrido"].isin(["%Alameda%"])
r_a = lineas.loc[condicion_a, ["numero", "recorrido"]].sort_values("recorrido")
r_a["recorrido"] = r_a["recorrido"].str.upper()
print(r_a)

#b) SELECT id_viaje, TO_CHAR(fecha, 'DD/MM/YYYY') AS dia, hora, FLOOR(retraso_min) FROM viajes WHERE id_linea = 'L06' AND hora >= 17 AND hora <= 19
r_b = viajes.query("id_linea == 'L06' and hora >= 17 and hora <= 19").loc[:, ["id_viaje", "hora", "retraso_min"]].copy()
r_b["dia"] = r_b.index.strftime("%d/%m/%Y")
r_b["retraso_min"] = np.floor(r_b["retraso_min"])
print(r_b[["id_viaje","dia", "hora", "retraso_min"]])

# fecha               id_viaje    dia       hora  retraso_min                                                    
#2026-01-02 17:52:00    V0011  02/01/2026    17          5.0
#2026-01-18 17:23:00    V0097  18/01/2026    17         11.0
#2026-02-14 17:40:00    V0242  14/02/2026    17         11.0

#c) SELECT * FROM tarjetas WHERE distrito = 'Centro' OR distrito = 'Este'
r_c = tarjetas["distrito"].isin(['Centro', 'Este'])
print(tarjetas.loc[r_c, :])
#   id_tarjeta tipo_tarjeta  descuento distrito
#2        T003      general          0     Este         30       T031   estudiante         50   Centro
#5        T006      general          0   Centro         33       T034   estudiante         50   Centro
#9        T010      general          0   Centro         38       T039   estudiante         50     Este
#10       T011      general          0     Este         43       T044     jubilado         70     Este
#15       T016      general          0     Este         44       T045     jubilado         70   Centro
#16       T017      general          0     Este         45       T046     jubilado         70     Este
#17       T018      general          0   Centro         46       T047     jubilado         70   Centro
#20       T021      general          0   Centro         47       T048     jubilado         70     Este
#23       T024      general          0     Este
#25       T026   estudiante         50   Centro
#26       T027   estudiante         50   Centro

#d) SELECT id_linea, ROUND(AVG(retraso_min), 1) FROM viajes GROUP BY id_linea HAVING AVG(retraso_min) > 4
r_d = viajes.groupby("id_linea")["retraso_min"].mean().reset_index().query("retraso_min > 4").round(1)
print(r_d)
#  id_linea  retraso_min
#4      L05         17.3
#5      L06          8.3
#8      L09          4.9

#e) SELECT COUNT(DISTINCT id_tarjeta) FROM viajes WHERE medio_pago = 'movil'
r_e = viajes.query("medio_pago == 'movil'")["id_tarjeta"].nunique()
print(r_e) #44

#7.2 Consultas con varias tablas.
#a) SELECT v.id_viaje, l.numero, v.retraso_min FROM viajes v JOIN lineas l ON v.id_linea = l.id_linea WHERE l.tipo_linea = 'circular' AND v.retraso_min > 3
unidas_a = pd.merge(viajes, lineas, on="id_linea", how="inner")
r_a2 = unidas_a.query("tipo_linea == 'circular'")
r_a2 =r_a2.loc[:,["id_viaje", "numero", "retraso_min"]]
print(r_a2)

#    id_viaje numero  retraso_min
#0      V0001     C2          4.5           293    V0297     C2          0.0
#14     V0016     C1          0.0           295    V0299     C1          1.6
#16     V0018     C2          0.5           301    V0305     C2          2.0
#20     V0022     C2          2.2           306    V0310     C2          1.7
#25     V0027     C1          1.4           308    V0312     C2          3.6
#..       ...    ...          ...           [72 rows x 3 columns]

#b) SELECT t.distrito, SUM(v.paradas)FROM viajes v JOIN tarjetas t ON v.id_tarjeta = t.id_tarjeta GROUP BY t.distrito
unidas_b = pd.merge(viajes, tarjetas, on="id_tarjeta", how="inner")
r_b2 = unidas_b.groupby("distrito")["paradas"].sum()
print(r_b2)
#DISTRITO: Carretera de Cádiz:405, Centro:610, Cruz de Humilladero:774, Este:486, Teatinos:660

#c)SELECT l.tipo_linea, AVG(v.retraso_min) FROM viajes v JOIN lineas l ON v.id_linea = l.id_linea GROUP BY l.tipo_linea
#unidas_c = unidas_a
r_c2 = unidas_a.groupby("tipo_linea")["retraso_min"].mean()
print(r_c2)
#tipo_linea - circular: 1.861299, especial: 4.883333, urbana: 6.634423

#d) SELECT recorrido FROM lineas l WHERE EXISTS (SELECT 1 FROM viajes v  WHERE v.id_linea = l.id_linea AND v.retraso_min >10)
lineas_retraso_alto = viajes.query("retraso_min > 10")["id_linea"].unique()
r_d2 = lineas.query("id_linea in @lineas_retraso_alto").loc[:, ["recorrido"]]
print(r_d2)
#               recorrido
# 4     Alameda - Teatinos
# 5  Alameda - Campanillas

#e)SELECT id_tarjeta, tipo_tarjeta, distrito FROM tarjetas WHERE id_tarjeta NOT IN (SELECT id_tarjeta FROM viajes WHERE fecha >= '2026-02-01')
viajes_fechas = viajes.reset_index()
tarjetas_febrero = (viajes_fechas.query("fecha >= '2026-02-01'")["id_tarjeta"].dropna().unique())
r_e2 = tarjetas.query("id_tarjeta not in @tarjetas_febrero").loc[:, ["id_tarjeta", "tipo_tarjeta", "distrito"]]
print(r_e2)
#   id_tarjeta tipo_tarjeta             distrito
# 36       T037   estudiante  Cruz de Humilladero



