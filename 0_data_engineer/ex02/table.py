import psycopg2


def create_connection():
    """create a database connection to a SQLite database"""
    return psycopg2.connect(
        dbname="piscineds",
        user="mdesmart",
        password="mysecretpassword",
        host="localhost",
        port="5432"
    )


def create_table(cursor):
    """create a table in the database"""
    cursor.execute("""
    DROP TABLE IF EXISTS data_2022_oct;

    CREATE TABLE data_2022_oct (
      event_time TIMESTAMPTZ,
      event_type TEXT,
      product_id INT,
      price FLOAT,
      user_id BIGINT,
      user_session UUID
    );
    """)


def copy_data_from_csv(cursor, file_path):
    """copy data from csv file"""
    with open(file_path, 'r') as f:
        next(f)
        cursor.copy_from(f, 'data_2022_oct', sep=',', null='')


def main():
    connection = create_connection()
    cursor = connection.cursor()

    create_table(cursor)
    copy_data_from_csv(cursor, '../../customer/data_2022_oct.csv')

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()
