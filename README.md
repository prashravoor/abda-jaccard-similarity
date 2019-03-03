# Implementation of Jaccard Similarity using Apache Spark (PySpark)

This repo has code to measure Jaccard Similarity for a set of documents, using the k-shingles approach. <br>
[See here for explaination of Jaccard Similarity](https://www.cs.utah.edu/~jeffp/teaching/cs5955/L4-Jaccard+Shingle.pdf)
## Setting Up
Download, install and configure [Apache Spark 2.4.0](https://spark.apache.org/downloads.html). <br>
Add the path to the Spark binaries to the PATH variable in `.bashrc` for ease of use. <br>
For the configuration of Spark in Cluster Mode, add the following variable to the `.bashrc` file for your user, replacing `$HADOOP_HOME` appropriately.
```
export HADDOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
```
## Testing Cluster Mode
First, start the Hadoop Cluster by starting YARN and DFS. <br>
Once the Hadoop cluster starts, run the following command to open an interactive Spark Shell: <br>
```
pyspark --master yarn
```
Ensure all is working OK by running a few simple commands. <br>
Alternatively, test by running one of the pre-built examples on the Hadoop Cluster (replace SPARK_HOME appropriately):
```bash
spark-submit --class org.apache.spark.examples.SparkPi \
    --master yarn \
    --deploy-mode cluster \
    $SPARK_HOME/examples/jars/spark-examples*.jar \
    10
```

## Running the program
Upload a test document to HDFS, and the also the set of documents to which it has to be compared. The Program can be run using:
```
spark-submit --master yarn --deploy-mode cluster jc.py <Path to document set directory> <Value of K> <Test document path>
```
On completion, the output will contain each document in the document set provided with the corresponding similarity score to the test document. This is displayed on screen only, and is not stored in any file. <br>
Example command:
```bash
spark-submit --master yarn --deploy-mode cluster \
    jc.py /usr/input/small 5 /usr/input/small/big.txt
```

Sample Output:
```
JC:
[(0.0003215224699437539, u'hdfs://ubuntu:9000/usr/input/small/rfc0001.txt'),
(1.0, u'hdfs://ubuntu:9000/usr/input/small/big.txt'),
(1.3605275581659545e-06, u'hdfs://ubuntu:9000/usr/input/small/test.txt'),
(0.026405088810002315, u'hdfs://ubuntu:9000/usr/input/small/dickens-david-626.txt')]

```
