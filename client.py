import aiohttp
import asyncio

async def main():
    async with aiohttp.ClientSession() as client:
        #1.Создание пользователя
        response = await client.post('http://127.0.0.1:8080/user/',
                                     json={'email': 'dimon@yandex.ru',
                                        'password': '12345678',
                                        'first_name': 'Дмитрий',
                                        'last_name': 'Дмитриев'})

        data = await response.json()
        print(data['answer'])

        # 2.Получение данных пользователя
        # response = await client.get('http://127.0.0.1:8080/user/2')
        #
        # data = await response.json()
        # print(data['answer'])

        # 3.Редактирование пользователя
        # response = await client.patch('http://127.0.0.1:8080/user/2',
        #                              json={'email': 'dimon@yandex.ru',
        #                                 'oldpassword': '12345678',
        #                                 'newpassword': 'password',
        #                                 'first_name': 'Дмитрий',
        #                                 'last_name': 'Дмитриев'})
        #
        # data = await response.json()
        # print(data['answer'])

        # 4.Удаление пользователя
        # response = await client.delete('http://127.0.0.1:8080/user/2',
        #                                json={'email': 'dimon@yandex.ru',
        #                                      'password': 'password',})
        #
        # data = await response.json()
        # print(data['answer'])

        # 5.Создание объявлений в БД
        # response = await client.post('http://127.0.0.1:8080/adv/',
        #                              json={'title': "Продам холодильник",
        #                                    'description': "Продам хороший советский холодильник Полюс-10 КШ-260",
        #                                    'email': 'dimon@yandex.ru',
        #                                     'password': '12345678',
        #                                    })
        # data = await response.json()
        # print(data['answer'])

        #  6.Получение объявлений
        # response = await client.get('http://127.0.0.1:8080/adv/',
        #                              json={
        #                                    'email': 'dimon@yandex.ru',
        #                                    })
        # data = await response.json()
        # for element in data['answer']:
        #     print(element)

        # 7.Удаление объявлений
        # response = await client.delete('http://127.0.0.1:8080/adv/4',
        #                                json={'email': 'dimon@yandex.ru',
        #                                      'password': '12345678',})
        #
        # data = await response.json()
        # print(data['answer'])

asyncio.run(main())
