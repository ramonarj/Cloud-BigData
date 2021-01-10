# Cloud & Big Data, UCM, 2021

# Ramon Arjona Quiniones
# Javier Gomez Moraleda
# Michael Steven Paredes Sanchez

'''Ejemplo de lectura de datos del archivo "IMDb_movies" '''

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, sum, mean, ceil, collect_list, asc

import string
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# Inicializamos Spark
conf = SparkConf().setMaster('local').setAppName('RatingPerCountry')
sc = SparkContext(conf = conf)
spark = SparkSession(sc)

# Lectura del archivo csv: con la opcion "header" hacemos que la primera fila haga de cabecera
DFVar = spark.read.option("header", "True").csv("IMDb_movies.csv")

DFVar2 = DFVar.select(DFVar['country'], DFVar['avg_vote'])
RDDVar = DFVar2.rdd.map(lambda (x, y): (x, y))

RDDVar2 = RDDVar.filter(lambda(x, y): len(y) < 4) 
RDDVar2.saveAsTextFile("output")