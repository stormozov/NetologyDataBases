from .read_json_file import read_json_file
from ..db_management.models import Book, Shop, Sale, Stock, Publisher


def convert_string_to_float(fields: dict) -> dict:
	"""Convert string values to float if possible"""
	for key, value in fields.items():
		if isinstance(value, str) and value.replace('.', '', 1).isdigit():
			try:
				fields[key] = float(value)
			except ValueError:
				pass
	return fields


def get_model(model_name: str, models: dict) -> type:
	"""Get a model class by its name"""
	return models.get(model_name)


def create_or_update_record(session, model: type, fields: dict) -> None:
	"""Create or update a record in the database"""
	existing_record = session.query(model).filter_by(**fields).first()

	if existing_record is not None:
		for key, value in fields.items():
			setattr(existing_record, key, value)
	else:
		session.add(model(**fields))


def import_json_data_to_db(session, path: str) -> None:
	"""Upload data from a JSON file to the database"""
	data = read_json_file(path)
	models = {
		'publisher': Publisher,
		'shop': Shop,
		'book': Book,
		'stock': Stock,
		'sale': Sale,
	}

	for record in data:
		model_name = record.get('model')
		model = get_model(model_name, models)

		if model is None:
			continue

		fields = record.get('fields')
		fields = convert_string_to_float(fields)

		create_or_update_record(session, model, fields)

	session.commit()
