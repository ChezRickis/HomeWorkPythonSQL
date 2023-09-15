import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            DROP TABLE Phone;
            DROP TABLE Client;
            """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS Client(
            id SERIAL PRIMARY KEY,
            name VARCHAR(60) NOT NULL,
            lastname VARCHAR(60) NOT NULL,
            email VARCHAR(60) NOT NULL UNIQUE);
            """)
        conn.commit()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS Phone(
            number DECIMAL UNIQUE CHECK (number <= 99999999999),
            id INTEGER REFERENCES Client(id));
            """)
        conn.commit()


def add_client(conn, name, lastname, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO Client (name, lastname, email)
            VALUES (%s, %s, %s)
            RETURNING id, name, lastname, email;
            """, (name, lastname, email,))
        print('Added client:', end=' ')
        return cur.fetchone()


def add_phone(conn, id, number):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO Phone (id, number)
            VALUES (%s, %s)
            RETURNING id, number;
            """, (id, number,))
        print('Added phone:', end=' ')
        return cur.fetchone()
# , name, lastname, email


def change_client(conn, id, name=None, lastname=None, email=None):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE Client
            SET name=%s, lastname=%s, email=%s
            WHERE id=%s
            RETURNING id, name, lastname, email;
            """, (name, lastname, email, id,))
        print('Changed client:', end=' ')
        return cur.fetchone()


def change_phone(conn, id, number=None):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE Phone
            SET number=%s
            WHERE id=%s
            RETURNING id, number;
            """, (number, id,))
        print('Changed phone:', end=' ')
        return cur.fetchone()


def delete_phone (conn, id, number=None):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM Phone
            WHERE id=%s OR number=%s
            RETURNING id, number;
            """, (id, number,))
        print('Deleted client:', end=' ')
        return cur.fetchone()


def delete_client(conn, id, name=None, lastname=None, email=None):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM Client
            WHERE id=%s OR name=%s OR lastname=%s OR email=%s
            RETURNING id, name, lastname, email;
            """, (id, name, lastname, email,))
        print('Deleted phone:', end=' ')
        return cur.fetchone()


def find_client(conn, name=None, lastname=None, email=None, number=None):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT c.name, c.email, p.number FROM Client c
            LEFT JOIN Phone p ON c.id = p.id
            WHERE c.name=%s OR c.lastname=%s OR c.email=%s OR p.number=%s;
            """, (name, lastname, email, number,))
        print('Found:', end=' ')
        return cur.fetchone()


with psycopg2.connect(database="HomeWorkPythonSQL", user="postgres", password="896261228ll") as conn:
    create_db(conn)
    print(add_client(conn, 'Jerry', 'Smits', 'jerry@mail.ru'))
    print(add_phone(conn, '1', '89355463327'))
    print(find_client(conn, 'Jerry'))
    print(change_client(conn, '1', 'Albert', 'Richards', 'albert@mail.com'))
    print(change_phone(conn, '1', '89109364535'))
    print(find_client(conn, 'Albert'))
    print(delete_phone(conn, '1', '89109467816'))
    print(delete_client(conn, '1'))
    print(find_client(conn, 'Albert'))
conn.close()