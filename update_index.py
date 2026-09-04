import sys

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

like_btn_html = """
                    <button class="like-btn {% if wishlist_ids is defined and prod.id in wishlist_ids %}liked{% endif %}" onclick="toggleWishlist(event, {{ prod.id }}, this)" aria-label="Like product">
                        <svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>
                    </button>
                    """

# Add to recommendations loop
rec_target = '<img src="{{ prod.image_url or \'/static/images/placeholder.jpg\' }}" alt="{{ prod.title }}" class="product-image" onerror="this.src=\'https://images.unsplash.com/photo-1546054454-aa26e2b734c7?auto=format&fit=crop&w=350&q=80\'">'
content = content.replace(rec_target, rec_target + like_btn_html)

# Add to main products loop
prod_target = '<img src="{{ prod.image_url or \'/static/images/placeholder.jpg\' }}" alt="{{ prod.title }}" class="product-image" onerror="this.src=\'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=350&q=80\'">'
content = content.replace(prod_target, prod_target + like_btn_html)

# Make sure product-card has position relative
content = content.replace('class="product-card"', 'class="product-card" style="position:relative;"')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html with like buttons.")
