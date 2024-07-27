def show_clients(conn) -> None:
	"""
	Show the content of the 'clients' table in the database.

	Parameters:
		conn (psycopg2.extensions.connection): The connection to the database.

	Returns:
		None
	"""
	with conn.cursor() as cur:
		cur.execute('SELECT * FROM clients')
		print('— Clients table content:\n', cur.fetchall())


def show_phones(conn) -> None:
	"""
	Show the content of the 'phones' table in the database.

	Parameters:
		conn (psycopg2.extensions.connection): The connection to the database.

	Returns:
		None
	"""
	with conn.cursor() as cur:
		cur.execute('SELECT * FROM phones')
		print('— Phones table content:\n', cur.fetchall())


def show_all_tables(conn) -> None:
	"""
	Displays the contents of the clients and phones tables in the given database connection.

	Args:
		conn (psycopg2.extensions.connection): The database connection object.

	Returns:
		None
	"""
	show_clients(conn)
	show_phones(conn)

