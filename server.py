import json
import asyncio
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from models import Base, Advertisement, Session, engine, Users
from aiohttp import web

from func import hash_password, get_user, validate, get_weather, paste_to_db


async def orm_context(app):
    print("START")
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    print("SHUT DOWN")


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request['session'] = session
        response = await handler(request)
        return response


app = web.Application()
app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)


class AdvertisementView(web.View):

    @property
    def session(self):
        return self.request['session']

    @property
    def weather_id(self):
        return int(self.request.match_info['weather_id'])


    async def get(self):
        advertisement_data = await self.request.json()

        email = advertisement_data['email']

        try:
            query = select(Users).where(Users.email == email)
            result = await self.request["session"].execute(query)
            user = result.scalar()
            user_id = user.id
            print(user_id)
            query = select().where(Advertisement.id_user == user_id)
            result = await self.request["session"].execute(query)
            adv = result.scalar()
            adv_id = adv.id

            print(adv_id)

            # answer_list = []
            # user = result.scalar()
            # print(user)
            # print(user)
            # for row in result:
            #     print(row['id'])

            # for element in result:
            #     print(element.id)
                # row = f'№{element.id}, Заголовок: {element.title}, описание: {element.description}.'
                # print(row)
                # answer_list.append(row)

            # for element in result:
            #     row = f'№{element[0].id}, Заголовок: {element[0].title}, описание: {element[0].description}, дата создания: {element[0].created_fild}.'
            #     answer_list.append(row)
            await self.request["session"].commit()
            return web.json_response({'answer': 1})

        except AttributeError:
            raise web.HTTPNotFound(
                text=json.dumps({'answer': ['Пользователь не найден или пароль неверен']}),
                content_type='application/json')


    async def post(self):
        advertisement_data = await self.request.json()

        email = advertisement_data['email']
        password = advertisement_data['password']

        query = select(Users).where(Users.email == email)
        result = await self.request["session"].execute(query)
        user = result.scalar()
        user_id = user.id

        if await validate(password, user.password):
            await paste_to_db(user_id, advertisement_data, self.session)
            return web.json_response({'answer': f'Объявление \"{advertisement_data["title"]}\" успешно добавлено в базу'})

        else:
            raise web.HTTPNotFound(
                text=json.dumps({'answer': 'Пользователь не найден или пароль неверен'}),
                content_type='application/json')


        # if await validate(password, user.password):
        #     cities_coros = []
        #     for city in cities:
        #         cities_coros.append(get_weather(city, key))
        #     result = await asyncio.gather(*cities_coros)
        #
        #     tasks, dict_weather = [], {}
        #     for element in result:
        #         dict_weather['city'] = element[0]
        #         dict_weather['description'] = element[1]
        #         dict_weather['temp'] = element[2]
        #         paste_to_db_coros = paste_to_db(user_id, dict_weather, self.session)
        #         task = asyncio.create_task(paste_to_db_coros)
        #         tasks.append(task)
        #
        #         for task in tasks:
        #             await task
        #
        #     return web.json_response({'answer': f'Данные по городам {", ".join(cities)} успешно добавлены в базу'})
        #
        # else:
        #     raise web.HTTPNotFound(
        #         text=json.dumps({'answer': 'Пользователь не найден'}),
        #         content_type='application/json')


    async def delete(self):
        # user_data = await self.request.json()
        # id_row = self.weather_id
        # email = user_data['email']
        # password = user_data['password']
        #
        # try:
        #     query = select(Users).where(Users.email == email)
        #     result = await self.request["session"].execute(query)
        #     user = result.scalar()
        #     user_password = user.password
        #
        #     if await validate(password, user_password):
        #         query = select(Weather).where(Weather.id_user == user.id)
        #         result = await self.request["session"].execute(query)
        #         id_list = []
        #         for element in result:
        #             id_list.append(element[0].id)
        #
        #         if id_row in id_list:
        #             weather_row = await self.session.get(Weather, id_row)
        #             await self.request["session"].delete(weather_row)
        #             await self.request["session"].commit()
        #             return web.json_response({'answer': f'Строка {weather_row.id} успешно удалена'})
        #         else:
        #             return web.json_response({'answer': 'Указанной строки нет в БД'})
        #     else:
        #         return web.json_response({'answer': 'Пароль не подходит'})
        #
        #
        # except AttributeError:
        #     raise web.HTTPNotFound(
        #         text=json.dumps({'answer': 'Пользователь не найден'}),
        #         content_type='application/json')
        pass


