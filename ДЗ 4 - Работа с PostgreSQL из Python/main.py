import psycopg2
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')
user, password = config['DB']['username'], config['DB']['password']
host, database = config['DB']['host'], config['DB']['database']


def create_db(conn) -> None:
    """
        Creates a database with two tables: 'clients' and 'phones'.

        Parameters:
            conn (psycopg2.extensions.connection): The database connection object.

        Returns:
            None
    """
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                surname VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phones (
                id SERIAL PRIMARY KEY,
                client_id INTEGER NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
                phone VARCHAR(20) UNIQUE CHECK (phone ~ '^[0-9+()-]{10,20}$')
            );
        """)
        conn.commit()


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
    """
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO clients (name, surname, email)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (name, surname, email)
        )
        client_id = cur.fetchone()[0]
        
        if phone:
            add_phone(conn, client_id, phone)
        
        conn.commit()
        return client_id


def add_phone(conn, client_id: int, phone: str) -> None:
    """
        Adds a new phone number to the phones table in the database.

        Args:
            conn (psycopg2.extensions.connection): The database connection.
            client_id (int): The ID of the client associated with the phone number.
            phone (str): The phone number to be added.

        Returns:
            None
    """
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO phones (client_id, phone)
            VALUES (%s, %s)
            """,
            (client_id, phone)
        )
        conn.commit()


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
            updates.append("name = %s")
            values.append(name)
        if surname is not None:
            updates.append("surname = %s")
            values.append(surname)
        if email is not None:
            updates.append("email = %s")
            values.append(email)

        if updates:
            query = "UPDATE clients SET " + ", ".join(updates) + " WHERE id = %s"
            values.append(client_id)
            cur.execute(query, values)

        if phones is not None:
            # Delete existing phones
            cur.execute('DELETE FROM phones WHERE client_id = %s', (client_id,))
            # Add new phones
            cur.executemany(
                'INSERT INTO phones (client_id, phone) VALUES (%s, %s)',
                [(client_id, phone) for phone in phones]
            )

        conn.commit()


def del_phone(conn, client_id: int, phone: str) -> None:
    """
        Deletes a phone number from the database.

        Args:
            conn (psycopg2.extensions.connection): The database connection object.
            client_id (int): The ID of the client associated with the phone number.
            phone (str): The phone number to be deleted.

        Returns:
            None
    """
    if not client_id or not phone:
        return None

    phone_id = get_phone_id(conn, client_id, phone)
    with conn.cursor() as cur:
        cur.execute('DELETE FROM phones WHERE id = %s', (phone_id,))
        conn.commit()


def get_phone_id(conn, client_id: int, phone: str) -> int or None:
    """
        Returns the ID of the phone number in the database.

        Args:
            conn (psycopg2.extensions.connection): The database connection object.
            client_id (int): The ID of the client associated with the phone number.
            phone (str): The phone number to be retrieved.

        Returns:
            int: The ID of the phone number in the database.
    """
    if not client_id or not phone:
        return None

    with conn.cursor() as cur:
        cur.execute('SELECT id FROM phones WHERE client_id = %s AND phone = %s', (client_id, phone))
        return cur.fetchone()[0]


def del_client(conn, client_id: int) -> None:
    """
        Deletes a client and their associated phone records from the database.

        Args:
            conn (psycopg2.extensions.connection): The database connection object.
            client_id (int): The ID of the client to be deleted.

        Returns:
            None
    """
    with conn.cursor() as cur:
        cur.execute('DELETE FROM clients WHERE id = %s', (client_id,))
        conn.commit()


def find_client(
        conn, name=None, surname=None,
        email=None, phone=None
) -> list:
    """
        Finds clients in the database that match the given criteria.

        Args:
            conn (psycopg2.extensions.connection): The database connection object.
            name (str): The first name of the client.
            surname (str): The last name of the client.
            email (str): The email of the client.
            phone (str): The phone number of the client.

        Returns:
            list: A list of client IDs that match the given criteria.
    """
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
        return [row[0] for row in cur.fetchall()]


with psycopg2.connect(
    user=user,
    password=password,
    host=host,
    database=database
) as conn:
    create_db(conn)
    # chanmina = add_client(conn, 'Chanmina', 'Chanmina', 'chanmina@example.com')
    # add_phone(conn, chanmina, '+193459463')
    # din = add_client(conn, 'Din', 'Sakay', 'dinsakay@example.com', '+193245463')
    # add_phone(conn, 18, '+144245463')
    # change_client_info(
    #     conn, client_id=13, name='Emely',
    #     surname='James', email='emelyjames@example.com', phones=['+193446464']
    # )
    # del_phone(conn, 20)
    # del_client(conn, 18)
    print(find_client(conn, 'John'))
    print(find_client(conn, email='johndoe12@example.com'))

    # Checking results from queries above in the terminal
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM clients')
        print('— Clients table content:\n', cur.fetchall())

        cur.execute('SELECT * FROM phones')
        print('— Phones table content:\n', cur.fetchall())

