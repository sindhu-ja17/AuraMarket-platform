import os
import glob
import sqlite3

# 1. Replace $ with ₹ in templates
template_dir = r'c:\Mini project\templates'
for filepath in glob.glob(os.path.join(template_dir, '*.html')):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple replace
    new_content = content.replace('${{', '₹{{')
    new_content = new_content.replace('Price: $', 'Price: ₹')
    new_content = new_content.replace('Price ($)', 'Price (₹)')
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

# 2. Add more featured listings to DB
db_path = r'c:\Mini project\marketplace.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get some valid category IDs
cursor.execute('SELECT id, name FROM categories')
cats = {row[1]: row[0] for row in cursor.fetchall()}

# Add 4 more products
new_products = [
    ('Sony PlayStation 5 Console', 'Almost new PS5 disc edition with 2 dualsense controllers. Barely used, works perfectly.', 45000.0, cats.get('Electronics', 1), '/static/images/placeholder.jpg', 2, 'active', 0.9, 'Highly Positive'),
    ('Nike Air Jordan 1 Retro High', 'Size 10, classic colorway. Only worn twice, excellent condition with original box.', 15000.0, cats.get('Fashion & Beauty', 4), '/static/images/placeholder.jpg', 3, 'active', 0.8, 'Positive'),
    ('Wooden Dining Table Set', 'Solid oak dining table with 6 matching chairs. Minor scratches on surface.', 25000.0, cats.get('Home & Garden', 6), '/static/images/placeholder.jpg', 4, 'active', 0.4, 'Neutral'),
    ('DJI Mini 3 Pro Drone', 'Ultra lightweight drone with 4k camera. Includes fly more combo (3 batteries, charging hub). Never crashed.', 65000.0, cats.get('Electronics', 1), '/static/images/placeholder.jpg', 2, 'active', 0.85, 'Highly Positive')
]

cursor.executemany('''
    INSERT INTO products (title, description, price, category_id, image_url, seller_id, status, sentiment_score, sentiment_label)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', new_products)

# Also update the prices of old products to reflect Rupees (since $850 is roughly ₹70,000)
cursor.execute('UPDATE products SET price = price * 83 WHERE price < 15000')

conn.commit()
conn.close()
print('Done!')
