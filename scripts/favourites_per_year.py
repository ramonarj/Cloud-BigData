#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# Cloud & Big Data, UCM, 2021

# Ramon Arjona Quiniones
# Javier Gomez Moraleda
# Michael Steven Paredes Sanchez

''' Procesa el archivo IMDb_movies para hallar la media aritmetica de las peliculas hechas por cada pais '''

## IMPORTS ##
# Python
import time
start_time = time.time()
import string
import sys
import re
reload(sys)
sys.setdefaultencoding('utf8')

# Spark
from pyspark import SparkConf, SparkContext, SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, sum, mean, ceil, collect_list, asc, desc

## INICILIAZACION DE SPARK ##
''' BENCHMARK: para obtener tiempos optimos 
- Numero de tareas = coincide con el num. de particiones del dataframe.
Por defecto se crean 200, pero nosotros usamos una heuristica de [num. ejecutores * num.cores de cada ejecutor] 
- Numero de ejecutores = 1 si se lanza en local, tantos como nodos si se trata de un cluster 
- Numero de hilos/ejecutor = usaremos tantos cores como tenga el ejecutor (local[*])
'''
conf = SparkConf().setMaster('local[*]').setAppName('FavouritesPerYear')
sc = SparkContext(conf = conf)
spark = SparkSession(sc)
sqlContext = SQLContext(sc)

# Num de tareas
DATAFRAME_PARTITIONS = 6
sqlContext.setConf("spark.sql.shuffle.partitions", DATAFRAME_PARTITIONS)

## PROCESAMIENTO DE LOS DATOS ##

# Lectura del archivo csv: con la opcion "header" hacemos que la primera fila haga de cabecera
DFVar = spark.read.option("header", "True").csv("../datasets/IMDb_movies.csv")

# Selecciono las columnas título, año y valoración media
DFVar = DFVar.select(DFVar['year'], DFVar['title'], DFVar['avg_vote'])

#Función que devuelve True si la valoracion se puede transformar en float 
def esFloat(valoracion):
    try:
        float(valoracion)
        return True
    except ValueError:
        return False

# Lo transformo en un rdd y hago un filtro de errores
RDDVar = DFVar.rdd.map(lambda (x, y, z): (x, y, z)).filter(lambda(x, y, z): esFloat(z)) 

DFVar = RDDVar.toDF(["Year", "Title", "Rating"]).sort(desc("Rating")).groupBy("Year") #.rdd.map(lambda (x, y, z): (x, y)).reduceByKey(lambda x, y: x).toDF(["Year", "Title"]).sort(desc("Year"))
print(DFVar)


'''

# Lo guardo en un fichero de texto
DFRes.write.format("csv").save("../output/rating_per_country")

# Debug del tiempo, para el benchmarking
print("--- %s seconds ---" % (time.time() - start_time))'''
