import sqlite3
import shutil
import os

db_path = r'c:\Mini project\marketplace.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Make sure static/images exists
os.makedirs(r'c:\Mini project\static\images', exist_ok=True)

# Define mappings
images = {
    'Scooter': {
        'src': r'C:\Users\acer\.gemini\antigravity-ide\brain\5fa2c9a3-b8f1-494a-9393-379c1f1c57d7\electric_scooter_img_1782396610467.png',
        'dest': r'c:\Mini project\static\images\electric_scooter.png',
        'url': '/static/images/electric_scooter.png',
        'like': '%Scooter%'
    },
    'Dress': {
        'src': r'C:\Users\acer\.gemini\antigravity-ide\brain\5fa2c9a3-b8f1-494a-9393-379c1f1c57d7\summer_dress_img_1782396623365.png',
        'dest': r'c:\Mini project\static\images\summer_dress.png',
        'url': '/static/images/summer_dress.png',
        'like': '%Dress%'
    },
    'Tent': {
        'src': r'C:\Users\acer\.gemini\antigravity-ide\brain\5fa2c9a3-b8f1-494a-9393-379c1f1c57d7\camping_tent_img_1782396634779.png',
        'dest': r'c:\Mini project\static\images\camping_tent.png',
        'url': '/static/images/camping_tent.png',
        'like': '%Tent%'
    },
    'Rug': {
        'src': r'C:\Users\acer\.gemini\antigravity-ide\brain\5fa2c9a3-b8f1-494a-9393-379c1f1c57d7\persian_rug_img_1782396646129.png',
        'dest': r'c:\Mini project\static\images\persian_rug.png',
        'url': '/static/images/persian_rug.png',
        'like': '%Rug%'
    }
}

for key, data in images.items():
    if os.path.exists(data['src']):
        shutil.copy(data['src'], data['dest'])
        c.execute("UPDATE products SET image_url = ? WHERE title LIKE ?", (data['url'], data['like']))
        print(f"Updated {key}")
    else:
        print(f"Source not found for {key}: {data['src']}")

conn.commit()
conn.close()
print("Images copied and database updated!")
