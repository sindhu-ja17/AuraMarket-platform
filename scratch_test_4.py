import sqlite3
import app as myapp

conn = sqlite3.connect('marketplace.db')
cursor = conn.cursor()
cursor.execute("INSERT INTO conversations (buyer_id, seller_id, product_id) VALUES (6, 2, 11)")
conv_id = cursor.lastrowid
conn.commit()
conn.close()

print("Created new conv:", conv_id)

client = myapp.app.test_client()
with client.session_transaction() as sess:
    sess['user_id'] = 6
res = client.get(f'/chat/{conv_id}')
html = res.data.decode('utf-8')

if 'chat-input-area' in html:
    print("Form is PRESENT!")
else:
    print("Form is MISSING!")

idx = html.find('chat-messages')
print(html[idx:idx+1500])
