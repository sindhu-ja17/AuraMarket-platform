import sqlite3

db_path = r'c:\Mini project\marketplace.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get some valid category IDs
cursor.execute('SELECT id, name FROM categories')
cats = {row[1]: row[0] for row in cursor.fetchall()}

new_products = [
    ('Apple MacBook Pro M3', '14-inch, 16GB RAM, 512GB SSD. Space Black. Like new condition with original packaging.', 145000.0, cats.get('Electronics', 1), 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=80', 2, 'active', 0.95, 'Highly Positive'),
    ('Ergonomic Office Chair', 'Premium mesh chair with lumbar support and adjustable armrests. Great for WFH.', 12500.0, cats.get('Home & Garden', 6), 'https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?auto=format&fit=crop&w=800&q=80', 3, 'active', 0.88, 'Positive'),
    ('Royal Enfield Classic 350', '2021 Model, driven only 12,000 km. Regularly serviced. Gunmetal grey.', 165000.0, cats.get('Vehicles', 2), 'https://images.unsplash.com/photo-1558981403-c5f9899a28bc?auto=format&fit=crop&w=800&q=80', 4, 'active', 0.85, 'Positive'),
    ('Vintage Denim Jacket', 'Original 90s vintage denim jacket. Size M. Excellent faded wash look.', 2500.0, cats.get('Fashion & Beauty', 4), 'https://images.unsplash.com/photo-1576871337622-98d48d1cf531?auto=format&fit=crop&w=800&q=80', 2, 'active', 0.75, 'Positive'),
    ('Professional Badminton Racket', 'Lightweight carbon fiber frame, strung at 26 lbs. Used for a few matches only.', 3200.0, cats.get('Sports & Outdoors', 5), 'https://images.unsplash.com/photo-1622279457486-62dcc4a431d6?auto=format&fit=crop&w=800&q=80', 3, 'active', 0.8, 'Positive'),
    ('Samsung 65" 4K Smart TV', 'Crystal 4K UHD. Beautiful display, 1 year old. Moving out sale.', 42000.0, cats.get('Electronics', 1), 'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?auto=format&fit=crop&w=800&q=80', 4, 'active', 0.82, 'Positive'),
    ('Mountain Bike Trek', '21 speed, 29 inch wheels, disc brakes. Great for trails and city commutes.', 18000.0, cats.get('Sports & Outdoors', 5), 'https://images.unsplash.com/photo-1532298229144-0ec0c57515c7?auto=format&fit=crop&w=800&q=80', 2, 'active', 0.8, 'Positive'),
    ('Floral Summer Dress', 'Brand new with tags. Size S. Beautiful breathable fabric perfect for summer.', 1500.0, cats.get('Fashion & Beauty', 4), 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?auto=format&fit=crop&w=800&q=80', 3, 'active', 0.9, 'Highly Positive'),
    ('Modern L-Shape Sofa', 'Grey premium fabric corner sofa. Extremely comfortable, fits 5 people easily.', 28000.0, cats.get('Home & Garden', 6), 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=800&q=80', 4, 'active', 0.85, 'Positive'),
    ('Canon Mirrorless Camera', 'Body + 24-105mm lens. Perfect for photography and vlogging. Great condition.', 85000.0, cats.get('Electronics', 1), 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=800&q=80', 2, 'active', 0.92, 'Highly Positive')
]

cursor.executemany('''
    INSERT INTO products (title, description, price, category_id, image_url, seller_id, status, sentiment_score, sentiment_label)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', new_products)

conn.commit()
conn.close()
print('10 products added successfully!')
