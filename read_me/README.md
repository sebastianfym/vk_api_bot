# Чат-бот для в VK (сообщения сообществ. Всё работает через официальное api. Подключение к VK работа через longpoll)
# Логика:
    Витрина выпечки/кондитерской. 3 раздела, в каждом по 3 товара. 
    У товара описание, название и фотография.
    Для навигации используются кнопки. (JSON-клавиатуру можно найти в папке "keyboards")

## config.py (ВАЖНО!)
    vk_api_token = специальный токен вашего бота. Получить его можно так:ваше сообщество -> управление -> работа с API
    -> создать ключ
    community_id = id вашего сообщества

    Для корректной работы бота необходимо поставить ваши данные в вышеперечисленные пункты!

## server_manager.py
    Файл служащий, для настройки и запуска сервера

## server.py
    Имеет в себе 1 класс Server и методы к нему:
    -send_msg(self, send_id, message) --- отправка сообщения через метод messages.send;
    -start(self) --- функция запускающая рабочий цикл, который получает события приходящие в сообщество;
    -processing_message(self, event) --- функция определяющая выбор пользователя, для дальнейшей работы;
    
## sql.py
    Файл отвечающий за работу с БД и обработку данных в ней.
    -create_table_db(table_name) --- функция для создания новой таблицы в БД;
    -convert_to_binary_data(filename)) --- функция предназначена для преобразования данных в двоичный формат;
    -insert_blob(emp_id, title, description, photo, table_name) --- функция предназначена для заполнения и загрузки 
    модели в БД;
    -write_to_file(data, filename, path) --- функция для преобразование двоичных данных в нужный формат 
    -read_blob_data --- функция служащая для выгрузки данных из БД. Обработки и отправки данных пользователю;
    -send_photo(table_name, photo, vk) --- функция служит, для формирования фото, под стандарт и формат vk_api.