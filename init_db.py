import sqlite3

conn = sqlite3.connect("users.db")

c = conn.cursor()

c.execute("""CREATE TABLE users (
            discord_id text NOT NULL UNIQUE,
            fortnite_id text NOT NULL UNIQUE,
            platform text NOT NULL, 
            duo_wins integer NOT NULL,
            duo_kills integer NOT NULL,
            duo_games integer NOT NULL,
            squad_wins integer NOT NULL,
            squad_kills integer NOT NULL,
            squad_games integer NOT NULL
            )""")

conn.commit()

conn.close()
