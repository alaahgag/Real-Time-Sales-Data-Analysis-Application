import logging
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *

def setup_logger():
    """
    Set up the logger for the application.

    This function configures the logging format and level.

    Returns:
        None
    """

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

def init_spark_session():
    """
    Initialize a Spark session.

    This function sets up a Spark session with specific configurations.

    Returns:
        SparkSession: The configured Spark session.
    """

    logger = logging.getLogger(__name__)
    logger.info("Setting up Spark session...")
    spark = SparkSession.builder \
        .appName("KafkaStructuredStreaming") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,") \
        .config('spark.jars', 'file:///home/alaa-haggag/Projects/Kafka-Spark_Streaming/lib/mongo-spark-connector_2.12-3.0.2.jar,') \
        .config("spark.driver.extraClassPath", "file:///home/alaa-haggag/Projects/Kafka-Spark_Streaming/lib/postgresql-42.6.0.jar") \
        .config("spark.executor.extraClassPath", "file:///home/alaa-haggag/Projects/Kafka-Spark_Streaming/lib/postgresql-42.6.0.jar") \
        .getOrCreate()

    spark.sparkContext.setLogLevel('ERROR')
    return spark

def read_kafka_data(spark, kafka_topic, kafka_bootstrap_servers):
    """
    Read data from Kafka.

    Args:
        spark (SparkSession): The Spark session.
        kafka_topic (str): The Kafka topic to subscribe to.
        kafka_bootstrap_servers (str): The Kafka bootstrap servers.

    Returns:
        DataFrame: The DataFrame containing Kafka data.
    """

    logger = logging.getLogger(__name__)
    logger.info("Setting up Kafka source for Structured Streaming...")
    
    sales_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", kafka_topic) \
        .option("startingOffsets", "latest") \
        .load()

    sales_df1 = sales_df.selectExpr('CAST(value AS STRING)')
    return sales_df1

def process_data(spark, kafka_topic, kafka_bootstrap_servers, stock_filepath, postgres_jdbc_url, postgres_config):
    """
    Process and analyze data from Kafka and external files, and write results to various sinks.

    Args:
        spark (SparkSession): The Spark session.
        kafka_topic (str): The Kafka topic to subscribe to.
        kafka_bootstrap_servers (str): The Kafka bootstrap servers.
        stock_filepath (str): The file path for the external stock data.
        hdfs_output_path (str): The HDFS path for storing sales data.
        postgres_jdbc_url (str): The JDBC URL for PostgreSQL.
        postgres_config (dict): Configuration parameters for PostgreSQL.

    Returns:
        None
    """

    logger = logging.getLogger(__name__)

    # Read Kafka data
    sales_df = read_kafka_data(spark, kafka_topic, kafka_bootstrap_servers)

    # Parse JSON data
    sales_schema = StructType() \
        .add('Sale_ID', IntegerType()) \
        .add('Product', StringType()) \
        .add('Quantity_Sold', IntegerType()) \
        .add('Each_Price', FloatType()) \
        .add('Sale_Date', TimestampType()) \
        .add('Sales', FloatType())
    
    sales_df = sales_df.select(from_json(col('value'), sales_schema).alias('sales_data'))
    sales_df = sales_df.select('sales_data.*')

    # Process sales data
    sales_df = sales_df \
        .withColumn("Date", to_date(col("Sale_Date"), "yyyy-MM-dd")) \
        .withColumn("Day", split(col("Date"), "-").getItem(2)) \
        .withColumn("Month", split(col("Date"), "-").getItem(1)) \
        .withColumn("Year", split(col("Date"), "-").getItem(0)) \
        .drop("Sale_Date") \
        .withColumn("day", col("day").cast(IntegerType())) \
        .withColumn("month", col("month").cast(IntegerType())) \
        .withColumn("year", col("year").cast(IntegerType()))

    # Read stock data
    stocks_df = spark.read.csv(stock_filepath, header=True, inferSchema=True)

    # Join dataframes
    stocks_df = stocks_df \
        .withColumnRenamed("Quantity_Sold", "Quantity_Sold_Stocks") \
        .join(sales_df
              .drop("Sale_ID")
              .drop("Each_Price")
              .drop("Sale_Date")
              .drop("Sales"), on="Product", how="inner") \
        .withColumnRenamed("Quantity_Sold", "Quantity_Sold_Sales")

    # Group and aggregate
    stocks_df = stocks_df \
        .groupBy("Product", "Stock_Quantity") \
        .agg({'Quantity_Sold_Sales': 'sum'}) \
        .select('Product', 'Stock_Quantity', col('sum(Quantity_Sold_Sales)').alias('Total_Quantity_Sold'))

    # Write to console
    query = sales_df.writeStream \
        .trigger(processingTime='5 seconds') \
        .outputMode('update') \
        .option('truncate', 'false') \
        .format('console') \
        .start()

    # Write to PostgreSQL sales table
    sales_df.writeStream \
        .trigger(processingTime='5 seconds') \
        .outputMode('update') \
        .foreachBatch(lambda df, epoch_id: df.write.jdbc(url=postgres_jdbc_url, table='sales', mode='append', properties=postgres_config)) \
        .start()

    # Write to PostgreSQL stocks table
    stocks_df.writeStream \
        .trigger(processingTime='5 seconds') \
        .outputMode('complete') \
        .option('truncate', 'true') \
        .foreachBatch(lambda df, epoch_id: df.write.jdbc(url=postgres_jdbc_url, table='stocks', mode='overwrite', properties=postgres_config)) \
        .start()

    query.awaitTermination()

def main():
    """
    Main function to orchestrate the execution of the Spark Structured Streaming application.

    This function sets up the logger, initializes the Spark session, defines configuration parameters,
    and calls the `process_data` function to execute the ETL process.

    Returns:
        None
    """
    
    setup_logger()
    spark = init_spark_session()

    KAFKA_TOPIC_NAME = 'sales'
    KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
    postgres_config = {
        'user': 'your_username',
        'password': 'your_password',
        'driver': 'org.postgresql.Driver',
    }
    postgres_jdbc_url = 'jdbc:postgresql://localhost:5432/sales'
    stock_filepath = "file:////home/alaa-haggag/Projects/Kafka-Spark_Streaming/Prepared_Data/Stock_Quantity.csv"

    process_data(spark, KAFKA_TOPIC_NAME, KAFKA_BOOTSTRAP_SERVERS, stock_filepath, postgres_jdbc_url, postgres_config)

if __name__ == '__main__':
    main()