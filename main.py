"""Data Engineering Assessment for Schiphol Airport"""
import os
import time
import random
from datetime import datetime, timedelta

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, row_number, udf, window # pylint: disable=no-name-in-module
from pyspark.sql.types import TimestampType
from pyspark.sql.window import Window

import schemas

def pyspark_session(app_name):
    """Gets or creates Spark Session"""
    spark_session = SparkSession\
        .builder\
        .master('local[2]')\
        .appName(app_name)\
        .getOrCreate()
    spark_session.sparkContext.setLogLevel("ERROR")
    return spark_session

def top_10_source_airports_no_streaming(data_source_path='data'):
    """
    First task of the assessment:

    - Loads `routes.dat` into Data Frame
    - Aggregates the top 10 source airports from the whole data set
    - Writes result to json file
    - Displays all 10 rows on screen
    """
    LOG.info('Starting Task 1: Execution with no streaming...')
    task_name = 'top_10_source_airports_no_streaming'
    spark_session = pyspark_session(task_name)

    routes_df = spark_session \
        .read \
        .schema(schemas.ROUTE_SCHEMA) \
        .csv(data_source_path) \
        .groupBy('source_airport') \
        .count() \
        .sort('count', ascending=False) \
        .limit(10) \
        .coalesce(1)

    routes_df \
        .write \
        .json('results/{}_{}'.format(
            task_name,
            int(time.time())))

    LOG.info('Top 10 source airports - No Streaming')
    routes_df.show(truncate=False)

def top_10_source_airports_with_streaming():
    """
    Second task of the assessment:

    - Reads `routes.dat` as a stream
    - Aggregates the top 10 source airports from the whole data set
    - Writes result to json file
    - Displays all 10 rows on screen
    """
    LOG.info('Starting Task 2: Execution with streaming...')
    task_name = 'top_10_source_airports_with_streaming'
    max_rows = 10
    query_timeout_seconds = 120
    def write_to_file(batch_df, batch_id):
        """Method used in the `foreach` of the streaming
        data frame to write data to file"""
        batch_df = batch_df\
            .coalesce(1)\
            .sort(col('count').desc())\
            .limit(max_rows)

        # Write current aggregations to json file
        batch_df.write \
            .format("json") \
            .mode('overwrite') \
            .option('path', os.path.realpath('results/{}_{}'.format(
                task_name,
                batch_id))) \
            .option('checkpointLocation', 'checkpoint')\
            .save()

        # Display 100 rows on screen after processing
        LOG.info('Top 10 source airports - With Streaming')
        batch_df.show(100, False)

    spark_session = pyspark_session(task_name)

    routes_stream = spark_session\
        .readStream\
        .option('path', os.path.realpath('data'))\
        .schema(schemas.ROUTE_SCHEMA)\
        .format('csv')\
        .load()

    airport_counts = routes_stream\
        .groupBy('source_airport')\
        .count()\
        .sort(col('count').desc())

    query = airport_counts\
        .writeStream\
        .foreachBatch(write_to_file)\
        .outputMode('complete')\
        .start()

    query.awaitTermination(query_timeout_seconds)

def top_10_source_airports_with_streaming_and_sliding_window():
    """
    Third task of the assessment:

    - Reads `routes.dat` as a stream
    - Sets sliding window and interval of 1 second
    - Aggregates the top 10 source airports in each window
    - Writes result to json file
    - Displays first 100 rows (first 10 windows) on screen
    """
    LOG.info('Starting Task 3: Execution with streaming and sliding windows...')
    task_name = 'top_10_source_airports_with_streaming_and_sliding_window'
    max_rows_per_sliding_window = 10
    query_timeout_seconds = 240

    def randomized_timestamp():
        """Generates a pseudo-randomized timestamp to 
        spread out events over a few seconds and emulate an event stream"""
        return datetime.now() + timedelta(milliseconds=random.randrange(-1000, 1000))

    randomized_timestamp_udf = udf(randomized_timestamp, TimestampType())

    def write_to_file(batch_df, batch_id):
        """Method used in the `foreach` of the streaming
        data frame to write data to file"""
        batch_df = batch_df.withColumn(
            "row_number",
            row_number()\
                .over(
                    Window\
                        .partitionBy('window')\
                        .orderBy(col('count').desc())))\
            .filter(col('row_number') <= max_rows_per_sliding_window)\
            .coalesce(1)\
            .sort(col('window'), col('row_number'))

        # Write current aggregations to json file
        batch_df.write \
            .format("json") \
            .mode('overwrite') \
            .option('path', os.path.realpath('results/{}_{}'.format(
                task_name,
                batch_id))) \
            .option('checkpointLocation', 'checkpoint')\
            .save()

        # Display 100 rows on screen after processing
        LOG.info('Top 10 source airports \
            - With Streaming and Sliding Window of 1 second and Interval of 1 second')
        batch_df.show(50, False)

    spark_session = pyspark_session(task_name)

    routes_stream = spark_session\
        .readStream\
        .option('path', os.path.realpath('data'))\
        .schema(schemas.ROUTE_SCHEMA)\
        .format('csv')\
        .load()

    routes_stream = routes_stream.withColumn(
        'timestamp',
        randomized_timestamp_udf())

    source_airports = routes_stream.select(
        'source_airport',
        'timestamp'
    )

    airport_counts = source_airports \
        .groupBy(
            window('timestamp', '1 second', '1 second'),
            'source_airport') \
        .count()

    query = airport_counts\
        .writeStream\
        .foreachBatch(write_to_file)\
        .outputMode('complete')\
        .start()

    query.awaitTermination(query_timeout_seconds)

    print('Finished')

if __name__ == "__main__":
    spark_context = SparkContext.getOrCreate() # pylint: disable=invalid-name
    spark_context.setSystemProperty('spark.executor.memory', '2g')
    LOG = spark_context._jvm.org.apache.log4j.LogManager.getLogger(__name__) # pylint: disable=protected-access

    top_10_source_airports_no_streaming()
    top_10_source_airports_with_streaming()
    top_10_source_airports_with_streaming_and_sliding_window()
