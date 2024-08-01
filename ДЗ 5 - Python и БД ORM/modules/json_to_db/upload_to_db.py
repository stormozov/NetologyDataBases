from .read_file import read_file
from ..db_management.models import Book, Shop, Sale, Stock, Publisher


def upload_to_db(session, path: str) -> None:
	"""Upload data from json file to database"""
	data = read_file(path)
	models = {
		'publisher': Publisher,
		'shop': Shop,
		'book': Book,
		'stock': Stock,
		'sale': Sale,
	}

	for record in data:
		model_name = record.get('model')
		model = models.get(model_name)

		if model is None:
			continue

		fields = record.get('fields')

		for key, value in fields.items():
			if isinstance(value, str) and value.replace('.', '', 1).isdigit():
				try:
					fields[key] = float(value)
				except ValueError:
					pass

		# Create a new instance of the model with the parsed fields and add it to the session
		session.add(model(**fields))

	session.commit()
