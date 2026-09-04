import sqlite3
import app as myapp

client = myapp.app.test_client()
with client.session_transaction() as sess:
    sess['user_id'] = 6
res = client.get('/chat/22')
html = res.data.decode('utf-8')

with open('full_chat.html', 'w', encoding='utf-8') as f:
    f.write(html)
