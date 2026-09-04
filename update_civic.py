import sqlite3, shutil
src = r'C:\Users\acer\.gemini\antigravity-ide\brain\5fa2c9a3-b8f1-494a-9393-379c1f1c57d7\honda_civic_img_1782397361271.png'
dst = r'c:\Mini project\static\images\honda_civic.png'
shutil.copy(src, dst)

conn = sqlite3.connect('marketplace.db')
c = conn.cursor()
c.execute("UPDATE products SET image_url = '/static/images/honda_civic.png' WHERE title LIKE '%Civic%'")
print('Updated:', c.rowcount)
conn.commit()
conn.close()
