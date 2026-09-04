import sqlite3
import re
import urllib.parse

db_path = r'c:\Mini project\marketplace.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("SELECT id, title FROM products")
products = c.fetchall()

# Mapping base titles to loremflickr keywords
keyword_map = {
    'Smart Home Hub': 'smarthome,device',
    'Wireless Earbuds': 'earbuds,headphones',
    'Gaming Monitor': 'monitor,gaming',
    'Mechanical Keyboard': 'keyboard,mechanical',
    '4K Drone': 'drone',
    'Tablet Pro': 'tablet,ipad',
    'Bluetooth Speaker': 'speaker,bluetooth',
    
    'Sedan 2020': 'sedan,car',
    'Sports Bike': 'sportbike,motorcycle',
    'SUV 4x4': 'suv,car',
    'Electric Scooter': 'scooter,electric',
    'Vintage Car': 'vintage,car',
    
    '2BHK Apartment': 'apartment,interior',
    'Luxury Villa': 'villa,house',
    'Studio Apartment': 'studio,apartment',
    'Beachhouse': 'beachhouse,house',
    'Commercial Space': 'office,workspace',
    
    'Designer Handbag': 'handbag,purse',
    'Men Leather Shoes': 'leathershoes,mens',
    'Winter Coat': 'wintercoat,jacket',
    'Summer Dress': 'dress,fashion',
    'Luxury Watch': 'watch,rolex',
    'Sunglasses': 'sunglasses',
    
    'Yoga Mat': 'yogamat,fitness',
    'Dumbbell Set': 'dumbbells,gym',
    'Camping Tent': 'tent,camping',
    'Tennis Racket': 'tennisracket',
    'Protein Powder': 'protein,supplement',
    'Running Shoes': 'runningshoes,sneakers',
    
    'Coffee Table': 'coffeetable,furniture',
    'Indoor Plant': 'indoorplant,houseplant',
    'Bookshelf': 'bookshelf,furniture',
    'Table Lamp': 'tablelamp,lighting',
    'Persian Rug': 'persianrug,carpet',
    'Dining Chairs': 'diningchair,furniture',
    'Ladder': 'ladder',
    'Mobile phone': 'mobilephone,smartphone'
}

for pid, title in products:
    # find which base title is in the title
    found_kw = 'product'
    for base, kw in keyword_map.items():
        if base.lower() in title.lower():
            found_kw = kw
            break
    
    # URL encode the keyword
    safe_kw = urllib.parse.quote(found_kw)
    
    # create unique URL for this specific product ID
    # lock={pid} ensures the image is unique for this product but consistent across reloads
    new_url = f"https://loremflickr.com/800/600/{safe_kw}?lock={pid}"
    
    c.execute("UPDATE products SET image_url = ? WHERE id = ?", (new_url, pid))

conn.commit()
conn.close()
print("All products updated with unique and semantic images!")
