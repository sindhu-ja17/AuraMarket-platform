import sqlite3
import os
import hashlib
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'marketplace.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        wallet_balance REAL DEFAULT 1000.0,
        rating REAL DEFAULT 5.0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        otp_code TEXT,
        otp_expiry TEXT,
        phone_number TEXT,
        address TEXT
    )
    ''')

    # Create Categories table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        icon TEXT NOT NULL
    )
    ''')

    # Create Products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        price REAL NOT NULL,
        category_id INTEGER NOT NULL,
        image_url TEXT,
        seller_id INTEGER NOT NULL,
        status TEXT DEFAULT 'active', -- active, sold, flagged
        sentiment_score REAL DEFAULT 0.0,
        sentiment_label TEXT DEFAULT 'Neutral',
        views INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES categories (id),
        FOREIGN KEY (seller_id) REFERENCES users (id)
    )
    ''')

    # Create Product Images table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        image_url TEXT NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
    )
    ''')

    # Create Reviews table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        reviewer_id INTEGER NOT NULL,
        rating INTEGER NOT NULL,
        comment TEXT NOT NULL,
        sentiment_score REAL DEFAULT 0.0,
        sentiment_label TEXT DEFAULT 'Neutral',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products (id),
        FOREIGN KEY (reviewer_id) REFERENCES users (id)
    )
    ''')

    # Create Conversations table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        buyer_id INTEGER NOT NULL,
        seller_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (buyer_id) REFERENCES users (id),
        FOREIGN KEY (seller_id) REFERENCES users (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    ''')

    # Create Messages table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id INTEGER NOT NULL,
        sender_id INTEGER NOT NULL,
        text TEXT NOT NULL,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (conversation_id) REFERENCES conversations (id),
        FOREIGN KEY (sender_id) REFERENCES users (id)
    )
    ''')

    # Create Interactions table (for Collaborative Recommendation Engine)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        type TEXT NOT NULL, -- view, like, buy
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    ''')

    # Create Transactions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        buyer_id INTEGER NOT NULL,
        seller_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        status TEXT DEFAULT 'completed', -- completed, pending, refunded
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products (id),
        FOREIGN KEY (buyer_id) REFERENCES users (id),
        FOREIGN KEY (seller_id) REFERENCES users (id)
    )
    ''')

    # Create Wishlist table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS wishlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE,
        UNIQUE(user_id, product_id)
    )
    ''')

    conn.commit()

    # Handle schema updates for existing databases
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN otp_code TEXT")
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN otp_expiry TEXT")
    except sqlite3.OperationalError:
        pass

    conn.commit()

    # Seed Categories if empty
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        categories = [
            ("Electronics", "cpu"),
            ("Vehicles", "car"),
            ("Real Estate", "home"),
            ("Fashion & Beauty", "shirt"),
            ("Hobbies & Sports", "activity"),
            ("Home & Garden", "package"),
            ("Books & Education", "book")
        ]
        cursor.executemany("INSERT INTO categories (name, icon) VALUES (?, ?)", categories)
        conn.commit()

    # Seed Users if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        # Create users: admin, seller1, buyer1, seller2
        # Password hash is sha256 of "password"
        pwd_hash = hashlib.sha256("password".encode()).hexdigest()
        users = [
            ("admin", "admin@marketplace.com", pwd_hash, 10000.0, 5.0),
            ("JohnSeller", "john@seller.com", pwd_hash, 1500.0, 4.8),
            ("AliceBuyer", "alice@buyer.com", pwd_hash, 2500.0, 5.0),
            ("SarahDeals", "sarah@deals.com", pwd_hash, 1800.0, 4.5),
        ]
        cursor.executemany("INSERT INTO users (username, email, password_hash, wallet_balance, rating) VALUES (?, ?, ?, ?, ?)", users)
        conn.commit()

    # Seed Products if empty
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        # Fetch category IDs
        cursor.execute("SELECT id, name FROM categories")
        cats = {row['name']: row['id'] for row in cursor.fetchall()}
        
        # Product details: title, description, price, category_id, image_url, seller_id, status, sentiment_score, sentiment_label
        products = [
            (
                "iPhone 14 Pro Max 256GB - Perfect Condition",
                "Selling my iPhone 14 Pro Max in Deep Purple color. It is in absolutely pristine condition, with 94% battery health. Comes with original box and cable. No scratches or dents. Highly reliable and beautiful smartphone with amazing camera capability.",
                850.0,
                cats["Electronics"],
                "/static/images/iphone.jpg",
                2, # JohnSeller
                "active",
                0.85,
                "Highly Positive"
            ),
            (
                "Vintage Brown Leather Jacket - Medium",
                "Authentic retro leather bomber jacket. Very comfortable, warm, and stylish for winter. Real heavy-duty cowhide leather. Shows minor signs of wear which adds to its classic vintage aesthetic. Fits like a true size M.",
                120.0,
                cats["Fashion & Beauty"],
                "/static/images/leather_jacket.jpg",
                2, # JohnSeller
                "active",
                0.65,
                "Positive"
            ),
            (
                "2018 Honda Civic LX Sedan",
                "Excellent daily driver, very fuel efficient and reliable. Single owner, clean title, and low mileage (45,000 miles). Regularly serviced at authorized dealerships. Perfect mechanical state, interior is neat. Selling due to relocation.",
                14500.0,
                cats["Vehicles"],
                "/static/images/honda_civic.jpg",
                4, # SarahDeals
                "active",
                0.75,
                "Positive"
            ),
            (
                "Canon EOS R5 Mirrorless Camera Body",
                "Professional mirrorless camera body with 45MP sensor and 8K video capability. Used lightly for studio work only. Extremely clean, minor rub mark on the bottom plate. Includes 2 batteries, charger, and strap. Selling to upgrade.",
                2200.0,
                cats["Electronics"],
                "/static/images/canon_r5.jpg",
                4, # SarahDeals
                "active",
                0.40,
                "Positive"
            ),
            (
                "Professional Mountain Trail Bike 29er",
                "Full suspension mountain bike. 29-inch wheels, lightweight aluminum frame, hydraulic disc brakes, and air-suspension fork. Handles technical trails wonderfully. Ready to ride with new tires installed last week. Minor cosmetic scratches on frame.",
                680.0,
                cats["Hobbies & Sports"],
                "/static/images/mountain_bike.jpg",
                2, # JohnSeller
                "active",
                0.55,
                "Positive"
            ),
            (
                "Mid-Century Modern Sofa Couch - Grey",
                "Comfortable 3-seater sofa. Solid wooden legs and durable grey fabric upholstery. Perfect addition to any modern living room. Very clean, smoke-free and pet-free household. A couple of tiny spots but overall in great shape.",
                350.0,
                cats["Home & Garden"],
                "/static/images/sofa.jpg",
                4, # SarahDeals
                "active",
                0.45,
                "Positive"
            )
        ]
        
        cursor.executemany('''
        INSERT INTO products (title, description, price, category_id, image_url, seller_id, status, sentiment_score, sentiment_label)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', products)
        conn.commit()

        # Seed reviews for iPhone 14
        cursor.execute("SELECT id FROM products WHERE title LIKE '%iPhone%'")
        iphone_id = cursor.fetchone()[0]
        
        reviews = [
            (iphone_id, 3, 5, "Outstanding phone! The seller John was very honest about the battery health and condition. Highly recommended!", 0.90, "Highly Positive"),
            (iphone_id, 4, 4, "Item is good. Exactly as described. Delivery was prompt.", 0.60, "Positive"),
        ]
        cursor.executemany('''
        INSERT INTO reviews (product_id, reviewer_id, rating, comment, sentiment_score, sentiment_label)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', reviews)
        conn.commit()

        # Seed user interactions for recommendation modeling
        # AliceBuyer (ID 3) interacts with Electronics:
        # iPhone (ID 1), Canon (ID 4)
        interactions = [
            (3, 1, 'view'),
            (3, 1, 'like'),
            (3, 4, 'view'),
            (2, 3, 'view'), # JohnSeller views Honda Civic
            (3, 5, 'view'), # Alice views Mountain Bike
        ]
        cursor.executemany('''
        INSERT INTO interactions (user_id, product_id, type)
        VALUES (?, ?, ?)
        ''', interactions)
        conn.commit()

    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully at:", DB_PATH)
