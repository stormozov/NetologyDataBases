import psycopg2
import configparser
from modules.create_db.create_db import create_db
from modules.management.client import add_client, del_client, change_client_info, find_client
from modules.management.phone import add_phone, del_phone
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
		# add_client(conn, 'Richard', 'Hamford', 'hamfordrich@ex.com')
		# add_client(conn, 'Richard', 'Rich', 'richman1@ex.com', '+1234567890')

		# |— Adding some phones
		# add_phone(conn, 30, '+1234567890')

		# |— Deleting some phones
		# del_phone(conn, 27, '1264567845')

		# |— Deleting some clients
		# del_client(conn, 29)

		# |— Updating client info
		# change_client_info(conn, 27, phones=['+1234567888', '+1234567889'])

		# |— Finding clients id in the database
		# find_client(conn, name='Ithan')

		# Checking results from queries above in the terminal
		show_all_tables(conn)

