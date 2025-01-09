print("Spark streaming script started")

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *

print("Creating Spark session...")
spark = (
    SparkSession.builder.appName("HealthMonitoring")
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0")
    .getOrCreate()
)

print("Spark session created")
spark.sparkContext.setLogLevel("WARN")

try:
    print("Starting to consume data from Kafka...")
    df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "kafka:29092")
        .option("subscribe", "emergency,normal")
        .option("startingOffsets", "earliest")
        .load()
    )
    print("Kafka connection established")

    print("Processing JSON data...")
    json_df = df.selectExpr("CAST(value AS STRING)")

    schema = StructType(
        [
            StructField("Timestamp", StringType(), True),
            StructField("PatientID", StringType(), True),
            StructField("DeviceID", StringType(), True),
            StructField("Metric", StringType(), True),
            StructField("Value", DoubleType(), True),
            StructField("Unit", StringType(), True),
            StructField("date", StringType(), True),
            StructField("time", StringType(), True),
            StructField("Sensor_ID", IntegerType(), True),
        ]
    )

    parsed_df = json_df.select(from_json(col("value"), schema).alias("data")).select(
        "data.*"
    )
    print("JSON parsing complete")

    print("Calculating windowed metrics...")
    windowed_metrics = (
        parsed_df.withColumn("timestamp", to_timestamp("Timestamp"))
        .withWatermark("timestamp", "90 seconds")
        .groupBy("PatientID", window("timestamp", "40 seconds"), "Metric")
        .agg(
            avg("Value").alias("avg_value"),
            max("Value").alias("max_value"),
            min("Value").alias("min_value"),
            count("Value").alias("reading_count"),
        )
    )

    print("Starting streaming query...")
    query = (
        windowed_metrics.select(
            "PatientID",
            "Metric",
            "window.start",
            "window.end",
            "avg_value",
            "max_value",
            "min_value",
            "reading_count",
        )
        .writeStream.outputMode("append")
        .format("console")
        .option("truncate", False)
        .trigger(processingTime="30 seconds")
        .start()
    )

    print("Streaming query started successfully")
    query.awaitTermination()

except Exception as e:
    print(f"Error occurred: {str(e)}")
    spark.stop()
