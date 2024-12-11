import sys
import pandas as pd
from sqlalchemy import create_engine, Column, DateTime, Integer, BigInteger, String, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import PrimaryKeyConstraint
import uuid
import time
from datetime import timedelta

DB_USER = 'mdesmart'
DB_PASSWORD = 'mysecretpassword'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'piscineds'

def configure_database():
    """Configure the database connection and return the engine, base, and session factory."""
    try:
        db_url = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        engine = create_engine(db_url)
        base = declarative_base()
        session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return engine, base, session_local
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def create_tables(engine, base, table_name):
    """Create the table in the database."""
    class DataModel(base):
        __tablename__ = table_name
        product_id = Column(Integer, nullable=False)
        category_id = Column(BigInteger, nullable=True)
        category_code = Column(BigInteger, nullable=True)
        brand = Column(String, nullable=True)
        __table_args__ = (
            PrimaryKeyConstraint('product_id', name=f'{table_name}_pkey'),
        )

    base.metadata.create_all(bind=engine)
    return DataModel

def load_and_validate_csv(file_path):
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    df['product_id'] = pd.to_numeric(df['product_id'], errors='coerce').astype('Int32')
    df['category_id'] = pd.to_numeric(df['category_id'], errors='coerce').astype('Int64')
    df['category_code'] = pd.to_numeric(df['category_code'], errors='coerce').astype('Int64')
    df['brand'] = df['brand'].astype(str)

    df.dropna(subset=['product_id'], inplace=True)
    df.drop_duplicates(subset=['product_id'], inplace=True)
    # df.drop_duplicates(inplace=True)
    df.replace({pd.NA: None}, inplace=True)

    return df

def insert_data(session, df, data_model):
    """Insert the validated data into the database using bulk insert."""
    try:
        data_list = []
        for index, row in df.iterrows():
            data = data_model(
                product_id=row['product_id'],
                category_id=row['category_id'],
                category_code=row['category_code'],
                brand=row['brand']
            )
            data_list.append(data)
        session.bulk_save_objects(data_list)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        sys.exit(1)

def format_time(seconds):
    """Format the elapsed time in minutes and seconds."""
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes)}mn{int(seconds)}s"

def main():
    """Main function to orchestrate the entire process."""
    start_time = time.time()

    engine, base, session_local = configure_database()
    session = session_local()

    csv_file = '../../../subject/item/item.csv'
    table_name = 'items'

    print(f"Starting database configuration: {format_time(time.time() - start_time)}")
    data_model = create_tables(engine, base, table_name)
    print(f"Tables created: {format_time(time.time() - start_time)}")

    print(f"Loading and validating CSV: {format_time(time.time() - start_time)}")
    df = load_and_validate_csv(csv_file)
    print(f"CSV loaded and validated: {format_time(time.time() - start_time)}")

    print(f"Inserting data into database: {format_time(time.time() - start_time)}")
    insert_data(session, df, data_model)
    print(f"Data inserted: {format_time(time.time() - start_time)}")

    session.close()
    print(f"Session closed: {format_time(time.time() - start_time)}")

if __name__ == '__main__':
    main()
