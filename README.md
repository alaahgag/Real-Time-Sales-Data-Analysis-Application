# Real-Time-Sales-Data-Analysis-Application
A real-time sales data analysis Application using Spark Structured Streaming, Kafka as a messaging system, PostgreSQL as a storage for processed data, and Superset for creating a dashboard.

## Project Description
Mya Gon Yaung is a men's traditional clothing retail shop that manually records everything in a book. Since sales are only written in a book, it is easy to find daily sales but difficult to know monthly or yearly sales. As a result, the shop owners do not know their monthly and yearly sales, what products are sold most in which month, and which stocks need to be refilled and which don't. As they don't know the answers to these questions, they often overstock or understock many products which greatly affects their profits.

This project is used to find out whether having a real-time sales data analysis application will be a solution to solve the problems faced at Mya Gon Yaung.


## Data Platform Architecture

![Data Platform Architecture](Images/Data_Platform_Architecture.PNG)

The Data Platform Architecture of the Real-Time Sales Data Analysis Application is designed to provide a streamlined and efficient process for handling sales data from its inception to real-time analytics. Customer purchase information is initially generated and transmitted through a Kafka producer, which then sends the data to a designated Kafka topic. Subsequently, an Apache Spark streaming application processes the data, extracting pertinent information and transforming it for further analysis. The processed data finds a reliable home in a PostgreSQL database, offering structured storage. 

Finally, the stored data is leveraged to create live dashboards using Apache Superset, enabling real-time analytics and visualization of key metrics. This architecture ensures a seamless and comprehensive flow of data, empowering the application to deliver timely insights into sales trends and inventory management.


## Project Workflow

### 1. Data Source

To simulate product checkouts, a Kaggle [sales dataset](https://www.kaggle.com/datasets/knightbearr/sales-product-data) is utilized in the Kafka Producer.

### 2. Data Preparation

The Kaggle dataset undergoes cleaning and column trimming to ensure data quality. Two primary datasets are prepared: Sales Data and Stock Quantity Data.

#### Sample Data:

- *Sales Data*:  
  <img src="Images/sales_data.PNG" width="400">

- *Stock Quantity Data*:  
  <img src="Images/stock_quantity.PNG" width="400">

### 3. Data Producer

A dedicated Kafka Producer streams sales data to the "sales" topic in Kafka, ensuring a reliable and real-time data flow.

### 4. Data Storage

A Python script creates a PostgreSQL database and tables for storing processed data, providing a structured storage solution.

### 5. Spark Structured Streaming

A Python script handles data ingestion, processing, and storage from the "sales" Kafka topic into PostgreSQL. It includes steps such as streaming data from Kafka using Spark, transforming data, and aggregating results in PostgreSQL.

### 6. Data Visualization with Apache Superset

The stored data in PostgreSQL is leveraged to build live dashboards using Apache Superset. This step enables real-time analytics and visualization of key metrics derived from the processed data.

This organized structure provides a clear understanding of the project, its architecture, and the detailed workflow. Contributors and users can easily navigate and comprehend the different components and steps involved in the Real-Time Sales Data Analysis Application.


## Project Files

- **`create_db_schema.py`:**
  *This script creates the sales database schema for stock and sales in PostgreSQL.*

- **`data_preparation.py`:**
  *The data_preparation.py script is responsible for preparing and cleaning the sales data, ensuring its quality and relevance for further analysis and streaming.*

- **`generate_sales_data.py`:**
  *The generate_sales_data.py script creates a Kafka producer to generate data and stream it to the "sales" topic in Kafka.*

- **`spark_streaming.py`:**
  *The spark_streaming.py file orchestrates the execution of the Spark Structured Streaming application. It sets up the logger, initializes the Spark session, defines configuration parameters, and calls the `process_data` function to execute the ETL process.*

- **`kafka_stream_dag.py`:**
  *The kafka_stream_dag.py file defines an Airflow Directed Acyclic Graph (DAG) responsible for streaming data to a Kafka topic. It is configured to run daily at 1 AM, designed not to run for any missed intervals (with catchup=False), and allows only one active run at a time.*


# Running the Project

To successfully run the Real-Time Sales Data Analysis Application, follow the steps outlined below.

## Prerequisites

Ensure that you have the following prerequisites installed on your system:

- Apache Spark
- Apache Kafka
- PostgreSQL
- Apache Superset
- Python (3.6 or higher)

## Setup and Configuration

- 1- Make sure that the Java version is compatible with Pyspark.
- 2- Clone the repository

```bash
  git clone https://github.com/alaahgag/Real-Time-Sales-Data-Analysis-Application.git
```

- 3- Navigate to the project directory

```bash
  cd Real-Time-Sales-Data-Analysis-Application
```

- 4- install the needed packages and libraries

```bash
  pip install -r ./requirements.txt
```

**Launch the project:**

- 1- Start Kafka:
```bash
  sh confg/start-zookeeper.sh
```
```bash
  sh confg/start-kafka.sh
```

- 2- Start Apache Superset:
```bash
  superset run -p 8088
```
- 3- Start Apache Superset:
```bash
  airflow db init
  airflow webserver
```
```bash
  airflow scheduler
```
- 4- run `spark_streaming.py` file
```bash
  spark-submit spark_streaming.py
```
- 4- Invoke `kafka_stream_dag.py` file

  

