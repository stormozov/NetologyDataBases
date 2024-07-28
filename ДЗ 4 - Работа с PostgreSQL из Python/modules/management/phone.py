from ..validate import validate_client_id, validate_phones


def add_phone(conn, client_id: int, phone: str) -> None:
    """
        Adds a new phone number to the phones table in the database.

        Args:
            conn (psycopg2.extensions.connection): The database connection.
            client_id (int): The ID of the client associated with the phone number.
            phone (str): The phone number to be added.

        Returns:
            None

        Raises:
            TypeError: If client_id is not an integer or phone is not a string.
            ValueError: If client_id is None or phone is an empty string.
    """
    validate_client_id(client_id)
    validate_phones(phone)

    phone = add_plus_to_phone(phone)

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO phones (client_id, phone)
            VALUES (%s, %s)
            RETURNING id
            """,
            (client_id, phone)
        )

        phone_id = cur.fetchone()[0]
        conn.commit()
        print(f"Phone '{phone}', with ID {phone_id}, has been successfully added "
              f"to the client's account with ID: {client_id}.", end='\n\n')


def del_phone(conn, client_id: int, phone: str) -> None:
    """
        Deletes a phone number from the database.

        Args:
            conn (psycopg2.extensions.connection): The database connection object.
            client_id (int): The ID of the client associated with the phone number.
            phone (str): The phone number to be deleted.

        Returns:
            None

        Raises:
            TypeError: If client_id is not an integer or phone is not a string.
            ValueError: If either client_id or phone is None or empty.
    """
    validate_client_id(client_id)
    validate_phones(phone)

    phone = add_plus_to_phone(phone)
    phone_id = get_phone_id(conn, client_id, phone)

    with conn.cursor() as cur:
        cur.execute('DELETE FROM phones WHERE id = %s', (phone_id,))
        conn.commit()
        print(f"Phone '{phone}' has been successfully deleted "
              f"from the client's account with ID: {client_id}.", end='\n\n')


def get_phone_id(conn, client_id: int, phone: str) -> int | None:
    """
        Returns the ID of the phone number in the database.

        Args:
            conn (psycopg2.extensions.connection): The database connection object.
            client_id (int): The ID of the client associated with the phone number.
            phone (str): The phone number to be retrieved.

        Returns:
            int: The ID of the phone number in the database.
            None: If the phone number is not found in the database.

        Raises:
            ValueError: If either client_id or phone is None.
    """

    with conn.cursor() as cur:
        cur.execute('SELECT id FROM phones WHERE client_id = %s AND phone = %s', (client_id, phone))
        result = cur.fetchone()
        return result[0] if result else None


def add_plus_to_phone(phone: str) -> str:
    """
    Adds a "+" symbol to the beginning of the phone number, but only if it's not already prefixed.

    Args:
        phone (str): The phone number to be prefixed.

    Returns:
        str: The phone number with a "+" symbol added to the beginning, if necessary.
    """
    return "+" + phone if not phone.startswith("+") else phone

