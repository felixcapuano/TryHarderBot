import sqlite3 as sql
import const
import json


async def create_user(data):
    # check user existence
    # add user

    req = """INSERT INTO users VALUES ('{discord_id}',
                                        '{fornite_id}',
                                        '{platform}')
                                        """.format(**data)
    res, error = await exec(req)
        
    if error is None:
        return None
    else:
        id_existing = (str(error).split("."))[1]
        if id_existing == "fortnite_id":
            return "This fortnite username has already been used"

        elif id_existing == "discord_id":
            return "You have already join!"

        else:
            return "Something goes wrong. Sorry!"

async def is_user_exist(user_id):
    res = await get_user(user_id)
    return res is not None 

async def get_user(user_id):
    req = "SELECT * FROM users WHERE discord_id='{}'".format(user_id)
    res, error = await exec(req)

    return res

async def remove_users(user_id=None):
    req = "DELETE FROM users"
    if user_id is not None:
        req += " WHERE discord_id='{}'".format(user_id)
    await exec(req)

async def exec(request):
    conn = sql.connect(const.DB_FILE)
    c = conn.cursor()

    try:
        c.execute(request)

        result = c.fetchone()
        return result, None
    except sql.IntegrityError as error:
        return None, error
    finally:
        conn.commit()
        conn.close()
    
async def save_setting(data):
    with open(const.SETTING_FILE, "w") as sf:
        json.dump(data, sf)

def load_setting():
    with open(const.SETTING_FILE, "r") as sf:
        return json.load(sf)
