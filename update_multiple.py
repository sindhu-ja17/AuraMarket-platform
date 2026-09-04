import sqlite3, shutil, os

os.makedirs(r'c:\Mini project\static\images', exist_ok=True)

updates = [
    {
        'src': r'C:\Users\acer\.gemini\antigravity-ide\brain\5fa2c9a3-b8f1-494a-9393-379c1f1c57d7\canon_eos_r5_img_1782397519334.png',
        'dst': r'c:\Mini project\static\images\canon_eos_r5.png',
        'url': '/static/images/canon_eos_r5.png',
        'title_like': '%Canon%'
    },
    {
        'src': r'C:\Users\acer\.gemini\antigravity-ide\brain\5fa2c9a3-b8f1-494a-9393-379c1f1c57d7\mountain_bike_img_1782397533718.png',
        'dst': r'c:\Mini project\static\images\mountain_bike.png',
        'url': '/static/images/mountain_bike.png',
        'title_like': '%Mountain%'
    },
    {
        'src': r'C:\Users\acer\.gemini\antigravity-ide\brain\5fa2c9a3-b8f1-494a-9393-379c1f1c57d7\grey_sofa_img_1782397548463.png',
        'dst': r'c:\Mini project\static\images\grey_sofa.png',
        'url': '/static/images/grey_sofa.png',
        'title_like': '%Sofa%'
    },
    {
        'src': r'C:\Users\acer\.gemini\antigravity-ide\brain\5fa2c9a3-b8f1-494a-9393-379c1f1c57d7\ps5_console_img_1782397563034.png',
        'dst': r'c:\Mini project\static\images\ps5_console.png',
        'url': '/static/images/ps5_console.png',
        'title_like': '%PlayStation%'
    },
    {
        'src': r'C:\Users\acer\.gemini\antigravity-ide\brain\5fa2c9a3-b8f1-494a-9393-379c1f1c57d7\jordan_1_img_1782397575691.png',
        'dst': r'c:\Mini project\static\images\jordan_1.png',
        'url': '/static/images/jordan_1.png',
        'title_like': '%Jordan%'
    }
]

conn = sqlite3.connect('marketplace.db')
c = conn.cursor()

for item in updates:
    shutil.copy(item['src'], item['dst'])
    c.execute("UPDATE products SET image_url = ? WHERE title LIKE ?", (item['url'], item['title_like']))
    print(f"Updated {item['title_like']}: {c.rowcount} rows")

conn.commit()
conn.close()
