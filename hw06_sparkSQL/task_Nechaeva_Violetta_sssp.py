import pyspark.sql.functions as F
from pyspark.sql.functions import col
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
sc = SparkContext('local')
spark = SparkSession(sc)

df = spark.read\
.format("text")\
.option("schema","col0: string ,col0: string")\
.option("sep", "\\t")\
.options(header = False)\
.load("hdfs:////data/twitter/twitter.txt")

split_col = F.split(df['value'], '\\t')
df = df.withColumn('user', split_col.getItem(0))\
.withColumn('follower', split_col.getItem(1))\
.drop('value')

df = df\
.withColumnRenamed("follower", "user0")\
.withColumnRenamed("user", 'follower')\
.withColumnRenamed("user0", 'user')

right = df
left = df\
.filter(col("user") == 12)

for i in range(0, 100):
    i+=1
    new_follower = "follower" + str(i)
    if i == 1:
        old_user = "user"
    else:
        old_user = "user" + str(i-1)
    new_user = "user" + str(i)
    left = left.withColumnRenamed("follower", new_follower).alias("left")
    right = right.withColumnRenamed(old_user, new_user).alias("right")
    join_condition = (col(new_follower) == col(new_user))
    left = left.join(right, join_condition, 'left').na.drop()
    tmp = left.filter(col("user") == 12).filter(col("follower") == 34).count()
    if tmp != 0:
        print(i+1)
        break
