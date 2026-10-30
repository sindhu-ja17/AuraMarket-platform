import os
import shutil
import sqlite3
from ai_engine import SentimentAnalyzer

# 1. Image source and destination mapping
brain_dir = r'C:\Users\acer\.gemini\antigravity-ide\brain\45b62c29-e268-4030-9cea-133a0d03fbe4'
static_dir = r'c:\Mini project\static\images'
os.makedirs(static_dir, exist_ok=True)

image_copies = {
    # 5 Neutral Images
    'hdmi_cable.jpg': 'hdmi_cable_1793028197943.jpg',
    'thermal_flask.jpg': 'thermal_flask_1793028225488.jpg',
    'study_desk.jpg': 'study_desk_1793028248785.jpg',
    'desk_clock.jpg': 'desk_clock_1793028271057.jpg',
    'laptop_backpack.jpg': 'laptop_backpack_1793028296458.jpg',
    # 5 Bad / Negative Images
    'cracked_phone.jpg': 'cracked_phone_1793028320690.jpg',
    'worn_office_chair.jpg': 'worn_office_chair_1793028351831.jpg',
    'rusty_bicycle.jpg': 'rusty_bicycle_1793028380048.jpg',
    'damaged_microwave.jpg': 'damaged_microwave_1793028408671.jpg',
    'damaged_guitar.jpg': 'damaged_guitar_1793028438449.jpg',
}

for dst_name, src_name in image_copies.items():
    src_path = os.path.join(brain_dir, src_name)
    dst_path = os.path.join(static_dir, dst_name)
    shutil.copyfile(src_path, dst_path)
    print(f"Copied {src_name} -> {dst_name}")

# 2. Database insertion without modifying existing products
analyzer = SentimentAnalyzer()
conn = sqlite3.connect('marketplace.db')
cur = conn.cursor()

# 5 Neutral Products (Category IDs: 1=Electronics, 6=Home & Garden, 4=Fashion & Beauty)
neutral_products = [
    {
        'title': 'High-Speed 4K HDMI Cable',
        'description': 'Standard 2-meter braided HDMI 2.1 cable. Supports 4K 60Hz and 8K video output. Gold-plated connectors, black color.',
        'price': 499.0,
        'category_id': 1,
        'image_url': '/static/images/hdmi_cable.jpg',
        'seller_id': 2,
        'review': {
            'reviewer_id': 3,
            'rating': 3,
            'comment': 'Standard product as described. Delivery arrived on time.'
        }
    },
    {
        'title': 'Stainless Steel Thermal Flask',
        'description': 'Double-walled insulated stainless steel bottle. 750ml capacity with leak-proof screw lid. Keeps beverages hot or cold for 12 hours.',
        'price': 799.0,
        'category_id': 6,
        'image_url': '/static/images/thermal_flask.jpg',
        'seller_id': 2,
        'review': {
            'reviewer_id': 3,
            'rating': 3,
            'comment': 'Basic product. Received in standard packaging without delays.'
        }
    },
    {
        'title': 'Solid Wood Minimalist Study Desk',
        'description': 'Rectangular engineered wood work desk. Dimensions 120cm length, 60cm depth, 75cm height. Metal legs with walnut veneer tabletop.',
        'price': 3999.0,
        'category_id': 6,
        'image_url': '/static/images/study_desk.jpg',
        'seller_id': 2,
        'review': {
            'reviewer_id': 3,
            'rating': 3,
            'comment': 'Matches description. Basic specifications are accurate.'
        }
    },
    {
        'title': 'Minimalist Digital Desk Clock',
        'description': 'Compact desktop digital clock with LCD screen displaying time, date, and temperature. Powered by two AAA batteries with silent operation.',
        'price': 649.0,
        'category_id': 1,
        'image_url': '/static/images/desk_clock.jpg',
        'seller_id': 2,
        'review': {
            'reviewer_id': 3,
            'rating': 3,
            'comment': 'Simple purchase. Product matches dimensions given in listing.'
        }
    },
    {
        'title': 'Everyday Laptop Backpack',
        'description': 'Polyester everyday backpack with 20L volume. Dedicated 15.6-inch laptop compartment, dual side water bottle pockets, and adjustable shoulder straps.',
        'price': 1199.0,
        'category_id': 4,
        'image_url': '/static/images/laptop_backpack.jpg',
        'seller_id': 2,
        'review': {
            'reviewer_id': 3,
            'rating': 3,
            'comment': 'Average item. Works as expected for basic daily usage.'
        }
    }
]

