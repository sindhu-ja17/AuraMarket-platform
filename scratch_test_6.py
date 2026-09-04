import sqlite3
conn = sqlite3.connect('marketplace.db')
print(conn.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='messages'").fetchone()[0])
