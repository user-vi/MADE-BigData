import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import split


parser = argparse.ArgumentParser()
parser.add_argument("--kafka-brokers", required=True)
parser.add_argument("--topic-name", required=True)
parser.add_argument("--starting-offsets", default='latest')

group = parser.add_mutually_exclusive_group()
group.add_argument("--processing-time", default='0 seconds')
group.add_argument("--once", action='store_true')

args = parser.parse_args()
if args.once:
    args.processing_time = None
else:
    args.once = None


spark = SparkSession \
    .builder \
    .config("spark.sql.shuffle.partitions", "4") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

rates = spark \
.readStream \
.format("kafka") \
.option("kafka.bootstrap.servers", args.kafka_brokers) \
.option("subscribe", args.topic_name) \
.option("startingOffsets", args.starting_offsets) \
.option("rowsPerSecond", 5) \
.option("numPartitions", 3) \
.load()

split_col = split(rates['value'], '\\t+')

split_col_df = rates \
.withColumn('ts', split_col.getItem(0)) \
.withColumn('uid', split_col.getItem(1)) \
.withColumn('url', split_col.getItem(2)) \
.withColumn('title', split_col.getItem(3)) \
.withColumn('ua', split_col.getItem(4))

split_url_df = split_col_df.withColumn('url', split(split_col_df['url'], '/').getItem(2))\
.createOrReplaceTempView("logs")

res = spark.sql(
    """
    SELECT url as domain, COUNT(*) as view, approx_count_distinct(uid) as unique
    FROM logs
    GROUP BY url
    ORDER BY view DESC
    LIMIT 10
    """
)

query = res \
.writeStream \
.outputMode("complete") \
.format("console") \
.trigger(once=args.once, processingTime=args.processing_time) \
.option("truncate", "false") \
.start()

query.awaitTermination()
