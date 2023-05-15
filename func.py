import json
import aiohttp
from models import Base, Advertisement, Session, engine, Users
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


async def get_weather(city, key):
    async with aiohttp.ClientSession() as client:
        response = await client.get(f'http://api.openweathermap.org/data/2.5/weather', params = {'q': city, 'APPID': key})
        json_data = await response.json()
        temp_degree = round((json_data["main"]["temp"] - 273), 1)
        # print(f'{city}: {json_data["weather"][0]["main"]}, температура - {round(temp_degree, 1)}')

        return city, json_data["weather"][0]["main"], temp_degree


async def paste_to_db(user_id, advertisement_data, session):
    orm_date = Advertisement(id_user= user_id, title=advertisement_data['title'], description=advertisement_data['description'])
    session.add(orm_date)

    await session.commit()
