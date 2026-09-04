import sqlite3

conn = sqlite3.connect('marketplace.db')
c = conn.cursor()

# Category ID for Fashion & Beauty is 4
category_id = 4
# High quality Unsplash image for running shoes
image_url = 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=80'

c.execute("UPDATE products SET category_id = ?, image_url = ? WHERE title LIKE ?", (category_id, image_url, '%Running Shoes%'))
print('Updated:', c.rowcount)

conn.commit()
conn.close()
