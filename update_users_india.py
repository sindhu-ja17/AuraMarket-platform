import sqlite3
import random

conn = sqlite3.connect('marketplace.db')
cur = conn.cursor()

addresses = [
    '12, MG Road, Bangalore, Karnataka 560001',
    '45, Anna Salai, Chennai, Tamil Nadu 600002',
    '78, Linking Road, Mumbai, Maharashtra 400050',
    '10, Connaught Place, New Delhi, Delhi 110001',
    '8, Park Street, Kolkata, West Bengal 700016'
]

cur.execute('SELECT id FROM users')
rows = cur.fetchall()

for r in rows:
    pid = r[0]
    ph = '+91 ' + str(random.randint(9000000000, 9999999999))
    ad = random.choice(addresses)
    cur.execute('UPDATE users SET phone_number=?, address=? WHERE id=?', (ph, ad, pid))

conn.commit()
conn.close()
print('Updated users')
