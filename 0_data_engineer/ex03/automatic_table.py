#!/usr/bin/env python3
import os
import csv
import glob
import psycopg2
from datetime import datetime

HOST = "localhost"
PORT = "5432"
DBNAME = "piscineds"
USER = "mdesmart"
PASSWORD = "mysecretpassword"

CSV_DIR = "/Users/mdesmartin/Documents/Dev/42/PostCC/subject/customer"

def infer_type(values):
    non_empty = [v for v in values if v.strip()]
    if not non_empty:
        return "TEXT"

    try:
        for v in non_empty:
            datetime.fromisoformat(v)
        return "TIMESTAMP"
    except:
        pass

    # Try int
    try:
        for v in non_empty:
            int(v)
        return "INT"
    except:
        pass

    try:
        for v in non_empty:
            float(v)
        return "NUMERIC"
    except:
        pass

    bool_set = set(v.lower() for v in non_empty)
    if bool_set.issubset({"true", "false", "t", "f", "0", "1"}):
        return "BOOLEAN"

    try:
        for v in non_empty:
            datetime.strptime(v, "%Y-%m-%d")
        return "DATE"
    except:
        pass

    return "TEXT"

def process_csv(conn, csv_file):
    cur = conn.cursor()
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        sample_data = []
        for i, row in enumerate(reader):
            sample_data.append(row)
            if i > 1000:
                break

    columns_samples = list(zip(*sample_data)) if sample_data else [[] for _ in header]

    column_types = []
    for i, col_name in enumerate(header):
        col_values = columns_samples[i] if columns_samples else []
        inferred = infer_type(col_values)
        column_types.append((col_name, inferred))

    if column_types[0][1] != "TIMESTAMP":
        column_types[0] = (column_types[0][0], "TIMESTAMP")

    base_name = os.path.basename(csv_file)
    table_name = os.path.splitext(base_name)[0]

    cols_def = ", ".join(f'"{name}" {ctype}' for name, ctype in column_types)
    create_sql = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({cols_def});'
    cur.execute(create_sql)

    copy_sql = f'COPY "{table_name}" FROM STDIN CSV HEADER'
    with open(csv_file, 'r', encoding='utf-8') as f:
        cur.copy_expert(copy_sql, f)

    cur.close()

def main():
    conn = psycopg2.connect(
        host=HOST,
        port=PORT,
        database=DBNAME,
        user=USER,
        password=PASSWORD
    )
    conn.autocommit = True

    csv_files = glob.glob(os.path.join(CSV_DIR, "*.csv"))
    for csv_file in csv_files:
        process_csv(conn, csv_file)

    conn.close()

if __name__ == "__main__":
    main()