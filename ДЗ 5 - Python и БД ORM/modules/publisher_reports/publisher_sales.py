from ..db_management.models import Book, Shop, Sale, Stock, Publisher
from ..db_session.create_db_session import create_database_session
from sqlalchemy import or_


def get_publisher(session, name_or_id: str | int) -> Publisher | None:
	"""Gets publisher by name or ID."""
	try:
		filtering_condition = or_(Publisher.name == name_or_id, Publisher.id == int(name_or_id))
	except ValueError:
		filtering_condition = Publisher.name == name_or_id

	publisher = session.query(Publisher).filter(filtering_condition).first()

	if not publisher:
		print(f'Publisher "{name_or_id}" not found.')
		return None

	return publisher


def get_sales_query(session, publisher: Publisher) -> list:
	"""Gets sales query by publisher."""
	return session.query(Book.title, Shop.name, Sale.price, Sale.date_sale). \
		join(Stock, Book.id == Stock.id_book). \
		join(Shop, Stock.id_shop == Shop.id). \
		join(Sale, Stock.id == Sale.id_stock). \
		filter(Book.publisher == publisher)


def print_sales_report(query: list, time_format: str = '%d.%m.%Y') -> None:
	"""Prints sales report by publisher."""
	for row in query:
		print(f'{row[0]} | {row[1]} | {row[2]} | {row[3].strftime(time_format)}')


def get_publisher_sales_report(config_dict: dict, name_or_id: str | int) -> None:
	"""Gets sales report by publisher."""
	session, engine = create_database_session(config_dict)
	publisher = get_publisher(session, name_or_id)
	query = get_sales_query(session, publisher)
	print_sales_report(query)
	session.close()
