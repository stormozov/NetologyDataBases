from .phone import add_phone, add_plus_to_phone
from ..validate import validate_client_info, validate_client_id


def add_client(conn, name: str, surname: str, email: str, phone=None) -> int:
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
	validate_client_info(name, surname, email, [phone])

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
		cur.execute('SELECT id FROM clients WHERE id = %s', (client_id,))
		client_exists = cur.fetchone() is not None

		if not client_exists:
			raise ValueError('Client ID does not exist in the database')

		cur.execute('DELETE FROM clients WHERE id = %s', (client_id,))
		conn.commit()
		print(f'The client with the identifier {client_id} has been permanently deleted!', end='\n\n')


def find_client(
		conn, name=None, surname=None,
		email=None, phone=None
) -> list | str:
	"""
		Finds clients in the database that match the given criteria.

		Args:
			conn (psycopg2.extensions.connection): The database connection object.
			name (str): The first name of the client.
			surname (str): The last name of the client.
			email (str): The email of the client.
			phone (str): The phone number of the client.

		Returns:
			list: A list of client IDs that match the given criteria in the database.
			str: A message indicating that no clients were found that match the given criteria.

		Raises:
			TypeError: If name, surname, email, or phone are not strings or None.
			ValueError: If all search criteria (name, surname, email, phone) are None.
	"""
	validate_client_info(name, surname, email, phone)

	with conn.cursor() as cur:
		query = """
			SELECT id FROM clients
			WHERE (%s IS NULL OR name = %s)
			AND (%s IS NULL OR surname = %s)
			AND (%s IS NULL OR email = %s)
			AND (%s IS NULL OR id IN (SELECT client_id FROM phones WHERE phone = %s))
		"""
		params = [name, name, surname, surname, email, email, phone, phone]
		cur.execute(query, params)

		if cur.rowcount != 0:
			client_ids = [row[0] for row in cur.fetchall()]
			print(f'The unique identifiers of the identified clients: {client_ids}', end='\n\n')
			return client_ids
		else:
			print('Warning: The search for the specified criteria was unsuccessful', end='\n\n')

