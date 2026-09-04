import sqlite3, shutil
src = r'C:\Users\acer\.gemini\antigravity-ide\brain\5fa2c9a3-b8f1-494a-9393-379c1f1c57d7\leather_jacket_img_1782397274697.png'
dst = r'c:\Mini project\static\images\leather_jacket.png'
shutil.copy(src, dst)

conn = sqlite3.connect('marketplace.db')
c = conn.cursor()
c.execute("UPDATE products SET image_url = '/static/images/leather_jacket.png' WHERE title LIKE '%Leather Jacket%'")
print('Updated:', c.rowcount)
conn.commit()
conn.close()
