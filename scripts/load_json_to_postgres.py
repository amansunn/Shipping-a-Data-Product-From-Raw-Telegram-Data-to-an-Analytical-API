import os
import json
import psycopg2
from pathlib import Path

conn = psycopg2.connect(
    dbname="mydatabase",
    user="myuser",
    password="mysecretpassword",
    host="localhost",
    port=5432
)
cur = conn.cursor()

# Create table if not exists
cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")
cur.execute("""
CREATE TABLE IF NOT EXISTS raw.telegram_messages (
    id SERIAL PRIMARY KEY,
    message_json JSONB
);
""")
conn.commit()

print("Connected to PostgreSQL and ensured raw.telegram_messages table exists.")

# Recursively find all JSON files in data/raw/telegram_messages
# This will find files in all subfolders, e.g., 2025/07-09/message_id.json

data_dir = Path("./data/raw/telegram_messages")
json_files = list(data_dir.rglob("*.json"))
print(f"Found {len(json_files)} JSON files to process.")

inserted_count = 0
for file in json_files:
    print(f"Processing file: {file}")
    with open(file, "r", encoding="utf-8") as f:
        try:
            messages = json.load(f)
        except Exception as e:
            print(f"Failed to load {file}: {e}")
            continue
        for msg in messages:
            cur.execute("INSERT INTO raw.telegram_messages (message_json) VALUES (%s)", [json.dumps(msg)])
            inserted_count += 1
    print(f"Inserted {len(messages)} messages from {file}.")

conn.commit()
print(f"Total messages inserted: {inserted_count}")
cur.close()
conn.close()
print("Database connection closed.")