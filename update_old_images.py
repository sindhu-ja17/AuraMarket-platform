import sqlite3
db_path = r'c:\Mini project\marketplace.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

updates = [
    ('https://images.unsplash.com/photo-1593640408182-31c70c8268f5?auto=format&fit=crop&w=800&q=80', 'Gaming Laptop Pro'),
    ('https://images.unsplash.com/photo-1532298229144-0ec0c57515c7?auto=format&fit=crop&w=800&q=80', 'Mountain Bike'),
    ('https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=800&q=80', 'Vintage Leather Jacket'),
    ('https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80', 'Sony Noise Cancelling Headphones'),
    ('https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?auto=format&fit=crop&w=800&q=80', 'Modern Sofa Couch')
]

cursor.executemany('UPDATE products SET image_url = ? WHERE title = ?', updates)
conn.commit()
conn.close()
print('Images for old dummy products updated successfully!')
