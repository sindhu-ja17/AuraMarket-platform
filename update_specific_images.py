import sqlite3

conn = sqlite3.connect('marketplace.db')
cur = conn.cursor()

cur.execute('UPDATE products SET image_url=? WHERE title LIKE ?', ('/static/images/gold_necklace.png', '%Gold Plated Necklace%'))
cur.execute('UPDATE products SET image_url=? WHERE title LIKE ?', ('/static/images/oxford_shoes.png', '%Formal Oxford Shoes%'))

conn.commit()
conn.close()
print("Updated images for Necklace and Shoes.")
