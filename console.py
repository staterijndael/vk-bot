# -*- coding: utf8 -*-
from connect import *
import datetime
class Color:
    Red = '\033[91m'
    Green = '\033[92m'
    Yellow = '\033[93m'
    Blue = '\033[94m'
    Magenta = '\033[95m'
    Cyan = '\033[96m'
    White = '\033[97m'
    Grey = '\033[90m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
def new_user(user_id,full_name_json):
    now = datetime.datetime.now()
    return print(Color.Yellow + 'Р—Р°СЂРµРіРёСЃС‚СЂРёСЂРѕРІР°РЅ РЅРѕРІС‹Р№ РїРѕР»СЊР·РѕРІР°С‚РµР»СЊ:' + Color.END + Color.Cyan + '[' + str(user_id) + ']' + '[' + full_name_json + ']' + '[' + str(now.day) + '.' + str(now.month) + ' ' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second) + ']' + Color.END )
def coins_get(user_id,full_name_json,coins_value,origin,btn):
    now = datetime.datetime.now()
    write_msg(user_id, 'Р’С‹ РїРѕР»СѓС‡РёР»Рё %r РїРёС‚РѕРЅРѕРІ Р·Р° %r. РџРѕР·РґСЂР°РІР»СЏРµРј!' % (str(coins_value), origin), btn)
    print(Color.Blue + '[' + str(user_id) + ']' + '[' + full_name_json + ']' + '[' + str(now.day) + '.' + str(now.month) + ' ' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second) + ']' + '[' + str(coins_value) + ']' + Color.END + Color.Green + ' РџРѕР»СѓС‡РёР» %i РїРёС‚РѕРЅРѕРІ Р·Р° %r'%(coins_value,origin) + Color.END)
def user_message_check(user_id,full_name_json,event_text):
    now = datetime.datetime.now()
    try:
        data.execute('''SELECT * FROM users WHERE user_id = %i'''%user_id)
        coins_value = data.fetchall()[0][9]
        return print(Color.Red + '[' + str(user_id) + ']' + '[' + full_name_json + ']' + '[' + str(now.day) + '.' + str(now.month) + ' ' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second) + ']' + '[' + str(coins_value) + ']' + Color.END + ' ' + Color.Blue + event_text + Color.END)
    except: pass
def user_buyed_script(user_id,full_name_json,buyed_script_id):
    now = datetime.datetime.now()
    try:
        data.execute('''SELECT * FROM users WHERE user_id = %i'''%user_id)
        coins_value = data.fetchall()[0][9]
        print(Color.Magenta + '[' + str(user_id) + ']' + '[' + full_name_json + ']' + '[' + str(now.day) + '.' + str(now.month) + ' ' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second) + ']' + '[' + str(coins_value) + ']' + Color.END + ' ' + Color.UNDERLINE + 'РљСѓРїРёР» СЃРєСЂРёРїС‚ РЅРѕРјРµСЂ ' + str(buyed_script_id) + Color.END)
    except: pass