# 5 Bad / Critical Products (Category IDs: 1=Electronics, 6=Home & Garden, 5=Hobbies & Sports)
bad_products = [
    {
        'title': 'Used Smartphone (Cracked Screen)',
        'description': 'Old second hand phone with cracked front glass and heavy scratch marks on body. Touch screen has broken sensor and battery has issue.',
        'price': 2499.0,
        'category_id': 1,
        'image_url': '/static/images/cracked_phone.jpg',
        'seller_id': 4,
        'review': {
            'reviewer_id': 3,
            'rating': 1,
            'comment': 'The item is broken and completely useless. Screen touch is unresponsive.'
        }
    },
    {
        'title': 'Worn Leather Office Chair',
        'description': 'Old office chair with worn fabric and peeling faux leather. Hydraulic lift has defect and height adjustment does not lock properly. Dirty wheels.',
        'price': 899.0,
        'category_id': 6,
        'image_url': '/static/images/worn_office_chair.jpg',
        'seller_id': 4,
        'review': {
            'reviewer_id': 3,
            'rating': 1,
            'comment': 'Very bad condition. Fabric is worn and dirty on arrival.'
        }
    },
    {
        'title': 'Vintage Bicycle (Needs Repair)',
        'description': 'Used commuter bicycle with defective chain and poor brakes. Frame has scratch marks and rust patches. Needs urgent repair before riding.',
        'price': 1800.0,
        'category_id': 5,
        'image_url': '/static/images/rusty_bicycle.jpg',
        'seller_id': 4,
        'review': {
            'reviewer_id': 3,
            'rating': 1,
            'comment': 'Poor quality item. Arrived with visible scratch and loose parts.'
        }
    },
    {
        'title': 'Defective Microwave Oven',
        'description': 'Faulty countertop microwave oven with heating problem. Interior light has issue and rotating plate has crack. Sold strictly as-is for repair.',
        'price': 1200.0,
        'category_id': 1,
        'image_url': '/static/images/damaged_microwave.jpg',
        'seller_id': 4,
        'review': {
            'reviewer_id': 3,
            'rating': 1,
            'comment': 'Waste of money. Has major problem with power and defect.'
        }
    },
    {
        'title': 'Damaged Acoustic Guitar',
        'description': 'Second-hand acoustic guitar with crack on wooden soundboard and missing tuning peg. Bridge has problem and body has deep scratch.',
        'price': 1500.0,
        'category_id': 5,
        'image_url': '/static/images/damaged_guitar.jpg',
        'seller_id': 4,
        'review': {
            'reviewer_id': 3,
            'rating': 2,
            'comment': 'Disappointed with purchase. Has defect and soundboard crack makes buzz sound.'
        }
    }
]

print("\n--- Inserting 5 Neutral Products ---")
for p in neutral_products:
    score, label = analyzer.analyze(p['description'])
    cur.execute('''
        INSERT INTO products (title, description, price, category_id, image_url, seller_id, status, sentiment_score, sentiment_label)
        VALUES (?, ?, ?, ?, ?, ?, 'active', ?, ?)
    ''', (p['title'], p['description'], p['price'], p['category_id'], p['image_url'], p['seller_id'], score, label))
    new_pid = cur.lastrowid
    print(f"Added ID {new_pid}: {p['title']} | Score: {score} | Label: {label}")

    # Add review
    rev = p['review']
    r_score, r_label = analyzer.analyze(rev['comment'])
    cur.execute('''
        INSERT INTO reviews (product_id, reviewer_id, rating, comment, sentiment_score, sentiment_label)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (new_pid, rev['reviewer_id'], rev['rating'], rev['comment'], r_score, r_label))
    print(f"  -> Added Review for ID {new_pid} | Rating: {rev['rating']} | Sentiment: {r_label}")

print("\n--- Inserting 5 Bad / Critical Products ---")
for p in bad_products:
    score, label = analyzer.analyze(p['description'])
    cur.execute('''
        INSERT INTO products (title, description, price, category_id, image_url, seller_id, status, sentiment_score, sentiment_label)
        VALUES (?, ?, ?, ?, ?, ?, 'active', ?, ?)
    ''', (p['title'], p['description'], p['price'], p['category_id'], p['image_url'], p['seller_id'], score, label))
    new_pid = cur.lastrowid
    print(f"Added ID {new_pid}: {p['title']} | Score: {score} | Label: {label}")

    # Add review
    rev = p['review']
    r_score, r_label = analyzer.analyze(rev['comment'])
    cur.execute('''
        INSERT INTO reviews (product_id, reviewer_id, rating, comment, sentiment_score, sentiment_label)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (new_pid, rev['reviewer_id'], rev['rating'], rev['comment'], r_score, r_label))
    print(f"  -> Added Review for ID {new_pid} | Rating: {rev['rating']} | Sentiment: {r_label}")

conn.commit()
conn.close()
print("\nSuccessfully added 10 new products (5 Neutral, 5 Bad/Critical) with images and reviews without modifying any previous products!")
