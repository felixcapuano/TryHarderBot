import sqlite3 as sql
import const
import json


async def create_user(data):
    # check user existence
    # add user

    req = """INSERT INTO users VALUES ('{d_id}',
                                        '{f_id}',
                                        '{plat}',
                                        '{d_w}',
                                        '{d_k}',
                                        '{d_g}',
                                        '{s_w}',
                                        '{s_k}',
                                        '{s_g}')
                                        """.format(**data)
    res, error = await exec(req)
        
    if error is None:
        return None
    else:
        return error

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
    conn = sql.connect(const.db)
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



