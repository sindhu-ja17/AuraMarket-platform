import sqlite3, shutil
src = r'C:\Users\acer\.gemini\antigravity-ide\brain\5fa2c9a3-b8f1-494a-9393-379c1f1c57d7\iphone_14_pro_max_img_1782397167436.png'
dst = r'c:\Mini project\static\images\iphone_14_pro_max.png'
shutil.copy(src, dst)

conn = sqlite3.connect('marketplace.db')
c = conn.cursor()
c.execute("UPDATE products SET image_url = '/static/images/iphone_14_pro_max.png' WHERE title LIKE '%iPhone%'")
print('Updated:', c.rowcount)
conn.commit()
conn.close()
