from modules.read_config.read_config import read_config
from modules.db_session.create_db_session import create_database_session
from modules.db_management.db_operations import *
from modules.json_to_db.json2db import import_json_data_to_db
from modules.publisher_reports.publisher_sales import get_publisher_sales_report
from modules.fs_tools.path_utils import get_absolute_path

if __name__ == '__main__':
	# Create paths
	json_data = get_absolute_path(['source', 'tests_data.json'])
	settings_data = get_absolute_path(['settings.ini'])

	# Read config file
	config_dict = read_config(settings_data)

	# Create engine for the database
	engine = create_database_session(config_dict)[1]

	# Create tables in the database
	create_tables(engine)

	# Create session for the database
	session = create_database_session(config_dict)[0]

	# (Task #3) Upload data from json file to database
	import_json_data_to_db(session, json_data)

	# (Task #2) Get sales report
	input_publisher = input("Enter the publisher's name or ID: ")
	get_publisher_sales_report(config_dict, input_publisher)

	# Close the session
	session.close()

