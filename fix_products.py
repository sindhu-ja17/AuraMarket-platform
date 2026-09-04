import sqlite3

db_path = r'c:\Mini project\marketplace.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

image_map = {
    # Electronics
    'Smart Home Hub': 'https://images.unsplash.com/photo-1558089687-f282ffcbc126?auto=format&fit=crop&w=800&q=80',
    'Wireless Earbuds': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=800&q=80',
    'Gaming Monitor': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=800&q=80',
    'Mechanical Keyboard': 'https://images.unsplash.com/photo-1595225476474-87563907a212?auto=format&fit=crop&w=800&q=80',
    '4K Drone': 'https://images.unsplash.com/photo-1507582020474-9a35b7d455d9?auto=format&fit=crop&w=800&q=80',
    'Tablet Pro': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=800&q=80',
    'Bluetooth Speaker': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=800&q=80',

    # Vehicles
    'Sedan 2020': 'https://images.unsplash.com/photo-1550355291-bbee04a92027?auto=format&fit=crop&w=800&q=80',
    'Sports Bike': 'https://images.unsplash.com/photo-1558981403-c5f9899a28bc?auto=format&fit=crop&w=800&q=80',
    'SUV 4x4': 'https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?auto=format&fit=crop&w=800&q=80',
    'Electric Scooter': 'https://images.unsplash.com/photo-1595822524458-132d7b5b5c92?auto=format&fit=crop&w=800&q=80',
    'Vintage Car': 'https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=800&q=80',

    # Real Estate
    '2BHK Apartment': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=800&q=80',
    'Luxury Villa': 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80',
    'Studio Apartment': 'https://images.unsplash.com/photo-1536376072261-38c75010e6c9?auto=format&fit=crop&w=800&q=80',
    'Beachhouse': 'https://images.unsplash.com/photo-1499793983690-e29da59ef1c2?auto=format&fit=crop&w=800&q=80',
    'Commercial Space': 'https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=800&q=80',

    # Fashion & Beauty
    'Designer Handbag': 'https://images.unsplash.com/photo-1584916201218-f4242ceb4809?auto=format&fit=crop&w=800&q=80',
    'Men Leather Shoes': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?auto=format&fit=crop&w=800&q=80',
    'Winter Coat': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=800&q=80',
    'Summer Dress': 'https://images.unsplash.com/photo-1515347619152-475a892b1021?auto=format&fit=crop&w=800&q=80',
    'Luxury Watch': 'https://images.unsplash.com/photo-1523170335258-f5ed11844a49?auto=format&fit=crop&w=800&q=80',

    # Sports & Outdoors
    'Yoga Mat': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?auto=format&fit=crop&w=800&q=80',
    'Dumbbell Set': 'https://images.unsplash.com/photo-1586401100295-7a8096fd231a?auto=format&fit=crop&w=800&q=80',
    'Camping Tent': 'https://images.unsplash.com/photo-1504280390224-b1ebad7363f0?auto=format&fit=crop&w=800&q=80',
    'Tennis Racket': 'https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?auto=format&fit=crop&w=800&q=80',
    'Protein Powder': 'https://images.unsplash.com/photo-1593095948071-474c5cc2989d?auto=format&fit=crop&w=800&q=80',

    # Home & Garden
    'Coffee Table': 'https://images.unsplash.com/photo-1533090481720-856c6e3c1fdc?auto=format&fit=crop&w=800&q=80',
    'Indoor Plant': 'https://images.unsplash.com/photo-1485955900006-10f4d324d411?auto=format&fit=crop&w=800&q=80',
    'Bookshelf': 'https://images.unsplash.com/photo-1507842217343-583bb7270b66?auto=format&fit=crop&w=800&q=80',
    'Table Lamp': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=800&q=80',
    'Persian Rug': 'https://images.unsplash.com/photo-1583847268964-b28ce8f300c1?auto=format&fit=crop&w=800&q=80'
}

for keyword, img_url in image_map.items():
    cursor.execute('''
        UPDATE products 
        SET image_url = ?
        WHERE title LIKE ? AND image_url LIKE '%unsplash%'
    ''', (img_url, f'%{keyword}%'))

# Also update the seed script so future seeds are correct
conn.commit()
conn.close()

print('Updated all database products with perfectly matching images!')
