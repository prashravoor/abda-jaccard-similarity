import sys
from operator import add
import itertools

from pyspark.sql import SparkSession 
from pyspark.sql.types import LongType
from pyspark.context import SparkContext
from pyspark.sql.functions import input_file_name

spark = SparkSession\
        .builder\
        .appName("Jaccard Similarity")\
        .getOrCreate()

sc = SparkContext.getOrCreate()

def compute_similarity(shingles_1, shingles_2):
    set1 = set(shingles_1[0][1][i] for i in range(len(shingles_1[0][1])))
    set2 = set(shingles_2)
    return len(set1.intersection(set2)) / \
                         float(len(set1.union(set2)))

print('***************************************')

if len(sys.argv) != 4:
    print("Usage: <CMD> <Input Folder> <K> <Test doc>")
    exit()

path = sys.argv[1]
slen = int(sys.argv[2])
doc = sys.argv[3]

docrdd = (spark.read.text(doc).select(input_file_name(), "value").rdd)
docrdd = docrdd.map(lambda (x,y): (x, y.split(' ')))
docrdd = docrdd.map(lambda (x,y): (x, list(hash(tuple(y[i:i+slen])) for i in range(len(y) - slen + 1))))
docrdd = docrdd.reduceByKey(lambda x,y: x+y)
docshingles = docrdd.collect()

bc = sc.broadcast(docshingles)

linesrdd = (spark.read.text(path).select(input_file_name(), "value").rdd)
rdd = linesrdd.map(lambda (x,y): (x, y.split(' ')))
rdd = rdd.map(lambda (x,y): (x, list(hash(tuple(y[i:i+slen])) for i in range(len(y) - slen + 1))))
rdd = rdd.reduceByKey(lambda x,y: x+y)
result = rdd.map(lambda (x,y): (compute_similarity(bc.value, y), x)).collect()

print("JC: {}".format(list(result)))
spark.stop() 
