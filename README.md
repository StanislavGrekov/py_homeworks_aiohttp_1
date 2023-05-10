## Кирилл, приветствую Вас.
### Сдаю домашнее задание по теме Aiohttp
### Немного изменил исходное задание (так как блок все равно закрыт,я немного решил поэксперементировать)
### Файл server.py содержит классы и роуты, файл func.py содержит функции запросов к Openweathermap и запись в базу.
### После регистрации пользователя (п.1-п.4 файла client.py) можно выполнить запрос погоды (п.5-п.7 файла client.py) по городам, указаным в списке .
### В файле server.py есть блок кода:

        if await validate(password, user.password):
            cities_coros = []
            for city in cities:
                cities_coros.append(get_weather(city, key))
            result = await asyncio.gather(*cities_coros)


            tasks, dict_weather = [], {}
            for element in result:
                dict_weather['city'] = element[0]
                dict_weather['description'] = element[1]
                dict_weather['temp'] = element[2]
                paste_to_db_coros = paste_to_db(user_id, dict_weather, self.session)
                task = asyncio.create_task(paste_to_db_coros)
                tasks.append(task)

                for task in tasks:
                    await task

### где я асинхронно получаю данные о погоде и записываю эти данные в БД. 
### Информация о погоде приходит асинхронно (проверял время выполнения).
### А вот запись в БД, кажется, выполняется не аснхронно. Я не уверен в правильности кода и не знаю как это проверить.

