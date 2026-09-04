import app as myapp

client = myapp.app.test_client()

# login
with client.session_transaction() as sess:
    sess['user_id'] = 1 # sindhuja-1712

res = client.get('/chat/22')
html = res.data.decode('utf-8')
idx = html.find('chat-window')
print(html[idx:idx+1500])
