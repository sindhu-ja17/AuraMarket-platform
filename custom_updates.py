import sqlite3

db_path = r'c:\Mini project\marketplace.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Update prices (and ensure images) for Electric Scooter, Summer Dress, and Camping Tent
updates = [
    # keyword, new_price
    ('Electric Scooter', 15000.00),
    ('Summer Dress', 1200.00),
    ('Camping Tent', 3500.00)
]

for keyword, price in updates:
    cursor.execute('''
        UPDATE products 
        SET price = ?
        WHERE title LIKE ?
    ''', (price, f'%{keyword}%'))

# 2. Delete all Protein Powder items
cursor.execute('''
    DELETE FROM products 
    WHERE title LIKE '%Protein Powder%'
''')

conn.commit()
conn.close()

print('Custom updates applied: updated prices for Scooter, Dress, and Tent, and removed Protein Powder.')
