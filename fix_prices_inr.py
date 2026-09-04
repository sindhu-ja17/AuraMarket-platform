import sqlite3

db_path = 'marketplace.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

sensible_prices = {
    'iPhone 14 Pro Max': 110000.0,
    'Vintage Brown Leather Jacket': 4500.0,
    '2018 Honda Civic': 1200000.0,
    'Canon EOS R5': 180000.0,
    'Professional Mountain Trail Bike': 15000.0,
    'Mid-Century Modern Sofa Couch': 25000.0,
    'Sony PlayStation 5': 45000.0,
    'Nike Air Jordan 1': 15000.0,
    'Wooden Dining Table Set': 30000.0,
    'DJI Mini 3 Pro Drone': 65000.0,
    'Apple MacBook Pro M3': 140000.0,
    'Ergonomic Office Chair': 8500.0,
    'Royal Enfield Classic 350': 180000.0,
    'Vintage Denim Jacket': 2500.0,
    'Professional Badminton Racket': 3500.0,
    
    'Smart Home Hub': 4500.0,
    'Wireless Earbuds': 2500.0,
    'Gaming Monitor': 18000.0,
    'Mechanical Keyboard': 6500.0,
    '4K Drone': 45000.0,
    'Tablet Pro': 35000.0,
    'Bluetooth Speaker': 3500.0,
    'Smartphone X': 65000.0,
    
    'Sedan 2020': 850000.0,
    'Sports Bike': 150000.0,
    'SUV 4x4': 1400000.0,
    'Electric Scooter': 65000.0,
    'Vintage Car': 2500000.0,
    'Hatchback 2018': 450000.0,
    
    '2BHK Apartment': 4500000.0,
    'Luxury Villa': 15000000.0,
    'Studio Apartment': 2500000.0,
    'Beachhouse': 8000000.0,
    'Commercial Space': 6000000.0,
    
    'Designer Handbag': 12000.0,
    'Men Leather Shoes': 3500.0,
    'Winter Coat': 4500.0,
    'Summer Dress': 1500.0,
    'Luxury Watch': 25000.0,
    'Sunglasses': 1500.0,
    
    'Yoga Mat': 800.0,
    'Dumbbell Set': 2500.0,
    'Camping Tent': 3500.0,
    'Tennis Racket': 4500.0,
    'Running Shoes': 3500.0,
    
    'Coffee Table': 5000.0,
    'Indoor Plant': 500.0,
    'Bookshelf': 7500.0,
    'Table Lamp': 1500.0,
    'Persian Rug': 12000.0,
    
    'Ladder': 2500.0,
    'Aluminium Ladder': 3500.0,
    'Mobile phone': 15000.0,
}

cursor.execute('SELECT id, title, price FROM products')
rows = cursor.fetchall()
for row in rows:
    pid = row[0]
    title = row[1]
    price = row[2]
    
    p = None
    for k, v in sensible_prices.items():
        if k.lower() in title.lower():
            p = v
            break
            
    if p:
        cursor.execute('UPDATE products SET price = ? WHERE id = ?', (p, pid))
    else:
        # Revert the x83 multiplier if price is ridiculously high for regular items
        if price > 100000 and not any(w in title for w in ['Car','Apartment','Villa','House','Sedan','SUV','Space','Bike']):
            while price > 50000:
                price = price / 83
            cursor.execute('UPDATE products SET price = ? WHERE id = ?', (round(price), pid))

conn.commit()
conn.close()
print("Prices updated successfully.")
