import sys
import os
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
    DataModel = type(
        f"DataModel_{table_name}",
        (base,),
        {
            '__tablename__': table_name,
            'event_time': Column(DateTime, nullable=False),
            'event_type': Column(String, nullable=False),
            'product_id': Column(Integer, nullable=False),
            'price': Column(Float, nullable=False),
            'user_id': Column(BigInteger, nullable=False),
            'user_session': Column(UUID(as_uuid=True), nullable=False),
            '__table_args__': (
                PrimaryKeyConstraint(
                    'event_time', 'event_type', 'product_id', 'price',
                    'user_id', 'user_session', name=f'{table_name}_pkey'
                ),
            )
        }
    )
    DataModel.__table__.drop(bind=engine, checkfirst=True)
    base.metadata.create_all(bind=engine)
    return DataModel

def load_and_validate_csv(file_path):
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    df['event_time'] = pd.to_datetime(df['event_time'], errors='coerce')
    df['event_type'] = df['event_type'].astype(str)
    df['product_id'] = pd.to_numeric(df['product_id'], errors='coerce').astype('Int32')
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['user_id'] = pd.to_numeric(df['user_id'], errors='coerce').astype('Int64')
    df['user_session'] = df['user_session'].apply(
        lambda val: uuid.UUID(val) if isinstance(val, str) and len(val) == 36 else None
    )

    df.dropna(subset=['event_time', 'event_type', 'product_id', 'price', 'user_id', 'user_session'], inplace=True)
    df.drop_duplicates(subset=['event_time', 'event_type', 'product_id', 'price', 'user_id', 'user_session'], inplace=True)

    assert not df.empty, "DataFrame is empty"
    return df

def insert_data(session, df, data_model):
    """Insert the validated data into the database using bulk insert."""
    try:
        data_list = []
        for index, row in df.iterrows():
            data = data_model(
                event_time=row['event_time'],
                event_type=row['event_type'],
                product_id=row['product_id'],
                price=row['price'],
                user_id=row['user_id'],
                user_session=row['user_session']
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

    folder_path = '../../../subject/customer/'
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    for csv_file in csv_files:
        table_name = os.path.splitext(csv_file)[0]

        data_model = create_tables(engine, base, table_name)
        print(f"Processing {csv_file} into table '{table_name}': {format_time(time.time() - start_time)}")

        csv_path = os.path.join(folder_path, csv_file)
        df = load_and_validate_csv(csv_path)

        insert_data(session, df, data_model)
        print(f"Finished inserting data for {csv_file}: {format_time(time.time() - start_time)}")

    session.close()
    print(f"All CSV files have been processed successfully: {format_time(time.time() - start_time)}")

if __name__ == '__main__':
    main()
