#import statements
import os
import pandas as pd
import logging
import mysql.connector

def read_data(filename):
	"""
	Loads the CSV into a pandas DataFrame
	"""
	#reads the file
	logging.info("Reading data from CSV file.")

	df = pd.read_csv(filename)

	#returns the dataframe
	logging.info("CSV file successfully loaded.")
	return df

def clean_data(data):
	"""
	Prepares the DataFrame for upload and remove rows with missing values, and return the cleaned DataFrame.
	"""

	#drops rows with missings values
	logging.info("Cleaning data")

	clean_data = data.dropna()

	#returns cleaned data
	logging.info("Missing rows removed")

	return clean_data

def load_data(data, table):
	"""
	writes the DataFrame to MySQL and create the mock table (if it doesn't exist) and upload the DataFrame into it
	"""

	logging.info("Starting database upload")

	#reading the DBs from the environment variables
	db_host = os.getenv("DB_HOST")
	db_name = os.getenv("DB_NAME")
	db_user = os.getenv("DB_USER")
	db_password = os.getenv("DB_PASSWORD")

	#connecting the database inside a try/except
	try:
		connection = mysql.connector.connect(
            		host=db_host,
            		database=db_name,
            		user=db_user,
            		password=db_password
        	)

		#connecting to the db with cursor
		cursor = connection.cursor()
		logging.info("Connected to the database")

		#creating the table if it does not exist
		create_table_query = f"""
        	CREATE TABLE IF NOT EXISTS {table} (
            		id BIGINT,
            		`group` VARCHAR(255),
            		first_name VARCHAR(255),
            		last_name VARCHAR(255),
            		city VARCHAR(255),
            		job VARCHAR(255)
        	);
        	"""
		cursor.execute(create_table_query)
		logging.info(f"Table '{table}' is done.")

		#uploading the rows to the datbase
		#Approach A: row-by-row inserts with mysql-connector-python

		insert_query = f"""
        	INSERT INTO {table} (id, `group`, first_name, last_name, city, job)
        	VALUES (%s, %s, %s, %s, %s, %s);
        	"""

		#looping over the dataframe by row
		logging.info("Uploading the rows to the database")
		for index, row in data.iterrows():
			row_values = (
                		int(row['id']),
                		str(row['group']),
                		str(row['first_name']),
                		str(row['last_name']),
                		str(row['city']),
                		str(row['job'])
            		)
			#executing the insert
			cursor.execute(insert_query, row_values)

		#commiting the connection
		connection.commit()
		logging.info("All data uploaded and commited")

	#catching errors
	except mysql.connector.Error as error:
        	logging.error(f"Failed to upload data to MySQL: {error}")

	finally:
		#closing the cursor and connection
		if 'connection' in locals() and connection.is_connected():
            		cursor.close()
            		connection.close()
            		logging.info("MySQL connection and cursor closed.")

def main():
	"""
	main function that calls the functions defined
	"""
	logging.info("Starting the main function")

	#read data
	dirty_df = read_data("MOCK_DATA.csv")

	#clean data
	clean_df = clean_data(dirty_df)

	#loading the data
	load_data(clean_df, table="mock")

	logging.info("Main function complete")

#call main
if __name__ == "__main__":
	main()
