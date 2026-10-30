import os
import sqlite3
import hashlib
import random
import time
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
import database as db
from ai_engine import SentimentAnalyzer, ContentModerator, ProductRecommender, get_collaborative_recommendations, get_view_based_recommendations, SmartChatbot

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
app.secret_key = os.environ.get('SECRET_KEY', 'auramarket_super_secret_key_change_me')

# Ensure the database is initialized
db.init_db()

# Initialize AI Modules
sentiment_analyzer = SentimentAnalyzer()
moderator = ContentModerator()
recommender = ProductRecommender()
chatbot = SmartChatbot()

def get_category_avg_price(category_id):
    """Calculate the average price of active products in a given category."""
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(price) FROM products WHERE category_id = ? AND status = 'active'", (category_id,))
    val = cursor.fetchone()[0]
    conn.close()
    return val or 0.0

@app.before_request
def make_session_permanent():
    session.permanent = True

# Context processor to make categories available in all templates
@app.context_processor
def inject_categories():
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories")
    categories = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return dict(categories=categories)

# ==========================================
# HOMEPAGE & SEARCH
# ==========================================
@app.route('/')
def index():
    query = request.args.get('q', '').strip()
    category_id = request.args.get('category', '').strip()
    
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    # 1. Fetch active listings to populate the recommendation engine
    cursor.execute('''
        SELECT p.*, c.name as category_name, u.username as seller_username
        FROM products p
        JOIN categories c ON p.category_id = c.id
        JOIN users u ON p.seller_id = u.id
        WHERE p.status = 'active'
    ''')
    all_products = [dict(row) for row in cursor.fetchall()]
    
    # Fit the TF-IDF recommendation engine with current active products
    recommender.fit(all_products)
    
    # 2. Main query logic
    products = all_products
    
    if category_id:
        products = [p for p in products if str(p['category_id']) == str(category_id)]
        
    if query:
        # Custom AI relevance ranking via TF-IDF scoring
        ranked_results = recommender.rank_search_results(query)
        if ranked_results:
            ranked_ids = {pid: score for pid, score in ranked_results}
            # Filter matches and assign scores
            matched_products = []
            for p in products:
                if p['id'] in ranked_ids:
                    p = dict(p)  # copy to avoid mutating cache
                    p['relevance_score'] = round(ranked_ids[p['id']], 2)
                    matched_products.append(p)
            # Sort by similarity score descending
            products = sorted(matched_products, key=lambda x: x['relevance_score'], reverse=True)
        else:
            # Fallback to simple SQL LIKE substring match
            cursor.execute('''
                SELECT p.*, c.name as category_name
                FROM products p
                JOIN categories c ON p.category_id = c.id
                WHERE p.status = 'active' AND (p.title LIKE ? OR p.description LIKE ?)
            ''', (f'%{query}%', f'%{query}%'))
            products = [dict(row) for row in cursor.fetchall()]

    # 3. Dynamic AI Recommended for You (Strictly prioritized by highest view counts)
    cursor.execute('''
        SELECT p.*, c.name as category_name
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.status = 'active'
        ORDER BY p.views DESC, p.id DESC
        LIMIT 4
    ''')
    recommendations = [dict(row) for row in cursor.fetchall()]
    most_viewed_product = recommendations[0] if recommendations else None

    # Fetch selected category name for UI header
    selected_category_name = None
    if category_id:
        cursor.execute("SELECT name FROM categories WHERE id = ?", (category_id,))
        row = cursor.fetchone()
        if row:
            selected_category_name = row['name']

    # Fetch wishlist
    wishlist_ids = []
    user_id = session.get('user_id')
    if user_id:
        cursor.execute("SELECT product_id FROM wishlist WHERE user_id = ?", (user_id,))
        wishlist_ids = [row['product_id'] for row in cursor.fetchall()]

    conn.close()
    return render_template('index.html', products=products, recommendations=recommendations, query=query, selected_category=category_id, selected_category_name=selected_category_name, wishlist_ids=wishlist_ids, most_viewed_product=most_viewed_product)

