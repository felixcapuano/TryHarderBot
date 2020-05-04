import sqlite3

conn = sqlite3.connect("users.db")

c = conn.cursor()

c.execute("""CREATE TABLE users (
            discord_id text NOT NULL UNIQUE,
            fortnite_id text NOT NULL UNIQUE,
            platform text NOT NULL 
            )""")

conn.commit()

conn.close()
