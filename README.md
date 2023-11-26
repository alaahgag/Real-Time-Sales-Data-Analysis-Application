# Real-Time-Sales-Data-Analysis-Application
A real-time sales data analysis Application using Spark Structured Streaming, Kafka as a messaging system, PostgreSQL as a storage for processed data, and Superset for creating a dashboard.

## Project Description
Mya Gon Yaung is a men's traditional clothing retail shop that manually records everything in a book. Since sales are only written in a book, it is easy to find daily sales but difficult to know monthly or yearly sales. As a result, the shop owners do not know their monthly and yearly sales, what products are sold most in which month, and which stocks need to be refilled and which don't. As they don't know the answers to these questions, they often overstock or understock many products which greatly affects their profits.

This project is used to find out whether having a real-time sales data analysis application will be a solution to solve the problems faced at Mya Gon Yaung.


## Data Platform Architecture

![Data Platform Architecture](Images/Real-Time%20Sales%20Data%20Analysis%20Application~2.png)


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

  
## General Challenges and Troubleshooting

1. **Configuration Challenges:**
   - **Issue:** Ensuring environment variables and configurations are correctly set can be tricky. An incorrect setting might prevent services from starting or communicating.
   - **Troubleshooting:**
     - Double-check environment variables and configurations in all scripts.
     - Ensure paths and file locations are correctly specified.

2. **Service Dependencies:**
   - **Issue:** Services like Kafka or Airflow have dependencies on other services (e.g., Zookeeper for Kafka). Ensuring the correct order of service initialization is crucial.
   - **Troubleshooting:**
     - Review service dependencies and start services in the correct order.
     - Check logs for dependency-related errors.

3. **Airflow DAG Errors:**
   - **Issue:** Syntax or logical errors in the DAG file (kafka_stream_dag.py) can prevent Airflow from recognizing or executing the DAG correctly.
   - **Troubleshooting:**
     - Thoroughly review the DAG file for syntax errors or logical issues.
     - Use Airflow CLI commands for DAG validation.

4. **Spark Dependencies:**
   - **Issue:** Ensuring all required JARs are available and compatible is essential for Spark's streaming job. Missing or incompatible JARs can lead to job failures.
   - **Troubleshooting:**
     - Verify the presence and compatibility of required JAR files.
     - Check Spark logs for dependency-related errors.

5. **Kafka Topic Management:**
   - **Issue:** Creating topics with the correct configuration (like replication factor) is essential for data durability and fault tolerance.
   - **Troubleshooting:**
     - Use Kafka command-line tools to inspect and manage topics.
     - Ensure topics are created with the desired configurations.

6. **Deprecation Warnings:**
   - **Issue:** The provided logs show deprecation warnings, indicating that some methods or configurations used might become obsolete in future versions.
   - **Troubleshooting:**
     - Refer to the official documentation for the deprecated features.
     - Update your scripts or configurations accordingly to use recommended alternatives.

## Dashboard Demo

Check out a brief demo of the Real-Time Sales Data Analysis Application dashboard:

[Images/real-time-dashboard.mp4](https://github.com/alaahgag/Real-Time-Sales-Data-Analysis-Application/assets/101465586/00d5e50c-1a91-434e-b178-bc40b1c17e93)

    
## Conclusion

The Real-Time Sales Data Analysis Application is a robust solution designed to address the challenges faced by Mya Gon Yaung, a traditional men's clothing retail shop. By leveraging the power of Spark Structured Streaming, Kafka, PostgreSQL, and Apache Superset, the application provides a seamless and efficient pipeline for processing, analyzing, and visualizing sales data in real-time.

### Key Achievements

- **Real-Time Analytics:** The application enables real-time analytics, allowing Mya Gon Yaung to monitor sales trends, identify popular products, and make informed decisions promptly.
  
- **Inventory Optimization:** By integrating with Spark Structured Streaming, the shop can now optimize inventory management, reducing instances of overstocking or understocking and ultimately improving profitability.

- **User-Friendly Dashboards:** The use of Apache Superset facilitates the creation of user-friendly dashboards, empowering shop owners to gain insights into their business without the need for complex queries or data analysis.

### Future Enhancements

While the Real-Time Sales Data Analysis Application has achieved significant milestones, continuous improvement is essential. Future enhancements may include:

- **Machine Learning Integration:** Incorporating machine learning models for predictive analytics, helping forecast sales trends and further refine inventory management.

- **Extended Data Sources:** Integrating additional data sources beyond sales data, such as customer feedback or external market trends, to provide a more comprehensive analysis.

- **Scalability:** Ensuring the application is scalable to accommodate the growth of Mya Gon Yaung or similar businesses.