# ==========================================
# AUTHENTICATION ROUTES
# ==========================================
@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password']
        
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        pwd_hash = hashlib.sha256(password.encode()).hexdigest()
        if user and user['password_hash'] == pwd_hash:
            # Generate OTP for 2FA
            otp = str(random.randint(100000, 999999))
            expiry = str(int(time.time()) + 300) # 5 minutes
            
            cursor.execute("UPDATE users SET otp_code = ?, otp_expiry = ? WHERE id = ?", (otp, expiry, user['id']))
            conn.commit()
            conn.close()
            
            # Store temporary identifier in session to verify OTP
            session['pending_user_id'] = user['id']
            
            # SIMULATED EMAIL SEND
            flash(f'[SIMULATED EMAIL] Your Login OTP is: {otp}', 'info')
            print(f'\n\n=== EMAIL SIMULATOR ===\nTo: {user["email"]}\nSubject: Login OTP\nCode: {otp}\n=======================\n\n', flush=True)
            
            return redirect(url_for('verify_otp'))
        else:
            conn.close()
            flash('Invalid email or password.', 'error')
            
    return render_template('auth.html', mode='login')

@app.route('/auth/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    pending_user_id = session.get('pending_user_id')
    if not pending_user_id:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        otp_input = request.form['otp'].strip()
        
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (pending_user_id,))
        user = cursor.fetchone()
        
        if user and user['otp_code'] == otp_input:
            if int(user['otp_expiry'] or 0) > int(time.time()):
                # Success
                cursor.execute("UPDATE users SET otp_code = NULL, otp_expiry = NULL WHERE id = ?", (pending_user_id,))
                conn.commit()
                conn.close()
                
                session.pop('pending_user_id', None)
                session['user_id'] = user['id']
                session['username'] = user['username']
                flash('Logged in successfully!', 'success')
                return redirect(url_for('index'))
            else:
                conn.close()
                flash('OTP has expired. Please login again.', 'error')
                return redirect(url_for('login'))
        else:
            conn.close()
            flash('Invalid OTP.', 'error')
            
    return render_template('auth.html', mode='verify_otp')

@app.route('/auth/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email'].strip()
        
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if user:
            otp = str(random.randint(100000, 999999))
            expiry = str(int(time.time()) + 600) # 10 minutes
            cursor.execute("UPDATE users SET otp_code = ?, otp_expiry = ? WHERE id = ?", (otp, expiry, user['id']))
            conn.commit()
            
            session['reset_email'] = email
            flash(f'[SIMULATED EMAIL] Your Password Reset OTP is: {otp}', 'info')
            print(f'\n\n=== EMAIL SIMULATOR ===\nTo: {user["email"]}\nSubject: Password Reset OTP\nCode: {otp}\n=======================\n\n', flush=True)
            conn.close()
            return redirect(url_for('reset_password'))
        else:
            conn.close()
            flash('If the email exists, an OTP has been sent.', 'info')
            
    return render_template('auth.html', mode='forgot_password')

@app.route('/auth/reset_password', methods=['GET', 'POST'])
def reset_password():
    email = session.get('reset_email')
    if not email:
        return redirect(url_for('forgot_password'))
        
    if request.method == 'POST':
        otp_input = request.form['otp'].strip()
        new_password = request.form['password']
        
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if user and user['otp_code'] == otp_input:
            if int(user['otp_expiry'] or 0) > int(time.time()):
                pwd_hash = hashlib.sha256(new_password.encode()).hexdigest()
                cursor.execute("UPDATE users SET password_hash = ?, otp_code = NULL, otp_expiry = NULL WHERE id = ?", (pwd_hash, user['id']))
                conn.commit()
                conn.close()
                
                session.pop('reset_email', None)
                flash('Password reset successfully. You can now login.', 'success')
                return redirect(url_for('login'))
            else:
                conn.close()
                flash('OTP has expired.', 'error')
        else:
            conn.close()
            flash('Invalid OTP.', 'error')
            
    return render_template('auth.html', mode='reset_password')

