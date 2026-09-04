import sqlite3

conn = sqlite3.connect('marketplace.db')
c = conn.cursor()

image_url = 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=800&q=80'

c.execute("UPDATE products SET image_url = ? WHERE title LIKE ?", (image_url, '%Smartphone X%'))
print('Updated:', c.rowcount)

conn.commit()
conn.close()