class UserView(web.View):

    @property
    def session(self):
        return self.request['session']

    @property
    def user_id(self):
        return int(self.request.match_info['user_id'])

    async def get(self):
        user = await get_user(self.user_id, self.session)
        return web.json_response({'answer': f'Пользователь {user.last_name} {user.first_name} зарегистрирован {user.registration_date}!'})

    async def post(self):
        user_data = await self.request.json()
        user_data['password'] = hash_password(user_data['password'])
        user = Users(**user_data)
        self.request['session'].add(user)
        try:
            await self.request['session'].commit()
        except IntegrityError as er:
            raise web.HTTPConflict(
                text = json.dumps({'answer': 'Пользователь с таким почтовым адресом уже создан'}),
                content_type = 'application/json'
            )
        return web.json_response({'answer': f'Пользователь {user.last_name} зарегистрирован!'})

    async def patch(self):
        user_data = await self.request.json()
        old_password = user_data['oldpassword']
        user = await get_user(self.user_id, self.session)
        user_password = user.password
        if await validate(old_password, user_password):
            user_data['password'] = hash_password(user_data['newpassword'])
            user_data.pop('oldpassword')
            user_data.pop('newpassword')
            for key, value in user_data.items():
                setattr(user, key, value)
            await self.request['session'].commit()
            return web.json_response({'answer': f'Информация по пользователю {user.last_name} успешно обновлена!'})
        else:
            raise web.HTTPNotFound(
                text=json.dumps({'answer': 'Пользователь не найден'}),
                content_type='application/json'
            )

    async def delete(self):
        user_data = await self.request.json()
        password = user_data['password']
        user = await get_user(self.user_id, self.session)
        user_password = user.password
        if await validate(password, user_password):
            await self.request["session"].delete(user)
            await self.request["session"].commit()
            return web.json_response({"answer": f"Пользователь {user.last_name} успешно удален"})
        else:
            raise web.HTTPNotFound(
                text=json.dumps({'answer': 'Пользователь не найден'}),
                content_type='application/json'
            )


app.add_routes([
    web.post('/weather/', AdvertisementView),
    web.get('/weather/', AdvertisementView),
    web.delete(r'/weather/{weather_id:\d+}',  AdvertisementView),

    web.post('/user/', UserView),
    web.get(r'/user/{user_id:\d+}', UserView),
    web.patch(r'/user/{user_id:\d+}', UserView),
    web.delete(r'/user/{user_id:\d+}', UserView),


])

web.run_app(app)




# This is a sample Python script.
# import asyncpg
# import asyncio
# import aiohttp
# import time
# from asyncio import run
# from pprint import pprint
# from models import Base, Weather_data, Session, engine


# async def get_weather(city):
#
#     # С использованием ассинхронного менеджера контекста
#     async with aiohttp.ClientSession() as client:
#         response = await client.get(f'http://api.openweathermap.org/data/2.5/weather', params = {'q': city, 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56'})
#         json_data = await response.json()
#         # print(f'{city}: {json_data["weather"][0]["main"]}')
#
#         #return json_data
#         return city, json_data["weather"][0]["main"]
#         # return json_data['name'], json_data["weather"][0]["main"]
#
#     # Без использования  ассинхронного менеджера контекста
#     # client = aiohttp.ClientSession()
#     # print(f'{city} bofore get')
#     # response = await client.get(f'http://api.openweathermap.org/data/2.5/weather', params = {'q': city, 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56'})
#     # json_data = await response.json()
#     # print(f'{city} json ready')
#     # print(f'{city}: {json_data["weather"][0]["main"]}')
#     # await client.close()
#     # return json_data
#
# cities = ['Moscow', 'St. Petersburg', 'Rostov-on-Don', 'Kaliningrad', 'Vladivostok',
#           'Minsk', 'Beijing', 'Delhi', 'Istanbul', 'Tokyo', 'London', 'New York', 'Miass']
#
#
# async def paste_to_db(json_data):
#     async with Session() as session:
#         for element in json_data:
#             orm_date = Weather_data(json=element)
#             session.add(orm_date)
#         await session.commit()
#
#
# tasks = []
# async def main():
#     async with engine.begin() as con:
#         await con.run_sync(Base.metadata.create_all)
#
#     # Первый вариант ассинхронного запроса
#     # coro_1 = get_weather(cities[0])
#     # coro_2 = get_weather(cities[1])
#     # coro_3 = get_weather(cities[2])
#     # coro_4 = get_weather(cities[3])
#     # coro_5 = get_weather(cities[4])
#     # coro_6 = get_weather(cities[5])
#     # result = await asyncio.gather(coro_1, coro_2,coro_3,coro_4,coro_5,coro_6)
#     # print(result)
#
#     # Второй вариант ассинхронного запроса с использованием create_task
#     # tasks = []
#     # for city in cities:
#     #     tasks.append(asyncio.create_task((get_weather(city))))
#     # result = await asyncio.gather(*tasks)
#     # print(result)
#
#     #Третий вариант ассинхронного запроса с использованием цикла
#     # cities_coros = []
#     # for city in cities:
#     #     cities_coros.append(get_weather(city))
#     # result = await asyncio.gather(*cities_coros)
#     #
#     # pprint(result)
#
#
#     # Вставка в базу данных
#     cities_coros = []
#     for city in cities:
#         cities_coros.append(get_weather(city))
#     result = await asyncio.gather(*cities_coros)
#
#     # pprint(result)
#
#
#     paste_to_db_coros = paste_to_db(result)
#     task = asyncio.create_task(paste_to_db_coros)
#     tasks.append(task)
#
#     for task in tasks:
#         await task
#
#     # await paste_to_db(result)
#
#
# if __name__ == "__main__":
#
#     print(time.strftime('%X'))
#
#     run(main())
#
#     print(time.strftime('%X'))