from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, count
from pyspark.sql.types import StructType, StringType, TimestampType

# Spark 세션 생성
spark = SparkSession.builder \
    .appName("Click Aggregator") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.elasticsearch:elasticsearch-spark-30_2.12:8.12.0") \
    .getOrCreate()

# Kafka에서 읽을 topic
kafka_topic = "click-log"

# Kafka 설정
df_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", kafka_topic) \
    .option("startingOffsets", "latest") \
    .load()

# JSON schema 정의
schema = StructType() \
    .add("userId", StringType()) \
    .add("productId", StringType()) \
    .add("timestamp", StringType())

# value 컬럼을 JSON으로 파싱
df_parsed = df_raw.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*") \
    .withColumn("event_time", col("timestamp").cast(TimestampType()))

# 1분 단위로 productId별 클릭 수 집계
df_agg = df_parsed \
    .groupBy(
        window(col("event_time"), "1 minute"),
        col("productId")
    ) \
    .agg(count("*").alias("click_count")) \
    .select(
        col("productId"),
        col("click_count"),
        col("window.start").alias("start_time"),
        col("window.end").alias("end_time")
    )

# Elasticsearch에 저장
df_agg.writeStream \
    .format("org.elasticsearch.spark.sql") \
    .option("checkpointLocation", "/tmp/spark-checkpoint") \
    .option("es.nodes", "elasticsearch") \
    .option("es.port", "9200") \
    .option("es.resource", "click-agg/_doc") \
    .option("es.nodes.wan.only", "true") \
    .outputMode("update") \
    .start() \
    .awaitTermination()

