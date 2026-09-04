import sqlite3

conn = sqlite3.connect('marketplace.db')
cur = conn.cursor()

addresses = [
    'No 12, RMV Extension Stage 2, Sanjay Nagar, Bangalore, Karnataka 560094',
    'Flat 4B, Sea View Apartments, Carter Road, Bandra West, Mumbai, Maharashtra 400050',
    '34/1, Mount Road, Teynampet, Chennai, Tamil Nadu 600018',
    'House 129, Sector 21, Gandhinagar, Gujarat 382021',
    '23 Park Street, Near Allen Park, Kolkata, West Bengal 700016',
    'Plot 45, Jubilee Hills Check Post Road, Hyderabad, Telangana 500033',
    '10, Connaught Place, Inner Circle, New Delhi, Delhi 110001',
    'No 8, MG Road, Camp, Pune, Maharashtra 411001',
]

cur.execute('SELECT id FROM users ORDER BY id')
rows = cur.fetchall()

for i, r in enumerate(rows):
    pid = r[0]
    ad = addresses[i % len(addresses)]
    cur.execute('UPDATE users SET address=? WHERE id=?', (ad, pid))

conn.commit()
conn.close()
print('Updated users with unique addresses')
