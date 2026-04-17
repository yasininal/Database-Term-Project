import mysql.connector

DB_CONFIG = {
    'host': 'localhost', 'user': 'root',
    'password': 'mysql1234', 'database': 'airbnb_clone', 'charset': 'utf8mb4'
}

db = mysql.connector.connect(**DB_CONFIG)
cur = db.cursor()
cur.execute("SELECT table_name, count(column_name) FROM information_schema.columns WHERE table_schema = 'airbnb_clone' GROUP BY table_name")
results = cur.fetchall()
total = 0
print(f"{'Table Name':20} | {'Attributes'}")
print("-" * 35)
for row in results:
    print(f"{row[0]:20} | {row[1]}")
    total += row[1]
print("-" * 35)
print(f"{'TOTAL ATTRIBUTES':20} | {total}")
cur.close(); db.close()
