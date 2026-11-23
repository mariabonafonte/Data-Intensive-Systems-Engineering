# %% [markdown]
# # Práctica 1 (guiada) · Préstamos de la biblioteca universitaria
# Alumno/a: María Bonafonte Sánchez 
# Lee el enunciado completo antes de empezar. Cada apartado debe imprimir su resultado
# (show, print...) para que se pueda corregir ejecutando el fichero.
import os
import sys
os.environ["PYSPARK_PYTHON"] = sys.executable
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType
from pyspark.sql.functions import col
# %% [markdown]
# ## PARTE 1 · Sesión, carga y exploración 
# %% 1.1 Crear la SparkSession  · diapositiva 10
spark = (SparkSession.builder
    .appName("Ejercicio Clase") # nombre de la aplicación
    .master("local[*]") # en local, usando todos los núcleos
    .getOrCreate()) # crea (o reutiliza) la sesión

spark.sparkContext.setLogLevel("ERROR") # solo mostrar errores, no avisos
print(spark.version)

# %% 1.2 Leer los ficheros · diapositivas 13, 14 y 15
esquema = StructType([
    StructField("id_prestamo", StringType()),
    StructField("id_socio", StringType()),
    StructField("id_libro", StringType()),
    StructField("fecha_prestamo", DateType()),
    StructField("dias_permitidos", IntegerType()),
    StructField("valoracion", IntegerType())
])

prestamos = spark.read.option("header", True).schema(esquema).csv("datos/prestamos.csv")

libros = spark.read.csv("datos/libros.csv", header=True, inferSchema=True)
socios = spark.read.json("datos/socios.json")

prestamos.printSchema()
libros.printSchema()
socios.printSchema()

# %% 1.3 Explorar  · diapositivas 18 y 19
# Problemas:
#  - 
prestamos.show(5)
print ("Préstamos:", prestamos.count(), "Libros:", libros.count(), "Socios:", socios.count())
print(prestamos.columns)
prestamos.describe("dias_permitidos", "valoracion").show()
libros.describe("anio_publicacion", "paginas").show()
socios.select("centro").distinct().show() #PARA QUE PINTE X PANTALLA HAY Q PONER PRINT O SHOW SIEMPRE 


# %% [markdown]
# ## PARTE 2 · Selección y filtrado con la API y con SQL 

# %% 2.1 Vistas temporales  · diapositiva 22
prestamos.createOrReplaceTempView("prestamos")
libros.createOrReplaceTempView("libros")
socios.createOrReplaceTempView("socios")

# %% 2.2 Título, autor y género de los libros  · diapositivas 23 y 27
libros.select("titulo", "autor", "genero").show(5, truncate=False)
spark.sql("SELECT titulo, autor, genero FROM libros").show(5, truncate=False)


# %% 2.3 Préstamos de 7 días con valoración de 4 o más  · diapositivas 29 y 30
#api
siete_dias = prestamos.filter((col("dias_permitidos") == 7) & (col("valoracion") >= 4))
siete_dias.show()

#sql
siete_dias_sql = spark.sql("""SELECT * FROM prestamos 
                            WHERE dias_permitidos = 7 
                            AND valoracion >= 4""")
siete_dias_sql.show()

# %% 2.4 Novelas o poesía publicadas antes de 1950, de la más antigua a la más moderna  · diapositivas 31 y 32
antes_1950 = libros.filter((col("genero").isin("Novela", "Poesía")) & (col("anio_publicacion") < 1950)).orderBy(col("anio_publicacion").asc())
antes_1950.show()

antes_1950_sql = spark.sql("""SELECT * FROM libros
                            WHERE genero IN ('Novela', 'Poesía')
                            AND anio_publicacion < 1950 """)
antes_1950_sql.show()

# %% 2.5 Los 3 libros con más páginas  · diapositiva 32
top3_paginas = libros.orderBy(col("paginas").desc()).limit(3)
top3_paginas.show()

top3_paginas_sql = spark.sql("""SELECT * FROM libros
                            ORDER BY paginas DESC
                            LIMIT 3""")
top3_paginas_sql.show()


# %% [markdown]
# ## PARTE 3 · Columnas nuevas 

# %% 3.1 Limpiar el centro de los socios  · diapositivas 35 y 37



# %% 3.2 Días que duró el préstamo y mes · diapositivas 35 y 38


# %% 3.3 Estado del préstamo con when y con CASE WHEN · diapositivas 36 y 49


# %% [markdown]
# ## PARTE 4 · Valores nulos 

# %% 4.1 Contar nulos  · diapositiva 43


# %% 4.2 Eliminar filas con nulos  · diapositiva 44


# %% 4.3 Rellenar nulos  · diapositivas 39, 45 y 46


# %% [markdown]
# ## PARTE 5 · Combinar DataFrames 

# %% 5.1 Unir los préstamos de marzo  · diapositiva 60


# %% 5.2 Préstamos con los datos del libro y del socio · diapositivas 55, 56 y 57


# %% 5.3 Libros que nunca se han prestado entre enero y marzo  · diapositiva 58


# %% [markdown]
# ## PARTE 6 · Agregaciones 

# %% 6.1 Préstamos por género  · diapositivas 49 y 32


# %% 6.2 Resumen por tipo de socio  · diapositiva 50


# %% 6.3 Autores con al menos 15 préstamos  · diapositiva 51


# %% [markdown]
# ## PARTE 7 · De Spark a pandas 

# %% 7.1 Pasar el resumen a pandas · diapositivas 63 y 69


# %% Cerrar la sesión
# spark.stop() 