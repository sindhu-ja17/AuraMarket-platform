import sys

with open('templates/product.html', 'r', encoding='utf-8') as f:
    content = f.read()

like_btn_html = """
            <button class="like-btn {% if wishlist_ids is defined and product.id in wishlist_ids %}liked{% endif %}" onclick="toggleWishlist(event, {{ product.id }}, this)" aria-label="Like product">
                <svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>
            </button>
"""

gallery_target = '<div class="product-gallery">'
gallery_replace = '<div class="product-gallery" style="position:relative;">'

img_target = '<img id="main-product-image" src="{{ product.image_url }}" alt="{{ product.title }}" style="width:100%; border-radius:12px; object-fit:cover; aspect-ratio:4/3;" onerror="this.src=\'https://images.unsplash.com/photo-1546054454-aa26e2b734c7?auto=format&fit=crop&w=800&q=80\'">'

content = content.replace(gallery_target, gallery_replace)
content = content.replace(img_target, img_target + like_btn_html)

with open('templates/product.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated product.html with like button.")
