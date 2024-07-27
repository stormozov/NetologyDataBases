from .phone import add_phone, add_plus_to_phone


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
	if not isinstance(name, str):
		raise TypeError('name must be a string')
	if not isinstance(surname, str):
		raise TypeError('surname should be a string')
	if not isinstance(email, str):
		raise TypeError('email should be a string')
	if not name.strip():
		raise ValueError('name cannot be empty')
	if not surname.strip():
		raise ValueError('surname cannot be empty')
	if not email.strip():
		raise ValueError('email cannot be empty')
	if phone is not None and not isinstance(phone, str):
		raise TypeError('phone must be a string or None')

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
	if not isinstance(client_id, int):
		raise TypeError('Client ID must be an integer')

	with conn.cursor() as cur:
		cur.execute('SELECT id FROM clients WHERE id = %s', (client_id,))
		client_exists = cur.fetchone() is not None

		if not client_exists:
			raise ValueError('Client ID does not exist in the database')

		cur.execute('DELETE FROM clients WHERE id = %s', (client_id,))
		conn.commit()
		print(f'The client with the identifier {client_id} has been permanently deleted!', end='\n\n')


def change_client_info(
		conn, client_id, name=None,
		surname=None, email=None, phones=None
) -> None:
	"""
		Updates a client record in the database with the given client_id
		and any of the optional parameters that are not None.

		Args:
			conn (psycopg2.extensions.connection): The database connection.
			client_id (int): The ID of the client to update.
			name (str): The new name for the client.
			surname (str): The new surname for the client.
			email (str): The new email for the client.
			phones (list): A list of phone numbers to replace the existing ones.

		Returns:
			None
	"""
	with conn.cursor() as cur:
		updates, values = [], []

		if name is not None:
			updates.append('name = %s')
			values.append(name)
		if surname is not None:
			updates.append('surname = %s')
			values.append(surname)
		if email is not None:
			updates.append('email = %s')
			values.append(email)

		if updates:
			query = 'UPDATE clients SET ' + ', '.join(updates) + ' WHERE id = %s'
			values.append(client_id)
			cur.execute(query, values)

		if phones:
			phones = [add_plus_to_phone(phone) for phone in phones]
			# Delete existing phones
			cur.execute('DELETE FROM phones WHERE client_id = %s', (client_id,))
			# Add new phones
			cur.executemany(
				'INSERT INTO phones (client_id, phone) VALUES (%s, %s)',
				[(client_id, phone) for phone in phones]
			)

		conn.commit()
		print(f"The client's data with ID {client_id} has been successfully updated!", end='\n\n')


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
	if name is not None and not isinstance(name, str):
		raise TypeError('name must be a string or Non')
	if surname is not None and not isinstance(surname, str):
		raise TypeError('surname must be a string or None')
	if email is not None and not isinstance(email, str):
		raise TypeError('email must be a string or None')
	if phone is not None and not isinstance(phone, str):
		raise TypeError('phone must be a string or None')

	if all(arg is None for arg in [name, surname, email, phone]):
		raise ValueError('At least one search criterion must be provided')

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
			return 'Warning: The search for the specified criteria was unsuccessful'

