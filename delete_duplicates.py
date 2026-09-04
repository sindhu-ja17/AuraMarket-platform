import sqlite3

conn = sqlite3.connect('marketplace.db')
c = conn.cursor()

# Delete products that share an image_url with a product that has a lower ID
c.execute('''
    DELETE FROM products 
    WHERE id NOT IN (
        SELECT MIN(id) 
        FROM products 
        GROUP BY image_url
    )
''')

deleted_count = c.rowcount
print(f"Deleted {deleted_count} duplicate products with repeating images.")

conn.commit()
conn.close()
