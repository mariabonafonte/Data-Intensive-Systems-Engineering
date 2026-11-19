import numpy as np
import pandas as pd


# PARTE 1. Carga y exploración
df_octubre = pd.read_csv("datos/recargas_octubre.csv")
df_noviembre = pd.read_csv("datos/recargas_noviembre.csv")

recargas = pd.concat([df_octubre, df_noviembre], ignore_index=True)
recargas["fecha"] = pd.to_datetime(recargas["fecha"])
recargas = recargas.set_index("fecha").sort_index()

# PARTE 2. Limpieza y columnas nuevas
# 2.1 Energía imposible (> 100 kWh)
recarga_anómala = recargas[recargas["energia_kwh"] > 100]
print("Recarga anómala:")
print(recarga_anómala)

idx_anomalo = recarga_anómala.index[0]
recargas.loc[idx_anomalo, "energia_kwh"] = np.nan
print("Nulos actuales en energia_kwh:", recargas["energia_kwh"].isnull().sum())

# 2.2 Tratamiento de nulos según el estado
sin_nulos = recargas.dropna()
print(f"Filas sin nulos: {len(sin_nulos)} | Filas totales: {len(recargas)}")

print(
    "Estados de las recargas sin energía:\n",
    recargas[recargas["energia_kwh"].isnull()]["estado"].value_counts(),
)

completadas = recargas[recargas["estado"] == "completada"]
interrumpidas = recargas[recargas["estado"] == "interrumpida"]

print("Media total:", recargas["energia_kwh"].mean())
print("Media completadas:", completadas["energia_kwh"].mean())
print("Media interrumpidas:", interrumpidas["energia_kwh"].mean())

# Rellenar nulos con la media de su grupo correspondiente
recargas.loc[recargas["estado"] == "completada", "energia_kwh"] = completadas[
    "energia_kwh"
].fillna(completadas["energia_kwh"].mean())

recargas.loc[recargas["estado"] == "interrumpida", "energia_kwh"] = (
    interrumpidas["energia_kwh"].fillna(interrumpidas["energia_kwh"].mean())
)

recargas = recargas.sort_index()
print(
    "Nulos restantes tras rellenar por grupo:",
    recargas["energia_kwh"].isnull().sum(),
)


# 2.3 Creación de la columna franja
def clasificar_franja(hora):
  if hora < 12:
    return "mañana"
  elif 12 <= hora <= 17:
    return "tarde"
  else:
    return "noche"


recargas["franja"] = recargas["hora"].apply(clasificar_franja)
print("Recargas por franja:\n", recargas["franja"].value_counts())


# PARTE 3. Selección e indexación
# 3.1 Columna energia_kwh de las dos formas y subconjunto
col1 = recargas["energia_kwh"]
col2 = recargas.energia_kwh
sub_cargador_energia = recargas[["id_cargador", "energia_kwh"]]

# 3.2 Primeras 5 recargas por posición, semana 1 de noviembre y fechas 10-12 octubre
print(recargas.iloc[:5])
primera_semana_nov = recargas.loc["2026-11-01":"2026-11-07"]
print(f"Recargas en la primera semana de noviembre: {len(primera_semana_nov)}")
print(
    recargas.loc["2026-10-10":"2026-10-12", ["id_cargador", "energia_kwh"]]
)

# 3.3 Undécima recarga y últimas 5 con 3 primeras columnas
print(recargas.iloc[10, :3])
print(recargas.iloc[-5:, :3])

# 3.4 por_id con id_recarga como índice
por_id = recargas.reset_index().set_index("id_recarga")
print(por_id.loc["R0150"])
print("Energía de R0150:", por_id.loc["R0150", "energia_kwh"])
print(por_id.nlargest(5, "energia_kwh")[["energia_kwh", "id_cargador"]])


# PARTE 4. Consultas con y sin query
rec_temp = recargas.reset_index()

# 4.1 Recargas interrumpidas
inter_corchetes = recargas[recargas["estado"] == "interrumpida"]
inter_query = recargas.query("estado == 'interrumpida'")
print(f"Interrumpidas (corchetes): {len(inter_corchetes)} | (query): {len(inter_query)}")

# 4.2 Más de 3 horas en C02
res_42_q = rec_temp.query("id_cargador == 'C02' and duracion_min > 180")[
    ["id_recarga", "duracion_min", "energia_kwh"]
]
print(res_42_q)

# 4.3 Query nocturnas > 30 kWh en C01 o C05
res_43 = rec_temp.query(
    "franja == 'noche' and energia_kwh > 30 and id_cargador in ['C01', 'C05']"
)
print(res_43[["id_recarga", "id_cargador", "hora", "energia_kwh"]])
print(f"Total recargas 4.3: {len(res_43)}")

