import psycopg2
import os
import glob


def create_connection():
    """create a database connection to a SQLite database"""
    return psycopg2.connect(
        dbname="piscineds",
        user="mdesmart",
        password="mysecretpassword",
        host="localhost",
        port="5432"
    )


def create_table(cursor, table_name):
    """create a table in the database"""
    cursor.execute(f"""
    DROP TABLE IF EXISTS {table_name};

    CREATE TABLE {table_name} (
      event_time TIMESTAMPTZ,
      event_type TEXT,
      product_id INT,
      price FLOAT,
      user_id BIGINT,
      user_session UUID
    );
    """)


def copy_data_from_csv(cursor, file_path, table_name):
    """copy data from csv file"""
    with open(file_path, 'r') as f:
        next(f)
        cursor.copy_from(f, table_name, sep=',', null='')


def main():
    connection = create_connection()
    cursor = connection.cursor()

    csv_files = glob.glob(os.path.join('../../../customer', '*.csv'))

    for csv_file in csv_files:
        table_name = os.path.splitext(os.path.basename(csv_file))[0]

        create_table(cursor, table_name)
        copy_data_from_csv(cursor, csv_file, table_name)

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()
