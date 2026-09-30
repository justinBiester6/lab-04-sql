#import statements
import os
import logging
import mysql.connector
import pandas as pd

#reading the DBs
DBHOST = os.getenv("DB_HOST", "localhost")
DBNAME = os.getenv("DB_NAME", "mock_database")
DBUSER = os.getenv("DB_USER", "root")
DBPASS = os.getenv("DB_PASSWORD", "")

#initialize connection and cursor
db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DBNAME)
cur = db.cursor()

def get_data_by_group(value):
	"""
	returns all rows where the group column equals value
	"""

	logging.info("Querying databases for '{value}'")

	#querying from mock by group
	query = "SELECT * FROM mock WHERE `group` = %s;"

	#using try/except for the query
	try:
		#executing the query
		cur.execute(query, (value,))
		results = cur.fetchall()
		#output array
		output = []

		#looping through the results of the query
		for i in results:
			#appending to the output array
			output.append(i)
		#returns output
		return output
	#catching error
	except mysql.connector.Error as e:
        	logging.error(f"MySQL Error in get_data_by_group: {str(e)}")
        	return None

def plot_counts(groupby):
	"""
	run a SELECT ... GROUP BY query that counts rows per distinct value of that column...return the counts
	"""
	logging.info(f"Running summary grouped by column: '{groupby}'")

	#puts the group in backticks if it is a keyword of 'group'
	backtick_column = f"`{groupby}`" if groupby.lower() == "group" else groupby
	query = f"SELECT {backtick_column}, COUNT({backtick_column}) FROM mock GROUP BY {backtick_column};"

	#executing the query for plotting in try/except
	try:
		#execute the query
		cur.execute(query)
		results = cur.fetchall()
                #output array
		output = []

		#looping through the results of the query
		for i in results:
                        #appending to the output array
			output.append(i)

		#creating pandas dataframe
		df = pd.DataFrame(output, columns=[groupby, "count"])

		#return the dataframe
		return df

	#catching error
	except mysql.connector.Error as e:
		logging.error(f"MySQL Error in plot_counts: {str(e)}")
		return None

def main():
	"""
	running the functions created
	"""

	#querying the rows with the specific group
	group_results = get_data_by_group("glorious")

	if group_results is not None:
		#print first 5 rows to test
		for row in group_results[:5]:
			print(row)
			print(f"Total records retrieved: {len(group_results)}")

	#grouping by the 'job' column to count and show bar chart
	df_count = plot_counts("job")
	if df_count is not None:
		#print first 10 rows
		print(df_count.head(10))

	#close cursor and connection
	cur.close()
	db.close()
	logging.info("Database connections successfully closed.")

#calling main
if __name__ == "__main__":
    main()