@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        
        pwd_hash = hashlib.sha256(password.encode()).hexdigest()
        
        conn = db.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, pwd_hash)
            )
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or Email already exists.', 'error')
        finally:
            conn.close()
            
    return render_template('auth.html', mode='register')

@app.route('/auth/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

# ==========================================
# PRODUCT MANIPULATION
# ==========================================
@app.route('/product/<int:product_id>')
def product_details(product_id):
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    # Increment views count
    cursor.execute("UPDATE products SET views = views + 1 WHERE id = ?", (product_id,))
    conn.commit()
    
    # Track views in session (immediate feedback for current browsing session)
    if 'view_counts' not in session:
        session['view_counts'] = {}
    session['view_counts'][str(product_id)] = session['view_counts'].get(str(product_id), 0) + 1
    session['last_viewed_id'] = product_id
    session.modified = True

    # Log 'view' interaction if logged in
    user_id = session.get('user_id')
    if user_id:
        cursor.execute("INSERT INTO interactions (user_id, product_id, type) VALUES (?, ?, 'view')", (user_id, product_id))
        conn.commit()

    # Get product details
    cursor.execute('''
        SELECT p.*, c.name as category_name
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.id = ?
    ''', (product_id,))
    product = cursor.fetchone()
    
    if not product:
        flash('Product not found.', 'error')
        conn.close()
        return redirect(url_for('index'))
        
    product = dict(product)
    
    # Get additional images
    cursor.execute("SELECT image_url FROM product_images WHERE product_id = ?", (product_id,))
    additional_images = [row['image_url'] for row in cursor.fetchall()]
    
    # Get seller information
    cursor.execute("SELECT id, username, rating, created_at, phone_number, address FROM users WHERE id = ?", (product['seller_id'],))
    seller = dict(cursor.fetchone())
    
    # Get product reviews
    cursor.execute('''
        SELECT r.*, u.username as reviewer_name
        FROM reviews r
        JOIN users u ON r.reviewer_id = u.id
        WHERE r.product_id = ?
        ORDER BY r.created_at DESC
    ''', (product_id,))
    reviews = [dict(row) for row in cursor.fetchall()]

    # Fetch all active listings to fit Content Recommendation similarity index
    cursor.execute('''
        SELECT p.*, c.name as category_name
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.status = 'active'
    ''')
    all_products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Generate similar products based on TF-IDF
    similar_products = []
    if product['status'] == 'active':
        recommender.fit(all_products)
        similar_ids = [pid for pid, score in recommender.get_similar_items(product_id, top_n=10)]
        similar_products = [p for p in all_products if p['id'] in similar_ids]

    return render_template('product.html', product=product, seller=seller, reviews=reviews, similar_products=similar_products, additional_images=additional_images)

@app.route('/product/add', methods=['GET', 'POST'])
def add_product():
    if not session.get('user_id'):
        flash('Please login to create a listing.', 'error')
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        title = request.form['title'].strip()
        description = request.form['description'].strip()
        price = float(request.form['price'])
        category_id = int(request.form['category_id'])
        uploaded_files = request.files.getlist('image_file')
        image_urls = []
        for file in uploaded_files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                filepath = os.path.join(app.root_path, 'static', 'uploads', unique_filename)
                try:
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    file.save(filepath)
                    image_urls.append(f'/static/uploads/{unique_filename}')
                except OSError:
                    # In read-only serverless environment (e.g. Vercel)
                    image_urls.append('/static/images/placeholder.jpg')
                
        main_image_url = image_urls[0] if image_urls else '/static/images/placeholder.jpg'
        seller_id = session['user_id']
        
        # Calculate sentiment scoring of description
        score, label = sentiment_analyzer.analyze(description)
        
        # Retrieve average category price for pricing anomaly validation
        avg_price = get_category_avg_price(category_id)
        
        # AI Moderation Check (Server-Side)
        is_flagged, reasons = moderator.moderate_listing(title, description, price, avg_price)
        status = 'flagged' if is_flagged else 'active'
        
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products (title, description, price, category_id, image_url, seller_id, status, sentiment_score, sentiment_label)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, price, category_id, main_image_url, seller_id, status, score, label))
        
        product_id = cursor.lastrowid
        
        # Insert additional images
        if len(image_urls) > 1:
            for url in image_urls[1:]:
                if url.strip():
                    cursor.execute("INSERT INTO product_images (product_id, image_url) VALUES (?, ?)", (product_id, url.strip()))
        
        conn.commit()
        conn.close()
        
        if is_flagged:
            flash('Warning: Your listing was flagged by AI Shield for moderation. It is undergoing admin review.', 'warning')
            return redirect(url_for('dashboard'))
        else:
            flash('Listing published successfully!', 'success')
            return redirect(url_for('index'))
            
    return render_template('add_product.html')

