import vk_api
import sqlite3
import json
import requests
from vk_api.longpoll import VkLongPoll, VkEventType
token = 'СЮДА СВОЙ ТОКЕН ВВЕДИ'
def write_msg(user_id,message,keyboard = False):
    if keyboard == False:
        vk.method('messages.send', {'user_id': user_id, 'message': message})
    else:
        vk.method('messages.send', {'user_id': user_id,'message': message, 'keyboard': str(json.dumps(keyboard,ensure_ascii=False))})
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
def get_nicname(user_ids):
    get_nickname = 'https://api.vk.com/method/users.get?user_ids=%i&fields=first_name&access_token=%token&v=5.87'%(user_ids,token)
    request = requests.get(get_nickname)
    return request
connection_database = sqlite3.connect('database.db')
data = connection_database.cursor()