from ..validate import validate_client_info
from .phone import add_plus_to_phone


def build_query(name: str, surname: str, email: str, phone: str) -> tuple:
	"""Forming a database query for finding clients by name, surname, email, and phone number."""
	query = """
		SELECT id FROM clients
		WHERE (%s IS NULL OR name = %s)
		AND (%s IS NULL OR surname = %s)
		AND (%s IS NULL OR email = %s)
		AND (%s IS NULL OR id IN (SELECT client_id FROM phones WHERE phone = %s))
	"""
	params = [name, name, surname, surname, email, email, phone, phone]
	return query, params


def execute_query(conn, query: str, params: list) -> list:
	"""Executing a database query"""
	with conn.cursor() as cur:
		cur.execute(query, params)
		return cur.fetchall()


def process_results(results: list) -> list:
	"""Processing the results of the enquiry"""
	if results:
		client_ids = [row[0] for row in results]
		print(f'The unique identifiers of the identified clients: {", ".join(f"{x}" for x in client_ids)}', end='\n\n')
		return client_ids
	else:
		print('Warning: The search for the specified criteria was unsuccessful', end='\n\n')


def find_client(
		conn, name: str = None, surname: str = None,
		email: str = None, phone: str = None
) -> list:
	"""Finding clients by name, surname, email, and phone number"""
	validate_client_info(name, surname, email, phone)
	phone = add_plus_to_phone(phone)
	query, params = build_query(name, surname, email, phone)
	results = execute_query(conn, query, params)
	return process_results(results)

