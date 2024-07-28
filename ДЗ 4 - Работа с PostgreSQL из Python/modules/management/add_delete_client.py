from .phone import add_phone, add_plus_to_phone
from ..validate import validate_client_id, validate_email, validate_string, validate_phones


def add_client(conn, name: str, surname: str, email: str, phone: str = None) -> int:
	"""
		Adds a new client to the database with the given name, surname, and email.

		Parameters:
			phone:
			conn (psycopg2.extensions.connection): The database connection object.
			name (str): The name of the client.
			surname (str): The surname of the client.
			email (str): The email of the client.

		Returns:
			int: The ID of the newly added client.

		Raises:
			TypeError: If the name, surname, or email data type is not str.
			ValueError: If name, surname or email is blank or None.
	"""
	validate_string('name', name)
	validate_string('surname', surname)
	validate_email(email)

	with conn.cursor() as cur:
		cur.execute(
			"""
			INSERT INTO clients (name, surname, email)
			VALUES (%s, %s, %s)
			RETURNING id
			""",
			(name.strip(), surname.strip(), email.strip())
		)
		client_id = cur.fetchone()[0]

		if phone:
			validate_phones(phone)
			phone = add_plus_to_phone(phone)
			add_phone(conn, client_id, phone)

		conn.commit()
		print(f'Client {name} {surname} added successfully! Client ID: {client_id} '
			  f'Email: {email}. Phone: {phone}', end='\n\n')
		return client_id


def del_client(conn, client_id: int) -> None:
	"""
		Deletes a client and their associated phone records from the database.

		Args:
			conn (psycopg2.extensions.connection): The database connection object.
			client_id (int): The ID of the client to be deleted.

		Returns:
			None

		Raises:
			TypeError: If client_id is not an integer.
			ValueError: If client_id does not exist in the database.
	"""
	validate_client_id(client_id)

	with conn.cursor() as cur:
		if not check_client_exists(conn, client_id):
			raise ValueError('Client ID does not exist in the database')

		cur.execute('DELETE FROM clients WHERE id = %s', (client_id,))
		conn.commit()
		print(f'The client with the identifier {client_id} has been permanently deleted from the database!', end='\n\n')


def check_client_exists(conn, client_id: int) -> bool:
	"""Checking the existence of the client in the database"""
	with conn.cursor() as cur:
		cur.execute('SELECT id FROM clients WHERE id = %s', (client_id,))
		return cur.fetchone() is not None

