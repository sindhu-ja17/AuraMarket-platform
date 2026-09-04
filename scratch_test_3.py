import sqlite3
import app as myapp

conn = sqlite3.connect('marketplace.db')
print("Conversations for user 6:")
for r in conn.execute("SELECT id FROM conversations WHERE buyer_id=6 OR seller_id=6 LIMIT 1"):
    conv_id = r[0]
    print("Conv ID:", conv_id)
    break
else:
    conv_id = None
conn.close()

if conv_id:
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
