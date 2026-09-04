import sqlite3, shutil, os

os.makedirs(r'c:\Mini project\static\images', exist_ok=True)

updates = [
    {
        'src': r'C:\Users\acer\.gemini\antigravity-ide\brain\5fa2c9a3-b8f1-494a-9393-379c1f1c57d7\dining_table_img_1782397791690.png',
        'dst': r'c:\Mini project\static\images\dining_table.png',
        'url': '/static/images/dining_table.png',
        'title_like': '%Dining%'
    },
    {
        'src': r'C:\Users\acer\.gemini\antigravity-ide\brain\5fa2c9a3-b8f1-494a-9393-379c1f1c57d7\dji_drone_img_1782397803993.png',
        'dst': r'c:\Mini project\static\images\dji_drone.png',
        'url': '/static/images/dji_drone.png',
        'title_like': '%DJI%'
    },
    {
        'src': r'C:\Users\acer\.gemini\antigravity-ide\brain\5fa2c9a3-b8f1-494a-9393-379c1f1c57d7\macbook_pro_img_1782397815573.png',
        'dst': r'c:\Mini project\static\images\macbook_pro.png',
        'url': '/static/images/macbook_pro.png',
        'title_like': '%MacBook%'
    },
    {
        'src': r'C:\Users\acer\.gemini\antigravity-ide\brain\5fa2c9a3-b8f1-494a-9393-379c1f1c57d7\office_chair_img_1782397831345.png',
        'dst': r'c:\Mini project\static\images\office_chair.png',
        'url': '/static/images/office_chair.png',
        'title_like': '%Office Chair%'
    },
    {
        'src': r'C:\Users\acer\.gemini\antigravity-ide\brain\5fa2c9a3-b8f1-494a-9393-379c1f1c57d7\royal_enfield_img_1782397843839.png',
        'dst': r'c:\Mini project\static\images\royal_enfield.png',
        'url': '/static/images/royal_enfield.png',
        'title_like': '%Royal Enfield%'
    }
]

external_updates = [
    {
        'url': 'https://loremflickr.com/800/600/denimjacket?lock=10',
        'title_like': '%Denim Jacket%'
    },
    {
        'url': 'https://loremflickr.com/800/600/badmintonracket?lock=20',
        'title_like': '%Badminton%'
    }
]

conn = sqlite3.connect('marketplace.db')
c = conn.cursor()

for item in updates:
    if os.path.exists(item['src']):
        shutil.copy(item['src'], item['dst'])
        c.execute("UPDATE products SET image_url = ? WHERE title LIKE ?", (item['url'], item['title_like']))
        print(f"Updated {item['title_like']}: {c.rowcount} rows")

for item in external_updates:
    c.execute("UPDATE products SET image_url = ? WHERE title LIKE ?", (item['url'], item['title_like']))
    print(f"Updated external {item['title_like']}: {c.rowcount} rows")

conn.commit()
conn.close()
