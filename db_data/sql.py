import os
import sqlite3
import vk_api


def create_table_db(table_name):
    """
    Функция для создания новой таблицы в БД.
    :param table_name:  --- имя таблицы.
    :return:
    """
    try:
        sqlite_connection = sqlite3.connect('bakery_database.db')
        sqlite_create_table_query = f'''CREATE TABLE {table_name} (
                                    id INTEGER PRIMARY KEY,
                                    title TEXT NOT NULL,
                                    description TEXT NOT NULL,
                                    pictures BLOB NOT NULL);'''

        cursor = sqlite_connection.cursor()
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()


def convert_to_binary_data(filename):
    """
    Данная функция предназначена для преобразования данных в двоичный формат.
    :param filename: --- название фото, которое хотите преобразовать в двоичный формат.
    :return:
    """
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


def insert_blob(emp_id, title, description, photo, table_name):
    """
    Данная функция предназначена для заполнения и загрузки модели в БД.
    :param emp_id: --- id товара;
    :param title:  --- название товара;
    :param photo:   --- фото товара;
    :param description:  --- описание товара;
    :param table_name:  --- имя таблицы для добавления товара;
    :return:
    """
    try:
        sqlite_connection = sqlite3.connect('bakery_database.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_insert_blob_query = f"""INSERT INTO {table_name}
                                  (id, title, description, pictures) VALUES (?, ?, ?, ?)"""

        emp_photo = convert_to_binary_data(photo)
        # Преобразование данных в формат кортежа
        data_tuple = (emp_id, title, description, emp_photo)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def write_to_file(data, filename, path):
    """
    Преобразование двоичных данных в нужный формат
    :param data: --- указатель на объект картинки
    :param filename: --- название картинки
    :param path: --- путь к картинке
    :return:
    """
    with open(path + filename + ".jpg", 'wb') as file:
        file.write(data)


def read_blob_data(table_name, vk, event):
    """
    Функция служащая для выгрузки данных из БД. Обработки и отправки данных пользователю.
    :param table_name: --- имя таблицы
    :param vk: --- vk_api.VkApi(token=api_token)
    :param event: --- обрабатываемое событие
    :return:
    """
    try:
        path = os.path.abspath(os.getcwd()) + "\db_data\\bakery_database.db"
        sqlite_connection = sqlite3.connect(path)
        cursor = sqlite_connection.cursor()

        sql_fetch_blob_query = f"""SELECT * from {table_name} """
        cursor.execute(sql_fetch_blob_query)
        record = cursor.fetchall()

        for row in record:
            title = row[1]
            description = row[2]
            photo = row[3]

            path = os.path.abspath(os.getcwd()) + f'\db_data\\db_pictures\{table_name}\\'
            write_to_file(photo, title, path)

            send_photo(table_name, title, vk)
            vk.method("messages.send",
                      {"peer_id": event.object['message']['from_id'],
                       "message": f"Название: {title}.\n"
                                  f"Описание: {description}.\n"
                                  f"Фото:\n",
                       "attachment": attachment,
                       "random_id": 0})
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def send_photo(table_name, photo, vk):
    """
    Функция служит, для формирования фото, под стандарт и формат vk_api
    :param table_name: - имя таблицы в которой находится фото
    :param photo: - название фото
    :param vk: - vk_api.VkApi(token=api_token)
    :return:
    """
    global attachment
    upload = vk_api.VkUpload(vk)
    path = os.path.abspath(os.getcwd()) + f'\db_data\db_pictures\\{table_name}\\{photo}.jpg'
    pict = upload.photo_messages(path)
    owner_id = pict[0]["owner_id"]
    photo_id = pict[0]["id"]
    access_key = pict[0]["access_key"]
    attachment = f"photo{owner_id}_{photo_id}_{access_key}"
