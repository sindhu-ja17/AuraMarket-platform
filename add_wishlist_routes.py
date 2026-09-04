import sys

with open('app.py', 'r') as f:
    content = f.read()

# 1. Update index() route return
old_index_return = """    conn.close()
    return render_template('index.html', products=products, recommendations=recommendations, query=query, selected_category=category_id, selected_category_name=selected_category_name)"""

new_index_return = """    # Fetch wishlist
    wishlist_ids = []
    user_id = session.get('user_id')
    if user_id:
        cursor.execute("SELECT product_id FROM wishlist WHERE user_id = ?", (user_id,))
        wishlist_ids = [row['product_id'] for row in cursor.fetchall()]

    conn.close()
    return render_template('index.html', products=products, recommendations=recommendations, query=query, selected_category=category_id, selected_category_name=selected_category_name, wishlist_ids=wishlist_ids)"""

content = content.replace(old_index_return, new_index_return)

# 2. Update product_details() route return
old_product_return = """    conn.close()
    return render_template('product.html', product=product, additional_images=additional_images, seller=seller, reviews=reviews, recommendation_context=recommendation_context)"""

new_product_return = """    # Fetch wishlist
    wishlist_ids = []
    user_id = session.get('user_id')
    if user_id:
        cursor.execute("SELECT product_id FROM wishlist WHERE user_id = ?", (user_id,))
        wishlist_ids = [row['product_id'] for row in cursor.fetchall()]

    conn.close()
    return render_template('product.html', product=product, additional_images=additional_images, seller=seller, reviews=reviews, recommendation_context=recommendation_context, wishlist_ids=wishlist_ids)"""

content = content.replace(old_product_return, new_product_return)

# 3. Insert Wishlist routes before the main block
wishlist_routes = """
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

"""

if 'def toggle_wishlist' not in content:
    content = content.replace("if __name__ == '__main__':", wishlist_routes + "\nif __name__ == '__main__':")

with open('app.py', 'w') as f:
    f.write(content)

print("Updated app.py with wishlist logic.")