@app.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    seller_id = session.get('user_id')
    if not seller_id:
        flash('Please login to edit listings.', 'error')
        return redirect(url_for('login'))
        
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    # Verify ownership
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    if not product or product['seller_id'] != seller_id:
        flash('You can only edit your own listings.', 'error')
        conn.close()
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        title = request.form['title'].strip()
        description = request.form['description'].strip()
        price = float(request.form['price'])
        category_id = int(request.form['category_id'])
        
        # Calculate new sentiment
        score, label = sentiment_analyzer.analyze(description)
        avg_price = get_category_avg_price(category_id)
        is_flagged, reasons = moderator.moderate_listing(title, description, price, avg_price)
        status = 'flagged' if is_flagged else 'active'
        
        # Handle new image upload if exists
        uploaded_files = request.files.getlist('image_file')
        new_image_url = product['image_url']
        for file in uploaded_files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                unique_filename = f"{int(time.time())}_{filename}"
                filepath = os.path.join(app.root_path, 'static', 'uploads', unique_filename)
                try:
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    file.save(filepath)
                    new_image_url = f'/static/uploads/{unique_filename}'
                except OSError:
                    pass
                break # Only update main image in this view
                
        cursor.execute('''
            UPDATE products 
            SET title = ?, description = ?, price = ?, category_id = ?, image_url = ?, status = ?, sentiment_score = ?, sentiment_label = ?
            WHERE id = ?
        ''', (title, description, price, category_id, new_image_url, status, score, label, product_id))
        
        conn.commit()
        conn.close()
        
        if is_flagged:
            flash('Listing updated, but flagged by AI Shield for moderation.', 'warning')
        else:
            flash('Listing updated successfully!', 'success')
            
        return redirect(url_for('product_details', product_id=product_id))
        
    conn.close()
    return render_template('edit_product.html', product=dict(product))

