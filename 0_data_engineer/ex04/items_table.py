import psycopg2

def create_connection():
    return psycopg2.connect(
        dbname="piscineds",
        user="mdesmart",
        password="mysecretpassword",
        host="localhost",
        port="5432"
    )

def create_table(cursor):
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
    with open(file_path, 'r') as f:
        next(f)
        cursor.copy_from(f, 'temp_items', sep=',', null='')

def remove_duplicates_and_insert(cursor):
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
