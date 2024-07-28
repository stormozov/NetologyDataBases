from .phone import add_phone, add_plus_to_phone
from ..validate import validate_client_info, validate_client_id


def update_client_info(
		conn, client_id: int, name: str = None,
		surname: str = None, email: str = None, phones: list[str] | str = None
) -> None:
	"""
		Updates the information of a client in the database.

		Args:
			conn (psycopg2.extensions.connection): The database connection object.
			client_id (int): The ID of the client.
			name (str, optional): The new name of the client. Defaults to None.
			surname (str, optional): The new surname of the client. Defaults to None.
			email (str, optional): The new email of the client. Defaults to None.
			phones (list[str] or str, optional): The new phone numbers of the client. Defaults to None.

		Returns:
			None

		Raises:
			None
	"""
	validate_client_id(client_id)
	validate_client_info(name, surname, email, phones)

	change_client_info(conn, client_id, name, surname, email)

	if phones:
		update_client_phones(conn, client_id, phones)

	conn.commit()
	print(f"The client's data with ID {client_id} has been successfully updated!", end='\n\n')


def build_update_query(updates: list) -> str:
	"""
	Builds the UPDATE query string.

	Args:
		updates (list): A list of update statements (e.g. ['name = %s', 'surname = %s'])

	Returns:
		str: The complete UPDATE query string
	"""
	return f'UPDATE clients SET {", ".join(updates)} WHERE id = %s'


def build_update_params(name: str = None, surname: str = None, email: str = None) -> tuple:
	"""
	Builds the update parameters and values.

	Args:
		name (str, optional): The new name of the client. Defaults to None.
		surname (str, optional): The new surname of the client. Defaults to None.
		email (str, optional): The new email of the client. Defaults to None.

	Returns:
		tuple: A tuple containing the update parameters and values
	"""
	fields = {'name': name, 'surname': surname, 'email': email}
	updates, values = [], []

	for field, value in fields.items():
		if value is not None:
			updates.append(f'{field} = %s')
			values.append(value)

	return updates, values


def change_client_info(
		conn, client_id: int, name: str = None,
		surname: str = None, email: str = None
) -> None:
	"""
	Updates the information of a client in the database.

	Args:
		conn (psycopg2.extensions.connection): The database connection object.
		client_id (int): The ID of the client to update.
		name (str, optional): The new name of the client. Defaults to None.
		surname (str, optional): The new surname of the client. Defaults to None.
		email (str, optional): The new email of the client. Defaults to None.

	Returns:
		None
	"""
	with conn.cursor() as cur:
		updates, values = build_update_params(name, surname, email)

		if updates:
			query = build_update_query(updates)
			with conn.cursor() as cur:
				cur.execute(query, tuple(values + [client_id]))


def update_client_phones(conn, client_id: int, phones: list[str] | str) -> None:
	"""
		Updates the phone numbers of a client in the database.

		Args:
			conn (psycopg2.extensions.connection): The database connection object.
			client_id (int): The ID of the client to update.
			phones (list[str] or str): The new phone numbers of the client.

		Returns:
			None

		Notes:
			This function first deletes all existing phone numbers associated with the client,
			and then inserts the new phone numbers. The `add_plus_to_phone` function is used
			to format the phone numbers before inserting them into the database.
	"""
	with conn.cursor() as cur:
		# Delete existing phones
		cur.execute('DELETE FROM phones WHERE client_id = %s', (client_id,))

		if isinstance(phones, str):
			phones = [phones]

		# Adding new phones
		phones = [add_plus_to_phone(phone) for phone in phones]
		cur.executemany(
			'INSERT INTO phones (client_id, phone) VALUES (%s, %s)',
			[(client_id, phone) for phone in phones]
		)

