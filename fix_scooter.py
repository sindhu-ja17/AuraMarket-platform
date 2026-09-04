import sqlite3

db_path = r'c:\Mini project\marketplace.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Specifically update Lightly Used Electric Scooter - #943 and any Electric Scooter
scooter_image = 'https://images.unsplash.com/photo-1595822524458-132d7b5b5c92?auto=format&fit=crop&w=800&q=80'

cursor.execute('''
    UPDATE products 
    SET image_url = ?
    WHERE title LIKE '%Electric Scooter%'
''', (scooter_image,))

conn.commit()
conn.close()

print('Updated Electric Scooter image!')
