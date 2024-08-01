from sqlalchemy import inspect
from modules.read_config.read_config import read_config
from modules.db_session.create_db_session import create_database_session
from modules.db_management.db_operations import *
from modules.json_to_db.upload_to_db import upload_to_db
from modules.db_management.models import Book, Shop, Sale, Stock, Publisher

if __name__ == '__main__':
	# Read config file
	config_dict = read_config('settings.ini')

	# Create engine for the database
	engine = create_database_session(config_dict)[1]

	# Create tables in the database
	create_tables(engine)

	# Create session for the database
	session = create_database_session(config_dict)[0]

	# Upload data from json file to database
	# upload_to_db(session, 'source/tests_data.json')

	# input_publisher = input("Enter the publisher's name or ID: ")
	# get_publisher_sales_report(config_dict, input_publisher)

	# Close the session
	session.close()

