import sqlite3
db_path = r'c:\Mini project\marketplace.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("UPDATE categories SET icon = 'truck' WHERE name = 'Vehicles'")
cursor.execute("UPDATE categories SET icon = 'shopping-bag' WHERE name = 'Fashion & Beauty'")

conn.commit()
conn.close()
print('Icons updated successfully!')
