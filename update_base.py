import sys

with open('templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Wishlist to nav
nav_target = '<a href="/my_listings" class="nav-link">My Listings</a>'
nav_replace = '<a href="/my_listings" class="nav-link">My Listings</a>\n                    <a href="/wishlist" class="nav-link"><i data-feather="heart" style="width:18px; height:18px; vertical-align:middle;"></i> Wishlist</a>'

content = content.replace(nav_target, nav_replace)

# 2. Add toggleWishlist function
js_target = '{% block scripts %}{% endblock %}'
js_replace = """
    <script>
        async function toggleWishlist(event, productId, btnElement) {
            event.preventDefault();
            event.stopPropagation();
            
            try {
                const response = await fetch('/api/wishlist/toggle', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ product_id: productId })
                });
                
                if (response.status === 401) {
                    const data = await response.json();
                    window.location.href = data.redirect;
                    return;
                }
                
                if (response.ok) {
                    const data = await response.json();
                    if (data.status === 'added') {
                        btnElement.classList.add('liked');
                    } else if (data.status === 'removed') {
                        btnElement.classList.remove('liked');
                        // If we are on the wishlist page, optionally remove the card
                        if (window.location.pathname === '/wishlist') {
                            const card = btnElement.closest('.product-card');
                            if (card) {
                                card.style.transition = 'opacity 0.3s';
                                card.style.opacity = '0';
                                setTimeout(() => card.remove(), 300);
                            }
                        }
                    }
                }
            } catch (err) {
                console.error("Error toggling wishlist:", err);
            }
        }
    </script>
    {% block scripts %}{% endblock %}
"""

content = content.replace(js_target, js_replace)

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated base.html with wishlist nav and JS.")