@app.route('/product/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    seller_id = session.get('user_id')
    if not seller_id:
        flash('Please login to delete listings.', 'error')
        return redirect(url_for('login'))
        
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    # Verify ownership
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    if not product or product['seller_id'] != seller_id:
        flash('You can only delete your own listings.', 'error')
        conn.close()
        return redirect(url_for('index'))
        
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    cursor.execute("DELETE FROM product_images WHERE product_id = ?", (product_id,))
    # We leave reviews/interactions for integrity or they could be deleted too
    conn.commit()
    conn.close()
    
    flash('Listing permanently deleted.', 'success')
    return redirect(url_for('my_listings'))

@app.route('/product/<int:product_id>/checkout')
def checkout(product_id):
    buyer_id = session.get('user_id')
    if not buyer_id:
        flash('Please login to checkout items.', 'error')
        return redirect(url_for('login'))
        
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    # Get product details
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    if not product or product['status'] != 'active':
        flash('Listing is no longer active.', 'error')
        conn.close()
        return redirect(url_for('index'))
        
    product = dict(product)
    
    # Get seller information
    cursor.execute("SELECT id, username FROM users WHERE id = ?", (product['seller_id'],))
    seller = dict(cursor.fetchone())
    
    conn.close()
    return render_template('checkout.html', product=product, seller=seller)

@app.route('/product/<int:product_id>/buy', methods=['POST'])
def buy_product(product_id):
    buyer_id = session.get('user_id')
    if not buyer_id:
        flash('Please login to buy items.', 'error')
        return redirect(url_for('login'))
        
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    # Get product details
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    prod = cursor.fetchone()
    if not prod or prod['status'] != 'active':
        flash('Listing is no longer active.', 'error')
        conn.close()
        return redirect(url_for('index'))
        
    # Get buyer info
    cursor.execute("SELECT wallet_balance FROM users WHERE id = ?", (buyer_id,))
    buyer_wallet = cursor.fetchone()['wallet_balance']
    
    if buyer_wallet < prod['price']:
        flash('Insufficient wallet balance to secure escrow transaction.', 'error')
        conn.close()
        return redirect(url_for('product_details', product_id=product_id))
        
    # Process simulated transactions
    new_balance = buyer_wallet - prod['price']
    cursor.execute("UPDATE users SET wallet_balance = ? WHERE id = ?", (new_balance, buyer_id))
    cursor.execute("UPDATE products SET status = 'sold' WHERE id = ?", (product_id,))
    
    # Store simulated secure escrow transaction
    cursor.execute('''
        INSERT INTO transactions (product_id, buyer_id, seller_id, amount, status)
        VALUES (?, ?, ?, ?, 'escrowed')
    ''', (product_id, buyer_id, prod['seller_id'], prod['price']))
    
    # Log 'buy' interaction
    cursor.execute("INSERT INTO interactions (user_id, product_id, type) VALUES (?, ?, 'buy')", (buyer_id, product_id))
    conn.commit()
    conn.close()
    
    flash('Checkout initiated! Product price has been held securely in Aura Escrow Protection.', 'success')
    return redirect(url_for('product_details', product_id=product_id))

@app.route('/product/<int:product_id>/review', methods=['POST'])
def add_review(product_id):
    reviewer_id = session.get('user_id')
    if not reviewer_id:
        flash('Please login to leave reviews.', 'error')
        return redirect(url_for('login'))
        
    rating = int(request.form['rating'])
    comment = request.form['comment'].strip()
    
    # Run NLP Sentiment Analysis on review comments!
    score, label = sentiment_analyzer.analyze(comment)
    
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    # Get product seller
    cursor.execute("SELECT seller_id FROM products WHERE id = ?", (product_id,))
    prod = cursor.fetchone()
    if not prod:
        flash('Listing not found.', 'error')
        conn.close()
        return redirect(url_for('index'))
        
    seller_id = prod['seller_id']
    
    # Write review
    cursor.execute('''
        INSERT INTO reviews (product_id, reviewer_id, rating, comment, sentiment_score, sentiment_label)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (product_id, reviewer_id, rating, comment, score, label))
    conn.commit()
    
    # Update seller average rating
    cursor.execute('''
        SELECT AVG(rating) FROM reviews r
        JOIN products p ON r.product_id = p.id
        WHERE p.seller_id = ?
    ''', (seller_id,))
    avg_rating = cursor.fetchone()[0] or 5.0
    cursor.execute("UPDATE users SET rating = ? WHERE id = ?", (round(avg_rating, 1), seller_id))
    conn.commit()
    conn.close()
    
    flash(f'Review posted! Sentiment Analyzer parsed rating tone: {label} ({score})', 'success')
    return redirect(url_for('product_details', product_id=product_id))

# ==========================================
# MESSAGING / NEGOTIATIONS
# ==========================================
@app.route('/chat')
@app.route('/chat/<int:conversation_id>')
def chat(conversation_id=None):
    user_id = session.get('user_id')
    if not user_id:
        flash('Please login to access messages.', 'error')
        return redirect(url_for('login'))
        
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    # Get list of all conversations for this user
    cursor.execute('''
        SELECT c.*, p.title as product_title, 
               u_buyer.username as buyer_name, u_seller.username as seller_name
        FROM conversations c
        JOIN products p ON c.product_id = p.id
        JOIN users u_buyer ON c.buyer_id = u_buyer.id
        JOIN users u_seller ON c.seller_id = u_seller.id
        WHERE c.buyer_id = ? OR c.seller_id = ?
        ORDER BY c.created_at DESC
    ''', (user_id, user_id))
    conversations = [dict(row) for row in cursor.fetchall()]
    
    active_conversation = None
    messages = []
    
    if conversation_id:
        # Verify user is part of the active conversation
        cursor.execute("SELECT * FROM conversations WHERE id = ?", (conversation_id,))
        conv_row = cursor.fetchone()
        if conv_row and (conv_row['buyer_id'] == user_id or conv_row['seller_id'] == user_id):
            # Fetch active details
            cursor.execute('''
                SELECT c.*, p.title as product_title, 
                       u_buyer.username as buyer_name, u_seller.username as seller_name
                FROM conversations c
                JOIN products p ON c.product_id = p.id
                JOIN users u_buyer ON c.buyer_id = u_buyer.id
                JOIN users u_seller ON c.seller_id = u_seller.id
                WHERE c.id = ?
            ''', (conversation_id,))
            active_conversation = dict(cursor.fetchone())
            
            # Fetch historic chat messages
            cursor.execute("SELECT * FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC", (conversation_id,))
            messages = [dict(row) for row in cursor.fetchall()]
        else:
            flash('Unauthorized conversation access.', 'error')
            conn.close()
            return redirect(url_for('chat'))

    conn.close()
    return render_template('chat.html', conversations=conversations, active_conversation=active_conversation, messages=messages)

@app.route('/chat/start/<int:product_id>')
def start_chat(product_id):
    buyer_id = session.get('user_id')
    if not buyer_id:
        flash('Please login to message sellers.', 'error')
        return redirect(url_for('login'))
        
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    # Get listing owner details
    cursor.execute("SELECT seller_id, title FROM products WHERE id = ?", (product_id,))
    prod = cursor.fetchone()
    if not prod:
        flash('Listing not found.', 'error')
        conn.close()
        return redirect(url_for('index'))
        
    seller_id = prod['seller_id']
    if buyer_id == seller_id:
        flash('You cannot start a negotiation chat with yourself.', 'error')
        conn.close()
        return redirect(url_for('product_details', product_id=product_id))
        
    # Check if conversation already exists
    cursor.execute(
        "SELECT id FROM conversations WHERE buyer_id = ? AND seller_id = ? AND product_id = ?",
        (buyer_id, seller_id, product_id)
    )
    conv_exists = cursor.fetchone()
    
    if conv_exists:
        conv_id = conv_exists['id']
    else:
        # Create a new conversation thread
        cursor.execute(
            "INSERT INTO conversations (buyer_id, seller_id, product_id) VALUES (?, ?, ?)",
            (buyer_id, seller_id, product_id)
        )
        conn.commit()
        conv_id = cursor.lastrowid
        
    conn.close()
    return redirect(url_for('chat', conversation_id=conv_id))

@app.route('/chat/<int:conversation_id>/send', methods=['POST'])
def send_message(conversation_id):
    sender_id = session.get('user_id')
    if not sender_id:
        flash('Please login to send messages.', 'error')
        return redirect(url_for('login'))
        
    text = request.form['message_text'].strip()
    if not text:
        return redirect(url_for('chat', conversation_id=conversation_id))
        
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    # Verify sender belongs to conversation
    cursor.execute("SELECT * FROM conversations WHERE id = ?", (conversation_id,))
    conv = cursor.fetchone()
    if not conv or (conv['buyer_id'] != sender_id and conv['seller_id'] != sender_id):
        flash('Unauthorized message posting.', 'error')
        conn.close()
        return redirect(url_for('chat'))
        
    # Insert user's message
    cursor.execute(
        "INSERT INTO messages (conversation_id, sender_id, text) VALUES (?, ?, ?)",
        (conversation_id, sender_id, text)
    )
    conn.commit() # Release the write lock so other threads can use the DB while we wait for AI
    
    # Insert simulated auto-reply from the other person
    receiver_id = conv['seller_id'] if sender_id == conv['buyer_id'] else conv['buyer_id']
    is_seller_replying = (receiver_id == conv['seller_id'])
    
    # Get the product to inform the chatbot
    cursor.execute('''
        SELECT p.*, c.name as category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.id = ?
    ''', (conv['product_id'],))
    prod = cursor.fetchone()
    
    # Get the chat history
    cursor.execute("SELECT * FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC", (conversation_id,))
    history = [dict(row) for row in cursor.fetchall()]

    # Generate reply using the SmartChatbot
    reply_text = chatbot.generate_reply(
        message=text, 
        is_seller_replying=is_seller_replying, 
        product_price=prod['price'] if prod else None,
        product_info=dict(prod) if prod else None,
        history=history,
        seller_id=conv['seller_id']
    )
    
    cursor.execute(
        "INSERT INTO messages (conversation_id, sender_id, text) VALUES (?, ?, ?)",
        (conversation_id, receiver_id, reply_text)
    )
    
    conn.commit()
    conn.close()
    return redirect(url_for('chat', conversation_id=conversation_id))

@app.route('/my_listings')
def my_listings():
    seller_id = session.get('user_id')
    if not seller_id:
        flash('Please login to view your listings.', 'error')
        return redirect(url_for('login'))
        
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.*, c.name as category_name
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.seller_id = ?
        ORDER BY p.created_at DESC
    ''', (seller_id,))
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return render_template('my_listings.html', products=products)

# ==========================================
# ADMIN & SELLER METRICS DASHBOARD
# ==========================================
@app.route('/dashboard')
def dashboard():
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    # Aggregate Stats
    cursor.execute("SELECT COUNT(*) FROM products WHERE status = 'active'")
    active_listings = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(views) FROM products")
    total_views = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE status = 'escrowed'")
    escrow_volume = cursor.fetchone()[0] or 0.0
    
    cursor.execute("SELECT COUNT(*) FROM products WHERE status = 'flagged'")
    flagged_listings_count = cursor.fetchone()[0]
    
    stats = {
        'active_listings': active_listings,
        'total_views': total_views,
        'escrow_volume': escrow_volume,
        'flagged_listings_count': flagged_listings_count
    }
    
    # Admin queue - get flagged listings
    cursor.execute('''
        SELECT p.*, u.username as seller_username
        FROM products p
        JOIN users u ON p.seller_id = u.id
        WHERE p.status = 'flagged'
        ORDER BY p.created_at DESC
    ''')
    flagged_listings = [dict(row) for row in cursor.fetchall()]
    
    # Transaction logs
    cursor.execute('''
        SELECT t.*, p.title as product_title, u_buyer.username as buyer_name, u_seller.username as seller_name
        FROM transactions t
        JOIN products p ON t.product_id = p.id
        JOIN users u_buyer ON t.buyer_id = u_buyer.id
        JOIN users u_seller ON t.seller_id = u_seller.id
        ORDER BY t.created_at DESC
    ''')
    transactions = [dict(row) for row in cursor.fetchall()]
    
    # Chart 1 Data: Top 5 products by views
    cursor.execute("SELECT title, views FROM products WHERE status='active' ORDER BY views DESC LIMIT 5")
    chart_products = cursor.fetchall()
    chart_titles = [row['title'][:15] + '...' if len(row['title']) > 15 else row['title'] for row in chart_products]
    chart_views = [row['views'] for row in chart_products]
    
    # Chart 2 Data: Category breakdown count
    cursor.execute('''
        SELECT c.name, COUNT(p.id) as item_count
        FROM categories c
        LEFT JOIN products p ON c.id = p.category_id AND p.status = 'active'
        GROUP BY c.id
    ''')
    cat_counts = cursor.fetchall()
    chart_categories = [row['name'] for row in cat_counts]
    chart_category_counts = [row['item_count'] for row in cat_counts]
    
    chart_data = {
        'titles': chart_titles,
        'views': chart_views,
        'categories': chart_categories,
        'category_counts': chart_category_counts
    }
    
    conn.close()
    return render_template('dashboard.html', stats=stats, flagged_listings=flagged_listings, transactions=transactions, chart_data=chart_data)

@app.route('/admin/listing/<int:product_id>/approve', methods=['POST'])
def admin_approve_listing(product_id):
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET status = 'active' WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    flash('Listing approved and released from quarantine status!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/admin/listing/<int:product_id>/delete', methods=['POST'])
def admin_delete_listing(product_id):
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    flash('Listing rejected and removed from marketplace.', 'success')
    return redirect(url_for('dashboard'))

# ==========================================
# API JSON ENDPOINTS
# ==========================================
@app.route('/api/moderate', methods=['POST'])
def api_moderate():
    data = request.get_json() or {}
    title = data.get('title', '')
    description = data.get('description', '')
    price = float(data.get('price') or 0.0)
    category_id = data.get('category_id')
    
    avg_price = 0.0
    if category_id:
        avg_price = get_category_avg_price(category_id)
        
    is_flagged, reasons = moderator.moderate_listing(title, description, price, avg_price)
    return jsonify({
        'is_flagged': is_flagged,
        'reasons': reasons
    })

@app.route('/api/search_suggest')
def api_search_suggest():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify(results=[])
        
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, price FROM products WHERE status = 'active'")
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Fit & Score query terms
    recommender.fit(products)
    results = recommender.rank_search_results(query, top_n=5)
    
    # Fetch details of scored items
    out = []
    prod_map = {p['id']: p for p in products}
    for pid, score in results:
        if pid in prod_map:
            out.append({
                'id': pid,
                'title': prod_map[pid]['title'],
                'score': round(score, 2)
            })
            
    return jsonify(results=out)


# ==========================================
# WISHLIST ROUTES
# ==========================================
@app.route('/api/wishlist/toggle', methods=['POST'])
def toggle_wishlist():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized', 'redirect': url_for('login')}), 401
    
    data = request.get_json()
    product_id = data.get('product_id')
    user_id = session['user_id']
    
    if not product_id:
        return jsonify({'error': 'Product ID required'}), 400
        
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    # Check if already liked
    cursor.execute("SELECT id FROM wishlist WHERE user_id = ? AND product_id = ?", (user_id, product_id))
    existing = cursor.fetchone()
    
    status = ''
    if existing:
        cursor.execute("DELETE FROM wishlist WHERE user_id = ? AND product_id = ?", (user_id, product_id))
        status = 'removed'
    else:
        cursor.execute("INSERT INTO wishlist (user_id, product_id) VALUES (?, ?)", (user_id, product_id))
        status = 'added'
        
    conn.commit()
    conn.close()
    return jsonify({'status': status})

@app.route('/wishlist')
def wishlist():
    if 'user_id' not in session:
        flash('Please login to view your wishlist.', 'info')
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT p.*, c.name as category_name
        FROM products p
        JOIN categories c ON p.category_id = c.id
        JOIN wishlist w ON p.id = w.product_id
        WHERE w.user_id = ? AND p.status = 'active'
        ORDER BY w.created_at DESC
    ''', (user_id,))
    products = [dict(row) for row in cursor.fetchall()]
    
    wishlist_ids = [p['id'] for p in products]
    
    conn.close()
    return render_template('wishlist.html', products=products, wishlist_ids=wishlist_ids)


if __name__ == '__main__':
    # Start on port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
