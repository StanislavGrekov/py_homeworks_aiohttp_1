# This is a sample Python script.
import asyncpg
import asyncio
import aiohttp
import time
from asyncio import run
from pprint import pprint
from models import Base, Weather_data, Session, engine
from aiohttp import web


app = web.Application()



async def get_weather(city, key):

    # С использованием ассинхронного менеджера контекста
    async with aiohttp.ClientSession() as client:
        response = await client.get(f'http://api.openweathermap.org/data/2.5/weather', params = {'q': city, 'APPID': key})
        json_data = await response.json()
        print(f'{city}: {json_data["weather"][0]["main"]}')

        #return json_data
        return city, json_data["weather"][0]["main"]
        # return json_data['name'], json_data["weather"][0]["main"]



async def paste_to_db(json_data):
    async with Session() as session:
        print(json_data)
        for element in json_data:
            orm_date = Weather_data(json=element)
            session.add(orm_date)
        await session.commit()


tasks = []
async def main(cities, key):

    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

    # Вставка в базу данных
    cities_coros = []
    for city in cities:
        cities_coros.append(get_weather(city, key))
    result = await asyncio.gather(*cities_coros)

    paste_to_db_coros = paste_to_db(result)
    task = asyncio.create_task(paste_to_db_coros)
    tasks.append(task)

    for task in tasks:
        await task

    # await paste_to_db(result)


class WeatherView(web.View):

    async def get(self):
        pass
    async def post(self):
        user_data = await self.request.json()
        cities = user_data['cities']
        key =  user_data['APPID']
        await main(cities, key)

        return web.json_response({'hellow': 'test'})

    async def patch(self):
        pass

    async def delete(self):
        pass


app.add_routes([
    web.get('/weather/', WeatherView),
    web.post('/weather/', WeatherView),
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