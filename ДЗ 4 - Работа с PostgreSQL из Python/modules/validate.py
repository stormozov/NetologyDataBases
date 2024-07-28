def validate_client_id(client_id: int) -> None:
    """Checks that client_id is a positive integer."""
    if not isinstance(client_id, int) or client_id <= 0:
        raise ValueError('client_id must be a positive integer')


def validate_string(arg_name: str, arg_value: str) -> None:
    """Checks that the string is not empty and is a string."""
    if arg_value is not None and not isinstance(arg_value, str):
        raise ValueError(f'{arg_name} must be a string or None')
    if arg_value == '':
        raise ValueError(f'{arg_name} cannot be an empty string')


def validate_email(email: str) -> None:
    """Checks that email contains the @ character and is not empty."""
    if email is not None and not isinstance(email, str):
        raise ValueError('email must be a string or None')
    if email == '':
        raise ValueError('email cannot be an empty string')
    if email is not None and '@' not in email:
        raise ValueError('email must contain the @ symbol')


def validate_phones(phones: list[str] | str = None) -> None:
    """Checks that the phone list is not empty and contains only strings."""
    if phones is None:
        return

    if isinstance(phones, str):
        phones = [phones]

    if not phones:
        raise ValueError('phones list cannot be empty')

    for phone in phones:
        if not isinstance(phone, str) or phone == '':
            raise ValueError('phone must be a non-empty string')


def validate_at_least_one_parameter(name: str, surname: str, email: str, phone: list[str] | str) -> None:
    """Checks that at least one parameter is not None."""
    if all(arg is None for arg in [name, surname, email, phone]):
        raise ValueError('At least one search criterion must be provided')


def validate_client_info(
    name: str = None, surname: str = None,
    email: str = None, phones: list[str] = None
) -> None:
    """Comprehensive checks of the client's information."""
    validate_at_least_one_parameter(name, surname, email, phones)
    validate_string('name', name)
    validate_string('surname', surname)
    validate_email(email)
    validate_phones(phones)

