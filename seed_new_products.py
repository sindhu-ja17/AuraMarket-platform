import sqlite3

db_path = 'marketplace.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# seller_id = 2 is JohnSeller
new_products = [
    # Hobbies & Sports (category_id = 5)
    ('Pro Basketball (Size 7)', 'Official size and weight basketball. Perfect for indoor and outdoor courts. Superior grip and durability.', 1500.0, 5, 'https://images.unsplash.com/photo-1519861531473-9200262188bf?auto=format&fit=crop&w=800&q=80', 2, 'active', 0.8, 'Positive'),
    ('Cricket Bat (English Willow)', 'Premium English Willow cricket bat. Excellent ping and balance. Pre-knocked and ready to play.', 8500.0, 5, 'https://images.unsplash.com/photo-1593341646782-e0b495cff86d?auto=format&fit=crop&w=800&q=80', 2, 'active', 0.9, 'Highly Positive'),
    ('Adjustable Dumbbells Set', 'Set of two adjustable dumbbells up to 25kg each. Space saving and perfect for home workouts.', 4500.0, 5, 'https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?auto=format&fit=crop&w=800&q=80', 2, 'active', 0.7, 'Positive'),
    ('Boxing Gloves (12oz)', 'Premium synthetic leather boxing gloves. Great wrist support and knuckle protection for sparring or bag work.', 2500.0, 5, 'https://images.unsplash.com/photo-1517438322307-e67111335449?auto=format&fit=crop&w=800&q=80', 2, 'active', 0.75, 'Positive'),
    ('Skateboard (Maple Wood)', 'Complete skateboard with 7-ply Canadian maple deck. Smooth ABEC-9 bearings and durable wheels.', 3000.0, 5, 'https://images.unsplash.com/photo-1520045892732-304bc3ac5d8e?auto=format&fit=crop&w=800&q=80', 2, 'active', 0.85, 'Highly Positive'),

    # Fashion & Beauty (category_id = 4)
    ('Gold Plated Necklace', 'Elegant 18k gold plated pendant necklace. Perfect for evening wear and special occasions. Non-tarnish material.', 2500.0, 4, 'https://images.unsplash.com/photo-1599643478524-fb66f70d00f8?auto=format&fit=crop&w=800&q=80', 2, 'active', 0.88, 'Highly Positive'),
    ('Designer Aviator Sunglasses', 'Classic aviator sunglasses with polarized UV400 lenses. Sturdy metal frame, includes protective case.', 1800.0, 4, 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=800&q=80', 2, 'active', 0.7, 'Positive'),
    ('Matte Red Lipstick', 'Long-lasting matte liquid lipstick. Deep red shade suitable for all skin tones. Cruelty-free and smudge-proof.', 800.0, 4, 'https://images.unsplash.com/photo-1586495777744-4413f21062fa?auto=format&fit=crop&w=800&q=80', 2, 'active', 0.65, 'Positive'),
    ("Men's Formal Oxford Shoes", 'Genuine leather formal Oxford shoes in black. Comfortable insole for all-day wear. Classic and sophisticated.', 3500.0, 4, 'https://images.unsplash.com/photo-1614252209844-784860b2184e?auto=format&fit=crop&w=800&q=80', 2, 'active', 0.75, 'Positive'),
    ('Floral Print Maxi Dress', 'Beautiful flowy maxi dress with summer floral prints. Breathable fabric, perfect for casual outings or beach vacations.', 2200.0, 4, 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?auto=format&fit=crop&w=800&q=80', 2, 'active', 0.8, 'Positive'),
]

cursor.executemany('''
    INSERT INTO products (title, description, price, category_id, image_url, seller_id, status, sentiment_score, sentiment_label)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', new_products)

conn.commit()
conn.close()
print("Products added successfully!")
