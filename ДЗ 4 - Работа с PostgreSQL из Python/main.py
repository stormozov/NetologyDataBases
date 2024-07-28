import psycopg2
import configparser
from modules.create_db.create_db import create_db
from modules.management.add_delete_client import add_client, del_client
from modules.management.find_client import find_client
from modules.management.phone import add_phone, del_phone
from modules.management.update_info import update_client_info
from modules.management.phone import show_client_phone
from modules.show_tables.show_tables import *

config = configparser.ConfigParser()
config.read('settings.ini')
user, password = config['DB']['username'], config['DB']['password']
host, database = config['DB']['host'], config['DB']['database']

if __name__ == '__main__':
	with psycopg2.connect(
			user=user,
			password=password,
			host=host,
			database=database
	) as conn:
		create_db(conn)

		# |— Adding some clients
		# add_client(conn, 'John', 'Doe', 'jdoe@ex.com')

		# |— Adding some phones
		# add_phone(conn, 1, '+1233336633')

		# |— Deleting some phones
		# del_phone(conn, 1, '+1233336633')

		# |— Deleting some clients
		# del_client(conn, 1)

		# |— Updating client info
		# update_client_info(conn, 1, surname='Petersen', email='petersen@ex.com')

		# |— Finding clients id in the database
		# find_client(conn, name='John')

		# |— Showing client phone
		# show_client_phone(conn, 1)

		# Checking results from queries above in the terminal
		# show_all_tables(conn)

