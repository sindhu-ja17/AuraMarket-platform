import sqlite3

external_updates = [
    {
        'url': 'https://loremflickr.com/800/600/badminton,racket?lock=51',
        'title_like': '%Badminton Racket%'
    },
    {
        'url': 'https://loremflickr.com/800/600/smarthome,device?lock=52',
        'title_like': '%Smart Home Hub%'
    },
    {
        'url': 'https://loremflickr.com/800/600/smartphone,phone?lock=53',
        'title_like': '%Smartphone X%'
    },
    {
        'url': 'https://loremflickr.com/800/600/handbag,fashion?lock=54',
        'title_like': '%Designer Handbag%'
    },
    {
        'url': 'https://loremflickr.com/800/600/runningshoes,sneakers?lock=55',
        'title_like': '%Running Shoes%'
    },
    {
        'url': 'https://loremflickr.com/800/600/ladder,stepladder?lock=56',
        'title_like': '%Aluminium Ladder%'
    },
    {
        'url': 'https://loremflickr.com/800/600/mobilephone,iphone?lock=57',
        'title_like': '%Mobile phone%'
    }
]

conn = sqlite3.connect('marketplace.db')
c = conn.cursor()

for item in external_updates:
    c.execute("UPDATE products SET image_url = ? WHERE title LIKE ?", (item['url'], item['title_like']))
    print(f"Updated external {item['title_like']}: {c.rowcount} rows")

conn.commit()
conn.close()