# 4.4 U99 y C11
print("Recargas de U99:", (rec_temp["id_usuario"] == "U99").sum())
print("Recargas en C11:", (rec_temp["id_cargador"] == "C11").sum())



# PARTE 5. Combinar tablas con merge
cargadores = pd.read_csv("datos/cargadores.csv")
usuarios = pd.read_csv("datos/usuarios.csv")
rec = recargas.reset_index()

# 5.1 Unir cargadores
completo = pd.merge(rec, cargadores, on="id_cargador", how="left", indicator=True)
no_cargador = completo[completo["_merge"] == "left_only"]
print(f"Recargas sin cargador: {len(no_cargador)}")
print("Cargador faltante:", no_cargador["id_cargador"].unique())

# 5.2 Unir usuarios, importe y reestablecer índice fecha
completo = pd.merge(completo, usuarios, on="id_usuario", how="left")
completo["tipo_usuario"] = completo["tipo_usuario"].fillna("invitado")
completo["importe"] = completo["energia_kwh"] * completo["precio_kwh"]
completo = completo.set_index("fecha")

# 5.3 Cargador no usado
cargadores_usados = rec["id_cargador"].unique()
cargador_no_usado = cargadores[
    ~cargadores["id_cargador"].isin(cargadores_usados)
]
print(cargador_no_usado)


# PARTE 6. Dividir, unir y agrupar
# 6.1 Dividir y unir trozos y estados
trozo1 = completo.iloc[:100]
trozo2 = completo.iloc[100:199]
trozo3 = completo.iloc[199:]
completo_unido = pd.concat([trozo1, trozo2, trozo3])
print("¿Tamaño correcto al unir 3 trozos?", len(completo_unido) == len(completo))

comp = completo[completo["estado"] == "completada"]
inter = completo[completo["estado"] == "interrumpida"]
completo_estados = pd.concat([comp, inter])
print("¿Tamaño correcto al unir estados?", len(completo_estados) == len(completo))

# 6.2 Agrupaciones
print("--- Energía e importe por zona ---")
print(completo.groupby("zona")[["energia_kwh", "importe"]].sum())

print("--- Energía total por zona y tipo de cargador ---")
print(completo.groupby(["zona", "tipo"])["energia_kwh"].sum())

print("--- Número de recargas por tipo de usuario ---")
print(completo.groupby("tipo_usuario")["id_recarga"].count())


# 6.3 Función nivel de energía
def clasificar_nivel(energia):
  if pd.isna(energia):
    return "desconocido"
  elif energia < 10:
    return "baja"
  elif energia <= 30:
    return "media"
  else:
    return "alta"


completo["nivel"] = completo["energia_kwh"].apply(clasificar_nivel)
print("Distribución por nivel:\n", completo["nivel"].value_counts())


# PARTE 7. Consultas SQL con DataFrame
rec_sql = completo.reset_index()

# 7.1
res_71 = (
    rec_sql.query("id_cargador == 'C07' and duracion_min > 120")
    .assign(dia=lambda x: x["fecha"].dt.strftime("%d/%m/%Y"))[
        ["id_recarga", "dia", "id_usuario", "energia_kwh"]
    ]
)
print("--- Resultado 7.1 ---")
print(res_71)

# 7.2
res_72 = (
    cargadores.query("zona == 'Centro' or zona == 'Litoral'")
    .assign(nombre=lambda x: x["nombre"].str.upper())[
        ["nombre", "zona", "potencia_kw"]
    ]
    .sort_values("potencia_kw")
)
print("--- Resultado 7.2 ---")
print(res_72)

# 7.3
res_73 = (
    rec_sql.groupby("id_usuario")["energia_kwh"]
    .sum()
    .reset_index()
    .query("energia_kwh > 600")
)
res_73["energia_kwh"] = res_73["energia_kwh"].round(1)
print("--- Resultado 7.3 ---")
print(res_73)

# 7.4
res_74 = (
    rec_sql.query("tipo == 'rapido'")
    .sort_values("energia_kwh", ascending=False)
    .head(5)
    .assign(energia_kwh=lambda x: np.floor(x["energia_kwh"]))[
        ["id_recarga", "nombre", "energia_kwh"]
    ]
)
print("--- Resultado 7.4 ---")
print(res_74)

# 7.5
usuarios_c01 = rec_sql.query("id_cargador == 'C01'")["id_usuario"].unique()
res_75 = usuarios.query("id_usuario not in @usuarios_c01")[
    ["id_usuario", "tipo_usuario"]
]
print("--- Resultado 7.5 ---")
print(res_75)
