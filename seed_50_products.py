import sqlite3
import random

db_path = r'c:\Mini project\marketplace.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('SELECT id, name FROM categories')
cats = {row[1]: row[0] for row in cursor.fetchall()}

base_data = {
    'Electronics': {
        'id': cats.get('Electronics', 1),
        'titles': ['Smart Home Hub', 'Wireless Earbuds', 'Gaming Monitor', 'Mechanical Keyboard', '4K Drone', 'Tablet Pro', 'Bluetooth Speaker'],
        'images': [
            'https://images.unsplash.com/photo-1498049794561-7780e7231661?auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1546868871-7041f2a55e12?auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80'
        ]
    },
    'Vehicles': {
        'id': cats.get('Vehicles', 2),
        'titles': ['Sedan 2020', 'Sports Bike', 'SUV 4x4', 'Electric Scooter', 'Vintage Car'],
        'images': [
            'https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=800&q=80'
        ]
    },
    'Real Estate': {
        'id': cats.get('Real Estate', 3),
        'titles': ['2BHK Apartment', 'Luxury Villa', 'Studio Apartment', 'Beachhouse', 'Commercial Space'],
        'images': [
            'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80'
        ]
    },
    'Fashion & Beauty': {
        'id': cats.get('Fashion & Beauty', 4),
        'titles': ['Designer Handbag', 'Men Leather Shoes', 'Winter Coat', 'Summer Dress', 'Luxury Watch'],
        'images': [
            'https://images.unsplash.com/photo-1445205170230-053b83016050?auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=800&q=80'
        ]
    },
    'Sports & Outdoors': {
        'id': cats.get('Sports & Outdoors', 5),
        'titles': ['Yoga Mat', 'Dumbbell Set', 'Camping Tent', 'Tennis Racket', 'Protein Powder'],
        'images': [
            'https://images.unsplash.com/photo-1517649763962-0c623066013b?auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?auto=format&fit=crop&w=800&q=80'
        ]
    },
    'Home & Garden': {
        'id': cats.get('Home & Garden', 6),
        'titles': ['Coffee Table', 'Indoor Plant', 'Bookshelf', 'Table Lamp', 'Persian Rug'],
        'images': [
            'https://images.unsplash.com/photo-1484101403633-562f891dc89a?auto=format&fit=crop&w=800&q=80',
            'https://images.unsplash.com/photo-1583847268964-b28ce8f300c1?auto=format&fit=crop&w=800&q=80'
        ]
    }
}

adjectives = ['Premium', 'Brand New', 'Lightly Used', 'High Quality', 'Beautiful', 'Classic', 'Modern', 'Sleek']
descriptions = [
    'Amazing product, barely used. Looks exactly like the pictures.',
    'Moving out sale! Needs to go ASAP. Great condition.',
    'Bought this a few months ago but rarely use it. Perfect working order.',
    'High quality item with original packaging included.',
    'Selling this because I upgraded. Works perfectly, no scratches.'
]

new_products = []
for i in range(50):
    cat_name = random.choice(list(base_data.keys()))
    cat_info = base_data[cat_name]
    
    title = f"{random.choice(adjectives)} {random.choice(cat_info['titles'])} - #{random.randint(100, 999)}"
    desc = random.choice(descriptions)
    price = random.randint(10, 500) * 100.0
    image = random.choice(cat_info['images'])
    seller_id = random.randint(2, 4)
    score = round(random.uniform(0.6, 0.95), 2)
    
    new_products.append((title, desc, price, cat_info['id'], image, seller_id, 'active', score, 'Positive'))

cursor.executemany('''
    INSERT INTO products (title, description, price, category_id, image_url, seller_id, status, sentiment_score, sentiment_label)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', new_products)

conn.commit()
conn.close()
print('50 products seeded successfully!')
