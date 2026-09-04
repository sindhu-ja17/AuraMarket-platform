import sqlite3

conn = sqlite3.connect('marketplace.db')
c = conn.cursor()

racket_url = 'https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?auto=format&fit=crop&w=800&q=80'
c.execute("UPDATE products SET image_url = ? WHERE title LIKE ?", (racket_url, '%Badminton%'))
print('Updated Badminton:', c.rowcount)

hub_url = 'https://images.unsplash.com/photo-1558089687-f282ffcbc126?auto=format&fit=crop&w=800&q=80'
c.execute("UPDATE products SET image_url = ? WHERE title LIKE ?", (hub_url, '%Smart Home Hub%'))
print('Updated Smart Home Hub:', c.rowcount)

conn.commit()
conn.close()
