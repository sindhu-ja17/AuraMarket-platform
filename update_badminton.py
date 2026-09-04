import sqlite3

conn = sqlite3.connect('marketplace.db')
c = conn.cursor()

image_url = 'https://images.unsplash.com/photo-1622279457486-640ca4a4da07?auto=format&fit=crop&w=800&q=80'

c.execute("UPDATE products SET image_url = ? WHERE title LIKE ?", (image_url, '%Badminton%'))
print('Updated:', c.rowcount)

conn.commit()
conn.close()
