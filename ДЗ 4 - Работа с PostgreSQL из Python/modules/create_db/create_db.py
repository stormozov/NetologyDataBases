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

