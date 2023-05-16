import json
from models import  Advertisement, Users
from aiohttp import web
from bcrypt import hashpw, gensalt, checkpw


def hash_password(password):
    password = password.encode()
    password = hashpw(password, salt=gensalt())
    password = password.decode()

    return password


async def get_user(user_id, session):
    user = await session.get(Users, user_id)
    if user is None:
        raise web.HTTPNotFound(
            text=json.dumps({'answer': 'Пользователь не найден'}),
            content_type='application/json'
        )
    return user


async def validate(old_password, user_password):
    if checkpw(old_password.encode(), user_password.encode()):
        return True
    else:
        return False


async def paste_to_db(user_id, advertisement_data, session):
    orm_date = Advertisement(id_user= user_id, title=advertisement_data['title'], description=advertisement_data['description'])
    session.add(orm_date)

    await session.commit()
