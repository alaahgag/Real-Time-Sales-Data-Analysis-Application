import os
import pandas as pd


def data_prepare():
    """
    Prepare and clean sales data for further analysis and streaming.

    This function performs the following steps:
    1. Concatenates multiple sales data files into a single DataFrame.
    2. Cleans the data by removing duplicate rows and entries with header names.
    3. Formats the data by changing column names and data types.
    4. Calculates total sales for each product.
    5. Sorts the data by sale date for realistic streaming simulation.
    6. Saves the cleaned and processed data to a CSV file.
    7. Computes and sets a fixed stock quantity for each product.
    8. Saves the stock quantity data to a separate CSV file.

    Note:
    - The input sales data files are expected to be located in the 'Data_Source' directory.
    - The cleaned and processed data is saved to the 'Prepared_Data/Processed_Data.csv' file.
    - The stock quantity data is saved to the 'Prepared_Data/Stock_Quantity.csv' file.

    Usage:
    To prepare and clean the sales data, call this function with no parameters.

    Example:
    data_prepare()
    """
    output_directory = '/home/alaa-haggag/Projects/Kafka-Spark_Streaming/Prepared_Data'
    os.makedirs(output_directory, exist_ok=True)

    print("Step 1: Concatenating data...")
    data_folder = '/home/alaa-haggag/Projects/Kafka-Spark_Streaming/Data_Source'
    file_names = [file for file in os.listdir(data_folder)]
    data_frames = [pd.read_csv(os.path.join(data_folder, file)) for file in file_names]
    merged_data_df = pd.concat(data_frames, ignore_index=True)
    print("Data concatenated successfully.")

    print("Step 2: Cleaning the data...")
    cleaned_data_df = merged_data_df.dropna(how='all').drop_duplicates().reset_index(drop=True)
    cleaned_data_df = cleaned_data_df[cleaned_data_df['Order ID'] != 'Order ID'].reset_index(drop=True)
    print("Data cleaned successfully.")

    print("Step 3: Formatting the data...")
    formatted_data_df = cleaned_data_df.drop("Purchase Address", axis=1)
    formatted_data_df = formatted_data_df.rename(columns={'Order ID': 'Sale_ID', 'Quantity Ordered': 'Quantity_Sold',
                                                        'Price Each': 'Each_Price', 'Order Date': 'Sale_Date'})
    formatted_data_df[['Sale_ID', 'Quantity_Sold', 'Each_Price']] = formatted_data_df[['Sale_ID', 'Quantity_Sold', 'Each_Price']].astype({'Sale_ID': 'int64', 'Quantity_Sold': 'int64', 'Each_Price': 'float64'})
    formatted_data_df['Sale_Date'] = pd.to_datetime(formatted_data_df['Sale_Date'])
    formatted_data_df['Sales'] = formatted_data_df['Quantity_Sold'] * formatted_data_df['Each_Price']
    formatted_data_df = formatted_data_df.sort_values(by='Sale_Date').reset_index(drop=True)
    print("Data formatted successfully.")

    print("Step 4: Saving the processed data to a CSV file...")
    output_directory = '/home/alaa-haggag/Projects/Kafka-Spark_Streaming/Prepared_Data'
    os.makedirs(output_directory, exist_ok=True)
    formatted_data_df.to_csv(os.path.join(output_directory, 'Processed_Data.csv'), index=False)
    print("Processed data saved successfully.")

    print("Step 5: Computing and setting stock quantity...")
    stock_df = formatted_data_df.drop(['Sale_ID', 'Each_Price', 'Sale_Date', 'Sales'], axis=1)
    stocks_df = stock_df.groupby(['Product'], as_index=False)['Quantity_Sold'].sum()
    stocks_df['Stock_Quantity'] = 31000
    stocks_df.to_csv('/home/alaa-haggag/Projects/Kafka-Spark_Streaming/Prepared_Data/Stock_Quantity.csv', index=False)
    print("Stock quantity data saved successfully.")
    print("Data preparation and processing complete.")


# Call the function to execute the data preparation
if __name__ == "__main__":
    data_prepare()
