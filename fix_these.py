import sqlite3

db_path = r'c:\Mini project\marketplace.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

image_map = {
    'Electric Scooter': '/static/images/electric_scooter.png',
}

for title, img_url in image_map.items():
    cursor.execute('''
        UPDATE products 
        SET image_url = ?
        WHERE title LIKE ?
    ''', (img_url, f'%{title}%'))

conn.commit()
conn.close()

print('Updated Electric Scooter image!')
