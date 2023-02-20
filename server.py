import threading
import vk_api.vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
from vk_api.utils import get_random_id

from db_data.sql import read_blob_data


class Server:

    def __init__(self, api_token, group_id, server_name: str = "Empty"):
        # Даем серверу имя
        self.server_name = server_name

        # Для Long Poll
        self.vk = vk_api.VkApi(token=api_token)

        # Для использования Long Poll API
        self.long_poll = VkBotLongPoll(self.vk, group_id)

        # Для вызова методов vk_api
        self.vk_api = self.vk.get_api()

    def send_msg(self, send_id, message):
        """
        Отправка сообщения через метод messages.send
        :param send_id: --- vk id пользователя, который получит сообщение
        :param message: --- содержимое отправляемого письма
        :return: None
        """
        self.vk_api.messages.send(peer_id=send_id, message=message, random_id=get_random_id(),
                                  keyboard=open(f"keyboards/keyboard_main.json", "r", encoding="UTF-8").read())

    def start(self):
        """
        Функция запускающая рабочий цикл, который получает события приходящие в сообщество
        """
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
                threading.Thread(target=self.processing_message(event), args=(event.obj.from_id, event.obj.text)).start()

    def processing_message(self, event):
        """
        Функция определяющая выбор пользователя, для дальнейшей работы.
        И вызывает основную рабочую функцию.
        :param event: --- обрабатываемое событие
        :return:
        """
        if event.message['text'] == "выпечка":
            choice = "pastries"
        elif event.message['text'] == "десерты":
            choice = "desserts"
        elif event.message['text'] == "пироги":
            choice = "pies"
        else:
            return
        read_blob_data(choice, self.vk, event)

