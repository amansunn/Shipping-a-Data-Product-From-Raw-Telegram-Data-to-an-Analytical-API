import psycopg2
import json
from pathlib import Path

conn = psycopg2.connect(
    dbname="mydatabase",
    user="myuser",
    password="mysecretpassword",
    host="localhost",
    port=5432
)
cur = conn.cursor()

cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")
cur.execute("""
CREATE TABLE IF NOT EXISTS raw.image_detections (
    id SERIAL PRIMARY KEY,
    message_id TEXT,
    detected_object_class TEXT,
    confidence_score FLOAT
);
""")
conn.commit()

json_path = Path("data/processed/image_detections.json")
if not json_path.exists():
    print(f"No detection file found at {json_path}")
else:
    with open(json_path, "r") as f:
        detections = json.load(f)
        inserted = 0
        for det in detections:
            cur.execute(
                "INSERT INTO raw.image_detections (message_id, detected_object_class, confidence_score) VALUES (%s, %s, %s)",
                (det["message_id"], det["detected_object_class"], det["confidence_score"])
            )
            inserted += 1
    conn.commit()
    print(f"Inserted {inserted} image detections into raw.image_detections.")
cur.close()
conn.close()
print("Database connection closed.")
