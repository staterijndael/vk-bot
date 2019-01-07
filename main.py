# -*- coding: utf8 -*-
from connect import *
import math
import time
from console import coins_get,user_buyed_script
import re
def get_button(label, color):
    return {
        "action": {
            "type": "text",
            "label": label
        },
        "color": color
    }
BTN_NP = {
    "one_time": False,
    "buttons": [

        [get_button(label="Р’РїРµСЂРµРґ", color="positive"),
         get_button(label="РќР°Р·Р°Рґ", color="primary")],
         [get_button(label="Р’С‹Р№С‚Рё", color="negative")]

    ]
}
BTN_SELECT = {
    "one_time": False,
    "buttons": [

        [get_button(label="1", color="positive"),
        get_button(label="2", color="positive"),
        get_button(label="3", color="positive"),
        get_button(label="4", color="positive")],
        [get_button(label='Р’С‹Р№С‚Рё', color='negative')]

    ]
}
def pages_cooldown(user_id,increase = False):
    data.execute('''SELECT * FROM users WHERE user_id = %i'''% user_id)
    max_page = data.fetchall()[0][5]
    data.execute('''SELECT * FROM users WHERE user_id = %i'''% user_id)
    max_page_now = data.fetchall()[0][6]
    if max_page_now < max_page:
        if increase == False:
            max_page_now += 1
            data.execute('''UPDATE users SET `max_page_now` = %i WHERE user_id = %i'''%(max_page_now,user_id))
            connection_database.commit()
        return True
    else:
        cooldown_end = 3600 + time.time()
        data.execute('''SELECT * FROM users WHERE user_id = %i''' % user_id)
        if data.fetchall()[0][7] == 0:
            data.execute('''SELECT * FROM users WHERE user_id = %i'''% user_id)
            data.execute('''UPDATE users SET `cooldown_end` = %i WHERE user_id = %i'''%(math.floor(cooldown_end),user_id))
            connection_database.commit()
        data.execute('''SELECT * FROM users WHERE user_id = %i'''% user_id)
        cooldown_now = data.fetchall()[0][7]
        if (math.floor((cooldown_now) - (time.time())) / 60) >= 0:
            write_msg(user_id,'Р›РёРјРёС‚ РЅР° РїСЂРѕСЃРјРѕС‚СЂ СЃС‚СЂР°РЅРёС† РїСЂРµРІС‹С€РµРЅ!\nРџСЂРѕСЃРјРѕС‚СЂ Р±СѓРґРµС‚ РґРѕСЃС‚СѓРїРµРЅ С‡РµСЂРµР·: %i:%i'%(math.floor((cooldown_now) - (time.time()))/60,(((cooldown_now - time.time())/60 - math.floor(((cooldown_now - time.time()))/60))*60)),BTN_NP)
            return False
        else:
            data.execute('''SELECT * FROM users WHERE user_id = %i''' % user_id)
            status_page = data.fetchall()[0][3]
            if status_page < len(ifs_fetched)-1:
                data.execute('''SELECT * FROM users WHERE user_id = %i''' % user_id)
                coins_value = data.fetchall()[0][9]
                new_coins_value = coins_value + 20
                data.execute('''UPDATE users SET coins = %i WHERE user_id = %i''' % (new_coins_value, user_id))
                connection_database.commit()
                data.execute('''UPDATE users SET max_page_now = %i,cooldown_end = %i WHERE user_id = %i''' % (0, 0, user_id))
                connection_database.commit()
                data.execute('''SELECT * FROM users WHERE user_id = %i''' % user_id)
                new_status_page = status_page + 1
                data.execute('''UPDATE users SET "status_page_ifs" = %i WHERE "user_id" = ?''' % new_status_page,[(user_id)])
                connection_database.commit()
                try:
                    data.execute('''SELECT * FROM 'users' WHERE user_id = %i''' % user_id)
                    status_page = data.fetchall()[0][3]
                except Exception as e:
                    print(e.__traceback__)
                coins_get(user_id, full_name_json , 20, 'РїСЂРѕСЃРјРѕС‚СЂ СЃС‚СЂР°РЅРёС†',BTN_NP)
                time.sleep(4)
                write_msg(event.user_id, ifs_fetched[status_page][2], BTN_NP)
            else:
                coins_get(user_id, full_name_json, 20, 'РїСЂРѕСЃРјРѕС‚СЂ СЃС‚СЂР°РЅРёС†')
                time.sleep(4)
                write_msg(event.user_id, 'Р’С‹ РЅР° РїРѕСЃР»РµРґРЅРµР№ СЃС‚СЂР°РЅРёС†Рµ!')
            return False


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            user_id = event.user_id
            request_nickname = get_nicname(user_id).json()
            firstname_json = request_nickname['response'][0]['first_name']
            lastname_json = request_nickname['response'][0]['last_name']
            full_name_json = firstname_json + ' ' + lastname_json
            from console import user_message_check, new_user
            user_message_check(user_id,full_name_json,request)
            try:
                data.execute('''SELECT * FROM users WHERE user_id = %i'''%user_id)
                if_now_page = data.fetchall()[0][2]
                data.execute('''SELECT * FROM users WHERE user_id = %i'''%user_id)
                if_now_stage = data.fetchall()[0][4]
                data.execute('''SELECT * FROM 'ifs' WHERE stage = %i AND page = %i'''%(if_now_stage,if_now_page))
                ifs_fetched = data.fetchall()
                data.execute('''SELECT * FROM 'users' WHERE user_id = %i'''%user_id)
                status_page = data.fetchall()[0][3]
            except: pass
            data.execute('''SELECT * FROM 'stages' WHERE `stage` = "0" AND `page` = "0"''')
            stages_fetched = data.fetchall()
            if request.lower() == 'РЅР°С‡Р°С‚СЊ':
                data.execute('''SELECT * FROM 'users' WHERE user_id = %i'''%user_id)
                if len(data.fetchall()) == 0:
                    data.execute('''INSERT INTO 'users'(user_id,user_name,status_page_stage,status_page_ifs,stage,max_pages,max_page_now,cooldown_end,max_ifs_page_synt,coins,max_ifs_page_mod) VALUES (?,?,?,?,?,?,?,?,?,?,?)''',(user_id,full_name_json,0,0,0,10,0,0,0,0,0))
                    connection_database.commit()
                    write_msg(event.user_id, stages_fetched[0][2], BTN_SELECT)
                    new_user(user_id,full_name_json)
            elif request == 'Р’РїРµСЂРµРґ':
                data.execute('''SELECT * FROM 'users' WHERE user_id = %i''' % user_id)
                max_ifs_page_synt = data.fetchall()[0][8]
                data.execute('''SELECT * FROM 'users' WHERE user_id = %i''' % user_id)
                max_ifs_page_mod = data.fetchall()[0][10]
                if status_page < len(ifs_fetched)-1:
                    if pages_cooldown(user_id,'increase'):
                        new_status_page = status_page + 1
                        data.execute('''UPDATE users SET "status_page_ifs" = %i WHERE "user_id" = ?'''%new_status_page,[(user_id)])
                        connection_database.commit()
                        try:
                            data.execute('''SELECT * FROM 'users' WHERE user_id = %i''' % user_id)
                            status_page = data.fetchall()[0][3]
                        except Exception as e:
                            print(e.__traceback__)
                        write_msg(event.user_id,ifs_fetched[status_page][2],BTN_NP)
                else:
                    write_msg(event.user_id,'Р’С‹ РЅР° РїРѕСЃР»РµРґРЅРµР№ СЃС‚СЂР°РЅРёС†Рµ!')
                data.execute('''SELECT * FROM 'users' WHERE user_id = %i''' % user_id)
                stage = data.fetchall()[0][4]
                data.execute('''SELECT * FROM 'users' WHERE user_id = %i''' % user_id)
                page = data.fetchall()[0][2]
                if stage == 2 and page == 2:
                    if status_page > max_ifs_page_synt :
                        sql = '''SELECT * FROM users WHERE user_id = %i'''%user_id
                        data.execute(sql)
                        database_fetch = data.fetchall()[:]
                        last_id = database_fetch[0][8]
                        last_id = last_id + 1
                        data.execute('''UPDATE users SET max_ifs_page_synt = %i WHERE user_id = %i'''%(last_id,user_id))
                        connection_database.commit()
                        pages_cooldown(user_id)
                elif stage == 3 and page == 2:
                    if status_page > max_ifs_page_mod :
                        sql = '''SELECT * FROM users WHERE user_id = %i'''%user_id
                        data.execute(sql)
                        database_fetch = data.fetchall()[:]
                        last_id = database_fetch[0][8]
                        last_id = last_id + 1
                        data.execute('''UPDATE users SET max_ifs_page_mod = %i WHERE user_id = %i'''%(last_id,user_id))
                        connection_database.commit()
                        pages_cooldown(user_id)
            elif request == 'РќР°Р·Р°Рґ':
                if pages_cooldown(user_id,'increase'):
                    if status_page >= 1:
                        new_status_page = status_page - 1
                        data.execute('''UPDATE users SET "status_page_ifs" = %i WHERE "user_id" = ?'''%new_status_page,[(user_id)])
                        connection_database.commit()
                        try:
                            data.execute('''SELECT * FROM 'users' WHERE user_id = %i''' % user_id)
                            status_page = data.fetchall()[0][3]
                        except:
                            pass
                        write_msg(event.user_id,ifs_fetched[status_page][2],BTN_NP)
                    else:
                        write_msg(event.user_id, 'Р’С‹ РЅР° РїРµСЂРІРѕР№ СЃС‚СЂР°РЅРёС†Рµ!')
            elif request == '1' or request == '2' or request == '3' or request == '4':
                try:
                    data.execute('''SELECT * FROM 'users' WHERE user_id = %i''' % user_id)
                    stage = data.fetchall()[0][4]
                    data.execute('''SELECT * FROM 'users' WHERE user_id = %i''' % user_id)
                    page = data.fetchall()[0][2]

                    if request == '1':
                        request = 1
                    elif request == '2':
                        request = 2
                    elif request == '3':
                        request = 3
                    elif request == '4':
                        request = 4
                    new_stage = stage + request
                    new_page = page + 1
                    data.execute('''UPDATE 'users' SET `status_page_stage` = %i, `stage` = %i WHERE user_id = %i''' %(new_page, new_stage, user_id))
                    connection_database.commit()
                    data.execute('''SELECT * FROM 'users' WHERE user_id = %i''' % user_id)
                    stage = data.fetchall()[0][4]
                    data.execute('''SELECT * FROM 'users' WHERE user_id = %i''' % user_id)
                    page = data.fetchall()[0][2]
                    data.execute('''SELECT * FROM `stages` WHERE page = %i AND stage = %i'''%(page,stage))
                    stage_text = data.fetchall()[0][2]
                try:
                    if stage_text != 'IFS':
                            data.execute('''SELECT * FROM 'stages' WHERE `page` = %i AND `stage` = %i'''%(new_page,new_stage))
                            write_msg(event.user_id,data.fetchall()[0][2],BTN_SELECT)
                    else:
                        if pages_cooldown(user_id,'increase'):
                            data.execute('''SELECT * FROM users WHERE user_id = %i'''%user_id)
                            if_now_page = data.fetchall()[0][2]
                            data.execute('''SELECT * FROM users WHERE user_id = %i'''%user_id)
                            if_now_stage = data.fetchall()[0][4]
                            data.execute('''SELECT * FROM `ifs` WHERE stage = %i AND page = %i'''%(if_now_stage,if_now_page))
                            write_msg(event.user_id,data.fetchall()[0][2],BTN_NP)
                except: pass
                try:
                    if (stage == 4 and page == 2): # Р’С‹СЃС‚Р°РІР»РµРЅРЅС‹Рµ СЃРєСЂРёРїС‚С‹
                            data.execute('''SELECT * FROM market WHERE status = "accepted"''')
                            accepted_script = data.fetchall()
                            if accepted_script:
                                i = 0
                                accepted_script_text = ''
                                for accepted in accepted_script:
                                    accepted_script_text += (str(i + 1) + '|' + ' РќР°Р·РІР°РЅРёРµ СЃРєСЂРёРїС‚Р°: ' + str(
                                        accepted_script[i][1]) + '|' + ' РћРїРёСЃР°РЅРёРµ С‚РѕРІР°СЂР°: ' + str(
                                        accepted_script[i][2]) + '|' + ' Р¦РµРЅР°: ' + str(
                                        accepted_script[i][3]) + ' РїРёС‚РѕРЅРѕРІ' + '\n\n')
                                    i += 1
                                write_msg(user_id,accepted_script_text + '\n _____________________________________________________________\n РґР»СЏ РїРѕРєСѓРїРєРё СЃРєСЂРёРїС‚Р°, РІРІРµРґРёС‚Рµ "buy РЅРѕРјРµСЂ СЃРєСЂРёРїС‚Р°"')
                            else:
                                write_msg(user_id, 'Р’ РґР°РЅРЅС‹Р№ РјРѕРјРµРЅС‚ РЅРµС‚ СЃРєСЂРёРїС‚РѕРІ РЅР° РїСЂРѕРґР°Р¶Рµ')
                except:
                    pass
                try:
                    if (stage == 5 and page == 2): # РљСѓРїР»РµРЅРЅС‹Рµ СЃРєСЂРёРїС‚С‹
                        data.execute('''SELECT * FROM buyed_scripts WHERE buyed_user_id = %i'''%user_id)
                        buyed_script_person = data.fetchall()
                        if buyed_script_person:
                            i = 0
                            buyed_script_person_text = ''
                            for buyed_script_person_one in buyed_script_person:
                                buyed_script_person_text += 'РќР°Р·РІР°РЅРёРµ: ' + str(buyed_script_person[i][2])  + '\n' + ' РћРїРёСЃР°РЅРёРµ: ' + str(buyed_script_person[i][3])  + '\n' + ' Р¦РµРЅР°: ' + str(buyed_script_person[i][4]) + " РїРёС‚РѕРЅРѕРІ"  + '\n' + ' РЎСЃС‹Р»РєР°: ' + str(buyed_script_person[i][6] + '\n\n')
                                i += 1
                            write_msg(user_id,buyed_script_person_text)
                        else: write_msg(user_id,"РЈ РІР°СЃ РЅРµС‚ РєСѓРїР»РµРЅРЅС‹С… СЃРєСЂРёРїС‚РѕРІ")
                except: pass
                if (stage == 4 and page == 1): # РЎС‚Р°С‚РёСЃС‚РёРєР°
                    data.execute('''SELECT * FROM users WHERE user_id = %i'''%user_id)
                    all_info = data.fetchall()
                    stats = 'рџђ© Р�РјСЏ: ' + all_info[0][1] + '\n' + 'рџ“њРЎС‚СЂР°РЅРёС† РїСЂРѕСЃРјРѕС‚СЂРµРЅРѕ: ' + str((all_info[0][8] + all_info[0][10])) + '\n' + 'рџђЌР‘Р°Р»Р°РЅСЃ: ' + str(all_info[0][9]) + ' РїРёС‚РѕРЅРѕРІ'
                    write_msg(user_id,stats)
                #if (stage == 7 and page == 2): # РџР°РЅРµР»СЊ СѓРїСЂР°РІР»РµРЅРёСЏ СЃРІРѕРёРјРё СЃРєСЂРёРїС‚Р°РјРё
            if request == 'admin' and user_id == 296346714:
                data.execute('''SELECT * FROM market WHERE status = "pending"''')
                pendings = data.fetchall()
                if pendings:
                    pending_text = ''
                    i = 0
                    for pending in pendings:
                        pending_text += (str(pendings[i][6])+ '|' + 'User_id: ' + str(pendings[i][0]) + '|' + ' Name: ' + str(pendings[i][1]) + '|' + ' Description: ' + str(pendings[i][2]) + '|' + ' Price: ' + str(pendings[i][3]) + '|' + ' Link:' + str(pendings[i][5]) + '\n\n')
                        i += 1
                    write_msg(user_id,pending_text)
                else: write_msg(user_id,'РќРµС‚ РЅРѕРІС‹С… Р·Р°СЏРІРѕРє!')
            try:
                if re.findall(r'^\w+', str(request))[0] == 'accept' and user_id == 296346714:
                    accepted_number = re.findall(r'\d+', request)[0]
                    data.execute('''SELECT * FROM market WHERE status = "accepted"''')
                    all_scripts = data.fetchall()
                    if all_scripts:
                        ids = []
                        i = 0
                        for script in all_scripts:
                            ids.append(all_scripts[i][6])
                            i += 1
                        new_id = max(ids) + 1
                        data.execute('''SELECT * FROM market WHERE id = %i AND status = "pending"''' %int(accepted_number))
                        owner_id = data.fetchall()[0][0]
                        data.execute('''UPDATE market SET status = 'accepted',id = %i WHERE id = %i AND status = "pending"'''%(new_id,int(accepted_number)))
                        connection_database.commit()
                        write_msg(user_id, 'Р—Р°СЏРІРєР° РїРѕРґ РЅРѕРјРµСЂРѕРј %r РїСЂРёРЅСЏС‚Р°'%(str(accepted_number)))
                        write_msg(owner_id,'Р’Р°С€Р° Р·Р°СЏРІРєР° Р±С‹Р»Р° РїСЂРёРЅСЏС‚Р°!')
                    else:
                        data.execute('''SELECT * FROM market WHERE id = %i AND status = "pending"''' %int(accepted_number))
                        owner_id = data.fetchall()[0][0]
                        data.execute('''UPDATE market SET status = 'accepted',id = %i WHERE id = %i AND status = "pending"'''%(1,int(accepted_number)))
                        connection_database.commit()
                        write_msg(user_id, 'Р—Р°СЏРІРєР° РїРѕРґ РЅРѕРјРµСЂРѕРј %r РїСЂРёРЅСЏС‚Р°'%(str(accepted_number)))
                        write_msg(owner_id,'Р’Р°С€Р° Р·Р°СЏРІРєР° Р±С‹Р»Р° РїСЂРёРЅСЏС‚Р°!')
            except: pass
            try:
                if re.findall(r'^\w+', str(request))[0] == 'deny' and user_id == 296346714:
                    deny_script_number = re.findall(r'&lt;(.+?)&gt;', request);
                    print(deny_script_number)
                    data.execute('''SELECT * FROM market WHERE id = %i'''%int(deny_script_number[0]))
                    owner_id = data.fetchall()[0][0]
                    data.execute('''DELETE FROM market WHERE id = %i''' %int(deny_script_number[0]))
                    connection_database.commit()
                    write_msg(user_id,'Р’С‹ РѕС‚РєР»РѕРЅРёР»Рё Р·Р°СЏРІРєСѓ РЅРѕРјРµСЂ %i'%int(deny_script_number[0]))
                    write_msg(owner_id,'Р’Р°С€Р° Р·Р°СЏРІРєР° РЅР° РґРѕР±Р°РІР»РµРЅРёРµ СЃРєСЂРёРїС‚Р° Р±С‹Р»Р° РѕС‚РєР»РѕРЅРµРЅР°. РџСЂРёС‡РёРЅР°: %r'%deny_script_number[1])
            except: pass
            try:
                if re.findall(r'^\w+', str(request))[0] == 'buy':
                    buy_number = re.findall(r'\d+', request)[0]
                    data.execute("""SELECT * FROM market WHERE status = 'accepted' AND id = %i"""%(int(buy_number)))
                    buyed_script = data.fetchall()
                    data.execute('''SELECT * FROM users WHERE user_id = %i'''%user_id)
                    coins = data.fetchall()[0][9]
                    if coins >= buyed_script[0][3]:
                        new_coins = coins - buyed_script[0][3]
                        data.execute('''UPDATE users SET coins = %i WHERE user_id = %i'''%(new_coins,user_id))
                        data.execute('''INSERT INTO buyed_scripts(buyed_user_id,creater_user_id,name,description,price,status,link,id) VALUES (?,?,?,?,?,?,?,?)''',(user_id,buyed_script[0][0],buyed_script[0][1],buyed_script[0][2],buyed_script[0][3],buyed_script[0][4],buyed_script[0][5],buyed_script[0][6]))
                        data.execute('''SELECT * FROM users WHERE user_id = %i'''%buyed_script[0][0])
                        script_creater_coins = data.fetchall()[0][9]
                        data.execute('''UPDATE users SET coins = %i WHERE user_id =%i'''%(int(script_creater_coins + buyed_script[0][3]),buyed_script[0][0]))
                        connection_database.commit()
                        write_msg(buyed_script[0][0],'Р’С‹ РїРѕР»СѓС‡РёР»Рё %i РїРёС‚РѕРЅРѕРІ Р·Р° РїСЂРѕРґР°Р¶Сѓ СЃРєСЂРёРїС‚Р° %r. РџРѕР·РґСЂР°РІР»СЏРµРј!'%(buyed_script[0][3],buyed_script[0][1]))
                        write_msg(user_id,'Р’С‹ РєСѓРїРёР»Рё СЃРєСЂРёРїС‚ %r Р·Р° %i РїРёС‚РѕРЅРѕРІ. РЎСЃС‹Р»РєР°: %r\nР’С‹ РІСЃРµРіРґР° СЃРјРѕР¶РµС‚Рµ РЅР°Р№С‚Рё СЌС‚РѕС‚ СЃРєСЂРёРїС‚ РІ СЂР°Р·РґРµР»Рµ "РљСѓРїР»РµРЅРЅС‹Рµ СЃРєСЂРёРїС‚С‹"'%(buyed_script[0][1],buyed_script[0][3],buyed_script[0][5]))
                        user_buyed_script(user_id,full_name_json,buy_number)
                    else: write_msg(user_id,'РЈ РІР°СЃ РЅРµРґРѕСЃС‚Р°С‚РѕС‡РЅРѕ СЃСЂРµРґСЃС‚РІ!')
            except: pass
            try:
                if re.findall(r'^\w+', str(request))[0] == 'add_script':
                    deny_script_number = re.findall(r'&lt;(.+?)&gt;', request);
                    data.execute('''SELECT * FROM market WHERE status = "pending"''')
                    all_scripts = data.fetchall()
                    try:
                        if all_scripts:
                            ids = []
                            i = 0
                            for script in all_scripts:
                                ids.append(all_scripts[i][6])
                                i += 1
                            new_id = max(ids) + 1
                            data.execute('''INSERT INTO market(user_id,name,description,price,status,link,id) VALUES (?,?,?,?,?,?,?)''',(user_id,deny_script_number[0],deny_script_number[1],deny_script_number[2],'pending',deny_script_number[3],new_id))
                        else: data.execute('''INSERT INTO market(user_id,name,description,price,status,link,id) VALUES (?,?,?,?,?,?,?)''',(user_id,deny_script_number[0],deny_script_number[1],deny_script_number[2],'pending',deny_script_number[3],1))
                        connection_database.commit()
                        write_msg(user_id,'Р’Р°С€Р° Р·Р°СЏРІРєР° СѓСЃРїРµС€РЅРѕ РїСЂРёРЅСЏС‚Р° РЅР° РїСЂРѕРІРµСЂРєСѓ! РћРЅР° Р±СѓРґРµС‚ РїСЂРѕРІРµСЂРµРЅР° РІ С‚РµС‡РµРЅРёРё 24 С‡Р°СЃРѕРІ. РџРѕСЃР»Рµ РїСЂРѕРІРµСЂРєРё РјС‹ РѕР±СЊСЏР·Р°С‚РµР»СЊРЅРѕ РѕРїРѕРІРµСЃС‚РёРј РІР°СЃ Рѕ СЂРµР·СѓР»СЊС‚Р°С‚Рµ.')
                    except: write_msg(user_id,'Р’Р°С€Р° Р·Р°СЏРІРєР° Р·Р°РїРѕР»РЅРµРЅРЅР° РЅРµРїСЂР°РІРёР»СЊРЅРѕ!')
            except: pass
            if request == 'Р’С‹Р№С‚Рё':
                try:
                    data.execute('''UPDATE users SET `status_page_stage` = 0, `stage` = 0, `status_page_ifs` = 0 WHERE user_id = %i'''%user_id)
                    connection_database.commit()
                    write_msg(event.user_id,stages_fetched[0][2],BTN_SELECT)
                except: pass