# Импортируем созданный нами класс Server
from server import Server
# Получаем из config.py наш api-token
from config import vk_api_token, community_id


server = Server(vk_api_token, community_id, "server")
"""
vk_api_token - API токен, который мы ранее создали
community_id - id сообщества-бота
"server" - имя сервера
"""

server.start()

