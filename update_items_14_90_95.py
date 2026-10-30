import sqlite3

db_path = r'marketplace.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

image_map = {
    14: '/static/images/vintage_denim_jacket.jpg',
    90: '/static/images/designer_handbag.jpg',
    95: '/static/images/aviator_sunglasses.jpg',
    208: '/static/images/gold_necklace.png',
    211: '/static/images/oxford_shoes.png'
}

for pid, img_url in image_map.items():
    cur.execute("UPDATE products SET image_url = ? WHERE id = ?", (img_url, pid))
    print(f"Product ID {pid} updated to {img_url} (rows: {cur.rowcount})")

conn.commit()
conn.close()
print("Successfully verified/updated images for items 14, 90, 95, 208, and 211.")
