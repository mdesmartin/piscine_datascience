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
    DROP TABLE IF EXISTS items;

    CREATE TABLE items (
      product_id INT,
      category_id BIGINT,
      category_code TEXT,
      brand TEXT
    );
    """)

def create_temp_table(cursor):
    """create a temporary table in the database"""
    cursor.execute("""
    DROP TABLE IF EXISTS temp_items;

    CREATE TEMP TABLE temp_items (
      product_id INT,
      category_id BIGINT,
      category_code TEXT,
      brand TEXT
    );
    """)

def copy_data_from_csv(cursor, file_path):
    """copy data from csv file"""
    with open(file_path, 'r') as f:
        next(f)
        cursor.copy_from(f, 'temp_items', sep=',', null='')

def remove_duplicates_and_insert(cursor):
    """remove duplicates and insert into table"""
    cursor.execute("""
    INSERT INTO items
    SELECT DISTINCT ON (product_id) *
    FROM temp_items
    ORDER BY product_id;
    """)

def main():
    connection = create_connection()
    cursor = connection.cursor()

    create_table(cursor)
    create_temp_table(cursor)
    copy_data_from_csv(cursor, '../../../item/item.csv')
    remove_duplicates_and_insert(cursor)

    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
