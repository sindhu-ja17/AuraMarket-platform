import sqlite3

conn = sqlite3.connect('marketplace.db')
c = conn.cursor()

image_url = 'https://loremflickr.com/800/600/badminton?lock=101'

c.execute("UPDATE products SET image_url = ? WHERE title LIKE ?", (image_url, '%Badminton%'))
print('Updated:', c.rowcount)

conn.commit()
conn.close()
