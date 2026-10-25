from app import BOT_TOKEN, API_TOKEN, API_BASE_URL, API_KEY, SEARCH_ENGINE_ID, CNDK_API_BASE, CNDK_API_KEY, CNDK_API_KEY2, API5_URL, API5_KEY, PALLY_SHOP_ID, PALLY_TOKEN
from app import GMAIL_TOKEN
from app import SWITCH_POPUG_PNG, BAD_POPUG_PNG, POPUGEI_JPG, PHOTO_PATCH, BREAKDANCE_VIDEO
from app import POPUSKI_DATA_SHELVE, PARTNERS_DATA_SHELVE, MDB_DATA_SHELVE, MDB_RESERV_DATA_SHELVE, MDB_LOCO_DATA_SHELVE, MDB_LOCO_RESERV_DATA_SHELVE, ADMIN_DATA_SHELVE, PROMOS_DATA_SHELVE, WATA_DATA_SHELVE


HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}




##############



##############


for_reports='5266773307'

ids=[
    '832182441',
    '588293874',
    '5266773307',
    '1676019994',
     ]
auth={
    '832182441':'👤 Илья (@bingupluss)',
    '588293874':'👤 Даниил (@lahtion0v)',
    '1676019994':'👤 Леонид (@melnikovlnd)',
    }

superids=[
    '832182441',
    '588293874',
    '5266773307',
     ]



import telebot
from telebot import types
from datetime import datetime,date
import time
import requests
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from xvfbwrapper import Xvfb
import re
import shelve
import random
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import httplib2 
from io import BytesIO
import subprocess
import os
import traceback
from datetime import datetime, timedelta
import psycopg2
import json
from datetime import datetime
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
import requests
import random
from io import BytesIO
import requests
import json
from typing import Optional, Dict
import html
import requests
from bs4 import BeautifulSoup
import re
import math
import requests
import json

import json
import re
import telebot
from telebot import types
from io import BytesIO

import secrets

import threading
import time
import schedule
from datetime import datetime



vdisplay = Xvfb()
vdisplay.start()

# === BIG WALK DISCOUNT ===
BIG_WALK_KEYWORD = "big walk"           # часть названия для поиска (lowercase)
NSO_1M_ORIG_PRICE = 399                 # оригинальная цена NSO 1 мес (для идентификации)
NSO_1M_DISC_PRICE = 299                 # цена со скидкой
BIG_WALK_PROMO_END = datetime(2026, 8, 13, 23, 59, 59)  # до 13.08.2026 включительно
BIG_WALK_DISCOUNT_DAYS = 7              # скидка висит 7 дней после покупки
# =========================


user_data={}




def send_report(component: str, report: str, timestamp: datetime = None):
    """Отправляет отчёт о состоянии парсера"""
    
    headers = {
        "X-API-Key": API5_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "component": component,  # например: "parser_ozon"
        "report": report,        # например: "✅ Парсинг завершён, 150 товаров"
        "timestamp": timestamp.isoformat() if timestamp else None
    }
    
    # Убираем None-поля
    payload = {k: v for k, v in payload.items() if v is not None}
    
    try:
        response = requests.post(API5_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()
        print(f"✅ Отчёт отправлен: {result['message']}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка отправки: {e}")
        return False

        

class Bot:
    def __init__(self):
        token = BOT_TOKEN # токен
        self.alarm=4*60*60 # количество секунд между обновлениями базы валют (сейчас 4 часа)
        self.alarm2=0
        self.alarm3=3
        
        self.routes=dict()# текущие пользователи и их переменные
        self.time=0 # время последнего обновления базы валют
        self.courses=dict() # текущие курсы валют
        self.my_bot=telebot.TeleBot(token)
        self.create_button()
        self.ids=ids
        self.superids=superids
        self.auth=auth

        self.price_settings=[
                [7,299],
                [18,349],
                [-1,399],
                [-2,1.11],
                [-3,100]
            ]
        
        db=shelve.open(MDB_DATA_SHELVE)
        self.routes=db.get('routes',dict())
        self.users=db.get('users',dict())
        self.lgames=db.get('lgames',dict())
        self.dgames=db.get('dgames',list())
        self.price_settings=db.get('price_settings',[
                [7,299],
                [18,349],
                [-1,399],
                [-2,1.11],
                [-3,100]
            ])
        self.price_settings2=db.get('price_settings2',85)
        self.favo=db.get('favo',{})
        self.favo_list=db.get('favo_list',[])
        self.favo_price=db.get('favo_price',{})
        self.favo_time=db.get('favo_time',{})
        self.users_time=db.get('users_time',{})
        self.num=db.get('num',51)
        self.loco_dct=db.get('loco_dct',{})
        self.ban_users=db.get('ban_users',[])
        self.auth=db.get('auth',auth)
        self.ids=db.get('ids',ids)
        self.great_dic=db.get('great_dic',{})
        self.great_box={} #db.get('great_box',{})
        self.cdc_id=db.get('cdc_id',8900000)
        self.cdc_orders=db.get('cdc_orders',{})
        self.cdc_koef=db.get('cdc_koef',1.2)
        self.brl50=db.get("brl50",9.5)
        self.yen500=db.get("yen500",370)
        self.yen1000=db.get("yen1000",700)

        self.partners=db.get("partners",0)
        self.closed_popups=db.get("closed_popups",[])
        db.close()
        
        db=shelve.open(ADMIN_DATA_SHELVE)
        self.auth=db.get('auth',auth)
        self.ids=db.get('ids',ids)
        
        db.close()
        
        db=shelve.open(MDB_LOCO_DATA_SHELVE)
        self.new_loco_dct=db.get('new_loco_dct',{})
        self.loco_list=db.get('loco_list',[])
        self.stack=db.get("stack",[])
        db.close()
        self.rassu_photo=-1
        self.rassu_photo2=-1
        self.rassu_message=''
        self.tlimit=48*60*60
        self.vars={}

      #  self.stack=[]
        self.fix_gms={}
        
      
        self.user_requests = {}
        self.MAX_REQUESTS = 5  # Максимум запросов в секунду
        self.BAN_TIME = 300    # Время бана в секундах
        

        self.cdc_hand={}

        try:
            self.reload_popup()
            
        except:
            
            self.popups={} # {}
            self.subs={}
            self.popups_codes={}
            self.my_bot.send_message(for_reports,traceback.format_exc())

        db=shelve.open(POPUSKI_DATA_SHELVE)
        self.popuski=db.get("popuski",{}) # "id":{"key","percent"}
        db.close()

        db=shelve.open(PROMOS_DATA_SHELVE)
        self.promos = db.get("promos", {}) # Хранилище промо-ссылок
        db.close()
        
        self.get_courses()

        
    def reload_popup(self):
        self.my_bot.send_message(for_reports,"Загрузка кодов")
        self.popups={} # {}
        self.subs={} # {}
        self.popups_codes={} # []
        mail='https://console.developers.google.com/cloud-resource-manager'
        token2=GMAIL_TOKEN
        CREDENTIALS_FILE = token2
        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
        service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API
        driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
        spreadsheetId ="1ep-NsK4-d1M13KrnXrLglPFK8-rppU2RZQrc0xJK8rk"
        results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                                     ranges = ["Sheet1!A2:F100"], 
                                                     valueRenderOption = 'FORMATTED_VALUE',  
                                                     dateTimeRenderOption = 'FORMATTED_STRING').execute() 
        sheet_values = results['valueRanges'][0]['values']
        for arr in sheet_values:
            while len(arr)<6:
                arr.append("")
            rubi=10
            try:
                rnb = float(arr[5])
                rnb = rnb * self.courses["Russian Ruble"] 
                rubi=rnb
            except:
                pass

            dct={"Артикул":arr[0],"Наименование":arr[1],"Регион":arr[2],"Сумма пополнения":arr[3],"Цена в рублях":arr[4],"Себестоимость в рублях": int(rubi)}
            self.popups[arr[0]]=dct

        results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                                     ranges = ["Sheet2!A2:F100"], 
                                                     valueRenderOption = 'FORMATTED_VALUE',  
                                                     dateTimeRenderOption = 'FORMATTED_STRING').execute() 
        sheet_values = results['valueRanges'][0]['values']
        for arr in sheet_values:
            while len(arr)<5:
                arr.append("")
            
            rubi=10
            try:
                rnb = float(arr[3])
                rnb = rnb * self.courses["Russian Ruble"] 
                rubi=rnb
            except:
                pass
            dct={"Артикул":arr[0],"Наименование":arr[1],"Цена в рублях":arr[2],"Себестоимость в рублях":int(rubi)}
            self.subs[arr[0]]=dct
        results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                                     ranges = ["Sheet3!A2:B1000"], 
                                                     valueRenderOption = 'FORMATTED_VALUE',  
                                                     dateTimeRenderOption = 'FORMATTED_STRING').execute() 
        sheet_values = results['valueRanges'][0]['values']
        varr=[]
        for arr in sheet_values:
            if len(arr)>=2:
                if arr[1] not in self.closed_popups:
                    b=self.popups_codes.get(arr[0],[])
                    b.append(arr[1])
                    self.popups_codes[arr[0]]=b.copy()
                    if [arr[0],arr[1]] not in varr:
                        varr.append([arr[0],arr[1]])
                    
        service.spreadsheets().values().clear(spreadsheetId = spreadsheetId,range="Sheet3!A2:B1000").execute()
        results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
    "valueInputOption": "USER_ENTERED", 
    "data": [
        {"range": "Sheet3!A2:B1000",
         "majorDimension": "ROWS",   
         "values": varr}
    ]}).execute()

        self.check_popups()
        self.my_bot.send_message(for_reports,"Загрузка кодов завершена")
        self.my_bot.send_message(for_reports,str(self.subs))

    def check_popups(self):
        st=""
        for key in self.popups:
            if len(self.popups_codes.get(key,[]))<=3:
                st+=f"по артикулу {key} осталось {len(self.popups_codes.get(key,[]))} кодов\n"
        for key in self.subs:
            if len(self.popups_codes.get(key,[]))<=3:
                st+=f"по артикулу {key} осталось {len(self.popups_codes.get(key,[]))} кодов\n"

        if st!="":
            msg="Внимание!! В таблице кодов:\n"+st
            for key in self.ids:
                try:
                    pass
                    self.my_bot.send_message(key,msg)
                except:
                    pass
      

    def check_rate_limit(self, user_id):
        current_time = time.time()
        
        if user_id in self.user_requests:
            # Удаляем старые записи
            self.user_requests[user_id] = [
                t for t in self.user_requests[user_id] 
                if current_time - t < 1
            ]
            
            if len(self.user_requests[user_id]) >= self.MAX_REQUESTS:
                return False
            
            self.user_requests[user_id].append(current_time)
        else:
            self.user_requests[user_id] = [current_time]
        
        return True

       # print(self.auth)

    def batya_report(self,caption,user):
        username=self.auth.get(str(user),str(user))
        caption=f"Пользователь {username}: "+caption
        self.my_bot.send_message('832182441',caption)
        self.my_bot.send_message(for_reports,caption)

    def trim_game_title(self,title, max_length=30):
        if len(title) > max_length:
            return title[:max_length - 3] + '...'
        return title

    def build_keyboard(self,games_list, current_page,message):
        """
        Создает инлайн-клавиатуру для списка игр с пагинацией.
        
        :param games_list: Полный список найденных игр
        :param current_page: Текущая страница (начинается с 0)
        :return: Объект InlineKeyboardMarkup
        """
        keyboard = types.InlineKeyboardMarkup(row_width=1)  
        items_per_page = 5
        start_index = current_page * items_per_page
        end_index = start_index + items_per_page
        games_on_page = games_list[start_index:end_index]
        iii=start_index+1
        try:
            message_id=message.id
        except:
            message_id=0
        # Добавляем кнопки с играми для текущей страницы
        for game in games_on_page:
            # game - это словарь, например {'name': 'Cyberpunk 2077', 'url': 'https://store...', 'price': '1999 руб.'}
            btn_text = f"{iii}. {self.trim_game_title(game['name'])} - {game['price']} ₽"
            if game['old_price']!=-1: btn_text="💸 "+btn_text
            keyboard.add(types.InlineKeyboardButton(text=btn_text, callback_data=f'selectgame_{str(iii)}${message_id}'))

            iii+=1

        # Добавляем кнопки навигации (в одну строку)
        nav_buttons = []
        
        # Кнопка "Назад"
        if current_page > 0:
            # Используем callback_data для передачи номера предыдущей страницы
            nav_buttons.append(types.InlineKeyboardButton(text="⬅️ Назад", callback_data=f"page_{current_page - 1}"))
        
        # Индикатор страницы (например, "2/5")
        total_pages = (len(games_list) - 1) // items_per_page + 1
        page_indicator = types.InlineKeyboardButton(text=f"{current_page + 1}/{total_pages}", callback_data="ignore_123")
        nav_buttons.append(page_indicator)
        
        # Кнопка "Вперед"
        if end_index < len(games_list):
            # Используем callback_data для передачи номера следующей страницы
            nav_buttons.append(types.InlineKeyboardButton(text="Вперед ➡️", callback_data=f"page_{current_page + 1}"))
        
        # Добавляем строку навигации, только если есть кнопки
        if nav_buttons:
            keyboard.row(*nav_buttons)
        
        return keyboard

    def convert_entities_to_html(self,text, entities):
        """
        Преобразует текст и список entities от Telegram Bot API в HTML строку.
        Работает с объектами telebot.types.MessageEntity.
        """
        if not text:
            return ""
        
        # Если entities нет или пустой список, просто экранируем текст
        if not entities:
            return html.escape(text)

        # 1. Сортируем entities по смещению (offset)
        # Используем атрибут .offset вместо ['offset']
        sorted_entities = sorted(entities, key=lambda e: e.offset)
        
        html_result = []
        last_pos = 0
        
        for ent in sorted_entities:
            start = ent.offset
            end = start + ent.length
            
            # Текст ДО этой сущности (экранируем его!)
            if start > last_pos:
                plain_text = text[last_pos:start]
                html_result.append(html.escape(plain_text))
            
            # Текст ВНУТРИ сущности (экранируем его!)
            inner_text = text[start:end]
            escaped_inner = html.escape(inner_text)
            
            tag_open = ""
            tag_close = ""
            
            t = ent.type  # Используем .type вместо ['type']
            
            # Определяем теги
            if t == 'bold': 
                tag_open, tag_close = "<b>", "</b>"
            elif t == 'italic': 
                tag_open, tag_close = "<i>", "</i>"
            elif t == 'underline': 
                tag_open, tag_close = "<u>", "</u>"
            elif t == 'strikethrough': 
                tag_open, tag_close = "<s>", "</s>"
            elif t == 'code': 
                tag_open, tag_close = "<code>", "</code>"
            elif t == 'pre': 
                tag_open, tag_close = "<pre>", "</pre>"
            elif t == 'url': 
                # Обычная ссылка: текст становится кликабельным
                url = html.escape(inner_text)
                tag_open, tag_close = f'<a href="{url}">', "</a>"
            elif t == 'text_link':
                # Скрытая ссылка: [текст](url)
                # Используем .url атрибут
                url = html.escape(ent.url) if ent.url else ""
                tag_open, tag_close = f'<a href="{url}">', "</a>"
            elif t == 'blockquote':
                # Цитата в Telegram HTML не поддерживается напрямую.
                # Заменяем на курсив или span с прозрачностью для визуального отличия.
                # Вариант 1: Просто курсив
                tag_open, tag_close = "<i>", "</i>"
                
                # Вариант 2: Более "цитатный" вид (серый курсив)
              #  tag_open = '<span style="opacity: 0.7; font-style: italic;">'
               # tag_close = '</span>'
            elif t == 'bot_command':
                # Команды просто текст
                html_result.append(escaped_inner)
                last_pos = end
                continue
            elif t == 'custom_emoji':
                # Кастомные эмодзи пока оставляем как текст, т.к. HTML не поддерживает ID
                html_result.append(escaped_inner)
                last_pos = end
                continue
                
            if tag_open:
                html_result.append(f"{tag_open}{escaped_inner}{tag_close}")
            
            last_pos = end
            
        # Остаток текста после последней сущности
        if last_pos < len(text):
            plain_text = text[last_pos:]
            html_result.append(html.escape(plain_text))
            
        return "".join(html_result)
    



    def search_eshop_prices_games(self, query):
        """
        Поиск игр на eshop-prices.com
        Возвращает список: [{'name': str, 'image_url': str, 'url': str}, ...]
        """
        url = f"https://eshop-prices.com/games?q={requests.utils.quote(query)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            games = []
            
            # Ищем все элементы игр
            for item in soup.find_all('a', class_='games-list-item'):
                try:
                    # Название
                    title_elem = item.find('h5')
                    if not title_elem:
                        continue
                    name = title_elem.text.strip()
                    
                    # Ссылка
                    href = item.get('href', '')
                    full_url = f"https://eshop-prices.com{href}" if href.startswith('/') else href
                    
                    # Изображение - ищем в picture теге
                    img_url = None
                    
                    # Пробуем найти в picture > img
                    picture = item.find('picture')
                    if picture:
                        # Сначала ищем JPEG (самый совместимый)
                        jpeg_source = picture.find('source', type='image/jpeg')
                        if jpeg_source and jpeg_source.get('srcset'):
                            # Берем первую URL из srcset (без 2x)
                            img_url = jpeg_source['srcset'].split(',')[0].split()[0]
                        
                        # Если нет JPEG, берем webp
                        if not img_url:
                            webp_source = picture.find('source', type='image/webp')
                            if webp_source and webp_source.get('srcset'):
                                img_url = webp_source['srcset'].split(',')[0].split()[0]
                        
                        # Если нет source, берем img src
                        if not img_url:
                            img_tag = picture.find('img')
                            if img_tag and img_tag.get('src'):
                                img_url = img_tag['src']
                    
                    # Если нашли игру - добавляем
                    if img_url:
                        games.append({
                            'name': name,
                            'image_url': img_url,
                            'url': full_url
                        })
                        
                except Exception as e:
                    print(f"Ошибка парсинга игры: {e}")
                    continue
            
            return games[:10]  # Возвращаем топ-10
            
        except Exception as e:
            print(f"Ошибка поиска на eshop-prices: {e}")
            return []


    def google_api_download_image(self, url):
        """Скачивает изображение и возвращает файловый объект"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            
            return BytesIO(response.content)
        except Exception as e:
            print(f"Ошибка скачивания изображения: {e}")
            return None


        
    def handle_search(self,message,results,url_image="",user_idm=1,add_title=""):
        found_games = []

        for r in results:
            dct={}
            dct['name']=r[0]
            dct['price']=r[1]
            dct['old_price']=r[3]
            dct['valu']=r[2]
            found_games.append(dct)
        
        try:
            user_id = message.chat.id
        except:
            user_id=int(user_idm)
        user_data[user_id] = {
            "games_list": found_games,
            "current_page": 0
        }
        
        keyboard = self.build_keyboard(found_games, 0,message)
        caption = self.build_caption(found_games, 0,add_title=add_title)

        try:
            if found_games[0]['name'].lower() in ['comic book legends',"to leave"]:
                a=1/0
            if url_image=="":
                try:
                    # Поиск через CNDK API
                    search_url = f"{CNDK_API_BASE}api/v1/games"
                    params = {
                        'q': found_games[0]['name'],
                        'limit': 1
                    }
                    response = requests.get(search_url, params=params,
                                headers={"Authorization": "Bearer " + CNDK_API_KEY}, timeout=30)
                    response.raise_for_status()
                    data = response.json()

                    games = data.get('games', [])
                    if games and games[0].get('cover_url'):
                        my_popug = games[0]['cover_url']
                    else:
                        # Fallback на Google если игра не найдена
                        my_popug = self.google_api_search_images(found_games[0]['name']+" official game art")[0]["url"]
                        my_popug = self.google_api_download_image(my_popug)
                except:
                    # Fallback на Google при любой ошибке API
                    my_popug = self.google_api_search_images(found_games[0]['name']+" official game art")[0]["url"]
                    my_popug = self.google_api_download_image(my_popug)
            else:
                my_popug = url_image
            self.my_bot.send_photo(
                    chat_id=user_id,
                    photo=my_popug,  # Передаем файловый объект
                    caption=caption,
                    reply_markup=keyboard,
                    parse_mode='HTML'
                )
       #          "<b>Жирный текст</b>\n"
      #  "<i>Курсив</i>\n"
      #  "<u>Подчеркнутый</u>\n"
      #  "<s>Зачеркнутый</s>\n"
     #   "<a href='https://example.com'>Гиперссылка</a>\n"
    #    "<code>Моноширинный код</code>\n"
    #    "<pre>Блок кода</pre>\n"
    #    "<b><i>Жирный + курсив</i></b>\n"
        except:
            my_popug=self.get_nice_popug()
            with open(my_popug, 'rb') as photo:
                self.my_bot.send_photo(
                    chat_id=user_id,
                    photo=photo,  # Передаем файловый объект
                    caption=caption,
                    reply_markup=keyboard,
                    parse_mode='HTML'
                )

    def build_caption(self,games_list, current_page=0,add_title=""):
        """
        Формирует текст с описанием для сообщения.
        Может включать информацию о играх на текущей странице.
        """
        items_per_page = 5
        start_index = current_page * items_per_page
        end_index = min(start_index + items_per_page, len(games_list))
        total_pages = (len(games_list) - 1) // items_per_page + 1
        
        

        if add_title!="":
            caption = f"<b>{add_title}</b>\n\n"
        else:
            caption = f"🎮 Найдено позиций: {len(games_list)}\n"
        caption += f"📄 Страница {current_page + 1} из {total_pages}\n\n"
        
        # Добавляем список игр на текущей странице с ценами
        for i, game in enumerate(games_list[start_index:end_index], start=start_index + 1):
            #caption += f"{i}. {game['name']} - {game['price']}\n"
            if game['old_price']!=-1:
                caption += f"{i}. 💸 {game['name']} - {game['price']} <del>{game['old_price']}</del> ₽\n"
            else:
                caption += f"{i}. {game['name']} - {game['price']} ₽\n"
        
        caption += "\nВыбери игру для перехода в магазин ↓"
        return caption
        
    # создаем и описываем кнопки
    def create_button(self):
        self.markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("🔎 Поиск игры")
        btn5= types.KeyboardButton("🌟 Избранное")
        btn6= types.KeyboardButton("🛒 Корзина")
        btn9= types.KeyboardButton("📜 Другое")
        
        btn87= types.KeyboardButton("💰 Коды пополнения")
        
        btn88= types.KeyboardButton("🧧 Nintendo Switch Online")
        self.markup.add(btn1, btn5,btn6,btn87,btn88,btn9) 

        self.markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("👤 Пользователь")
        btn2 = types.KeyboardButton("👨‍💻 Админ")
        btn3 = types.KeyboardButton("🤝 Партнер")
        btn4 = types.KeyboardButton("🔍 Админ поиск")
      # btn1 = types.KeyboardButton("Пользователи")
     #   btn3 = types.KeyboardButton("Рассылки")
      #  btns45 = types.KeyboardButton("Создать ссылку на игру")
      #  btn7= types.KeyboardButton("🌟 Избранное")
      #  btn8= types.KeyboardButton("🛒 Корзина")
      #  btn9= types.KeyboardButton("📜 Другое")
        
      #  btn87= types.KeyboardButton("💰 Коды пополнения")
        
      #  btn88= types.KeyboardButton("🧧 Nintendo Switch Online")
        
    #    self.markup2.add(btn1,btn3,btn7,btns45,btn8,btn9,btn87,btn88)
        
        self.markup2.add(btn1,btn2,btn3,btn4)

        self.markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btns4 = types.KeyboardButton("🔗 Создать ссылку на игру")
        btns45 = types.KeyboardButton("🔗 Создать ссылку на бота")
        btns2 = types.KeyboardButton("📘 Docs")
        btns3 = types.KeyboardButton("📊 Статистика интеграции")
        
        self.markup3.add(btns1,btns4,btns45,btns2,btns3)

        
        self.markup2d = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("👤 Пользователь")
        btn2 = types.KeyboardButton("👨‍💻 Админ")
        btn3 = types.KeyboardButton("🤝 Партнер")
        btn4 = types.KeyboardButton("🔍 Админ поиск")
      #  btn1 = types.KeyboardButton("Пользователи")
      #  btn3 = types.KeyboardButton("Рассылки")
       # btns45 = types.KeyboardButton("Создать ссылку на игру")
       # btn7= types.KeyboardButton("🌟 Избранное")
       # btn8= types.KeyboardButton("🛒 Корзина")
       # btn9= types.KeyboardButton("📜 Другое")
        
      #  btn87= types.KeyboardButton("💰 Коды пополнения")
        
       # btn88= types.KeyboardButton("🧧 Nintendo Switch Online")
       # btns3d = types.KeyboardButton("📊 Статистика интеграции")
        
        self.markup2d.add(btn1,btn2,btn3,btn4)
        
     #   self.markup2d.add(btn1,btn3,btns45,btn7,btn8,btn9,btn87,btn88,btns3d)
    
    def pro_start(self,message):
        markup=self.markup
        if str(message.from_user.id) in self.ids:
            markup=self.markup2

        if str(message.from_user.id)  in bot.popuski:
            markup=self.markup3
        if str(message.from_user.id)=="832182441" or str(message.from_user.id)=="5266773307":
            markup=self.markup2d
        st='search'
        txt568="Здравствуйте! Пожалуйста, введите название игры для Nintendo Switch на английском для расчёта актуальной стоимости её покупки на ваш аккаунт."
        if self.routes.get(message.from_user.id,{}).get('route','')=='a.start': st='a.search'; txt568='Введите название игры для поиска её цены (результат в USD).'
        
        self.my_bot.send_message(message.from_user.id, txt568,reply_markup=markup)
        
        self.routes[message.from_user.id]={'route':st}
        
    def pro2_start(self,message):
        markup=self.markup
        if str(message.from_user.id) in self.ids:
            markup=self.markup2

        if str(message.from_user.id)  in bot.popuski:
            markup=self.markup3
        
        if str(message.from_user.id)=="832182441" or str(message.from_user.id)=="5266773307": 
            markup=self.markup2d
        st='search'
        if self.routes.get(message.from_user.id,{}).get('route','')=='a2.start': st='a2.search'; txt568='Введите название игр через запятую для поиска их цен (результат в USD).'
        
        self.my_bot.send_message(message.from_user.id, txt568,reply_markup=markup)
        
        self.routes[message.from_user.id]={'route':st}

   
        
    def pro_search(self,message):
        ji=message.text.split("_pass")
        target=ji[0]
        if "/start" in target:
            target=target[6:]
        if target=="":
            target="Hollow Knight"
       # self.my_bot.send_message(for_reports, message.text+f"\n{target}")
        markup=self.markup
        if str(message.from_user.id) in self.ids:
            markup=self.markup2

        if str(message.from_user.id)  in bot.popuski:
            markup=self.markup3
        if str(message.from_user.id)=="832182441" or str(message.from_user.id)=="5266773307":
            markup=self.markup2d
        self.my_bot.send_message(message.from_user.id, "🔍 Производится поиск...",reply_markup=markup)
        if time.time()-self.time>self.alarm: # обновляем базу валют, если таймер вышел
            self.get_courses()

        url_image=""
        results=self.search_game(target,str(message.from_user.id)) # [['Hollow Knight', 27.99, 'Brazil Hueta', -1], ['Hollow Knight: Silksong [Switch 2]', 19.99, 'USD', -1], ['Hollow Knight: Silksong', 19.99, 'USD', -1], ['Hollow World: Dark Knight', 7.99, 'USD', -1]]


        results545=[]
        for r in results:
            results545.append(r.copy())
        self.routes[message.from_user.id]['gamelist545']=results545
        arrord={
    # === ОФИЦИАЛЬНЫЕ ISO КОДЫ СТРАН (Alpha-2) ===
    'US': '$ (США)',
    'GB': '£ (Великобритания)',
    'UK': '£ (Великобритания)',  # Неофициальный, но часто встречается
    'CA': '$ (Канада)',
    'MX': 'Peso (Мексика)',
    'PL': 'zł (Польша)',
    'AU': '$ (Австралия)',
    'JP': '￥ (Япония)',
    'NO': 'kr (Норвегия)',
    'SE': 'kr (Швеция)',
    'BR': 'R$ (Бразилия)',
    'HK': 'HK$ (Гонконг)',
    'KR': '₩ (Южная Корея)',
    
    # === ДОП. ПОПУЛЯРНЫЕ РЕГИОНЫ (на всякий случай, для игр) ===
    'TR': '₺ (Турция)',
    'AR': '$ (Аргентина)',
    'IN': '₹ (Индия)',
    'UA': '₴ (Украина)',
    'KZ': '₸ (Казахстан)',
    'CN': '¥ (Китай)',
    'NZ': '$ (Новая Зеландия)',
    'CH': 'CHF (Швейцария)',
    'DK': 'kr (Дания)',
    'CZ': 'Kč (Чехия)',"Brazil Hueta":"(Бразилия)","Honkbong Hueta":"(ХонгБонг)","Korean Hueta":"(Корея)",'British Pound':'£ (Англия)','British Pound':'£ (Англия)','British Pound':'£ (Англия)','British Pound':'£ (Англия)','USD':'$ (США)','Canadian Dollar':'$ (Канада)','Mexican Peso':'Peso (Мексика)','Polish Zloty':'zł (Польша)','Australian Dollar':'$ (Австралия)','Japanese Yen':'￥ (Япония)','USD+':'$ (Мексика [PsPrices])','Norwegian Krone':'kr (Норвегия)','Swedish Krona':'kr (Швеция)'}
        
        if self.routes.get(message.from_user.id,{}).get('route','')=='a.search':
            for r in results:
                txt521=r[2]
                r[1]=r[1]*100//1/100

                r.append(r[1])

                if r[3]!=-1: r[3]=r[3]*100//1/100
                val=arrord.get(r[2],r[2])
                r.append(r[2])
                try:
                    r[2]=val[val.index('('):]
                except:
                    pass

                #
                r[1]=str(r[1])+' $ ('+str(self.usd_to_rub(r[1],txt521))+' ₽) '
                if r[3]!=-1: r[3]=str(r[3])+' $ ('+str(self.usd_to_rub(r[3],txt521))+' ₽) '
                

                #
                
                
        else:
            for r in results:
                r.append(r[1])
                r[1]=self.usd_to_rub(r[1],r[2])
                r.append(r[2])
                if r[3]!=-1: r[3]=self.usd_to_rub(r[3],r[2])
        # если нет результатов
        if len(results)==0:
            self.my_bot.send_message(message.from_user.id, 'По Вашему запросу ничего не найдено',reply_markup=self.markup)
            return 0
        ########################################################################################################################
        txt=["По Вашему запросу найдено:\n"]
       # self.my_bot.send_message(for_reports, str(results))

        self.handle_search(message,results,url_image)


        txtsu=["null"]
        ind=1
        for i in results:
            st567=i[0]
            dst=''
            val=' ₽ '
            #
            loco=self.new_loco_dct.get(st567,{})
            loco=loco.get(i[-1],[True,0])[0]
            #
            txtsu.append(st567)
            if self.routes.get(message.from_user.id,{}).get('route','')=='a.search': dst=i[2]; val=''
            txt504='\n'+str(ind)+'. '+st567+' - '+str(i[1])+' '+val+dst
            if i[3]!=-1:
                txt504='\n'+str(ind)+'. 💸'+st567+': '+str(i[1])+' <del>'+str(i[3])+'</del> '+val+dst
            
            #
                if self.routes.get(message.from_user.id,{}).get('route','')!='a.search':
                    a=self.my_check(self.lgames,st567)
                    if a!='':
                        self.lgames[a]=[i[1],i[3],time.time(),i[-2]]

            if loco is False:
                txt504+=' [EN]'
            #
                

            txt.append(txt504)
            ind+=1
        txt2=''
        ind=0
        page=1
        while ind<len(txt):
            #!
            txt2=""
            if ind==0:
                txt2+=txt[ind]
                ind+=1
            markupin=types.InlineKeyboardMarkup()
            
            for i in range(10):
                if ind>=len(txt): break
                txt2+=txt[ind]
                if ind<len(txtsu):
                    markupin.add(types.InlineKeyboardButton(txtsu[ind],callback_data='selectgame_'+str(ind)+'$'+str(message.id)))
                    
                ind+=1
            #self.my_bot.send_message(message.from_user.id, txt2, parse_mode='HTML',reply_markup=markupin)


        self.routes[message.from_user.id]['route']='gamelist'
        self.routes[message.from_user.id]['gamelist']=results
        
    def pro2_search(self,message):
        markup=self.markup
        if str(message.from_user.id) in self.ids:
            markup=self.markup2

        if str(message.from_user.id)  in bot.popuski:
            markup=self.markup3
        if str(message.from_user.id)=="832182441" or str(message.from_user.id)=="5266773307":
            markup=self.markup2d
        self.my_bot.send_message(message.from_user.id, "🔍 Производится поиск...",reply_markup=markup)
        if time.time()-self.time>self.alarm: # обновляем базу валют, если таймер вышел
            self.get_courses()
        trgs=message.text.split(',')
        for trg in trgs:
            results=self.search_game(trg,'')
            results545=[]
            for r in results:
                results545.append(r.copy())
            self.routes[message.from_user.id]['gamelist545']=results545
            arrord={
    # === ОФИЦИАЛЬНЫЕ ISO КОДЫ СТРАН (Alpha-2) ===
    'US': '$ (США)',
    'GB': '£ (Великобритания)',
    'UK': '£ (Великобритания)',  # Неофициальный, но часто встречается
    'CA': '$ (Канада)',
    'MX': 'Peso (Мексика)',
    'PL': 'zł (Польша)',
    'AU': '$ (Австралия)',
    'JP': '￥ (Япония)',
    'NO': 'kr (Норвегия)',
    'SE': 'kr (Швеция)',
    'BR': 'R$ (Бразилия)',
    'HK': 'HK$ (Гонконг)',
    'KR': '₩ (Южная Корея)',
    
    # === ДОП. ПОПУЛЯРНЫЕ РЕГИОНЫ (на всякий случай, для игр) ===
    'TR': '₺ (Турция)',
    'AR': '$ (Аргентина)',
    'IN': '₹ (Индия)',
    'UA': '₴ (Украина)',
    'KZ': '₸ (Казахстан)',
    'CN': '¥ (Китай)',
    'NZ': '$ (Новая Зеландия)',
    'CH': 'CHF (Швейцария)',
    'DK': 'kr (Дания)',
    'CZ': 'Kč (Чехия)',"Brazil Hueta":"(Бразилия)","Honkbong Hueta":"(ХонгБонг)","Korean Hueta":"(Корея)",'British Pound':'£ (Англия)','USD':'$ (США)','Canadian Dollar':'$ (Канада)','Mexican Peso':'Peso (Мексика)','Polish Zloty':'zł (Польша)','Australian Dollar':'$ (Австралия)','Japanese Yen':'￥ (Япония)','USD+':'$ (Мексика [PsPrices])','Norwegian Krone':'kr (Норвегия)','Swedish Krona':'kr (Швеция)'}
            
            if self.routes.get(message.from_user.id,{}).get('route','')=='a2.search':
                for r in results:
                    txt521=r[2]
                    r[1]=r[1]*100//1/100
                    if r[3]!=-1: r[3]=r[3]*100//1/100
                    val=arrord.get(r[2],r[2])
                    try:
                        r[2]=val[val.index('('):]
                    except:
                        pass
    
                    #
                    pmj="$"
                    if 'Yen' in txt521:
                        pmj='￥'
                    if 'Brazil Hueta' in txt521:
                        pmj='R$'
                    if 'Honkbong Hueta' in txt521:
                        pmj='HK$'
                    if 'Korean Hueta' in txt521:
                        pmj='₩'
                    r[1]=str(r[1])+f' {pmj} ('+str(self.usd_to_rub(r[1],txt521))+' ₽) '
                    if r[3]!=-1: r[3]=str(r[3])+f' {pmj} ('+str(self.usd_to_rub(r[3],txt521))+' ₽) '
                    #
                    
                    
            else:
                for r in results:
                    r[1]=self.usd_to_rub(r[1],r[2])
                    if r[3]!=-1: r[3]=self.usd_to_rub(r[3],r[2])
            
           
            # если нет результатов
            if len(results)==0:
                self.my_bot.send_message(message.from_user.id, 'По Вашему запросу ничего не найдено',reply_markup=self.markup)
                return 0
            txt=["По Вашему запросу найдено:\n"]
            ind=1
            for i in results:
                st567=i[0]
             #   su=['!','.','-','~']
            #    ind48=0
            #    while ind48<len(st567):
              #      if st567[ind48] in su:
                #        st567=st567[:ind48]+'\\'+st567[ind48:]
             #           ind48+=1
                #    ind48+=1
                dst=''
                val=''  #!!!!!!!!!!
                #
                loco=self.loco_dct.get(st567,[True,0])[0]
                #
                if self.routes.get(message.from_user.id,{}).get('route','')=='a2.search': dst=i[2]; val=''
                txt504='\n'+str(ind)+'. '+st567+' - '+str(i[1])+' '+val+dst
                if i[3]!=-1:
                    txt504='\n'+str(ind)+'. 💸 '+st567+': '+str(i[1])+' <del>'+str(i[3])+'</del> '+val+dst
                
                #
                    if self.routes.get(message.from_user.id,{}).get('route','')!='a2.search':
                        a=self.my_check(self.lgames,st567)
                        if a!='':
                            self.lgames[a]=[i[1],i[3],time.time(),i[-1]]

                if loco is False:
                    txt504+=' [EN]'
                #
                    
    
                txt.append(txt504)
                ind+=1
            
            txt2=''
            ind=0
            while ind<len(txt):
                txt2=''
                for i in range(30):
                    if ind>=len(txt): break
                    txt2+=txt[ind]
                    ind+=1
                self.my_bot.send_message(message.from_user.id, txt2, parse_mode='HTML')
        self.routes[message.from_user.id]['route']=''
        
    def get_day(self):
        t=int(time.time()/60/60/24)
        return t

    def is_nso_1month(self, item):
        """Определяет, является ли позиция NSO на 1 месяц (по цене 399)."""
        try:
            price = float(item.get("Цена в рублях", 0))
        except (ValueError, TypeError):
            return False
        return price == NSO_1M_ORIG_PRICE

    def has_big_walk_discount(self, user_id):
        """
        Проверяет, активна ли скидка на NSO 1 мес для пользователя.
        Условия:
        - промо не истекло (до 13.08.2026)
        - BIG WALK в текущей корзине ИЛИ
        - BIG WALK куплен в последние 7 дней (заказ в great_dic)
        """
        now = datetime.now()
        if now > BIG_WALK_PROMO_END:
            return False

        # 1) BIG WALK в текущей корзине
      #  bx = self.great_box.get(user_id, [])
       # for b in bx:
          #  try:
          #      game_name = b[0][0].lower()
          #  except (IndexError, AttributeError):
          #      continue
          #  if BIG_WALK_KEYWORD in game_name:
          #      return True

        # 2) BIG WALK в оплаченных заказах за последние 7 дней
        current_day = self.get_day()
        for order_num in self.great_dic:
            order = self.great_dic[order_num]
            if str(order.get('Клиент', '')) != str(user_id):
                continue
            # статус: не отменён
            status = order.get('Статус', '')
            if 'Отменен' in status or 'Отозван' in status:
                continue
            order_text = str(order.get('Заказ', '')).lower()
            if BIG_WALK_KEYWORD in order_text:
                order_day = order.get('Дата', 0)
                if current_day - order_day <= BIG_WALK_DISCOUNT_DAYS:
                    return True

        return False
        
        
    def get_nice_popug(self):
        directory_path= PHOTO_PATCH
        if not os.path.exists(directory_path):
            print(f"Ошибка: путь '{directory_path}' не существует.")
            return POPUGEI_JPG
        if not os.path.isdir(directory_path):
            print(f"Ошибка: '{directory_path}' не является директорией.")
            return POPUGEI_JPG
    
        # Получаем список файлов (исключаем поддиректории)
        try:
            files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        except PermissionError:
            print(f"Ошибка: нет доступа к папке '{directory_path}'.")
            return POPUGEI_JPG
    
        # Проверяем, есть ли файлы
        if not files:
            print(f"В папке '{directory_path}' нет файлов.")
            return POPUGEI_JPG
    
        # Выбираем случайный файл
        random_file = PHOTO_PATCH + "/"+random.choice(files)
        return random_file
        
    def check_num(self,num):
        
        db=shelve.open(WATA_DATA_SHELVE)
        wd=db.get("orders2",{})
        #wd[str(num)]={"id":response.json()["id"],"url": str(response.json()["url"]),"status":"no"}
        db.close()
        
        idn=wd.get(str(num),{}).get("id","")
        
        cool=wd.get(str(num),{}).get("status","")

        tpy=wd.get(str(num),{}).get("tpy","wata")
        
        if cool=="yes": return "✅ Оплачен"
        
        if idn=="": return "неизвестно"
        
        coll=-1
        if tpy=="pally":
            shop_id=PALLY_SHOP_ID
            token=PALLY_TOKEN
            try:
                headers = {
        'Authorization': f'Bearer {token}',
    }

                params = {
        'id': idn,
    }

                response = requests.get('https://pal24.pro/api/v1/bill/status', params=params, headers=headers)
                if str(response.status_code)=="200":
                    st=str(response.json()["status"])
                    if st in ["SUCCESS","OVERPAID"]: coll=1
                    else: coll=0
                    
            except:
                self.my_bot.send_message(for_reports,traceback.format_exc())

            
        if coll==-1: st="(?) Неизвестно"
        if coll==0: st="❌Не оплачен"
        if coll==1: st="✅ Оплачен"
            
        if coll==1:
            db=shelve.open(WATA_DATA_SHELVE)
            wd=db.get("orders2",{})
            ordr=wd.get(str(num),{})
            ordr["status"]="yes"
            wd[str(num)]=ordr
            db["orders2"]=wd
            db.close()
        return st
        
    def create_url_pally(self,count,num):
        try:
            desc="Подключение цифровых игр для Nintendo Switch"
            
            shop_id=PALLY_SHOP_ID
            token=PALLY_TOKEN
            
            headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/x-www-form-urlencoded',
            }

            data = f'amount={float(count)}&description={desc}&order_id={num}&shop_id={shop_id}'

            response = requests.post('https://pal24.pro/api/v1/bill/create', headers=headers, data=data)
            
            
            
            
            
            if str(response.status_code)!="200":
                return "Ошибка: "+str(response.status_code)
            else:
                url=str(response.json()["link_page_url"])
                bill_id=str(response.json()["bill_id"])
                db=shelve.open(WATA_DATA_SHELVE)
                wd=db.get("orders2",{})
                wd[str(num)]={"id":bill_id,"url": url,"status":"no","tpy":"pally"}
                db["orders2"]=wd
                db.close()

                if os.path.exists(WATA_DATA_SHELVE):  # проверяем, существует ли файл
                    os.remove(WATA_DATA_SHELVE)

                db=shelve.open(WATA_DATA_SHELVE)
                db["orders2"]=wd
                db.close()
                return url
        except:
            self.my_bot.send_message(for_reports,traceback.format_exc())
    def google_api_search_images(self,query):
        num_results=10
        """Поиск изображений через Google Custom Search API"""
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": API_KEY,
            "cx": SEARCH_ENGINE_ID,
            "q": query,
            "searchType": "image",
            "num": num_results,
            "fileType": "jpg|png|jpeg",
            "imgSize": "large",  # Большие изображения (до 8 МП) xxlarge huge
            "safe": "active"     # Безопасный поиск
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            images = []
            if "items" in data:
                for item in data["items"]:
                    try:
                        width = int(item["image"]["width"])
                        height = int(item["image"]["height"])
                        megapixels = (width * height) / 1_000_000

                        images.append({
                                "url": item["link"],
                                "size": (width, height),
                                "megapixels": round(megapixels, 2),
                                "title": item.get("title", "Без названия")
                            })
                    except (KeyError, ValueError) as e:
                        bot.my_bot.send_message(for_reports, f"Ошибка обработки элемента: {e}")
                        continue
            
            return images
        except requests.exceptions.RequestException as e:
            bot.my_bot.send_message(for_reports, f"Ошибка API запроса: {e}")
            return []
    def pro_gamelist(self,message):
        try:
            ind=int(message.text)
        except ValueError:
            self.pro_start(message)
            return 0
            #self.handle_search(message,self.routes[message.from_user.id]['gamelist'],"")
            #return 0
        ind-=1
        results=self.routes[message.from_user.id]['gamelist']
        if ind>=0 and ind<len(results):
            arr=results[ind]
            markupin=types.InlineKeyboardMarkup()
            markupin.add(types.InlineKeyboardButton('💸 Купить игру сразу',callback_data='buygame_'+str(message.from_user.id)+'+'+str(ind)+'$'+str(message.id)))
            markupin.add(types.InlineKeyboardButton('🛒 Добавить игру в корзину',callback_data='boxgame_'+str(message.from_user.id)+'+'+str(ind)+'$'+str(message.id)))
            markupin.add(types.InlineKeyboardButton('🌟 Добавить в Избранное',callback_data='pingame_'+str(message.from_user.id)+'+'+str(ind)))
      
            markupin.add(types.InlineKeyboardButton('Отмена',callback_data='ndelgame_'+str(message.from_user.id)+'+'+str(ind)))
            self.my_bot.send_message(message.from_user.id, "Вы выбрали "+arr[0]+". Стоимость: "+str(arr[1])+" руб",reply_markup=markupin)
        else:
            self.my_bot.send_message(message.from_user.id, 'Пожалуйста, введите номер игры от 1 до '+str(len(results)),reply_markup=self.markup)
            return 0

    def pro_gamelist545(self,user,ind,message_id):
        results=self.routes[user]['gamelist']
        results545=self.routes[user]['gamelist545']

      #  try:
         #   self.my_bot.send_message(for_reports, str(results))
         #   self.my_bot.send_message(for_reports, str(results545))
         #   self.my_bot.send_message(for_reports, str(results545[ind]))
       # except:
        #    pass
        if ind>=0 and ind<len(results):
            arr=results[ind]
            arr545=results545[ind]
            arrord={
    # === ОФИЦИАЛЬНЫЕ ISO КОДЫ СТРАН (Alpha-2) ===
    'US': '$ (США)',
    'GB': '£ (Великобритания)',
    'UK': '£ (Великобритания)',  # Неофициальный, но часто встречается
    'CA': '$ (Канада)',
    'MX': 'Peso (Мексика)',
    'PL': 'zł (Польша)',
    'AU': '$ (Австралия)',
    'JP': '￥ (Япония)',
    'NO': 'kr (Норвегия)',
    'SE': 'kr (Швеция)',
    'BR': 'R$ (Бразилия)',
    'HK': 'HK$ (Гонконг)',
    'KR': '₩ (Южная Корея)',
    
    # === ДОП. ПОПУЛЯРНЫЕ РЕГИОНЫ (на всякий случай, для игр) ===
    'TR': '₺ (Турция)',
    'AR': '$ (Аргентина)',
    'IN': '₹ (Индия)',
    'UA': '₴ (Украина)',
    'KZ': '₸ (Казахстан)',
    'CN': '¥ (Китай)',
    'NZ': '$ (Новая Зеландия)',
    'CH': 'CHF (Швейцария)',
    'DK': 'kr (Дания)',
    'CZ': 'Kč (Чехия)','British Pound':'£ (Англия)','USD':'$ (США)','Canadian Dollar':'$ (Канада)','Mexican Peso':'Peso (Мексика)','Polish Zloty':'zł (Польша)','Australian Dollar':'$ (Австралия)','Japanese Yen':'￥ (Япония)','USD+':'$ (Мексика [PsPrices])','Norwegian Krone':'kr (Норвегия)','Swedish Krona':'kr (Швеция)'}
            dst=arrord.get(arr[2],arr[2])
            dst=dst[dst.find('('):]
            self.stack.append({'Дата':self.get_day(),'Заказ':arr[0],'Менеджер':'','Клиент':user,'Статус':'Создан','Цена':float(arr[1]),'Профит':self.get_my_profit(arr[1]),'stga':arr[0]+' '+dst,'stpusa':float(arr545[1]),"Номер":self.num})
            self.num+=1
            markup=types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Отправить заказ',callback_data='acceptorder_'+str(user)+'+'+str(len(self.stack)-1)+'$'+str(message_id)))
            markup.add(types.InlineKeyboardButton('Отменить заказ',callback_data='breakorder_'+str(user)))
            self.my_bot.send_message(user, "🛍 Вы приобретаете: \n"+arr[0]+" - "+str(arr[1])+" ₽",reply_markup=markup)
            
            self.routes[user]['route']='start'

            
        else:
            self.my_bot.send_message(user, 'Пожалуйста, введите номер игры от 1 до '+str(len(results)),reply_markup=self.markup)
            return 0
            
            
    def pro_gamelist545_boxgame(self,user,ind,message_id):
        results=self.routes[user]['gamelist']
        results545=self.routes[user]['gamelist545']
        if ind>=0 and ind<len(results):
            arr=results[ind]
            arr545=results545[ind]
            
            bx=self.great_box.get(user,[])
            bx.append([arr,arr545])
            self.great_box[user]=bx
            ngm=0
            for b in bx:
                ngm+=float(b[0][1])
            ngm2=ngm+0
            if len(bx)>=3: ngm2=(ngm*0.95)//1
            markupin=types.InlineKeyboardMarkup()
            markupin.add(types.InlineKeyboardButton('🔎 Найти ещё игру',callback_data='findgame_'+str(user)))
            markupin.add(types.InlineKeyboardButton('🛒 Перейти к корзине',callback_data='mybox_'+str(user)+'+'+str(message_id)))
            markupin.add(types.InlineKeyboardButton('Назад',callback_data='nbackgame_'+str(user)+'+'+str(0)))
            ttxt="🛒 "+arr[0]+" добавлена в корзину.\n Сейчас в Вашей корзине игр: "+str(len(bx))+"\nОбщая стоимость: "+str(ngm)+" ₽"
            if ngm2!=ngm:
                ttxt="🛒 "+arr[0]+" добавлена в корзину.\n Сейчас в Вашей корзине игр: "+str(len(bx))+"\nОбщая стоимость: "+str(ngm2)+" <del>"+str(ngm)+"</del> ₽\nДобавлена скидка 5% за покупку от 3 игр"
            self.my_bot.send_message(user, ttxt,reply_markup=markupin,parse_mode='HTML')
            self.routes[user]['route']='start'
        else:
            self.my_bot.send_message(user, 'Пожалуйста, введите номер игры от 1 до '+str(len(results)),reply_markup=self.markup)
            return 0
        

            
    def au_start(self,message):
            txt='Зарегистрировано уникальных пользователей: '+str(len(self.users))+'. \n'
            self.my_bot.send_message(message.from_user.id,txt,reply_markup=self.markup2)
    def au_game(self,message):
            
            
            ng1=0
            ng2=0
            for key in self.dgames:
                gm=self.lgames[key]
                if time.time()-gm[2]<self.tlimit:
                    ng2+=1
                    if gm[0]<gm[1]:
                        ng1+=1
            txt='Количество игр для рассылки: '+str(len(self.dgames))+'. \nИз них продаются со скидками: '+str(ng1)+'\nДанные актуальны для '+str(ng2)+' игр\n /list - вывести список игр полностью \n /add - добавить игру в список \n /delete - удалить игры из списка'
            self.my_bot.send_message(message.from_user.id,txt,reply_markup=self.markup2)
    def au_game_list(self,message):
            arr=[]
            ind=1
            for g in self.dgames:
                gm=self.lgames[g]
                if gm[0]>=gm[1]:
                    txt504='\n'+str(ind)+'. '+g
                else:
                    txt504='\n'+str(ind)+'. 💸 '+g+': '+str(gm[0])+' <del>'+str(gm[1])+'</del> ₽'
                    if time.time()-gm[2]>=self.tlimit or len(gm)<4:
                        txt504+=" (данные о скидке нуждаются в проверке)"
                ind+=1
                arr.append(txt504)
            ind=0
            txt=''
            for i in range(len(arr)):
                txt+=arr[i]
                ind+=1
                if ind>=30:
                    self.my_bot.send_message(message.from_user.id,txt,parse_mode='HTML')
                    ind=0
                    txt=''
            if txt!='':
                self.my_bot.send_message(message.from_user.id,txt,parse_mode='HTML')
            elif ind==0:
                self.my_bot.send_message(message.from_user.id,'Список игр пуст')
    def au_game_add(self,message):
            self.routes[message.from_user.id]['route']='au_game_add'
            self.my_bot.send_message(message.from_user.id,'Введите название игры или выберите команду отмены (/back)',reply_markup=self.markup2)
    def save_promos(self):
        db = shelve.open(PROMOS_DATA_SHELVE)
        db["promos"] = self.promos
        db.close()
    def au_game_add2(self,message):
            txt=message.text
            self.dgames.append(txt)
            a=self.lgames.get(txt,[])
            if len(a)==0:
                self.lgames[txt]=[0,0,0,0] # цена1,цена2,время
            self.routes[message.from_user.id]['route']='start'
            self.my_bot.send_message(message.from_user.id,'Игра успешно добавлена. Для добавления еще одной игры выберите команду (/add)',reply_markup=self.markup2)
    
    def au_ban(self,message):
            self.routes[message.from_user.id]['route']='au_ban'
            self.my_bot.send_message(message.from_user.id,'Введите id пользователя, которого хотите заблокировать или выберите команду отмены (/back). Для получения id перешлите любое его сообщение @getidsbot.',reply_markup=self.markup2)
    def au_ban2(self,message):
            txt=message.text
            self.ban_users.append(txt)
            self.routes[message.from_user.id]['route']='start'
            self.my_bot.send_message(message.from_user.id,'Пользователь заблокирован',reply_markup=self.markup2)
    def au_list_admin(self,message):
        txt="Администраторы:\n"
        for key in self.auth:
            txt+=str(key)+" - "+self.auth[key]+'\n'
        self.my_bot.send_message(message.from_user.id,txt,reply_markup=self.markup2)
        
    def au_load_admin(self,message):



        db=shelve.open(ADMIN_DATA_SHELVE)
        self.auth=db.get('auth',auth)
        self.ids=db.get('ids',ids)
        db.close()
        fids=[]
        for nu in self.ids:
            if nu not in fids:
                fids.append(nu)
        self.ids=fids

        db=shelve.open(ADMIN_DATA_SHELVE)
        db["ids"]=self.ids
        db.close()
        txt="Администраторы:\n"
        for key in self.auth:
            txt+=self.auth[key]+'\n'
        self.my_bot.send_message(message.from_user.id,txt)


        
    def au_del_admin(self,message):
            self.routes[message.from_user.id]['route']='au_del_admin'
            self.my_bot.send_message(message.from_user.id,'Введите id администратору, которого хотите удалить или выберите команду отмены (/back). Для получения id перешлите любое его сообщение @getidsbot.',reply_markup=self.markup2)
    def au_del_admin2(self,message):
            txt=message.text
            idm=txt
            tx=self.auth.get(idm,'')
            if txt in self.ids:
                self.ids.pop(self.ids.index(txt))
            if txt in self.auth:
                self.auth.pop(txt)
            self.routes[message.from_user.id]['route']='start'
            self.my_bot.send_message(message.from_user.id,'Администратор удален',reply_markup=self.markup2)
            self.batya_report(f"удалил менеджера {idm} ({tx})",message.from_user.id)
            db=shelve.open(ADMIN_DATA_SHELVE)
            db['auth']=self.auth
            db['ids']=self.ids
            db.close()
    def create_popusk_key(self,mid):
            st=""
            st2="soatmericuh"
            for su in mid:
                st+=st2[int(su)]
            return st
    def au_new_admin(self,message):
            self.routes[message.from_user.id]['route']='au_new_admin'
            self.my_bot.send_message(message.from_user.id,'Введите id пользователя, которого хотите сделать новым администратором или выберите команду отмены (/back). Для получения id перешлите любое его сообщение @getidsbot.',reply_markup=self.markup2)
    def au_new_admin2(self,message):
            txt=message.text
           # self.ids.append(txt)
            self.routes[message.from_user.id]['cash']=txt
            self.routes[message.from_user.id]['route']='au_new_admin2'
            self.my_bot.send_message(message.from_user.id,'Введите имя нового администратора. Например, 👤 Николай (@tg_kolya)',reply_markup=self.markup2)
    def au_new_admin3(self,message):
            txt=message.text
            idm=self.routes[message.from_user.id].get('cash','-1')
            if idm!='-1':
                self.ids.append(idm)
                self.auth[idm]=txt
                self.routes[message.from_user.id]['route']='start'
                self.my_bot.send_message(message.from_user.id,'Новый администратор успешно добавлен',reply_markup=self.markup2)
                self.batya_report(f"добавил менеджера {idm} ({txt})",message.from_user.id)
            
                db=shelve.open(ADMIN_DATA_SHELVE)
                db['auth']=self.auth
                db['ids']=self.ids
                db.close()
            else:
                self.routes[message.from_user.id]['route']='start'
                self.my_bot.send_message(message.from_user.id,'Ошибка ввода id администратора',reply_markup=self.markup2)
                
    def au_game_del(self,message):
            arr=[]
            ind=1
            for g in self.dgames:
                gm=self.lgames[g]
                if gm[0]>=gm[1]:
                    txt504='\n'+str(ind)+'. '+g
                else:
                    txt504='\n'+str(ind)+'. 💸 '+g+': '+str(gm[0])+' <del>'+str(gm[1])+'</del> ₽'
                ind+=1
                arr.append(txt504)
            ind=0
            txt=''
            for i in range(len(arr)):
                txt+=arr[i]
                ind+=1
                if ind>=30:
                    self.my_bot.send_message(message.from_user.id,txt,parse_mode='HTML')
                    ind=0
                    txt=''
            if txt!='':
                self.my_bot.send_message(message.from_user.id,txt,parse_mode='HTML')
            elif ind==0:
                self.my_bot.send_message(message.from_user.id,'Список игр пуст')
            self.routes[message.from_user.id]['route']='au_game_del'
            self.my_bot.send_message(message.from_user.id,'Введите номер игры, выберите команду для удаления всех игр (/delete_all) или выберите команду отмены (/back)',reply_markup=self.markup2)
            
    def au_game_del2(self,message):
            txt=message.text
            try:
                ind=int(message.text)-1
            except:
                ind=-1
            if ind==-1:
                self.my_bot.send_message(message.from_user.id,'Игра не найдена. Для повторного удаления игры выберите команду (/delete)',reply_markup=self.markup2)
            else:
                self.dgames.pop(ind)
                self.my_bot.send_message(message.from_user.id,'Игра удалена из списка. Для повторного удаления игры выберите команду (/delete)',reply_markup=self.markup2)
                
            self.routes[message.from_user.id]['route']='start'
            
            
    def au_rassu(self,message):
            
            self.my_bot.send_message(message.from_user.id,'Отправьте фото с подписью для рассылки или выберите команду отмены (/back)',reply_markup=self.markup2)
            self.routes[message.from_user.id]['route']='au_rassu'
            
    def au_give_stat(self,user23):
            txt="Статистика за последние 30 дней"
            n=0
            n1=0
            n2=0
            s1=0
            s2=0
            day=self.get_day()
            mg={}
            
            for key in self.great_dic:
                try:
                    st=self.great_dic[key]
                    if day-st['Дата']<=30:
                        m=st['Менеджер']
                        ss=st['Статус']
                        money1=st['Цена']
                        money2=st['Профит']
                        if ss=='Принят':
                            n+=1
                            n1+=1
                            s1+=float(money1)
                            s2+=money2
                            
                            mm=mg.get(m,[0,0])
                            mm[0]+=1
                            mm[1]+=money2
                            mg[m]=mm.copy()
                        elif 'Отозван' in ss:
                            n+=1
                            n2+=1
                except:
                    pass
            txt+="\nОформлено заказов: "+str(n)
            txt+="\nПринято заказов: "+str(n1)
            txt+="\nОтозвано заказов: "+str(n2)
            txt+="\n\nОбщая сумма покупок: "+str(s1)
            txt+="\nПрофит: "+str(s2)
            txt+="\n\nОформлено менеджерами:"
            for m in mg:
                mm=mg[m]
                txt+="\n\n"+m
                txt+="\nПринял заказов: "+str(mm[0])
                txt+="\nПрофит: "+str(mm[1])
            self.my_bot.send_message(user23,txt,reply_markup=self.markup2)
            
    def au_rassu3(self,message):
            self.original_message_id = message.id
            self.from_chat_id = message.chat.id

            self.rassu_text=message.text
            self.rassu_entities = message.entities

            self.rassu_message = self.convert_entities_to_html(self.rassu_text, self.rassu_entities)

            self.my_bot.send_message(message.from_user.id,'Сообщение для рассылки:')
            if self.rassu_photo!=-1:
                self.my_bot.send_photo(message.from_user.id,self.rassu_photo)
                self.routes[message.from_user.id]['route']='au_rassu3'
            else:
                self.routes[message.from_user.id]['route']='au_rassu2'
            #self.my_bot.send_message(message.from_user.id,self.rassu_message,parse_mode='HTML')
            self.my_bot.copy_message(
                            chat_id=message.from_user.id, 
                            from_chat_id=self.from_chat_id, # ID чата, откуда берем оригинал
                            message_id=self.original_message_id # ID того самого сообщения с эмодзи
                        )
            self.my_bot.send_message(message.from_user.id,'Подвердите рассылку (/accept) или выберите команду отмены (/back)',reply_markup=self.markup2)
            
    def au_rassu4(self,message):
            self.my_bot.send_message(message.from_user.id,'Подвердите отправку (/accept), подвердите рассылку без фото (/without_photo) или выберите команду отмены (/back)',reply_markup=self.markup2)
            self.routes[message.from_user.id]['route']='au_rassu2'
            
    def au_rassu2(self,message):  # Непосредственно рассылка
            cou=0
            us=self.users.copy()
            for key in us:
                if us[key]==1:
                    try:
                        self.my_bot.copy_message(
                            chat_id=key, 
                            from_chat_id=self.from_chat_id, # ID чата, откуда берем оригинал
                            message_id=self.original_message_id # ID того самого сообщения с эмодзи
                        )
                    except:
                        pass
                    
            for key in self.ids:
                if 1==1:
                    try:
                        self.my_bot.copy_message(
                            chat_id=key, 
                            from_chat_id=self.from_chat_id, # ID чата, откуда берем оригинал
                            message_id=self.original_message_id # ID того самого сообщения с эмодзи
                        )
                    except:
                        pass

                   # if self.rassu_photo!=-1:
                     #   try:
                            
                        #    self.my_bot.send_photo(key,self.rassu_photo,caption=self.rassu_message,parse_mode='HTML')
                       #     cou+=1
                      #  except:
                     #       pass
                  #  else:
                   #     try:
                     #       self.my_bot.send_message(key,self.rassu_message,parse_mode='HTML')
                    #        cou+=1
                   #     except:
                   #         pass
                    
                 #          "<b>Жирный текст</b>\n"
      #  "<i>Курсив</i>\n"
      #  "<u>Подчеркнутый</u>\n"
      #  "<s>Зачеркнутый</s>\n"
     #   "<a href='https://example.com'>Гиперссылка</a>\n"
    #    "<code>Моноширинный код</code>\n"
    #    "<pre>Блок кода</pre>\n"
    #    "<b><i>Жирный + курсив</i></b>\n"
            self.my_bot.send_message(message.from_user.id,'Сообщение разослано '+str(cou)+' пользователям',reply_markup=self.markup2)
            
            if self.rassu_photo!=-1:
                self.my_bot.send_photo(message.from_user.id,self.rassu_photo,caption=self.rassu_message,parse_mode='HTML')
            else:
                self.my_bot.send_message(message.from_user.id,self.rassu_message,parse_mode='HTML')
            
            self.rassu_photo=-1
            
            self.routes[message.from_user.id]['route']='start'
    
    def au_lpr(self,message):
            if self.rassu_photo2!=-1:
                    self.my_bot.send_message(message.from_user.id,'Сейчас загружено фото:')
                    self.my_bot.send_photo(message.from_user.id,self.rassu_photo2)
            else:
                    self.my_bot.send_message(message.from_user.id,'В данный момент фото не добавлено')
            self.my_bot.send_message(message.from_user.id,'Отправьте фотографию или подвердите рассылку о скидках (/accept) или выберите команду отмены (/back)',reply_markup=self.markup2)
            self.routes[message.from_user.id]['route']='au_lpr'
            
    def au_lpr2(self,message=None): # Непосредственно рассылка
            txt=''
            results=[]
            gamelist545=[]
            arr=['Доступны скидки на следующие игры:\n']
            ind=1
            coll=0
            dg=[]
            resultsabu=[]
            ind5=-1

            add_title=random.choice(['''Тук-тук-тук! 🚪
Это скидки на игры… можно войти?''',
'''Собрано с любовью 💌
Классные игры по неприлично низким ценам — это тебе!''',
'''Никому не говори 🤫
ПОПУГАЙ собрал самые классные скидки — забирай, если хочешь!''',
'''Тихо-тихо… что это? 👀
Кажется, это свежие скидки на хиты и новинки — специально для тебя!''',
'''Только сегодня 😦
Ну, может, ещё и завтра! Скидки на несколько хитов и эксклюзивов уже ждут.''',
'''Кррр, кррр 🦜
ПОПУГАЙ снова здесь — прилетел с новыми скидками! Лови!'''])

            for key in self.dgames:
                try:
                    ind5+=1
                    gdata=self.lgames.get(key,[0,0,0,0])
                    if (gdata[0]<gdata[1]) and gdata[0]!=0 and time.time()-gdata[2]<self.tlimit: #time.time()-gdata[2]<self.tlimit and 
                        results.append([key,str(gdata[0]),''])
                        resultsabu.append([key,gdata[0],"da_ne_ebu",gdata[1],gdata[3],"da_ne_ebu"])
                        gamelist545.append([key,str(gdata[3]),''])
                        txt504='\n'+str(ind)+'. 💸 '+key+': '+str(gdata[0])+' <del>'+str(gdata[1])+'</del> ₽'
                        coll+=1
                        ind+=1
                        arr.append(txt504)
                    elif gdata[0]>=gdata[1]:
                        dg.append(ind5)
                except:
                    pass


                    #['Hollow Knight [Switch 2]', 1378, 'Norwegian Krone', -1, 10.3942000363797, 'Norwegian Krone']
            arr.append('''\n\nЕсли вы хотите закупиться на скидках, введите номер игры из рассылки (например: 2).

Чтобы купить / узнать цену / добавить в избранное и следить за скидками на другую игру, нажмите "🔎 Поиск игры"''')
            for i in range(len(dg)):
                try:
                    self.dgames.pop(dg[-1-i])
                except:
                    pass
            cou=0
            us=self.users.copy()
            imu=0
            for key in us:
                imu+=1
                if imu%200==0:
                    bot.my_bot.send_message(for_reports, f"{imu} из {len(us)} [{cou}]")
            #    if str(key)!="5266773307": continue
                if us[key]==1 and coll!=0:
                    ind=0
                    txt2=''
                    try:
                        a=self.routes.get(int(key),dict())
                        if a==dict():
                            self.routes[int(key)]=dict()
                        self.routes[int(key)]['route']='gamelist'
                        self.routes[int(key)]['gamelist']=results
                        self.routes[int(key)]['gamelist545']=gamelist545
                        url_image=""
                        if self.rassu_photo2!=-1:
                            url_image=self.rassu_photo2
                        self.handle_search("abu_daba",resultsabu,url_image,int(key),add_title=add_title)
                        cou+=1
                        
                    except:
                        time.sleep(0.017)
                        pass
                       # bot.my_bot.send_message(for_reports, traceback.format_exc())
            
            if coll==0:
                for ids in self.ids:
                    try:
                        self.my_bot.send_message(ids,'В данный момент нет скидок: сообщение не доставлено',reply_markup=self.markup2)
                    except:
                        pass
            else:
                for idm in self.ids:
                    try:
                        self.my_bot.send_message(idm,'Сообщение о скидках разослано '+str(cou)+' пользователям',reply_markup=self.markup2)
                    except:
                        pass
                
            for key in self.ids:
            #    if str(key)!="5266773307": continue
                if coll!=0:
                   # if self.rassu_photo2!=-1:
                     #   try:
                    #        self.my_bot.send_photo(key,self.rassu_photo2)
                    #    except:
                    #        pass
                    ind=0
                    txt2=''
                   # for st in arr:
                       # txt2+=st
                       # ind+=1
                       # if ind>=30:
                          #  try:
                          #      self.my_bot.send_message(key, txt2, parse_mode='HTML')
                           # except:
                           #     pass
                        #    ind=0
                        #    txt2=''
                   # if txt2!='':
                       # try:
                           # self.my_bot.send_message(key, txt2, parse_mode='HTML')
                       # except:
                       #     pass
                    try:
                        a=self.routes.get(int(key),dict())
                        if a==dict():
                            self.routes[int(key)]=dict()
                        self.routes[int(key)]['route']='gamelist'
                        self.routes[int(key)]['gamelist']=results
                        self.routes[int(key)]['gamelist545']=gamelist545
                        url_image=""
                        if self.rassu_photo2!=-1:
                            url_image=self.rassu_photo2
                        self.handle_search("abu_daba",resultsabu,url_image,int(key),add_title=add_title)
                    except:
                        bot.my_bot.send_message(for_reports, traceback.format_exc())
                    
            self.rassu_photo2=-1
            if self.routes.get(message.from_user.id,{'route':''})['route']=='au_lpr':
                self.routes[message.from_user.id]['route']='start'
            
    def au_photo(self,message):
            self.routes[message.from_user.id]['route']='au_photo'
            if self.rassu_photo2!=-1:
                self.my_bot.send_message(message.from_user.id,'Сейчас загружено фото:')
                self.my_bot.send_photo(message.from_user.id,self.rassu_photo2)
            else:
                self.my_bot.send_message(message.from_user.id,'В данный момент фото не добавлено')
            self.my_bot.send_message(message.from_user.id,'Отправьте фото для рассылки о скидках, удалите текущее фото (/delete_photo) или выберите команду отмены (/back)',reply_markup=self.markup2)
            
    def au_update(self):
            ulist=[]
            for key in self.dgames:
                gm=self.lgames[key]
                if time.time()-gm[2]>=self.tlimit/4:
                    ulist.append(key)
            for ids in self.ids:
                try:
                    self.my_bot.send_message(ids,'Начато обновление данных о скидках, это может занять около 20-30 минут. В списке игр: '+str(len(ulist)))
                except:
                    pass
            
            for key in self.dgames:
                gm=self.lgames[key]
                if time.time()-gm[2]>=self.tlimit/4:
                    try:
                        self.update_game(key)
                    except:
                        pass
            for ids in self.ids:
                try:
                    self.my_bot.send_message(ids,'Обновление завершено')
                except:
                    pass

    def validate_shopa(self,text: str) -> bool:
        if not text:
            return False
        
        clean_text = text.strip().lower()
        
        junk_words = {
            "привет", "здрасьте", "здравствуйте", "хай", "ку", "прив",
            "старт", "start", "помоги", "help", "лох", "бот", "админ",
            "как дела", "что ты умеешь", "цена", "купить", "продажа", 
            "спасибо", "пока", "тест"
        }
        
        # Если текст полностью совпадает с мусорным словом
        if clean_text in junk_words:
            return False

        # 2. ПРОВЕРКА ДЛИНЫ
        if len(clean_text) < 2:
            return False # Слишком коротко для любого нормального запроса

        # 3. СТРУКТУРНАЯ ПРОВЕРКА
        # Проверяем, есть ли в строке хотя бы одна цифра или латинская буква
        has_alphanumeric = bool(re.search(r'[0-9a-zA-Z]', clean_text))
        
        # Проверяем, состоит ли строка ТОЛЬКО из кириллицы, пробелов и дефисов
        is_only_cyrillic = bool(re.match(r'^[а-яё\s\-]+$', clean_text))

        if is_only_cyrillic:
            return False
        if not has_alphanumeric and len(clean_text) < 8:
            return False

        return True
            
            
    def update_game(self,name):
        
        if time.time()-self.time>self.alarm: # обновляем базу валют, если таймер вышел
            self.get_courses()
        target=name
        if "[Switch 2]" in target:
            ind=target.find("[Switch 2]")
            target=target[:ind]
        results=self.search_game(target,'')
        
        for r in results:
            usd=r[1]
            r[1]=self.usd_to_rub(r[1],r[2])
            a=self.my_check(self.lgames,r[0])
            if a!='':
                self.lgames[a]=[r[1],r[1],time.time(),usd]
            if r[3]!=-1 and a!='': self.lgames[a][1]=self.usd_to_rub(r[3],r[2])
        if len(results)==0:
            self.lgames[name]=[0,0,time.time(),0]
            
    def adbot_refresh(self):
            lst=[]
            dg=[]
            for u in self.favo:
                for g in self.favo[u]:
                    if g not in lst:
                        lst.append(g)
                tm=self.users_time.get(str(u),-1)
                if tm>0 and time.time()-tm>=60*60*24*30:
                    dg.append(str(u))
            self.favo_list=lst
            
            for d in dg:
                self.favo.pop(d)

    def adbot_auto_dgames(self):
                rz=[]
                cookies = {
                    'rack.session': 'BAh7DEkiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkUwMTU5YjU3M2Y4MTMyMWJkZmRiYTlkNTRjYzgzMGVlMWE1ZDEwMTg5YTFjZTE4YzAzMTM2MmIyYTI0ZDg5YTE0BjsARkkiCWNzcmYGOwBGSSIxUFBuWU1GRXVwaGRQcllva2V6ZTdYdHVOWWtJTlR5dHRkVUU0MnJvc0N5az0GOwBGSSIOX19GTEFTSF9fBjsARnsASSIMY291bnRyeQY7AEZJIgd1cwY7AFRJIgtzb3VyY2UGOwBGIhdodHRwczovL3lhbmRleC5ydS9JIgxsYW5kaW5nBjsARkkiBi8GOwBUSSIJYWJpZAY7AEZJIhk2NTAyODM1ODc2MzQ1OTk2OTEyMQY7AEY%3D--dbc752314c9806dae201e3e6ff40549ab9a56591',
                }

                headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 YaBrowser/25.12.0.0 Safari/537.36',
 }

                response = requests.get('https://www.dekudeals.com/hottest?sort=hottest', cookies=cookies, headers=headers)
                soup = BeautifulSoup(response.content, "html.parser")
                alldiv=soup.select('div > div > div > div > div')
                skip=0
                for div in alldiv:
                    txt=div.text
                    if ('kr' in txt or 'zł' in txt or '$' in txt  or '￥' in txt or '¥' in txt or '£' in txt) and skip==0:
                        try:
                            vl255=[]
                            lasts2=txt.split('\n')
                            lasts=[]
                            vl=0
                            for st in lasts2:
                                if st=='':
                                    pass
                                elif 'kr' in st or 'zł' in st or '$' in st  or '￥' in st or '¥' in st or '£' in txt:
                                    
                                    vl=''
                                    for su in st:
                                        if su in '1234567890.,':
                                            vl+=su
                                    if vl[-3]==',':
                                        vl=vl[:-3]+'.'+vl[-2:]
                                    ind6=vl.find(',')
                                    if ind6!=-1: vl=vl[:ind6]+vl[ind6+1:]
                                    vl255.append(float(vl))
                                else:
                                    lasts.append(st)
                                    
                            for vl in vl255:
                                #print(vl)
                                if vl!=0:
                                    st2=self.filter_names(lasts,"Hollow Knight")
                                    if st2!='':
                                        ind6=st2.find('™')
                                        if ind6!=-1: st2=st2[:ind6]+st2[ind6+1:]
                                        if st2 not in rz:
                                            rz.append(st2)
                        except:
                            pass
                #self.my_bot.send_message(for_reports,str(len(rz)))
                #self.my_bot.send_message(for_reports,str(rz[:5]))
                for game in rz:
                    if game not in self.dgames:
                        self.dgames.append(game)
                        a=self.lgames.get(game,[])
                        if len(a)==0:
                            self.lgames[game]=[0,0,0,0] # цена1,цена2,время
                    a=self.lgames.get(game,[])
                    if len(a)==0:
                        self.lgames[game]=[0,0,0,0] # цена1,цена2,время

               
                self.adbot_save()

    def adbot_reprice(self):
        self.alarm2=time.time()
        self.au_update()
            
    def adbot_reprice2(self):
            dct={}
            for g in self.favo_list:
                if time.time()-self.time>self.alarm: # обновляем базу валют, если таймер вышел
                    self.get_courses()
                results=self.search_game(g,'')
                
                for r in results:
                    usd=r[1]
                    val=r[2]
                    r[1]=self.usd_to_rub(r[1],r[2])
                    a=''
                    if self.st_in_lowst(r[0])==self.st_in_lowst(g):
                        a=g
                    if a!='':
                        dct[a]=[r[1],r[1],time.time(),usd,val]
                    if r[3]!=-1 and a!='': dct[a][1]=self.usd_to_rub(r[3],r[2])
            
            self.favo_price=dct
            
            
    def adbot_send2(self):
            for u in self.favo:
                
                try:
                    favo_time=self.favo_time.get(u,{})
                    lst=['Доступны скидки на следующие игры:\n']
                    ind=1
                    results=[]
                    results545=[]
                    for g in self.favo[u]:
                        gdata=self.favo_price[g]
                        if g in self.favo_price and time.time()-favo_time.get(g,time.time()-4*24*60*60)>2.5*24*60*60 and float(gdata[0])+1<float(gdata[1]):
                            favo_time[g]=time.time()
                            lst.append('\n'+str(ind)+'. 💸 '+g+': '+str(gdata[0])+' <del>'+str(gdata[1])+'</del> ₽')
                            ind+=1
                            results.append([g,str(gdata[0]),gdata[4]])
                            results545.append([g,str(gdata[3]),gdata[4]])
                    lst.append('''\n\nЕсли вы хотите закупиться на скидках, введите номер игры из рассылки (например: 1).

Чтобы купить / узнать цену / добавить в избранное и следить за скидками на другую игру, нажмите "🔎 Поиск игры"''')
                    if ind>1:
                        a=self.routes.get(int(u),dict())
                        if a==dict():
                            self.routes[int(u)]=dict()
                        self.routes[int(u)]['route']='gamelist'
                        self.routes[int(u)]['gamelist']=results
                        self.routes[int(u)]['gamelist545']=results545
                        txt2=''
                        for t in lst:
                            txt2+=t
                        self.my_bot.send_message(u, txt2, parse_mode='HTML')
                    self.favo_time[u]=favo_time
                except:
                    pass
         
            
    def usd_to_rub(self,x,val): # функция рассчета цены

        
      
        k=1.11
        usd=100
        ks=[
                
        ]
        inf=399
        for st in self.price_settings:
            if st[0]==-1:
                inf=float(st[1])
            elif st[0]==-2:
                k=float(st[1])
            elif st[0]==-3:
                usd=float(st[1])
            else:
                ks.append(st)
        ks.sort()

        if val in ["AD","AE","AF","AG","AI","AL","AM","AO","AQ","AR","AS","AT","AU","AW","AX","AZ","BA","BB","BD","BE","BF","BG","BH","BI","BJ","BL","BM","BN","BO","BQ","BR","BS","BT","BV","BW","BY","BZ","CA","CC","CD","CF","CG","CH","CI","CK","CL","CM","CN","CO","CR","CU","CV","CW","CX","CY","CZ","DE","DJ","DK","DM","DO","DZ","EC","EE","EG","EH","ER","ES","ET","FI","FJ","FK","FM","FO","FR","GA","GB","GD","GE","GF","GG","GH","GI","GL","GM","GN","GP","GQ","GR","GS","GT","GU","GW","GY","HK","HM","HN","HR","HT","HU","ID","IE","IL","IM","IN","IO","IQ","IR","IS","IT","JE","JM","JO","JP","KE","KG","KH","KI","KM","KN","KP","KR","KW","KY","KZ","LA","LB","LC","LI","LK","LR","LS","LT","LU","LV","LY","MA","MC","MD","ME","MF","MG","MH","MK","ML","MM","MN","MO","MP","MQ","MR","MS","MT","MU","MV","MW","MX","MY","MZ","NA","NC","NE","NF","NG","NI","NL","NO","NP","NR","NU","NZ","OM","PA","PE","PF","PG","PH","PK","PL","PM","PN","PR","PS","PT","PW","PY","QA","RE","RO","RS","RU","RW","SA","SB","SC","SD","SE","SG","SH","SI","SJ","SK","SL","SM","SN","SO","SR","SS","ST","SV","SX","SY","SZ","TC","TD","TF","TG","TH","TJ","TK","TL","TM","TN","TO","TR","TT","TV","TW","TZ","UA","UG","UM","US","UY","UZ","VA","VC","VE","VG","VI","VN","VU","WF","WS","YE","YT","ZA","ZM","ZW"]:
         
            x*=k 
            col=-1
            for st in ks:
                if x<st[0]:
                    x*=usd
                    x+=st[1]
                    col=1
                    break
            
            if col==-1:
                x*=usd
                x+=inf
            return int(x)



        if "Yen" in val:
            orig=x
            rz=0

            mj=orig//500
            if orig%500!=0:
                mj+=1
            rz=mj*self.yen500
            
            rz*=k
            usdes=rz/usd
         #   usdes=x/self.courses['Japanese Yen']
         #   usdes*=k 
            col=-1
            for st in ks:
                if usdes<st[0]:
                    rz+=st[1]
                    col=1
                    break
            
            if col==-1:
                rz+=inf

            return int(rz)
        if "Brazil Hueta" in val:
            orig=x
            rz=0
            brz50=9.5 #usd
            brz100=19.5 #usd

            while orig>250:
                orig-=100
                rz+=brz100
            rz+=(orig//50)*brz50
            if orig%50!=0:
                rz+=brz50
            
            rz*=k
            usdes=rz + 0 
            rz = rz * usd
         #   usdes=x/self.courses['Japanese Yen']
         #   usdes*=k 
            col=-1
            for st in ks:
                if usdes<st[0]:
                    rz+=st[1]
                    col=1
                    break
            
            if col==-1:
                rz+=inf

            return int(rz)
        if "Honkbong Hueta" in val:
            orig=x
            rz=0
            hkd100=11.5 #usd
            rz+=(orig//100)*hkd100
            if orig%100!=0:
                rz+=hkd100
            
            rz*=k
            usdes=rz + 0 
            rz = rz * usd
         #   usdes=x/self.courses['Japanese Yen']
         #   usdes*=k 
            col=-1
            for st in ks:
                if usdes<st[0]:
                    rz+=st[1]
                    col=1
                    break
            
            if col==-1:
                rz+=inf

            return int(rz)
        if "Korean Hueta" in val:
            orig=x
            rz=0
            kr5000=5 #usd
            rz+=(orig//5000)*kr5000
            if orig%5000!=0:
                rz+=kr5000
            
            rz*=k
            usdes=rz + 0 
            rz = rz * usd
         #   usdes=x/self.courses['Japanese Yen']
         #   usdes*=k 
            col=-1
            for st in ks:
                if usdes<st[0]:
                    rz+=st[1]
                    col=1
                    break
            
            if col==-1:
                rz+=inf

            return int(rz)

        if 'USD' in val:
        #    m=x//10
       #     n=x%10
          #  if n>=7.99:
           #     x=(m+1)*10
          #      usd=self.price_settings2
                
          #  x*=k
            usd_needed_cards = math.ceil(x / 10) * 10
            x_cards = usd_needed_cards * k
            rub_cards = -1
            for st in ks:
                if x_cards < st[0]:
                    rub_cards = (x_cards * self.price_settings2) + st[1]
                    break
            if rub_cards == -1:
                rub_cards = (x_cards * self.price_settings2) + inf

            # --- ВАРИАНТ 2: Чистая покупка (без округления до 10) ---
            x_clean = x * k
            
            rub_clean = -1
            for st in ks:
                if x_clean < st[0]:
                    rub_clean = (x_clean * usd) + st[1]
                    break
            if rub_clean == -1:
                rub_clean = (x_clean * usd) + inf

            # Возвращаем минимальную из двух стоимостей
            return int(min(rub_cards, rub_clean))
        else:
            x*=k
        
        col=-1
        for st in ks:
             if x<st[0]:
                x*=usd
                x+=st[1]
                col=1
                break
        
        if col==-1:
            x*=usd
            x+=inf
        return int(x)

    def get_my_profit(self,y):
        k=1.11
        usd=100
        ks=[
                
        ]
        inf=399
        for st in self.price_settings:
            if st[0]==-1:
                inf=float(st[1])
            elif st[0]==-2:
                k=float(st[1])
            elif st[0]==-3:
                usd=float(st[1])
            else:
                ks.append(st)
        ks.sort()

        
        x=inf
        for st in ks:
            if float(y)<=st[0]*usd+st[1]:
                x=st[1]
                break
        
        return x
           
        
    def adbot_save(self):
            db=shelve.open(MDB_RESERV_DATA_SHELVE)
            db['users']=self.users
            db['lgames']=self.lgames
            db['dgames']=self.dgames
            db['price_settings']=self.price_settings
            db['price_settings2']=self.price_settings2
            db['favo']=self.favo
            db['favo_list']=self.favo_list
            db['favo_price']=self.favo_price
            db['favo_time']=self.favo_time
            db['users_time']=self.users_time
            db['num']=self.num
            db['loco_dct']=self.loco_dct
            db['routes']=self.routes
            db['ban_users']=self.ban_users
            db['auth']=self.auth
            db['ids']=self.ids
            db['great_dic']=self.great_dic

            db["partners"]=self.partners
            db["closed_popups"]=self.closed_popups
            db['cdc_id']=self.cdc_id
            db["yen500"]=self.yen500
            db["yen1000"]=self.yen1000
            
            db['cdc_koef']=self.cdc_koef
            db['cdc_orders']=self.cdc_orders
        #    db['great_box']=self.great_box
            db.close()


            file_path = MDB_DATA_SHELVE  # путь к файлу

            if os.path.exists(file_path):  # проверя
                os.remove(file_path)       #
            db=shelve.open(MDB_DATA_SHELVE)
            db['users']=self.users
            db['lgames']=self.lgames
            db['dgames']=self.dgames
            db['price_settings']=self.price_settings
            db['price_settings2']=self.price_settings2
            db['favo']=self.favo
            db['favo_list']=self.favo_list
            db['favo_price']=self.favo_price
            db['favo_time']=self.favo_time
            db['users_time']=self.users_time
            db['num']=self.num
            db['loco_dct']=self.loco_dct
            db['routes']=self.routes
            db['ban_users']=self.ban_users
            db['auth']=self.auth
            db['ids']=self.ids
            db['great_dic']=self.great_dic
            
            db["partners"]=self.partners
            db["closed_popups"]=self.closed_popups
            db['cdc_id']=self.cdc_id
            db["yen500"]=self.yen500
            db["yen1000"]=self.yen1000
            
            db['cdc_koef']=self.cdc_koef
            db['cdc_orders']=self.cdc_orders
        #    db['great_box']=self.great_box
            db.close()

            db=shelve.open(MDB_LOCO_RESERV_DATA_SHELVE)
            db['new_loco_dct']=self.new_loco_dct
            db['loco_list']=self.loco_list
            db["stack"]=self.stack
            db.close()


            file_path = MDB_LOCO_DATA_SHELVE  # путь к файлу

            if os.path.exists(file_path):  # проверяем, существует ли файл
                os.remove(file_path)       #

            db=shelve.open(MDB_LOCO_DATA_SHELVE)
            db['new_loco_dct']=self.new_loco_dct
            db['loco_list']=self.loco_list
            db["stack"]=self.stack
            db.close()


            file_path = MDB_LOCO_RESERV_DATA_SHELVE  # путь к файлу

            if os.path.exists(file_path):  # проверяем, существует ли файл
                os.remove(file_path)       #

            file_path = PROMOS_DATA_SHELVE  # путь к файлу

            if os.path.exists(file_path):  # проверяем, существует ли файл
                os.remove(file_path)       #

            db=shelve.open(PROMOS_DATA_SHELVE)
            db["promos"] = self.promos
            db.close()
        
    def get_courses(self):
            self.adbot_save()
            
            st_accept = "text/html" # говорим веб-серверу, 
                        # что хотим получить html
# имитируем подключение через браузер Mozilla на macOS
            st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
# формируем хеш заголовков
            headers = {
   "Accept": st_accept,
   "User-Agent": st_useragent
}
            currency='USD'
            amount=1
            content = requests.get(f"https://www.x-rates.com/table/?from={currency}&amount={amount}",headers).content
            soup = BeautifulSoup(content, "html.parser")
            exchange_tables = soup.find_all("table")
            exchange_rates = {}
            for exchange_table in exchange_tables:
                for tr in exchange_table.find_all("tr"):
                   tds = tr.find_all("td")
                   if tds:
                                 currency = tds[0].text
                                 exchange_rate = float(tds[1].text)
                                 exchange_rates[currency] = exchange_rate        
            self.time=time.time()
            exchange_rates['USD']=1
            self.courses=exchange_rates
            
    def st_in_lowst(self,st):
        if st=='Cuphead & The Delicious Last Course':
            st='Cuphead & Cuphead - The Delicious Last Course'
        st=st.lower()
        st2=''
        for su in st:
            if su in '1234567890qwertyuiopasdfghjklzxcvbnm+':
                st2+=su
            elif su=='ō':
                st2+='o'
        return st2
    def my_check(self,dct,key): # более сложная проверка
        fnd=''
        keyst=self.st_in_lowst(key)
        for st in dct:
            st25=self.st_in_lowst(st)
            if keyst==st25:
                fnd=st
                break
            dfm=0
            st11=keyst
            if len(st25)<len(st11):
                st11,st25=st25,st11
            dfm+=len(st25)-len(st11)
            for i in range(len(st11)):
                if st11[i]!=st25[i]:
                    dfm+=1
                    if st11[i].isdigit() or st25[i].isdigit():
                        dfm+=111
                        break
            if dfm<1:
                fnd=st
                break
        return fnd
    def tr_chose(self,lst,target):
        rz=''
        arr=[]
        for st in lst:
            n=0
            for word in target.split():
                if word.lower() in st.lower():
                    n+=len(word)
            arr.append(n)
        rz=lst[arr.index(max(arr))]
        return rz
    def filter_names(self,lst,target):
        rz=''
        lst2=[]
        wrnlist=['Switch', '','PlayStation Price Tracker','Xbox Price Tracker','Lowest','New lowest!','NEW', '\n\npsprices.com\n\nAll game discounts\n','settings','Matches previous low','Lowest price ever']
        wrnlist2=[r'[0-9]*',r'-[0-9]*%','[0-9]*,[0-9]*']
        wrnlist3=['sale ends']
        for st in lst:
            if st not in wrnlist:
                coll=0
                for reg in wrnlist2:
                    if (re.match(reg,st) is None or len(re.match(reg,st).group(0))!=len(st))==False:
                        coll=1
                        break
                if coll==0:
                    for wrn in wrnlist3:
                        if wrn in st.lower():
                            coll=1
                            break
                if coll==0: lst2.append(st)
        if len(lst2)==1: rz=lst2[0]
        elif len(lst2)>1: rz=self.tr_chose(lst2,target);#print('Warning: i cannt chose... but i try',lst2,rz); 
        ##print(lst2)
        return rz

    def check_update_loco(self,url,name):
        dataset_pre3=[
            ['BAh7DEkiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkU0ZjEzMjA3OWZjNWFmYTY0NjI0Njk2OGQyOGYzZTdhMzUyNGJlNzMzMTU0OTkzMDUzYmQ5Y2U5MWU3YmExZGEyBjsARkkiCWNzcmYGOwBGSSIxUnVPMWN3WkUwS3hXWE5jd2l1ZlpTdkctMDJHLUUtMl9ISFRXVjhfNWxUYz0GOwBGSSIOX19GTEFTSF9fBjsARnsASSILc291cmNlBjsARiIXaHR0cHM6Ly9lLm1haWwucnUvSSIMbGFuZGluZwY7AEZJIgYvBjsAVEkiDGNvdW50cnkGOwBGSSIHdXMGOwBUSSIJYWJpZAY7AEZJIhk5MDQyNDgxOTg2OTYxNTk0ODk5MgY7AEY%3D--be10e9f18362118284078c9f9c33b6f92eb694a7','USD'],
            ['BAh7DEkiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkU0ZjEzMjA3OWZjNWFmYTY0NjI0Njk2OGQyOGYzZTdhMzUyNGJlNzMzMTU0OTkzMDUzYmQ5Y2U5MWU3YmExZGEyBjsARkkiCWNzcmYGOwBGSSIxUnVPMWN3WkUwS3hXWE5jd2l1ZlpTdkctMDJHLUUtMl9ISFRXVjhfNWxUYz0GOwBGSSIOX19GTEFTSF9fBjsARnsASSILc291cmNlBjsARiIXaHR0cHM6Ly9lLm1haWwucnUvSSIMbGFuZGluZwY7AEZJIgYvBjsAVEkiDGNvdW50cnkGOwBGSSIHYXUGOwBUSSIJYWJpZAY7AEZJIhk5MDQyNDgxOTg2OTYxNTk0ODk5MgY7AEY%3D--a8612898686ba545d4b6801c3c9f93c642ef84b7','Canadian Dollar'],
     #       ['BAh7DEkiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkU0ZjEzMjA3OWZjNWFmYTY0NjI0Njk2OGQyOGYzZTdhMzUyNGJlNzMzMTU0OTkzMDUzYmQ5Y2U5MWU3YmExZGEyBjsARkkiCWNzcmYGOwBGSSIxUnVPMWN3WkUwS3hXWE5jd2l1ZlpTdkctMDJHLUUtMl9ISFRXVjhfNWxUYz0GOwBGSSIOX19GTEFTSF9fBjsARnsASSILc291cmNlBjsARiIXaHR0cHM6Ly9lLm1haWwucnUvSSIMbGFuZGluZwY7AEZJIgYvBjsAVEkiDGNvdW50cnkGOwBGSSIHbXgGOwBUSSIJYWJpZAY7AEZJIhk5MDQyNDgxOTg2OTYxNTk0ODk5MgY7AEY%3D--41208fa69ed74dfea5c7ee206cb4d2eea0f0d4d1','Mexican Peso'],
            ['BAh7DEkiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkU0ZjEzMjA3OWZjNWFmYTY0NjI0Njk2OGQyOGYzZTdhMzUyNGJlNzMzMTU0OTkzMDUzYmQ5Y2U5MWU3YmExZGEyBjsARkkiCWNzcmYGOwBGSSIxUnVPMWN3WkUwS3hXWE5jd2l1ZlpTdkctMDJHLUUtMl9ISFRXVjhfNWxUYz0GOwBGSSIOX19GTEFTSF9fBjsARnsASSILc291cmNlBjsARiIXaHR0cHM6Ly9lLm1haWwucnUvSSIMbGFuZGluZwY7AEZJIgYvBjsAVEkiDGNvdW50cnkGOwBGSSIHcGwGOwBUSSIJYWJpZAY7AEZJIhk5MDQyNDgxOTg2OTYxNTk0ODk5MgY7AEY%3D--f2a67ccab18be772682a6d4dca4d14dc21ce51c9','Polish Zloty'],
            ['BAh7DEkiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkU0ZjEzMjA3OWZjNWFmYTY0NjI0Njk2OGQyOGYzZTdhMzUyNGJlNzMzMTU0OTkzMDUzYmQ5Y2U5MWU3YmExZGEyBjsARkkiCWNzcmYGOwBGSSIxUnVPMWN3WkUwS3hXWE5jd2l1ZlpTdkctMDJHLUUtMl9ISFRXVjhfNWxUYz0GOwBGSSIOX19GTEFTSF9fBjsARnsASSILc291cmNlBjsARiIXaHR0cHM6Ly9lLm1haWwucnUvSSIMbGFuZGluZwY7AEZJIgYvBjsAVEkiDGNvdW50cnkGOwBGSSIHYXUGOwBUSSIJYWJpZAY7AEZJIhk5MDQyNDgxOTg2OTYxNTk0ODk5MgY7AEY%3D--a8612898686ba545d4b6801c3c9f93c642ef84b7','Australian Dollar'],
            ['BAh7DEkiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkU0ZjEzMjA3OWZjNWFmYTY0NjI0Njk2OGQyOGYzZTdhMzUyNGJlNzMzMTU0OTkzMDUzYmQ5Y2U5MWU3YmExZGEyBjsARkkiCWNzcmYGOwBGSSIxUnVPMWN3WkUwS3hXWE5jd2l1ZlpTdkctMDJHLUUtMl9ISFRXVjhfNWxUYz0GOwBGSSIOX19GTEFTSF9fBjsARnsASSILc291cmNlBjsARiIXaHR0cHM6Ly9lLm1haWwucnUvSSIMbGFuZGluZwY7AEZJIgYvBjsAVEkiDGNvdW50cnkGOwBGSSIHanAGOwBUSSIJYWJpZAY7AEZJIhk5MDQyNDgxOTg2OTYxNTk0ODk5MgY7AEY%3D--478d1fe716a71a9521675145da4702600df21a6c','Japanese Yen'],
            ['BAh7C0kiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkUyMDMxYjQxM2E2NDY2NjAyYWQwYmQ3YWE2MDQyODM4NjlkM2VkODUwZGI5NjJmMzE1Y2ZkODcwODJhNTdjY2IzBjsARkkiCWNzcmYGOwBGSSIxSXFPdzgtWWFjN3dSeHpnMlpmQXBzZ0JDTXhmcUJTVHROZWNKazlYUjFnZz0GOwBGSSIOX19GTEFTSF9fBjsARnsASSILc291cmNlBjsARiIcaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS9JIgxsYW5kaW5nBjsARkkiBi8GOwBUSSIMY291bnRyeQY7AEZJIgdnYgY7AFQ%3D--2871c24261c03fa09d98103440f42870cc4aa624','British Pound']
                ]
        url='https://www.dekudeals.com'+url
        bibi2=self.new_loco_dct.get(name,{})
        if bibi2=={}:
            self.new_loco_dct[name]={}
        for datat in dataset_pre3:
            valu=datat[1]
            coo=datat[0]
            bi2=bibi2.get(valu,[True,0])
            if bi2==[True,0] or time.time()-bi2[1]>90*24*60*60:
                cookies = {'rack.session': coo,

            }
                headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
                }        
                response = requests.get(url,  cookies=cookies, headers=headers) #params=params,
                soup = BeautifulSoup(response.content, "html.parser")
                li = soup.select('div > div > ul > li')
                for l in li:
                    txt=l.text
                    if 'Languages:' in txt:
                        if 'Russian' not in txt:
                            self.new_loco_dct[name][valu]=[False,time.time()]
                        else:
                            self.new_loco_dct[name][valu]=[True,time.time()]

    def parse_switch_games(self, api_response):
        # Если передана строка, парсим JSON
        if isinstance(api_response, str):
            data = json.loads(api_response)
        else:
            data = api_response

        result = []

        for match in data.get("matches", []):
            game_title = match.get("title")
            
            for variant in match.get("variants", []):
                game_title_tau = variant.get("title", game_title)
                # Новое поле - purchase_prices вместо base_prices
                prices = variant.get("purchase_prices", [])
                
                # Если нет purchase_prices, пробуем base_prices для обратной совместимости
                if not prices:
                    prices = variant.get("base_prices", [])

                # 1. Оставляем только Switch (игнорируем PSN, Xbox и т.д.)
                switch_prices = [p for p in prices if 'switch' in p.get("console", "").lower()]
                
                # Если не нашли по console, пробуем source_console
                if not switch_prices:
                    switch_prices = [p for p in prices if 'switch' in p.get("source_console", "").lower()]

                # 2. Для каждой консоли берем приоритетно standard edition (базовую цену игры)
                best_prices = {}
                for p in switch_prices:
                    # Используем console (или source_console как fallback)
                    console = p.get("console") or p.get("source_console")
                    tier = p.get("tier", "standard")  # если tier нет, считаем standard
                    
                    # Если еще не добавили или нашли standard (он важнее premium)
                    if console not in best_prices or tier == "standard":
                        best_prices[console] = p

                # 3. Формируем итоговый список
                for console, p in best_prices.items():
                    # Получаем цену
                    pprice = p.get("cost_usd")
                    price = float(pprice.get("price", 0))
                    
                    # Валюта/регион - берем source_region
                    currency = p.get("source_region", "USD")
                    # Обработка скидки (original_price)
                    original_price = pprice.get("original_price")
                    if original_price is None:
                        original_price = -1
                    else:
                        original_price = float(original_price)
                    
                    # Логика названий
                    if console == "switch":
                        result.append([game_title_tau, price, currency, original_price])
                    elif console == "switch_2":
                        result.append([f"{game_title_tau} [Switch 2]", price, currency, original_price])
                    else:
                        # На случай других вариаций
                        result.append([f"{game_title_tau} [{console.upper()}]", price, currency, original_price])

        return result

    def cndk_base_prices_search(self, query, limit=100):
        """POST /ext/v1/base-prices/search. Возвращает dict ответа API или None."""
        
        q = (query or "").strip()
        if len(q) < 2 or not CNDK_API_KEY:
            return None
        try:
            r = requests.get(
                    CNDK_API_BASE + "/ext/v1/purchase-prices/games",  # ← только эндпоинт поменялся
                    params={"query": q, "limit": 20,
        "include_disabled": "true",       # <-- добавлено
        "exclude_source_regions": "BR",
                "filters": {
                    "console": ["switch", "switch_2"]  # Фильтруем только Nintendo Switch
                }},
                    headers={"Authorization": "Bearer " + CNDK_API_KEY},
                    timeout=10,
                )
            if r.status_code == 200:
                return r.json()
                # 401/403/429/503/422 — не падаем, просто сообщаем админу и уходим в selenium
            self.my_bot.send_message(for_reports,f"⚠️ CNDK API {r.status_code} | query: {q}\n{r.text[:1000]}")
            return None
        except Exception as e:
            self.my_bot.send_message(for_reports,f"⚠️ CNDK API недоступен: {e}")
            return None

    def search_game(self,name,user):
            
            time_mark0=time.time()
            
            main_target=name
            
            #
            mtg = name.lower()
            mtg2=""
            for su in mtg:
                if su in '1234567890qwertyuiopasdfghjklzxcvbnm+':
                    mtg2+=su
            mtg=mtg2
            if mtg in self.fix_gms and len(self.fix_gms[mtg])>0:
                rs=[]
                gms=self.fix_gms[mtg]
                for g in gms:
                    rs.append(g.copy())

                self.my_bot.send_message(for_reports, "Мистер Кеш"+str(rs))
                return rs


            api_query = name

            api_resp = self.cndk_base_prices_search(api_query)
            try:
                if api_resp is not None:

                   # usd=100
                   # for st in self.price_settings:
                   #     if st[0]==-3:
                    #        usd=float(st[1])


                    formatted_data = self.parse_switch_games(api_resp)
                    games=formatted_data.copy()
                   # for f in games:
                      #  f[1]/=usd
                       # if f[3]!=-1:
                         #   f[3]/=usd
                    self.my_bot.send_message(for_reports, str(games))
                    
                    self.fix_gms[mtg]=games.copy()
                    #print(games)
                    
                    if len(games)>0:
                        for key in self.fix_gms:
                            fgms=self.fix_gms[key].copy()
                            for arro in fgms:
                                for i in range(len(games)):
                                    if games[i][0]==arro[0]:
                                        games[i]=arro.copy()
                                        break
                        return games
            except:
                pass
            #
            
            otchet=[]
            othcet5048_3=[]
        
            res_name=name
            results=[
        ['Игра 1',125,'ссылка 1'],
        ['Игра 2',245,'ссылка 2']
        ]
            options = Options()
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-setuid-sandbox")
            driver = wd.Chrome(options=options)
            
            #
            dxt={'breath of the wild':'Legend of zelda'}
            a=self.my_check(dxt,name)
            if a!='':
                name=dxt[a]
            
            name=name.split()
            txt=''
            for n in name:
                txt+=n+'+'
            txt=txt[:-1]
            
            
            
            games=dict()
            games2=dict()
            dls_hu=dict()

            ttxt=txt
            #
            dataset=[
 #       ['https://www.nintendo.com/us/search/#q='+ttxt+'&p=1&cat=gme&sort=rd&f=availability&availability=Available+now','USD'],
      #  ['https://www.nintendo.com/en-ca/search/#q='+ttxt+'&p=1&cat=gme&sort=rd&f=availability&availability=Available+now','Canadian Dollar'],
      #  ['https://www.nintendo.com/es-mx/search/#q='+ttxt+'&p=1&cat=gme&sort=rd&f=availability&availability=Available+now','Mexican Peso'],


    ]
            dataset_pre3=[
            ['BAh7DEkiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkU0ZjEzMjA3OWZjNWFmYTY0NjI0Njk2OGQyOGYzZTdhMzUyNGJlNzMzMTU0OTkzMDUzYmQ5Y2U5MWU3YmExZGEyBjsARkkiCWNzcmYGOwBGSSIxUnVPMWN3WkUwS3hXWE5jd2l1ZlpTdkctMDJHLUUtMl9ISFRXVjhfNWxUYz0GOwBGSSIOX19GTEFTSF9fBjsARnsASSILc291cmNlBjsARiIXaHR0cHM6Ly9lLm1haWwucnUvSSIMbGFuZGluZwY7AEZJIgYvBjsAVEkiDGNvdW50cnkGOwBGSSIHdXMGOwBUSSIJYWJpZAY7AEZJIhk5MDQyNDgxOTg2OTYxNTk0ODk5MgY7AEY%3D--be10e9f18362118284078c9f9c33b6f92eb694a7','USD'],
            ['BAh7DEkiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkU0ZjEzMjA3OWZjNWFmYTY0NjI0Njk2OGQyOGYzZTdhMzUyNGJlNzMzMTU0OTkzMDUzYmQ5Y2U5MWU3YmExZGEyBjsARkkiCWNzcmYGOwBGSSIxUnVPMWN3WkUwS3hXWE5jd2l1ZlpTdkctMDJHLUUtMl9ISFRXVjhfNWxUYz0GOwBGSSIOX19GTEFTSF9fBjsARnsASSILc291cmNlBjsARiIXaHR0cHM6Ly9lLm1haWwucnUvSSIMbGFuZGluZwY7AEZJIgYvBjsAVEkiDGNvdW50cnkGOwBGSSIHYXUGOwBUSSIJYWJpZAY7AEZJIhk5MDQyNDgxOTg2OTYxNTk0ODk5MgY7AEY%3D--a8612898686ba545d4b6801c3c9f93c642ef84b7','Canadian Dollar'],
    #        ['BAh7DEkiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkU0ZjEzMjA3OWZjNWFmYTY0NjI0Njk2OGQyOGYzZTdhMzUyNGJlNzMzMTU0OTkzMDUzYmQ5Y2U5MWU3YmExZGEyBjsARkkiCWNzcmYGOwBGSSIxUnVPMWN3WkUwS3hXWE5jd2l1ZlpTdkctMDJHLUUtMl9ISFRXVjhfNWxUYz0GOwBGSSIOX19GTEFTSF9fBjsARnsASSILc291cmNlBjsARiIXaHR0cHM6Ly9lLm1haWwucnUvSSIMbGFuZGluZwY7AEZJIgYvBjsAVEkiDGNvdW50cnkGOwBGSSIHbXgGOwBUSSIJYWJpZAY7AEZJIhk5MDQyNDgxOTg2OTYxNTk0ODk5MgY7AEY%3D--41208fa69ed74dfea5c7ee206cb4d2eea0f0d4d1','Mexican Peso'],
            ['BAh7DEkiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkU0ZjEzMjA3OWZjNWFmYTY0NjI0Njk2OGQyOGYzZTdhMzUyNGJlNzMzMTU0OTkzMDUzYmQ5Y2U5MWU3YmExZGEyBjsARkkiCWNzcmYGOwBGSSIxUnVPMWN3WkUwS3hXWE5jd2l1ZlpTdkctMDJHLUUtMl9ISFRXVjhfNWxUYz0GOwBGSSIOX19GTEFTSF9fBjsARnsASSILc291cmNlBjsARiIXaHR0cHM6Ly9lLm1haWwucnUvSSIMbGFuZGluZwY7AEZJIgYvBjsAVEkiDGNvdW50cnkGOwBGSSIHcGwGOwBUSSIJYWJpZAY7AEZJIhk5MDQyNDgxOTg2OTYxNTk0ODk5MgY7AEY%3D--f2a67ccab18be772682a6d4dca4d14dc21ce51c9','Polish Zloty'],
            ['BAh7DEkiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkU0ZjEzMjA3OWZjNWFmYTY0NjI0Njk2OGQyOGYzZTdhMzUyNGJlNzMzMTU0OTkzMDUzYmQ5Y2U5MWU3YmExZGEyBjsARkkiCWNzcmYGOwBGSSIxUnVPMWN3WkUwS3hXWE5jd2l1ZlpTdkctMDJHLUUtMl9ISFRXVjhfNWxUYz0GOwBGSSIOX19GTEFTSF9fBjsARnsASSILc291cmNlBjsARiIXaHR0cHM6Ly9lLm1haWwucnUvSSIMbGFuZGluZwY7AEZJIgYvBjsAVEkiDGNvdW50cnkGOwBGSSIHYXUGOwBUSSIJYWJpZAY7AEZJIhk5MDQyNDgxOTg2OTYxNTk0ODk5MgY7AEY%3D--a8612898686ba545d4b6801c3c9f93c642ef84b7','Australian Dollar'],
            ['BAh7DEkiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkU0ZjEzMjA3OWZjNWFmYTY0NjI0Njk2OGQyOGYzZTdhMzUyNGJlNzMzMTU0OTkzMDUzYmQ5Y2U5MWU3YmExZGEyBjsARkkiCWNzcmYGOwBGSSIxUnVPMWN3WkUwS3hXWE5jd2l1ZlpTdkctMDJHLUUtMl9ISFRXVjhfNWxUYz0GOwBGSSIOX19GTEFTSF9fBjsARnsASSILc291cmNlBjsARiIXaHR0cHM6Ly9lLm1haWwucnUvSSIMbGFuZGluZwY7AEZJIgYvBjsAVEkiDGNvdW50cnkGOwBGSSIHanAGOwBUSSIJYWJpZAY7AEZJIhk5MDQyNDgxOTg2OTYxNTk0ODk5MgY7AEY%3D--478d1fe716a71a9521675145da4702600df21a6c','Japanese Yen'],
            ['BAh7C0kiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkUyMDMxYjQxM2E2NDY2NjAyYWQwYmQ3YWE2MDQyODM4NjlkM2VkODUwZGI5NjJmMzE1Y2ZkODcwODJhNTdjY2IzBjsARkkiCWNzcmYGOwBGSSIxSXFPdzgtWWFjN3dSeHpnMlpmQXBzZ0JDTXhmcUJTVHROZWNKazlYUjFnZz0GOwBGSSIOX19GTEFTSF9fBjsARnsASSILc291cmNlBjsARiIcaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS9JIgxsYW5kaW5nBjsARkkiBi8GOwBUSSIMY291bnRyeQY7AEZJIgdnYgY7AFQ%3D--2871c24261c03fa09d98103440f42870cc4aa624','British Pound'],
            
            ['BAh7D0kiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkU0OTk5MWFiZmU0MzNkN2YzNjY4ZmUwZjk5OGIxODhiMWY0MGRlNWZmMDllNzk0NjZlOWM5ZDJmNjliYWEwYzMyBjsARkkiCWNzcmYGOwBGSSIxdjVhaTdUU3l2dl9oOVdFbmpBenhLLU1QR2dqOHdYMGNOc1F0QWhyLWlJMD0GOwBGSSIOX19GTEFTSF9fBjsARnsASSIMY291bnRyeQY7AEZJIgdubwY7AFRJIgtzb3VyY2UGOwBGIhdodHRwczovL3lhbmRleC5ydS9JIgxsYW5kaW5nBjsARkkiBi8GOwBUSSIVcGxhdGZvcm1fZmlsdGVycwY7AEZ7BzoNc3dpdGNoXzI6DGRpZ2l0YWw6C3N3aXRjaDsJSSINc3BlY2lhbHMGOwBGWwBJIhFzd2l0Y2hfMl9zZXQGOwBGaQZJIhBicm93c2VfdmlldwY7AEY6CWxpc3Q%3D--f3bff436787bb6c48de0a8c358a2d9e1baf02609','Norwegian Krone'],
            ['BAh7D0kiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkU0OTk5MWFiZmU0MzNkN2YzNjY4ZmUwZjk5OGIxODhiMWY0MGRlNWZmMDllNzk0NjZlOWM5ZDJmNjliYWEwYzMyBjsARkkiCWNzcmYGOwBGSSIxdjVhaTdUU3l2dl9oOVdFbmpBenhLLU1QR2dqOHdYMGNOc1F0QWhyLWlJMD0GOwBGSSIOX19GTEFTSF9fBjsARnsASSIMY291bnRyeQY7AEZJIgdzZQY7AFRJIgtzb3VyY2UGOwBGIhdodHRwczovL3lhbmRleC5ydS9JIgxsYW5kaW5nBjsARkkiBi8GOwBUSSIVcGxhdGZvcm1fZmlsdGVycwY7AEZ7BzoNc3dpdGNoXzI6DGRpZ2l0YWw6C3N3aXRjaDsJSSINc3BlY2lhbHMGOwBGWwBJIhFzd2l0Y2hfMl9zZXQGOwBGaQZJIhBicm93c2VfdmlldwY7AEY6CWxpc3Q%3D--c98bfc1ec8c69dba5e8b8d370dcfb5987c00f058','Swedish Krona'],
            
         #   ['BAh7C0kiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkU0OTk5MWFiZmU0MzNkN2YzNjY4ZmUwZjk5OGIxODhiMWY0MGRlNWZmMDllNzk0NjZlOWM5ZDJmNjliYWEwYzMyBjsARkkiCWNzcmYGOwBGSSIxdjVhaTdUU3l2dl9oOVdFbmpBenhLLU1QR2dqOHdYMGNOc1F0QWhyLWlJMD0GOwBGSSIOX19GTEFTSF9fBjsARnsASSIMY291bnRyeQY7AEZJIgdicgY7AFRJIgtzb3VyY2UGOwBGIhdodHRwczovL3lhbmRleC5ydS9JIgxsYW5kaW5nBjsARkkiBi8GOwBU--308a5f479b0b21bfbfbdfb178702c5d73469232d','Brazilian Real'],
           # ['BAh7C0kiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkUyMDMxYjQxM2E2NDY2NjAyYWQwYmQ3YWE2MDQyODM4NjlkM2VkODUwZGI5NjJmMzE1Y2ZkODcwODJhNTdjY2IzBjsARkkiCWNzcmYGOwBGSSIxSXFPdzgtWWFjN3dSeHpnMlpmQXBzZ0JDTXhmcUJTVHROZWNKazlYUjFnZz0GOwBGSSIOX19GTEFTSF9fBjsARnsASSILc291cmNlBjsARiIcaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS9JIgxsYW5kaW5nBjsARkkiBi8GOwBUSSIMY291bnRyeQY7AEZJIgdnYgY7AFQ%3D--2871c24261c03fa09d98103440f42870cc4aa624','British Pound'],
            
               ]


            dataset78=[
                ["https://eshop-prices.com/games?platform=switch&oic=BR&q="+ttxt,"Brazil Hueta"],
                ["https://eshop-prices.com/games?platform=switch&oic=HK&q="+ttxt,"Honkbong Hueta"],
                ["https://eshop-prices.com/games?platform=switch&oic=KR&q="+ttxt,"Korean Hueta"],
            ]
                
            time_mark1=time.time()-time_mark0

           
            pgama=1
            for minidata in dataset78:
                coo = minidata[0]
                valu = minidata[1]
                search = ttxt

                cookies = {
                    '__cmpcc': '1',
                    '__cmpconsentx66181': 'CQZ1xggQZ1xggAfC1BENCCFsAP_gAEPgAAigLPtR_C_fbWlj-TL3afskeYxP99hr5sQxBgLJg04BzDrW5JwTx2EwNEzShqAKmRIAqnRBIQFlGAjURUAAIIAVJSDMYESUgRNIJuBAgFMRAwNYCFhnmYtBGQCRwkpxchZgmRsM6Vrs2NxAw4gDPUSRIyQlUJgNAYMoCQmsZBKT85IEd-x8v4vw9F7oE2-eSVn_pCtp6h8IABAAJAAgAAAABAAAAAAABIQAAAAAUAAAEAgEAAAAAAgreACYKFRBCWBAAEAgYQQIAFBWEAFAgCAAAIGiAgBMGBTkDABVYTIAQAIAAAgBAACCAAEAAAkACEQAQAEAgAAgACgABAAAAAgAYEAAMAFCABAACAaBikABAIFAAkJhEGCBCAAgEALYUABAECAsAIQBoABAiAgIAAAQACgIAAHgsBCSQErEggCwgmgAAIAAAogQIEUhRgAAAAAEACAAACAEAAAAAAAABAAAAAAQAAAACAAA',
                    '__cmpcccx66181': 'aCQZ4hU-gADAdrnjD3mZz00xjNY56zvGTMM5nX3z83eYe2OG1jWWDMaZ3zxpoY62Z56xjMae-3jw95Z2dsmcfPvGGs55rRnePZrNMZ7Ze8saGZZjGO-PXP3zzjaM0wyZ48Yxw8syxzzGWasaNaY7yzDPemNMM54tTB14MxiZYYZhka00wxlp4eZWjF4zBh7eDxk0Ofeco8wYMmQ56mVgWhjNdHgyY9tZGBlOHlNMBgZMsjGmjTNTBmrCZaGTHQ81iacXg8PHnneLE6NgM48MYx4eI0Y0ZYNLLTxsYd5pzzCZGCYWjHDxMPeEwMMHvJ62jVho0NZhZzy0dbQw0uB548xjOPTLLGu3bXfN32553pjJjGsl33q0ZahxeYsRmmsrrzJ49YaaDltDRmMMLk8uE2gZWSMLTNDnrAYYaWBgtQwAZIIi8A',
                    '_sharedID': '988e1ed7-0769-478a-ad05-ac33d7a45f7c',
                    '_sharedID_cst': 'KSw%2FLOYstg%3D%3D',
                    'pbjs-unifiedid': '%7B%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222025-10-25T17%3A00%3A17%22%7D',
                    'pbjs-unifiedid_cst': 'KSw%2FLOYstg%3D%3D',
                    '_cc_id': '298e7ac3d13204852441ac8f9cf17e3f',
                    '__aim_p': '1334c3d515df717b5e5c5a2137fa64ed865612ccf8a854924f88b0c5270fdaaf',
                    'cf_clearance': 'nhKnqYwvhodwHzco3.iD0shDA.2YpaYW.qgRd3Fa1TY-1762257145-1.2.1.1-77JT4OBiqsiazfbc6cCU9GelNXVrgo0LHYEp3x4ww.yhm.ZpWVKhggXw_07YwYsCqk6p_vTrS7X.f9AGtbZTjJjJniewexvRLNd.0FiAmiTphjzexpG7JIJARADbNb1aNtFieBiEwvxh3Y5J4ssuVpQWtBpzIUSX1Me_e5hO1fX60hpe.QLvkkOvKDgYu9yCy6Ju_V.GMAUNJSeElMh9lPXTCvBLLiMmZ6h21HwUdgs',
                    'FCCDCF': '%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5B32%2C%22%5B%5C%222de7d200-02d4-469d-9936-844279e25668%5C%22%2C%5B1762257148%2C188000000%5D%5D%22%5D%5D%5D',
                    'connectId': '{"ttl":86400000,"lastUsed":1762257148808,"lastSynced":1762257148808}',
                    'fidsdk_consent': '1',
                    'firstid': '6152e47766df4f1490024597e92953c3',
                    'firstid_flex_type': '0',
                    '__aim_f': '25a8fd95cc98ecbee66a94c6d86bfa992143484330346b15b50b2bb19c8140d2',
                    '__gads': 'ID=8be901224b8a7657:T=1762257148:RT=1762270295:S=ALNI_MYgqhQPBKm7xel5BaxBB-xa6CLGPg',
                    '__gpi': 'UID=00001307f5ef6720:T=1762257148:RT=1762270295:S=ALNI_MbzQjuiGudcjC7zZoZwAwxRhTvEKw',
                    '__eoi': 'ID=02d2da34799cebf8:T=1762257148:RT=1762270295:S=AA-AfjZZJTOfd7f43x_J0W90l15V',
                }

                headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'ru,en;q=0.9',
                    'cache-control': 'no-cache',
                    'pragma': 'no-cache',
                    'priority': 'u=0, i',
                    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "YaBrowser";v="25.10", "Yowser";v="2.5"',
                    'sec-ch-ua-arch': '"x86"',
                    'sec-ch-ua-bitness': '"64"',
                    'sec-ch-ua-full-version': '"25.10.0.2474"',
                    'sec-ch-ua-full-version-list': '"Chromium";v="140.0.7339.2474", "Not=A?Brand";v="24.0.0.0", "YaBrowser";v="25.10.0.2474", "Yowser";v="2.5"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-model': '""',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-ch-ua-platform-version': '"19.0.0"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 YaBrowser/25.10.0.0 Safari/537.36',
                }

 
                response = requests.get(coo,  cookies=cookies, headers=headers)
                soup = BeautifulSoup(response.content, "html.parser")
                
                # Парсим результаты
                game_items = soup.select('a.games-list-item')
                
                for item in game_items:
                    try:
                        # Название игры
                        title_elem = item.select_one('.games-list-item-title h5')
                        if not title_elem:
                            continue
                            
                        game_title = title_elem.text.strip()
                        
                        # Цена
                        price_elem = item.select_one('.price-tag')
                        if not price_elem:
                            continue
                            
                        price_text = price_elem.text.strip()
                        
                        # Парсим цену (аналогично твоему коду)
                        vl = ''
                        for su in price_text:
                            if su in '1234567890.,':
                                vl += su
                        
                        # Обработка формата цены
                        if vl and len(vl) >= 3 and vl[-3] == ',':
                            vl = vl[:-3] + '.' + vl[-2:]
                        
                        ind6 = vl.find(',')
                        if ind6 != -1: 
                            vl = vl[:ind6] + vl[ind6+1:]
                        
                        try:
                            price_value = float(vl)
                        except:
                            continue
                        
                        # Обработка названия игры
                        st2 = self.filter_names([game_title], main_target)
                        if st2 != '':
                            ind6 = st2.find('™')
                            if ind6 != -1: 
                                st2 = st2[:ind6] + st2[ind6+1:]
                            
                            a = self.my_check(games, st2)
                            if a == '':
                                games[st2] = []
                                avr = st2
                                games[avr].append([price_value, valu])
                                pgama+=1
                                if f'eShop-Prices {valu}' not in otchet: 
                                    otchet.append(f'eShop-Prices {valu}')
                                if 'eShop-Prices' not in othcet5048_3: 
                                    othcet5048_3.append('eShop-Prices')
                            elif a != '':
                                st2 = a
                                avr = st2
                                games[avr].append([price_value, valu])
                                pgama+=1
                                if f'eShop-Prices {valu}' not in otchet: 
                                    otchet.append(f'eShop-Prices {valu}')
                                if 'eShop-Prices' not in othcet5048_3: 
                                    othcet5048_3.append('eShop-Prices')
                                    
                    except Exception as e:
                        # Логируй ошибку если нужно
                        pass

            if pgama>0:
                send_report("parser_popugEShop", "ya")
            pgama=0
            for minidata in dataset_pre3:
                coo=minidata[0]
                valu=minidata[1]
                search=ttxt
                

                cookies = {'rack.session': coo,

}

                headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',

                }

                
                url2='https://www.dekudeals.com/search?q='+ttxt+"&filter[platform]=switch"
                if valu in ['USD','Canadian Dollar','British Pound']:
                    url2+='&filter[format]=digital'
                    url2+='&filter[shop]=eshop'
                    url2+='&filter[store]=eshop'
                elif valu=='Australian Dollar':
                    url2+='&filter[format]=digital&filter[store]=eshop_au'
                elif valu=="Japanese Yen":
                    url2+="&filter[store]=eshop_jp&filter[format]=digital"
                #self.my_bot.send_message(for_reports, url2+' '+valu)          
                response = requests.get(url2,  cookies=cookies, headers=headers) #params=params,
                soup = BeautifulSoup(response.content, "html.parser")
                alldiv=soup.select('div > div > div > div > div')
                #skip=1
                skip=0
                #self.my_bot.send_message(for_reports, str(games)+' '+valu) 
                for div in alldiv:
                    #
                    
                    #
                    
                    txt=div.text
                    #print(txt)£49.99
                    if ('kr' in txt or 'zł' in txt or '$' in txt  or '￥' in txt or '¥' in txt or '£' in txt) and skip==0:
                        
                        try:
                            vl255=[]
                            lasts2=txt.split('\n')
                            lasts=[]
                            vl=0
                            for st in lasts2:
                                if st=='':
                                    pass
                                elif 'kr' in st or 'zł' in st or '$' in st  or '￥' in st or '¥' in st or '£' in txt:
                                    
                                    vl=''
                                    for su in st:
                                        if su in '1234567890.,':
                                            vl+=su
                                    if vl[-3]==',':
                                        vl=vl[:-3]+'.'+vl[-2:]
                                    ind6=vl.find(',')
                                    if ind6!=-1: vl=vl[:ind6]+vl[ind6+1:]
                                    vl255.append(float(vl))
                                else:
                                    lasts.append(st)
                                    
                            for vl in vl255:
                                #print(vl)
                                if vl!=0:
                                    st2=self.filter_names(lasts,main_target)
                                    if st2!='':
                                        ind6=st2.find('™')
                                        if ind6!=-1: st2=st2[:ind6]+st2[ind6+1:]
                                        a=self.my_check(games,st2)
                                        if a=='' and (valu!='Japanese Yen' or st2 in ["Merry Bunny Garden"]):
                                            games[st2]=[];avr=st2;games[avr].append([vl,valu])
                                            pgama+=1
                                            if 'DekuDeals '+valu not in otchet: otchet.append('DekuDeals '+valu)
                                            if 'DekuDeals' not in othcet5048_3: othcet5048_3.append('DekuDeals')
                                        elif a!='':
                                            st2=a;avr=st2;games[avr].append([vl,valu])
                                            pgama+=1
                                            if 'DekuDeals '+valu not in otchet: otchet.append('DekuDeals '+valu)
                                            if 'DekuDeals' not in othcet5048_3: othcet5048_3.append('DekuDeals')
                                        #print(avr,games[avr])
                                        try:
                                            aa=div.select('a')
                                            for a in aa:
                                                mdba=[a['href'],avr]
                                                if mdba not in self.loco_list:
                                                    self.loco_list.append(mdba)
                                            #    self.check_update_loco(a['href'],avr)
                                                break
                                        except Exception as e:
                                            pass
                        except:
                            pass
                
                url2='https://www.dekudeals.com/search?q='+ttxt+"&filter[platform]=switch_2"
                if valu in ['USD','Canadian Dollar','British Pound']:
                    #params['filter[format]']='digital'
                    #params['filter[store]']='eshop'
                    url2+='&filter[format]=digital'
                    url2+='&filter[shop]=eshop'
                    url2+='&filter[store]=eshop'
                elif valu=='Australian Dollar':
                    url2+='&filter[format]=digital&filter[store]=eshop_au'
                elif valu=="Japanese Yen":
                    url2+="&filter[store]=eshop_jp&filter[format]=digital"
                #self.my_bot.send_message(for_reports, url2+' '+valu)          
                response = requests.get(url2,  cookies=cookies, headers=headers) #params=params,
                soup = BeautifulSoup(response.content, "html.parser")
                alldiv=soup.select('div > div > div > div > div')
                #skip=1
                skip=0
                #self.my_bot.send_message(for_reports, str(games)+' '+valu) 
                for div in alldiv:
                    #
                    
                    #
                    
                    txt=div.text
                    #print(txt)£49.99
                    if ('kr' in txt or 'zł' in txt or '$' in txt  or '￥' in txt or '¥' in txt or '£' in txt) and skip==0:
                        
                        try:
                            vl255=[]
                            lasts2=txt.split('\n')
                            lasts=[]
                            vl=0
                            for st in lasts2:
                                if st=='':
                                    pass
                                elif 'kr' in st or 'zł' in st or '$' in st  or '￥' in st or '¥' in st or '£' in txt:
                                    
                                    vl=''
                                    for su in st:
                                        if su in '1234567890.,':
                                            vl+=su
                                    if vl[-3]==',':
                                        vl=vl[:-3]+'.'+vl[-2:]
                                    ind6=vl.find(',')
                                    if ind6!=-1: vl=vl[:ind6]+vl[ind6+1:]
                                    vl255.append(float(vl))
                                else:
                                    lasts.append(st)
                                    
                            for vl in vl255:
                                #print(vl)
                                if vl!=0:
                                    st2=self.filter_names(lasts,main_target)
                                    if st2!='':
                                        ind6=st2.find('™')
                                        if ind6!=-1: st2=st2[:ind6]+st2[ind6+1:]
                                        a=self.my_check(games,st2)
                                        #print(a,vl,valu)
                                        #print(games.get(a,""))
                                        if a=='' and valu!='Japanese Yen':
                                            games[st2]=[];
                                            avr=st2;
                                            avr+=" [Switch 2]"
                                            games[avr].append([vl,valu])
                                            pgama+=1

                                            if 'DekuDeals '+valu not in otchet: otchet.append('DekuDeals '+valu)
                                            if 'DekuDeals' not in othcet5048_3: othcet5048_3.append('DekuDeals')
                                        elif a!='':
                                            colli=0
                                            #if [vl,valu] not in games[a]:
                                            #    colli=1

                                            st2=a;
                                            avr=st2;
                                            #if colli==1:
                                            avr+=" [Switch 2]"
                                            if avr not in games: games[avr]=[]
                                            games[avr].append([vl,valu])
                                            pgama+=1
                                            if 'DekuDeals '+valu not in otchet: otchet.append('DekuDeals '+valu)
                                            if 'DekuDeals' not in othcet5048_3: othcet5048_3.append('DekuDeals')
                                        #print(avr,games[avr])
                        except:
                            pass
            

            if pgama>0:
                send_report("parser_popugDekuDeals", "ya")
            pgama=0
            time_mark5=time.time()-time_mark0
           # print(otchet)
            if 'DekuDeals USD' not in otchet: dataset.append(['https://www.nintendo.com/us/search/#q='+ttxt+'&p=1&cat=gme&sort=rd&f=availability&availability=Available+now','USD'])
            if 'DekuDeals Canadian Dollar' not in otchet: dataset.append(['https://www.nintendo.com/en-ca/search/#q='+ttxt+'&p=1&cat=gme&sort=rd&f=availability&availability=Available+now','Canadian Dollar'])

            
            
            
            for minidata in dataset:
                url=minidata[0]
                valu=minidata[1]
                driver.get(url)
                time.sleep(3)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                ##print(driver.page_source)
                alldiv = soup.select('div > div > div > div')
                for div2 in alldiv:
                    ##print(div2)
                    if div2 is not None and 'Nintendo Switch' in div2.text and ('Regular Price:' in div2.text or 'Precio' in div2.text):
                        ##print(div2)
                        
                        st2=div2.find('h3').text
                      #  #print(div2)
                        if st2 is not None:
                            #
                            ind6=st2.find('™')
                            if ind6!=-1: st2=st2[:ind6]+st2[ind6+1:]
                            
                            if ('DLC' in div2.text or 'Dlc' in div2.text or 'dlc' in div2.text) and ('game +' not in div2.text.lower()):
                                dls_hu[st2]=' (dlc)'
                           
                           # print(st2)
                            a=self.my_check(games,st2)
                            if a=='' and valu in ['USD','Canadian Dollar']: games[st2]=[]
                            elif a!='': st2=a
                            else: break
                            avr=st2
                            #
                            span=div2.find_all('span')
                            for sp in span:
                                
                                if sp is not None and ('Price:' in sp.text or 'Precio' in sp.text):
                                    if valu=='USD' or valu=='Canadian Dollar':
                                        if len(sp.text)>15 and ('Current Price:' in sp.text or 'Regular Price:' in sp.text):
                                            try:
                                                st=sp.text[15:]
                                                while st.find(',')!=-1:
                                                    ind9=st.find(',')
                                                    if ind9!=-1 and ind9<len(st)-3: st=st[:ind9]+st[ind9+1:]
                                                    else: break
                                                games[avr].append([float(st),valu])
                                                pgama+=1
                                                if 'Official '+valu not in otchet: otchet.append('Official '+valu)
                                                if 'Official' not in othcet5048_3: othcet5048_3.append('Official')
                                            except Exception as e:
                                                aeeriop89=0
                                                print(e)
                                    elif valu=='Mexican Peso':
                                        if len(sp.text)>20 and 'Precio promocional:' in sp.text:
                                            try:
                                                st=sp.text[20:]
                                                while st.find(',')!=-1:
                                                    ind9=st.find(',')
                                                    if ind9!=-1 and ind9<len(st)-3: st=st[:ind9]+st[ind9+1:]
                                                    else: break
                                                games[avr].append([float(st),valu])
                                                pgama+=1
                                                if 'Official '+valu not in otchet: otchet.append('Official '+valu)
                                                if 'Official' not in othcet5048_3: othcet5048_3.append('Official')
                                            except:
                                                aeeriop89=0
                                        elif len(sp.text)>15 and 'Precio normal:' in sp.text:
                                            try:
                                                st=sp.text[15:]
                                                while st.find(',')!=-1:
                                                    ind9=st.find(',')
                                                    if ind9!=-1 and ind9<len(st)-3: st=st[:ind9]+st[ind9+1:]
                                                    else: break
                                                games[avr].append([float(st),valu])
                                                pgama+=1
                                                if 'Official '+valu not in otchet: otchet.append('Official '+valu)
                                                if 'Official' not in othcet5048_3: othcet5048_3.append('Official')
                                            except:
                                                aeeriop89=0
            
            driver.quit()
            

            if pgama>0:
                send_report("parser_popugNintendo", "ya")
            time_mark4=time.time()-time_mark0
            if user !='':
                gtxt=random.choice([
"⌛️ Почти нашел...",
"⌛️ Еще несколько секунд...",
"⌛️ В процессе поиска...",
"⌛️ Почти готово...",
                ])
                self.my_bot.send_message(user, gtxt)

                
            

            for game in games:
                coll=[0,0,0,0]
                minds=['Polish Zloty','Japanese Yen','Swedish Krona','Norwegian Krone','British Pound']
                for m in games[game]:
                    for mind in range(4):
                        if m[1]==minds[mind]:
                            coll[mind]=1
                if game not in ['Dying Light: Definitive Edition','Dying Light: Definitive Edition & Call of Juarez: Gunslinger','Saints Row: The Big Purple Package','Metro Redux','Cult of the Lamb - Cultist, Heretic, and Sinful Pack Bundle',"Merry Bunny Garden"]:
                    if 1 not in coll or 'Minecraft: Nintendo Switch Edition' in game:
                        games[game]=[]
                if "S.T.A.L.K.E.R." in game:
                    games[game]=[]
                
            for key in dls_hu:
                a=games.get(key,'')
                if a!='':
                    b=key
                    b+=dls_hu[key]
                    games[b]=games[key]
                    games.pop(key)
                    
            #print(games)      
          #  self.my_bot.send_message(for_reports, str(games))                          
            time_mark2=time.time()-time_mark0
            valuD=self.courses

        #    try:
         #       self.my_bot.send_message(for_reports, str(games))
         #   except:
          #      pass

            valuD['USD']=1
            valuD['USD+']=1
            valuD['Canadian Dollar']/=1.05
            #print(games)
            for key in games:
                prices=[]
                for p in games[key]:
                    if p[0]>0:
                        if "Yen" in p[1] or "Hueta" in p[1]:
                            prices.append([self.usd_to_rub(p[0],p[1]),p[0],p[1]]) #!!
                        else:
                            prices.append([self.usd_to_rub(p[0]/valuD[p[1]],p[1]),p[0]/valuD[p[1]],p[1]]) #!!
                p2=games2.get(key,[])
                if p2!=[]: prices.append(p2)
                prices.sort()
                #print(prices)
                if len(prices)>0:
                    games2[key]=[prices[0].copy(),-1]
                    games2[key][0].pop(0)
                    mn=prices[0][0],prices[0][1]+0
                    vl=prices[0][2]
                    ind89=1
                    while ind89<len(prices):
                        if prices[ind89][2]==vl:
                            mn=prices[ind89][0], prices[ind89][1]
                        ind89+=1
                    if mn[1]!=prices[0][1] and prices[0][0]!=mn[0]: games2[key][1]=mn[1]
            games3=[]
            for key in games2:
                games3.append([key,games2[key][0][0],games2[key][0][1],games2[key][1]])
            games=[]
            spt=res_name.split()
            games45=[]
            
            rs_name2=res_name.lower()
            rs_name=''
            for su in rs_name2:
                if su in '1234567890qwertyuiopasdfghjklzxcvbnm ': rs_name+=su
           
            for i in range(len(games3)):

                arr=games3[len(games3)-1-i]
                coll=0
                
                if 'dlc' not in arr[0]:
                    for word in spt:
                        if len(word)>2:
                            st569=''
                            for su in arr[0].lower():
                                if su in '1234567890qwertyuiopasdfghjklzxcvbnm ':
                                    st569+=su
                            if rs_name in st569:
                                coll=2
                                break
                            if word.lower() in st569:
                                coll=1
                                break
                    if coll==2:
                        #print(2,arr)
                        games.insert(0,arr)
                    elif coll==1:
                        #print(1,arr)
                        games.insert(len(games),arr)
                    else:
                        #print(0,arr)
                        games45.insert(0,arr)
                else:
                    for word in spt:
                        if len(word)>2:
                            st569=''
                            for su in arr[0].lower():
                                if su in '1234567890qwertyuiopasdfghjklzxcvbnm':
                                    st569+=su
                            if word.lower() in st569:
                                coll=1
                                break
                    if coll==1:
                        #print("dlc1",arr)
                        games.append(arr)
                    else:
                        #print("dlc0",arr)
                        games45.append(arr)
            games+=games45
            #print(games)
            #print(games45)
           # print(games)
            #print(otchet)

            # ебать костыль для 2 свитча
            dfg=[]
            for i in range(len(games)):
                if "[Switch 2]" in games[i][0]:
                    dfg.append(i)
            dfg2=[]
            for i in range(len(dfg)):
                dfg2.append(games.pop(dfg[-1-i]))
            for i in range(len(dfg2)):
                nmj=dfg2[i][0][:-len(" [Switch 2]")]
                colli=-1
                for j in range(len(games)):
                    if games[j][0]==nmj:
                        colli=j
                        break
                if colli!=-1:
                    games.insert(colli,dfg2[i])
                else:
                    games.insert(0,dfg2[i])
            #
            # а теперь ебать костыль на фльтр длс
            dfg=[]
            for i in range(len(games)):
                if "upgrade pack" in games[i][0].lower():
                    dfg.append(i)
            dfg2=[]
            for i in range(len(dfg)):
                dfg2.append(games.pop(dfg[-1-i]))
            games+=dfg2
            #

            otchet2=''
            time_mark3=time.time()-time_mark0

            if otchet2=='':
                arr=['USD','Canadian Dollar','Mexican Peso','Polish Zloty','Norwegian Krone','Swedish Krona','Australian Dollar','Japanese Yen']
                arr2=[]
                for su in arr:
                    coll=0
                    for st in otchet:
                        if su in st:
                            coll=1
                            break
                    if coll==0: arr2.append(su)
                if len(arr2)!=0:
                    othcet2='Запрос: '+main_target+'\n'
                    othcet2+='Нет данных из следующих регионов: '
                    for su in arr2:
                        otchet2+=su+', '
            #if otchet2!='':
                #self.my_bot.send_message(for_reports, otchet2+ttxt)
            othcet5048_3=str(othcet5048_3)
            
            othcet5048_3+='\n'+str(time_mark1)
            othcet5048_3+='\n'+str(time_mark2)
            othcet5048_3+='\n'+str(time_mark3)
            othcet5048_3+='\n official end '+str(time_mark4)
            othcet5048_3+='\n dd end '+str(time_mark5)
            
            #if othcet5048_3!="['Official', 'DekuDeals', 'PSP', 'NTDeals']":
                #self.my_bot.send_message(for_reports, othcet5048_3+' '+ttxt)
            self.fix_gms[mtg]=games.copy()
            #print(games)
            
            for key in self.fix_gms:
                fgms=self.fix_gms[key].copy()
                for arro in fgms:
                    for i in range(len(games)):
                        if games[i][0]==arro[0]:
                            games[i]=arro.copy()
                            break
            
            self.my_bot.send_message(for_reports, "Мистер Смеш"+str(games))

            return games
            
        
bot=Bot()




@bot.my_bot.message_handler(content_types=['photo'])
def get_photo(message):
   
       route=bot.routes.get(message.from_user.id,dict())
       if route==dict(): bot.routes[message.from_user.id]={'route':'start'}
       route=route.get('route','start')
       if route=='au_rassu':
            bot.original_message_id = message.id
            bot.from_chat_id = message.chat.id
            bot.rassu_photo=message.photo[0].file_id
            bot.routes[message.from_user.id]['route']='au_rassu2'
            bot.my_bot.copy_message(
                            chat_id=message.from_user.id, 
                            from_chat_id=bot.from_chat_id, # ID чата, откуда берем оригинал
                            message_id=bot.original_message_id # ID того самого сообщения с эмодзи
                        )
            bot.my_bot.send_message(message.from_user.id,'Подвердите рассылку (/accept) или выберите команду отмены (/back)',reply_markup=bot.markup2)
       if route=='au_lpr': #'au_lpr'
            bot.rassu_photo2=message.photo[0].file_id
            bot.my_bot.send_message(message.from_user.id, 'Изображение загружено', reply_markup=bot.markup2)
    





def escape_md_v2(text):
    """Экранирует спецсимволы для MarkdownV2"""
    if not text:
        return ""
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    regex = re.compile(f'([{re.escape(escape_chars)}])')
    return regex.sub(r'\\\1', text)
                       
                       
@bot.my_bot.message_handler(content_types=['text'])
def get_text_messages(message):
    try:
        chat = message.chat
        if message.chat.type in ["group", "supergroup", "channel"]:
            try:
                if chat.username:
                    link = f"https://t.me/{chat.username}"
        
                    bot.my_bot.send_message(for_reports, f"Ссылка на этот чат: {link}")
                    
            except:
                pass
            return None
            a=1/0
        ddos=bot.check_rate_limit(message.from_user.id)
        if ddos==False:
            bot.my_bot.send_message(for_reports, f"[DDOS] от {message.from_user.id}")
        bot.users_time[str(message.from_user.id)]=time.time()
        if str(message.from_user.id) not in bot.users and str(message.from_user.id) not in bot.ids:
            bot.users[str(message.from_user.id)]=1
         #   prv='''Привет! Я создан, чтобы помогать покупать игры в Nintendo eShop по самой низкой цене. Если у тебя есть вопросы, нажми «📜 Другое», «FAQ» или используй кнопку «🔎 Поиск игры», чтобы найти интересующую игру / DLC.'''
         #   bot.my_bot.send_message(message.from_user.id, prv)
        markup=bot.markup
        if str(message.from_user.id)  in bot.ids:
            markup=bot.markup2

        if str(message.from_user.id)  in bot.popuski:
            markup=bot.markup3

        
        if str(message.from_user.id)=="832182441" or str(message.from_user.id)=="5266773307":
            markup=bot.markup2d
        route=bot.routes.get(message.from_user.id,dict())
        if route==dict(): bot.routes[message.from_user.id]={'route':'start'}
        route=route.get('route','start')
        if str(message.from_user.id) in bot.ban_users:
            pass
    # получаем режим написавшего пользователя и в зависимости от режима выбираем функцию, формирующую ответ
        elif message.text=="🧧 Nintendo Switch Online" or ("/start" in message.text and message.text!='/start' and "NintendoSwitchOnline" in message.text):

            cdc=[]
            try:
                for arti in bot.subs:
                    pass
            except:
                bot.reload_popup()
            for arti in bot.subs:
                n=len(bot.popups_codes.get(arti,[]))
                dct=bot.subs[arti].copy()
                dct["Количество"]=n
                if n>=0:
                    cdc.append(dct)
            

            #
            bw_discount_active = bot.has_big_walk_discount(message.from_user.id)
            msg="По Вашему запросу найдено:\n\n"
            i=1
            markupin=types.InlineKeyboardMarkup()
            for offer in cdc:
                display_price = offer['Цена в рублях']
                # Применяем скидку на NSO 1 мес
                if bw_discount_active and bot.is_nso_1month(offer):
                    display_price = NSO_1M_DISC_PRICE
                    msg += f"{i}. {offer['Наименование']} - {display_price} ₽ <s>{offer['Цена в рублях']}</s> ₽ 🔥\n"
                else:
                    msg += f"{i}. {offer['Наименование']} - {display_price} ₽\n"
                
              #  msg+=f"{i}. {offer['Наименование']} - {offer['Цена в рублях']} ₽\n"
                hj=f"{i}. {offer['Наименование']}"[:40]+f" - {offer['Цена в рублях']} ₽"
                markupin.add(types.InlineKeyboardButton(hj,callback_data='subbuy_'+offer['Артикул']))
                i+=1
            
            my_popug= SWITCH_POPUG_PNG
            with open(my_popug, 'rb') as photo:
                bot.my_bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo,  # Передаем файловый объект
                    caption=msg,
                    
                    reply_markup=markupin,
                    parse_mode='HTML'
                )

        elif "/start promo_" in message.text:
            promo_id = message.text.split("promo_")[1].strip()
            user_id = str(message.from_user.id)
            
            if promo_id in bot.promos:
                p = bot.promos[promo_id]
                if time.time() > p['expires_at']:
                    bot.my_bot.send_message(message.from_user.id, " Срок действия этой промо-ссылки истек.")
                elif p['max_uses'] > 0 and p['current_uses'] >= p['max_uses']:
                    bot.my_bot.send_message(message.from_user.id, "🚫 Лимит использований этой промо-ссылки исчерпан.")
                else:
                    # Активируем промо
                    bot.routes[int(user_id)] = bot.routes.get(int(user_id), {})
                    bot.routes[int(user_id)]['active_promo'] = promo_id
                    
                    if int(user_id) not in bot.great_box:
                        bot.great_box[int(user_id)] = []
                    
                    # 🔥 БЕРЕМ ГОТОВЫЕ ДАННЫЕ ИЗ КЕША
                    games_data = p.get('games_data', [])
                    added_count = 0
                    
                    for gd in games_data:
                        # Формируем структуру для great_box
                        arrord = {
                            'British Pound': '(Англия)', 'USD': '(США)', 'Canadian Dollar': '(Канада)',
                            'Mexican Peso': '(Мексика)', 'Polish Zloty': '(Польша)', 'Australian Dollar': '(Австралия)',
                            'Japanese Yen': '(Япония)', 'USD+': '(Мексика [PsPrices])',
                            'Norwegian Krone': '(Норвегия)', 'Swedish Krona': '(Швеция)'
                        }
                        currency_text = arrord.get(gd['currency'], gd['currency'])
                        if '(' in currency_text:
                            currency_text = currency_text[currency_text.find('('):]
                        else:
                            currency_text = ""
                        
                        # arr: [name, price_rub, currency_text, old_price_rub, price_usd, currency]
                        arr = [
                            gd['name'],
                            str(gd['price_rub']),
                            currency_text,
                            str(gd['old_price_rub']),
                            str(gd['price_usd']),
                            gd['currency']
                        ]
                        # arr545: [name, price_usd, currency, old_price_usd]
                        arr545 = [
                            gd['name'],
                            str(gd['price_usd']),
                            gd['currency'],
                            str(gd['old_price_usd'])
                        ]
                        
                        # Проверяем, нет ли уже в корзине
                        already_in = False
                        for b in bot.great_box[int(user_id)]:
                            if bot.st_in_lowst(b[0][0]) == bot.st_in_lowst(gd['name']):
                                already_in = True
                                break
                        
                        if not already_in:
                            bot.great_box[int(user_id)].append([arr, arr545])
                            added_count += 1
                    
                    # Сохраняем корзину
                    db = shelve.open(MDB_DATA_SHELVE)
                    db["great_box"] = bot.great_box
                    db.close()
                    
                    if added_count > 0:
                        bot.my_bot.send_message(message.from_user.id, 
                            f"🎉 Промокод активирован!\n\n"
                            f"В корзину добавлено игр: {added_count}\n"
                            f"💸 Скидка: {p['discount_pct']}%\n\n"
                            f"Перейдите в 🛒 Корзину, чтобы оформить заказ!", 
                            reply_markup=bot.markup)
                    else:
                        bot.my_bot.send_message(message.from_user.id, 
                            f"🎉 Промокод активирован (скидка {p['discount_pct']}%), "
                            f"но игры уже есть в корзине.")
            else:
                bot.pro_start(message)
        
        elif "/start" in message.text and message.text!='/start':
            bot.my_bot.send_message(for_reports, message.text)
            

            db=shelve.open(PARTNERS_DATA_SHELVE)
            referals=db.get("referals",{})
            db.close()

            if '_pass' in message.text:
                ji=message.text.split("_pass")
            else:
                ji=message.text.split("folownu_")
            patg=""
            if len(ji)>1:
                patg=ji[-1]
            if patg=="":
                patg="psprices"
            rem=referals.get(patg,{})
            if str(message.from_user.id) not in rem:
                rem[str(message.from_user.id)]={"sum":0,"orders":[],"search":1,"profit":0}
                referals[patg]=rem
            else:
                rem[str(message.from_user.id)]["search"]+=1
                referals[patg]=rem


            db=shelve.open(PARTNERS_DATA_SHELVE)
            db["referals"]=referals
            db.close()


            if "folownu" in message.text:
                bot.routes[message.from_user.id]={'route':'start'}
                bot.pro_start(message)
            else:
                bot.routes[message.from_user.id]={'route':'search'}
                bot.pro_search(message)
            bot.partners+=1
            


        
        elif message.text=="/get_partners":
            bot.my_bot.send_message(message.from_user.id, f"По партнерсокой ссылки перешли {bot.partners} раз")
        elif message.text=='/start':
            #print(message)
            route='start'; bot.pro_start(message)

        elif (message.text=='/search_a' or message.text=='🔍 Админ поиск') and str(message.from_user.id)  in bot.ids:
            bot.routes[message.from_user.id]['route']='a2.start';
            bot.pro2_start(message); 

    # Проверяем, является ли это первым сообщением после глубокой ссылки
    
        
        elif message.text=='/adbot_reprice' and str(message.from_user.id) in bot.ids:
            bot.adbot_reprice()
        elif message.text=='/adbot_send' and str(message.from_user.id) in bot.ids:
            bot.alarm3=time.time()
            bot.au_lpr2(message)
        elif message.text=='/adbot_auto_dgames' and str(message.from_user.id) in bot.ids:
            bot.adbot_auto_dgames()
            bot.au_update()
            bot.my_bot.send_message(message.from_user.id, "Успешно")
        elif message.text=='/adbot_refresh' and str(message.from_user.id) in bot.ids:
            bot.adbot_refresh()
            bot.adbot_auto_dgames()
            bot.au_update()
            bot.my_bot.send_message(message.from_user.id, "Успешно")
        elif message.text=='/adbot_reprice2' and str(message.from_user.id) in bot.ids:
            bot.fix_gms={}
            bot.adbot_reprice2()
            bot.my_bot.send_message(message.from_user.id, "Успешно")
        elif message.text=='/adbot_send2' and str(message.from_user.id) in bot.ids:
            bot.adbot_send2()
        elif message.text=='/adbot_save' and str(message.from_user.id) in bot.ids:
            bot.adbot_save()
        elif message.text=='/adbot2_static' and str(message.from_user.id) in bot.ids:
            for idn in bot.ids:
                bot.au_give_stat(idn)
        
        elif message.text=='/update_loco' and str(message.from_user.id) in bot.ids:
            for mdba in bot.loco_list:
                bot.check_update_loco(mdba[0],mdba[1])
        elif message.text=='🔎 Поиск игры' or message.text=='/search':
            bot.routes[message.from_user.id]['route']='search'
            bot.my_bot.send_message(message.from_user.id, "Пожалуйста, отправьте название интересующей игры или дополнения для поиска в eShop", reply_markup=markup)
        elif message.text=='Пользователи' and str(message.from_user.id) in bot.ids:
            bot.au_start(message)
        elif message.text=='Список игр' and str(message.from_user.id) in bot.ids:
            bot.au_game(message)
        elif message.text=='/reload' and str(message.from_user.id) in bot.ids:
            bot.reload_popup()
            bot.my_bot.send_message(message.from_user.id, "Загружено")

        elif (message.text == '🎟 Управление промо' or message.text == '/new_promo') and str(message.from_user.id) in bot.ids:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("➕ Создать новое промо", callback_data="admincreatepromo_1"))
            markup.add(types.InlineKeyboardButton("📋 Список активных промо", callback_data="adminlistpromos_1"))
            bot.my_bot.send_message(message.from_user.id, "🎟 *Управление промокодами*\n\nВыберите действие:", parse_mode='Markdown', reply_markup=markup)

        elif (message.text == '/new_promo' or message.text == 'Новое промо') and str(message.from_user.id) in bot.ids:
            bot.routes[message.from_user.id]['route'] = 'admin_promo_games'
            bot.my_bot.send_message(message.from_user.id, "🎟 *Создание промо-ссылки*\n\nВведите названия игр, на которые будет действовать скидка (через запятую).\nНапример: `Hollow Knight, Cuphead`", parse_mode='Markdown', reply_markup=bot.markup2)
                    
        elif message.text == '/list_promos' and str(message.from_user.id) in bot.ids:
            if not bot.promos:
                bot.my_bot.send_message(message.from_user.id, "Активных промокодов нет.")
            else:
                txt = "📋 *Список промокодов:*\n\n"
                for pid, p in bot.promos.items():
                    expires = datetime.fromtimestamp(p['expires_at']).strftime('%d.%m.%Y')
                    games = ", ".join(p['games_exact'])
                    uses = f"{p['current_uses']}/{p['max_uses']}" if p['max_uses'] > 0 else "Безлимит"
                    txt += f"🆔 `{pid}`\n🎮 Игры: {games}\n💸 Скидка: {p['discount_pct']}%\n🔄 Использований: {uses}\n⏳ До: {expires}\n\n"
                txt += "💡 Для удаления используйте: `/del_promo <ID>`"
                bot.my_bot.send_message(message.from_user.id, txt, parse_mode='Markdown')

        elif message.text.startswith('/del_promo ') and str(message.from_user.id) in bot.ids:
            promo_id = message.text.split('/del_promo ')[1].strip()
            if promo_id in bot.promos:
                del bot.promos[promo_id]
                bot.save_promos() # 🔥 Обязательно сохраняем!
                bot.my_bot.send_message(message.from_user.id, f"✅ Промокод `{promo_id}` успешно удален.", parse_mode='Markdown')
            else:
                bot.my_bot.send_message(message.from_user.id, "❌ Промокод не найден. Проверьте ID.")

        elif message.text=='👤 Пользователь' and str(message.from_user.id) in bot.ids:
            
            prv='👤 Пользователь'
            markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("🔎 Поиск игры")
            btn5= types.KeyboardButton("🌟 Избранное")
            btn6= types.KeyboardButton("🛒 Корзина")
            btn9= types.KeyboardButton("📜 Другое")
            
            btn87= types.KeyboardButton("💰 Коды пополнения")
            
            btn88= types.KeyboardButton("🧧 Nintendo Switch Online")
            
            sub_button4 = telebot.types.KeyboardButton('Назад')
            markup3.add(btn1, btn5,btn6,btn87,btn88,btn9,sub_button4)
            bot.my_bot.send_message(message.from_user.id, prv, parse_mode='HTML', reply_markup=markup3)
        elif message.text=='👨‍💻 Админ' and str(message.from_user.id) in bot.ids:
            
            prv='👨‍💻 Админ'
            markup3 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Пользователи")
            btn3 = types.KeyboardButton("Рассылки")
            btns45 = types.KeyboardButton("🔗 Создать ссылку на игру")
          #  btns445 = types.KeyboardButton("Новое промо") btns445,
            btn_promo = types.KeyboardButton("🎟 Управление промо")
            
            btn7= types.KeyboardButton("🌟 Избранное")
            btn8= types.KeyboardButton("🛒 Корзина")
            btn9= types.KeyboardButton("📜 Другое")
            
            btn87= types.KeyboardButton("💰 Коды пополнения")
            
            btn88= types.KeyboardButton("🧧 Nintendo Switch Online")
            
            sub_button4 = telebot.types.KeyboardButton('Назад')
            
            markup3.add(btn1,btn3,btn7,btns45,btn_promo,btn8,btn9,btn87,btn88,sub_button4)
            bot.my_bot.send_message(message.from_user.id, prv, parse_mode='HTML', reply_markup=markup3)
        elif message.text=='🤝 Партнер' and str(message.from_user.id) in bot.ids:
            
            prv='🤝 Партнер'
            markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btns4 = types.KeyboardButton("🔗 Создать ссылку на игру")
            btns45 = types.KeyboardButton("🔗 Создать ссылку на бота")
            btns2 = types.KeyboardButton("📘 Docs")
            btns3 = types.KeyboardButton("📊 Статистика интеграции")
            
            sub_button4 = telebot.types.KeyboardButton('Назад')
            markup3.add(btns1,btns4,btns45,btns2,btns3,sub_button4)

            bot.my_bot.send_message(message.from_user.id, prv, parse_mode='HTML', reply_markup=markup3)
        elif message.text=='Рассылки' and str(message.from_user.id) in bot.ids:
            
            prv='Рассылки'
            markup3 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn2 = types.KeyboardButton("Список игр")
            btn6 = types.KeyboardButton("Обновить данные")
            sub_button1 = telebot.types.KeyboardButton('Обычная рассылка')
            sub_button2 = telebot.types.KeyboardButton('Рассылка о скидках')
            sub_button4 = telebot.types.KeyboardButton('Назад')
            markup3.add(btn2,btn6,sub_button1, sub_button2,sub_button4 )
            bot.my_bot.send_message(message.from_user.id, prv, parse_mode='HTML', reply_markup=markup3)
        elif message.text=='Обычная рассылка' and str(message.from_user.id) in bot.ids:
            bot.au_rassu(message)
        elif message.text=='Рассылка о скидках' and str(message.from_user.id) in bot.ids:
            bot.au_lpr(message)
        elif message.text=='Добавить фото' and str(message.from_user.id) in bot.ids:
            bot.au_photo(message)
        elif message.text=='Обновить данные' and str(message.from_user.id) in bot.ids:
            bot.au_update()

        

        elif message.text=="🔗 Создать ссылку на игру" and (str(message.from_user.id) in bot.popuski or str(message.from_user.id) in bot.ids):
            bot.my_bot.send_message(message.from_user.id, "Укажите название игры")
            bot.routes[message.from_user.id]['route']='popusk_search'

        elif message.text=="🔗 Создать ссылку на бота":
            url= "https://teleg.one/cyndykbot?start=folownu"
            if str(message.from_user.id) in bot.popuski:
                    url+="_"+bot.popuski[str(message.from_user.id)]["key"]
                    url=url.replace("iucsoccccs_","")
            url2=url.replace("https://teleg.one"," https://t.me")

                
            url=url.replace(":","")
            url2=url2.replace(":","")
            url=url.replace("https//","https://")
            url2=url2.replace("https//","https://")
            bot.my_bot.send_message(message.from_user.id, f"🔗 tg: {url2}")
            bot.my_bot.send_message(message.from_user.id, f"🌐 web: {url}")

          

        elif bot.routes[message.from_user.id]['route'] == 'popusk_search' and (str(message.from_user.id) in bot.popuski or str(message.from_user.id) in bot.ids):
            bot.routes[message.from_user.id]['route'] = 'start'
            game_name = message.text.strip()
            
            if not game_name:
                bot.my_bot.send_message(message.from_user.id, "Пожалуйста, введите название игры.")
                return

            # 1. Очищаем название: оставляем только буквы (рус/анг), цифры и пробелы
            clean_name = re.sub(r'[^a-zA-Zа-яА-ЯёЁ0-9\s]', '', game_name)
            
            # 2. Заменяем пробелы на нижнее подчеркивание и делаем нижний регистр
            clean_name = clean_name.replace(' ', '_').lower()
            
            # 3. Убираем множественные подчеркивания и лишние по краям (на всякий случай)
            clean_name = re.sub(r'_+', '_', clean_name).strip('_')
            
            # 4. Формируем базовый параметр start
            start_param = f"{clean_name}_pass"
            
            # 5. Если у пользователя есть ключ в popuski, добавляем его в конец
            user_id_str = str(message.from_user.id)
            if user_id_str in bot.popuski:
                key = bot.popuski[user_id_str].get("key", "")
                if key:
                    start_param += f"_{key}"
                    
            # 6. Генерируем ссылки
            tg_url = f"https://t.me/cyndykbot?start={start_param}"
            web_url = tg_url.replace("https://t.me/", "https://teleg.one/")
            
            # 7. Отправляем сообщения (без цены, красиво оформленные)
            # Можно отправить одним сообщением (рекомендую, так удобнее пользователю):
            response_text = (
                f"🎮 *{game_name}*\n\n"
                f"🔗 *Telegram:*\n`{tg_url}`\n\n"
                f"🌐 *Web-версия:*\n`{web_url}`"
            )
            bot.my_bot.send_message(message.from_user.id, f"🎮 {game_name}\n\n🔗 TG: {tg_url}")
            bot.my_bot.send_message(message.from_user.id, f"🌐 Web: {web_url}")
            
        
        
        elif message.text=="📘 Docs"  and (str(message.from_user.id) in bot.popuski or str(message.from_user.id) in bot.ids):
            prv='''Пример запроса актуальной цены и ссылки в бота:
https://webapp.cyndykshop.ru/api/external/search/?title=Hollow Knight
Ответ:
{'success': True, 'found': True, 'game': {'id': 1, 'title': 'Hollow Knight', 'has_russian': True, 'image_url': 'https://cdn.dekudeals.com/images/7bf6d8d16a502f7b78bc85554d1c302b1adafdae/w500.jpg', 'description': '<p>Hollow Knight is a classically styled 2D action adventure across a vast interconnected world. Explore twisting caverns, ancient cities and deadly wastes; battle tainted creatures and befriend bizar...', 'tg_url': 'https://t.me/cyndykbot?start=Hollow_Knight_passiucsoccccs'}, 'price': {'available': True, 'price_rub': 866.0, 'currency': 'RUB'}, 'match_confidence': 'exact'}
'''
            bot.my_bot.send_message(message.from_user.id, prv)
            prv='''
import requests




API_URL = "https://webapp.cyndykshop.ru/api/external/search/"
API_KEY = "g7i2y_hdDIT5612qwcy_3dyu"


def search_game(title, platform="nswitch", exact=False):
    """
    Поиск игры через API
   
    :param title: Название игры
    :param platform: Платформа (по умолчанию nswitch)
    :param exact: Точное совпадение
    :return: Результат поиска
    """
    params = {
        'title': title,
        'platform': platform,
        'exact': str(exact).lower(),
        'api_key': API_KEY
    }
   
    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            'error': f'Request failed: {str(e)}',
            'success': False
        }
'''
            bot.my_bot.send_message(message.from_user.id, prv)
        

        
        elif message.text=="📊 Статистика интеграции" and str(message.from_user.id) in bot.popuski:
            kkey=bot.popuski[str(message.from_user.id)]["key"]
            percent=bot.popuski[str(message.from_user.id)]["percent"]/100

            db=shelve.open(PARTNERS_DATA_SHELVE)
            referals=db.get("referals",{})
            db.close()

            popusk=referals.get(kkey,{})
            us=0
            su=0
            orders=0
            search=0
            profit=0
            for usser in popusk:
                orders+=len(popusk[usser]["orders"])
                search+=popusk[usser]["search"]
                profit+=popusk[usser]["profit"]
                us+=1
                su+=popusk[usser]["sum"]
            pper=profit*percent*100//1/100

            cash=bot.popuski[str(message.from_user.id)].get("cash",pper)

            db=shelve.open(POPUSKI_DATA_SHELVE)
            db["popuski"]=bot.popuski
            db.close()

            necash=bot.popuski[str(message.from_user.id)].get("necash",0)

            cash=cash*100//1/100
            necash=necash*100//1/100
            
            bot.my_bot.send_message(message.from_user.id, 
            f"Всего рефералов:{us}\nОбщая сумма заказов: {su} рублей\nОбщая сумма профита: {profit} рублей\nТекущий процент: {percent*100}%\nПроцент с продаж: {cash} рублей\nВыплачено: {necash} рублей\nК выплате: {(cash-necash)*100//1/100} рублей\nВсего заказов:{orders}\nВсего поисков рефералами:{search}")
        
        
        elif message.text=="📊 Статистика интеграции" and str(message.from_user.id) in bot.ids:
            

            db=shelve.open(PARTNERS_DATA_SHELVE)
            referals=db.get("referals",{})
            db.close()
            for key in bot.popuski:
                try:
                    markupin=types.InlineKeyboardMarkup()
                    markupin.add(types.InlineKeyboardButton('Изменить процент',callback_data='newpercent_'+str(key)))
                    markupin.add(types.InlineKeyboardButton('Выплатить денег',callback_data='cashcashcash_'+str(key)))
                    kkey=bot.popuski[key]["key"]
                    percent=bot.popuski[key]["percent"]/100
                    kkeym=kkey
                    if kkeym=="ateotcms": kkeym="Михаил PSprices"
                    if kkeym=="rteimceaa": kkeym="Андрей PSprices"
                    popusk=referals[kkey]
                    us=0
                    su=0
                    orders=0
                    search=0
                    profit=0
                    for usser in popusk:
                        orders+=len(popusk[usser]["orders"])
                        search+=popusk[usser]["search"]
                        profit+=popusk[usser]["profit"]
                        us+=1
                        su+=popusk[usser]["sum"]
                    pper=profit*percent*100//1/100

                   # if kkeym=="Михаил PSprices":

                      #  bot.popuski[key]["cash"]=pper

                        

                     #   db=shelve.open(POPUSKI_DATA_SHELVE)
                     #   db["popuski"]=bot.popuski
                    #    db.close()

                    cash=bot.popuski[key].get("cash",pper)

                    necash=bot.popuski[key].get("necash",0)

                    bot.popuski[key]["cash"]=cash

                    bot.popuski[key]["necash"]=necash

                    

                    cash=cash*100//1/100
                    necash=necash*100//1/100
                        
                    bot.my_bot.send_message(message.from_user.id, f"{kkeym}\nВсего рефералов:{us}\nОбщая сумма заказов: {su} рублей\nОбщая сумма профита: {profit} рублей\nТекущий процент: {percent*100}%\nПроцент с продаж: {cash} рублей\nВыплачено: {necash} рублей\nК выплате: {(cash-necash)*100//1/100} рублей\nВсего заказов:{orders}\nВсего поисков рефералами:{search}",reply_markup=markupin)

                    bot.my_bot.send_message(for_reports,str(referals[kkey]))

                except:
                    bot.my_bot.send_message(for_reports,traceback.format_exc())
            bot.adbot_save()
            
        #
        elif message.text=="🌟 Избранное":
            markupin=types.InlineKeyboardMarkup()
            markupin.add(types.InlineKeyboardButton('Добавить игру',callback_data='newgame_'+str(message.from_user.id)))
            markupin.add(types.InlineKeyboardButton('Удалить игру',callback_data='delgame_'+str(message.from_user.id)))
            fv=bot.favo.get(str(message.from_user.id),[])
            txt=''
            n=1
            dct=bot.favo_price
            for f in fv:
                    txt2='\n'+str(n)+'. '+f
                    price=dct.get(f,[0,0])
                    if price!=[0,0]:
                        if price[0]!=price[1]:
                            txt2='\n💸'+str(n)+'. '+f+': '+str(price[0])+' <del>'+str(price[1])+'</del> '+' рублей'
                        else:
                            txt2='\n'+str(n)+'. '+f+': '+str(price[0])+' рублей'
                    txt+=txt2
                    n+=1
            prv='''🌟 Вы можете добавить игры в Избранное, чтобы получать уведомления о всех
скидках и распродажах!
\nВаш список Избранного пуст! Воспользуйтесь поиском, чтобы добавить в него
интересующие игры.'''
            if txt!='':
                prv='''🌟 Вы можете добавить игры в Избранное, чтобы получать уведомления о всех скидках и распродажах!
\nИгры, которые вы добавили в Избранное:'''+txt
            bot.my_bot.send_message(message.from_user.id, prv, parse_mode='HTML', reply_markup=markupin)
        

     #   elif "закончить чат" in message.text.lower():
       #     bot.routes[message.from_user.id]['route']='start'
     #       bot.my_bot.send_message(message.from_user.id, "Чат закрыт")

        elif message.text=="Чат по заказу" and  str(message.from_user.id) not in bot.ids:

            coll=-1
            for key in bot.great_dic:
                if str(bot.great_dic[key]["Клиент"])==str(message.from_user.id) and bot.great_dic[key]["Менеджер"]:
                    coll=key 
            if coll!=-1:
                bot.routes[message.from_user.id]['route']='chat_order'
                bot.routes[message.from_user.id]['chat_order']=coll
           #     bot.my_bot.send_message(message.from_user.id, f"Вы перешли в чат по заказу {coll}. Ваш менеджер: {bot.great_dic[coll]["Менеджер"]}\nНапишите \"Закончить чат\", чтобы вернуться в основной режим работы бота")
                bot.my_bot.send_message(message.from_user.id, f"Вы перешли в чат по заказу {coll}. Ваш менеджер: {bot.great_dic[coll]['Менеджер']}")
            else:
                bot.my_bot.send_message(message.from_user.id, "К сожалению, чат не найден")

        elif bot.routes[message.from_user.id]['route']=='chat_order' and bot.routes[message.from_user.id].get('chat_order','')!='':
            try:
                manager=-1
                for key in bot.auth:
                    if bot.auth[key]==bot.great_dic[bot.routes[message.from_user.id]['chat_order']]['Менеджер']:
                        manager=key 
                        break
                caption=f"[Сообщение из заказа {bot.routes[message.from_user.id]['chat_order']}]\n[Клиент: {message.from_user.id}]\n{message.text}"
                markupin=types.InlineKeyboardMarkup()
                markupin.add(types.InlineKeyboardButton("Ответить",callback_data=f"reorder_{message.from_user.id}"))
            
                if manager==-1:
                    a=1/0
                bot.my_bot.send_message(manager, caption,reply_markup=markupin)
            except:
                bot.my_bot.send_message(message.from_user.id, "К сожалению, сообщение не доставлено")
            

        elif bot.routes[message.from_user.id]['route']=='reorder':
            bot.routes[message.from_user.id]['route']='start'
            manager=bot.auth.get(str(message.from_user.id),str(message.from_user.id))
            caption=f"[{manager}]\n{message.text}"
            try:
                bot.my_bot.send_message(bot.routes[message.from_user.id]['reorder'], caption)
                bot.my_bot.send_message(message.from_user.id, "Сообщение доставлено")
            except:
                bot.my_bot.send_message(message.from_user.id, "К сожалению, сообщение не доставлено")


        elif bot.routes[message.from_user.id]['route']=='newpercent':
            bot.routes[message.from_user.id]['route']='start'
            try:
                percent=float(message.text)
                bot.popuski[bot.routes[message.from_user.id]['mypopusk']]["percent"]=percent
                bot.my_bot.send_message(message.from_user.id, f"Процент с продаж изменен. Теперь наш партнёр будет получать {percent}% с продаж")

                db=shelve.open(POPUSKI_DATA_SHELVE)
                db["popuski"]=bot.popuski
                db.close()
            except:
                bot.my_bot.send_message(message.from_user.id, "У Вас не получилось")


        elif bot.routes[message.from_user.id]['route']=='cashcashcash':
            bot.routes[message.from_user.id]['route']='start'
            try:
                percent=float(message.text)
                bot.popuski[bot.routes[message.from_user.id]['mypopusk']]["necash"]+=percent
                bot.my_bot.send_message(message.from_user.id, f" Доброму человеку выплачено {percent} рублей")
                bot.my_bot.send_message(bot.routes[message.from_user.id]['mypopusk'], f" Вам выплачено {percent} рублей")

                db=shelve.open(POPUSKI_DATA_SHELVE)
                db["popuski"]=bot.popuski
                db.close()
            except:
                bot.my_bot.send_message(message.from_user.id, "У Вас не получилось")

        elif bot.routes[message.from_user.id]['route'] == 'admin_promo_games':
            games = [g.strip() for g in message.text.split(',')]
            bot.routes[message.from_user.id]['promo_games'] = games
            bot.routes[message.from_user.id]['route'] = 'admin_promo_pct'
            bot.my_bot.send_message(message.from_user.id, "Укажите размер скидки в процентах (например: `15` для 15%)", parse_mode='Markdown', reply_markup=bot.markup2)

        elif bot.routes[message.from_user.id]['route'] == 'admin_promo_pct':
            try:
                pct = float(message.text.replace('%', '').strip())
                bot.routes[message.from_user.id]['promo_pct'] = pct
                bot.routes[message.from_user.id]['route'] = 'admin_promo_uses'
                bot.my_bot.send_message(message.from_user.id, "Укажите максимальное количество использований ссылки.\nВведите `0`, если количество неограниченно.", reply_markup=bot.markup2)
            except:
                bot.my_bot.send_message(message.from_user.id, "❌ Ошибка: введите число. Попробуйте еще раз.", reply_markup=bot.markup2)

        elif bot.routes[message.from_user.id]['route'] == 'admin_promo_uses':
            try:
                uses = int(message.text.strip())
                bot.routes[message.from_user.id]['promo_uses'] = uses
                bot.routes[message.from_user.id]['route'] = 'admin_promo_days'
                bot.my_bot.send_message(message.from_user.id, "Укажите срок действия ссылки в днях (например: `7`)", reply_markup=bot.markup2)
            except:
                bot.my_bot.send_message(message.from_user.id, "❌ Ошибка: введите целое число.", reply_markup=bot.markup2)

        elif bot.routes[message.from_user.id]['route'] == 'admin_promo_days':
            try:
                days = int(message.text.strip())
                expires_at = time.time() + (days * 24 * 60 * 60)
                
                
                promo_id = "PROMO_" + secrets.token_hex(4).upper()
                
                # 🔥 ИЩЕМ ИГРЫ СРАЗУ ПРИ СОЗДАНИИ ПРОМОКОДА
                games_data = []  # Полные данные игр для корзины
                games_norm = []  # Нормализованные названия для сравнения
                games_exact = bot.routes[message.from_user.id]['promo_games']  # Оригинальные названия
                not_found = []  # Игры, которые не удалось найти
                
                bot.my_bot.send_message(message.from_user.id, "🔍 Ищу игры в магазине...")
                
                for game_name in games_exact:
                    results = bot.search_game(game_name, str(message.from_user.id))
                    
                    if results:
                        norm_target = bot.st_in_lowst(game_name)
                        best_match = None
                        
                        # 🔥 ПРИОРИТЕТ 1: Полное совпадение (без учета спецсимволов)
                        for r in results:
                            if bot.st_in_lowst(r[0]) == norm_target:
                                best_match = r
                                break
                        
                        #  ПРИОРИТЕТ 2: Частичное совпадение (если полное не нашли)
                        if not best_match:
                            for r in results:
                                if norm_target in bot.st_in_lowst(r[0]):
                                    best_match = r
                                    break
                        
                        if best_match:
                            # best_match: [name, price_usd, currency, old_price_usd]
                            name = best_match[0]
                            price_usd = float(best_match[1])
                            currency = best_match[2]
                            old_price_usd = float(best_match[3]) if best_match[3] != -1 else -1
                            
                            # Считаем цены в рублях
                            price_rub = bot.usd_to_rub(price_usd, currency)
                            old_price_rub = bot.usd_to_rub(old_price_usd, currency) if old_price_usd != -1 else -1
                            
                            # Сохраняем полные данные
                            games_data.append({
                                'name': name,
                                'price_rub': price_rub,
                                'price_usd': price_usd,
                                'currency': currency,
                                'old_price_rub': old_price_rub,
                                'old_price_usd': old_price_usd
                            })
                            games_norm.append(bot.st_in_lowst(name))
                        else:
                            not_found.append(game_name)
                    else:
                        not_found.append(game_name)
                
                # 🔥 СОХРАНЯЕМ ПРОМОКОД С ПОЛНЫМИ ДАННЫМИ
                bot.promos[promo_id] = {
                    "games_exact": games_exact,
                    "games_norm": games_norm,
                    "games_data": games_data,  # 🔥 НОВОЕ: полные данные игр
                    "discount_pct": bot.routes[message.from_user.id]['promo_pct'],
                    "max_uses": bot.routes[message.from_user.id]['promo_uses'],
                    "current_uses": 0,
                    "expires_at": expires_at,
                    "created_by": message.from_user.id
                }
                
                
                bot.save_promos() # 🔥 Обязательно сохраняем!
                
                link = f"https://t.me/cyndykbot?start=promo_{promo_id}"
                
                # Формируем отчет для админа
                report = f"✅ *Промо-ссылка создана!*\n\n🔗 Ссылка: `{link}`\n"
                report += f"💸 Скидка: {bot.promos[promo_id]['discount_pct']}%\n"
                report += f"🔄 Лимит: {'Безлимит' if bot.promos[promo_id]['max_uses']==0 else bot.promos[promo_id]['max_uses']} раз\n"
                report += f"⏳ Действует до: {datetime.fromtimestamp(expires_at).strftime('%d.%m.%Y')}\n\n"
                
                report += f" *Найдено игр: {len(games_data)} из {len(games_exact)}*\n"
                for gd in games_data:
                    report += f"  ✅ {gd['name']} - {gd['price_rub']} ₽\n"
                
                if not_found:
                    report += f"\n❌ *Не найдено:*\n"
                    for nf in not_found:
                        report += f"  ❌ {nf}\n"
                
                bot.routes[message.from_user.id]['route'] = 'start'
                bot.my_bot.send_message(message.from_user.id, report, parse_mode='Markdown')
                
            except:
                bot.my_bot.send_message(message.from_user.id, "❌ Ошибка: введите целое число дней.", reply_markup=bot.markup2)


        elif bot.routes[message.from_user.id]['route']=='fv_newgame':
            markupin=types.InlineKeyboardMarkup()
            markupin.add(types.InlineKeyboardButton("🚫 Убрать из Избранного",callback_data='delpingame_'+str(message.from_user.id)))
            markupin.add(types.InlineKeyboardButton("🔎 Найти ещё игру",callback_data='findgame_'+str(message.from_user.id)))
            bot.routes[message.from_user.id]['route']='start'
            fv=bot.favo.get(str(message.from_user.id),[])
            gm=message.text
            if gm not in fv:
                    fv.append(gm)
                    results=bot.search_game(gm,'')
                    for r in results:
                        usd=-1
                        val=r[2]
                       # r[1]=bot.usd_to_rub(r[1],r[2])
                        a=''
                        if bot.st_in_lowst(r[0])==bot.st_in_lowst(gm):
                            a=gm
                        if a!='':
                            bot.favo_price[a]=[r[1],r[1],time.time(),usd,val]
                        if r[3]!=-1 and a!='': bot.favo_price[a][1]=bot.usd_to_rub(r[3],r[2])
            
                #
                
            bot.favo[str(message.from_user.id)]=fv
            bot.my_bot.send_message(message.from_user.id, str(gm)+" успешно добавлена в 🌟 Избранное. Вы получите уведомление, когда на игру будет действовать скидка",reply_markup=markupin)
            


        elif bot.routes[message.from_user.id]['route']=='fv_delgame':
            try:
                bot.routes[message.from_user.id]['route']=''
                num=int(message.text)-1
                fv=bot.favo.get(str(message.from_user.id),[])
                name=fv.pop(num)
                bot.favo[str(message.from_user.id)]=fv
                bot.my_bot.send_message(message.from_user.id, str(name)+''' удалена из вашего списка избранного. Воспользуйтесь поиском, чтобы добавить в него интересующие игры.''')
            except:
                bot.my_bot.send_message(message.from_user.id, "Пожалуйста, введите номер игры из списка")
        #

        elif message.text=='/price_help' and str(message.from_user.id) in bot.ids:
                st=''
                st+='Справка по изменению формулы расчета цен\n\n'
                st+='/price_usa 85 - установит курс доллара по купону\n'
                st+='/price_list - выведет текущую формулы расчета цен\n'
                st+='/price_change clear - вернет формулу в исходное состояние\n'
                st+='/price_change 10 del - удалит порог в 10 USD\n'
                st+='/price_change usd 110 - примет курс доллара равным 110 рублей за USD\n'
                st+='/price_change k 1.15 - примет общую наценку равной 15%\n'
                st+='/price_change inf 100 - повысит наценку на игры дороже максимального порога на 100 рублей\n'
                st+='/price_change 10 -200 - понизит наценку на игры дешевле 10 USD на 200 рублей\n'
                
                st+='/yen500_change 400 - задаст курс для карты пополненич на 500 йен\n'
                st+='/yen1000_change 800 - задаст курс для карты пополненич на 1000 йен\n'
                bot.my_bot.send_message(message.from_user.id,st,reply_markup=markup)


        elif '/yen500' in message.text and str(message.from_user.id) in bot.ids:
            try:
                arro=message.text.split()
                arro=int(arro[-1])
                bot.yen500=arro
                bot.my_bot.send_message(message.from_user.id,'Изменения внесены',reply_markup=markup)
            except:
                pass


        elif '/yen1000' in message.text and str(message.from_user.id) in bot.ids:
            try:
                arro=message.text.split()
                arro=int(arro[-1])
                bot.yen1000=arro
                bot.my_bot.send_message(message.from_user.id,'Изменения внесены',reply_markup=markup)
            except:
                pass
        elif '/price_usa' in message.text and str(message.from_user.id) in bot.ids:
            try:
                arro=message.text.split()
                arro=int(arro[-1])
                bot.price_settings2=arro
                bot.my_bot.send_message(message.from_user.id,'Изменения внесены',reply_markup=markup)
            except:
                pass
        elif '/price_change' in message.text and str(message.from_user.id) in bot.ids:
                try:
                    arro=message.text.split()
                    print(arro)
                    if arro[1]=='clear':
                        bot.price_settings=[
                [7,299],
                [18,349],
                [-1,399],
                [-2,1.11],
                [-3,100]
            ]
                        bot.my_bot.send_message(message.from_user.id,'Изменения внесены',reply_markup=markup)
                    elif arro[2]=='clear' or arro[2]=='del':
                        ind=float(arro[1])
                        ind2=-1
                        for ij in range(len(bot.price_settings)):
                            if bot.price_settings[ij][0]==ind:
                                ind2=ij
                                break
                        if ind2!=-1:
                            bot.price_settings.pop(ind2)
                            bot.my_bot.send_message(message.from_user.id,'Изменения внесены',reply_markup=markup)
                    elif arro[1]=='usd':
                        rz=float(arro[2])
                        for ij in range(len(bot.price_settings)):
                            if bot.price_settings[ij][0]==-3:
                                bot.price_settings[ij][1]=rz
                                bot.my_bot.send_message(message.from_user.id,'Изменения внесены',reply_markup=markup)
                                break
                    elif arro[1]=='k':
                        rz=float(arro[2])
                        for ij in range(len(bot.price_settings)):
                            if bot.price_settings[ij][0]==-2:
                                bot.price_settings[ij][1]=rz
                                bot.my_bot.send_message(message.from_user.id,'Изменения внесены',reply_markup=markup)
                                break
                    elif arro[1]=='inf':
                        rz=int(arro[2])
                        for ij in range(len(bot.price_settings)):
                            if bot.price_settings[ij][0]==-1:
                                bot.price_settings[ij][1]+=rz
                                bot.my_bot.send_message(message.from_user.id,'Изменения внесены',reply_markup=markup)
                                break
                    else:
                        ind=float(arro[1])
                        rz=int(arro[2])
                        print(ind,rz)
                        print(bot.price_settings)
                        if ind>0:
                            ind2=-1
                            for ij in range(len(bot.price_settings)):
                                if bot.price_settings[ij][0]==ind:
                                    ind2=ij
                                    break
                            if ind2==-1:
                                bot.price_settings.append([ind,rz])
                            else:
                                bot.price_settings[ind2][1]+=rz
                            bot.my_bot.send_message(message.from_user.id,'Изменения внесены',reply_markup=markup)
           
                except Exception as e:
                    pass

        
        elif message.text=='/price_list' and str(message.from_user.id) in bot.ids:
                st=f'Стоимость карты пополнения на 500 йен составляет {bot.yen500} рублей\nНа 1000 йен - {bot.yen1000}\nИспользуются следующая формула:\n x - цена из источника в USD\n'
                usd=100
                k=1.11
                inf=399
                arro23=[]
                for iji in bot.price_settings:
                    if iji[0]==-1: inf=iji[1]
                    elif iji[0]==-2: k=iji[1]
                    elif iji[0]==-3: usd=iji[1]
                    else:
                        arro23.append([iji[0],iji[1]])
                arro23.sort()
                st+='x домножается на '+str(k)+'\n'
                last=0
                for a in arro23:
                    st+='если x<'+str(a[0])+': x*'+str(usd)+'+'+str(a[1])+'\n'
                    last=a[0]
                st+='если x>='+str(last)+': x*'+str(usd)+'+'+str(inf)+'\n'
                bot.my_bot.send_message(message.from_user.id,st,reply_markup=markup)
            
        elif message.text=='/list' and str(message.from_user.id) in bot.ids:
            bot.au_game_list(message)

        elif message.text=='/add' and str(message.from_user.id) in bot.ids:
            bot.au_game_add(message)
        elif message.text=='/delete' and str(message.from_user.id) in bot.ids:
            bot.au_game_del(message)

        elif message.text=='/ban' and str(message.from_user.id) in bot.ids:
            bot.au_ban(message)

        elif message.text=='/new_admin' and str(message.from_user.id) in bot.ids:
            bot.au_new_admin(message)
        elif message.text=='/del_admin' and str(message.from_user.id) in bot.ids:
            bot.au_del_admin(message)
        elif message.text=='/list_admin' and str(message.from_user.id) in bot.ids:
            bot.au_list_admin(message)
        elif message.text=='/load_admin' and str(message.from_user.id) in bot.ids:
            bot.au_load_admin(message)
        elif message.text=='/list_popusk' and str(message.from_user.id) in bot.ids:
            msg=""
            for key in bot.popuski:
                msg+=f"{key} - {bot.popuski[key]}\n"
            bot.my_bot.send_message(message.from_user.id, msg)
        elif '/new_popusk' in message.text and str(message.from_user.id) in bot.ids:
            miig=message.text.split()
            mid=miig[1]
            

            db=shelve.open(POPUSKI_DATA_SHELVE)
            popuski=db.get("popuski",{}) # "id":"key"
            popuski[str(mid)]={"key":bot.create_popusk_key(str(mid)),"percent":15,"cash":0,"necash":0}
            db["popuski"]=popuski
            db.close()
            
            
            bot.popuski=popuski
            db=shelve.open(PARTNERS_DATA_SHELVE)
            referals=db["referals"]
            if bot.create_popusk_key(str(mid)) not in referals:
                referals[bot.create_popusk_key(str(mid))]={}
                db["referals"]=referals
                bot.my_bot.send_message(message.from_user.id, 'Новый popusk успешно добавлен')
            else:
                bot.my_bot.send_message(message.from_user.id, 'Данный popusk уже добавлен')
            db.close()

            

        elif message.text=='/admin_help' and str(message.from_user.id) in bot.ids:
            bot.my_bot.send_message(message.from_user.id, '''
/ban - заблокировать пользователя,
/new_admin - добавить нового администратора,
/list_admin - список администраторов,
/del_admin - удалить администратора,,
/load_admin - перезагрузить список админов,
/price_help - справка по работе с ценами
/month_stat - статистика за последние 30 дней
''', reply_markup=markup)
        elif message.text=='Назад':
            bot.my_bot.send_message(message.from_user.id, 'Вы вернулись в главное меню', reply_markup=markup)
        elif message.text=="💰 Коды пополнения":
            markupin=types.InlineKeyboardMarkup()
            regions=[]
            
            try:
                for arti in bot.popups:
                    pass
            except:
                bot.reload_popup()
            for arti in bot.popups:
                if bot.popups[arti]["Регион"] not in regions:
                    regions.append(bot.popups[arti]["Регион"])
            for i in range(len(regions)):
                markupin.add(types.InlineKeyboardButton(regions[i],callback_data='codeofkpk_'+str(i)))
            bot.my_bot.send_message(message.from_user.id, 'Выберите регион вашего аккаунта Nintendo для активации кодов пополнения',reply_markup=markupin)
        
        
        elif message.text=='📜 Другое':
            prv='📜 Другое'
            markup3 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            sub_button1 = telebot.types.KeyboardButton('FAQ')
            sub_button2 = telebot.types.KeyboardButton('Наши ресурсы')
        #    sub_button3 = telebot.types.KeyboardButton('Подписка Nintendo Switch Online')
            sub_button5 = telebot.types.KeyboardButton('Сообщить о проблеме')
            sub_button4 = telebot.types.KeyboardButton('Назад')
            markup3.add(sub_button1, sub_button2, sub_button5, sub_button4 )
            bot.my_bot.send_message(message.from_user.id, prv, reply_markup=markup3)


        elif message.text=='FAQ': 
            prv='''
❓ Как работает наш бот для выгодной покупки игр Nintendo?
🖐 От первого клика в боте до игры на вашем аккаунте вас отделяет всего 5 шагов:
1. Вы ищете игру: Просто напишите полное название игры на английском
2. Мы находим лучшие предложения: Бот сравнивает цены в разных странах Nintendo eShop, учитывая скидки, курс валюты, налог и комиссию платежных систем, и предлагает игры / дополнения по вашему запросу
3. Вы выбираете нужную игру: достаточно просто написать номер игры в списке
4. Связь с менеджером: Ваш запрос отправляется администратору для оформления покупки
5. Важно! Если у вас есть неиспользованные деньги на балансе аккаунта Nintendo, они могут быть списаны при смене региона. В отдельных случаях (регион-блок) может потребоваться доплата или создание нового профиля
⚠️ Обратите внимание! Для покупки игры менеджеру необходимо войти на ваш аккаунт Nintendo. Мы гарантируем безопасность процедуры. Если вы всё-таки беспокоитесь по этому поводу, установите двухэтапную аутентификацию в настройках, поменяйте пароль после покупки игры или используйте отдельный аккаунт для покупок в боте.
            '''
            bot.my_bot.send_message(message.from_user.id, prv, reply_markup=markup)
        elif message.text=='Сообщить о проблеме': 
            prv='''
            ✍️ Пожалуйста, опишите проблему с которой вы столкнулись!
            '''
            bot.my_bot.send_message(message.from_user.id, prv, reply_markup=markup)
            bot.routes[message.from_user.id]['route']='problems'
        elif bot.routes[message.from_user.id]['route']=='problems':
            msg=message.text
            prv='''
            ✔️ Ваше сообщение передано!\n
В ближайшее время с вами свяжется менеджер для уточнения деталей. Если ваш
профиль закрыт, пожалуйста, напишите администратору: @bingupluss
            '''
            bot.routes[message.from_user.id]['route']='start'
            bot.my_bot.send_message(message.from_user.id, prv, reply_markup=markup)
            for id1 in bot.ids:
                try:
                    username="неизветсно"
                    user = message.from_user
                    if user.username:  # Проверяем, есть ли username
                        username = f"@{user.username}"
                    bot.my_bot.send_message(id1,f"Новая проблема от {username}:\n"+msg)
                    bot.my_bot.forward_message(id1, message.from_user.id, message.id)
                except:
                    pass
                    
        elif message.text=='Наши ресурсы':
            bot.my_bot.send_message(message.from_user.id, '''
🌐 Наши ресурсы
🟡 СУНДУК Премиум: t.me/cyndykshop
🔴 СУНДУК Стандарт: t.me/cyndykshop_bp
🔵 СУНДУК Playstation: t.me/cyndykpsn
''', reply_markup=markup)
        elif message.text=='Подписка Nintendo Switch Online':
            bot.my_bot.send_message(message.from_user.id, '''
🧧 Подписка Nintendo Switch Online открывает доступ к онлайн-функциям, а так же

бесплатным играм с ретро-консолей (NES/SNES/Gameboy и пр.)

💸 Актуальные цены на подписку здесь: t.me/cyndykshop/2959

Купить: @bingupluss
''', reply_markup=markup)
        elif message.text == '🛒 Корзина':
            user = message.from_user.id
            bx = bot.great_box.get(user, [])
            
            if len(bx) == 0:
                bot.my_bot.send_message(message.from_user.id, 'Ваша корзина пуста', reply_markup=markup)
            else:
                # --- ПРОВЕРКА ПРОМОКОДА ДЛЯ ОТОБРАЖЕНИЯ В КОРЗИНЕ ---
                promo_id = bot.routes.get(int(user), {}).get('active_promo')
                promo_active = False
                discount_pct = 0
                discounted_games_norm = []
                
                if promo_id and promo_id in bot.promos:
                    p = bot.promos[promo_id]
                    if time.time() <= p['expires_at'] and (p['max_uses'] == 0 or p['current_uses'] < p['max_uses']):
                        promo_active = True
                        discount_pct = p['discount_pct']
                        discounted_games_norm = p['games_norm']
                # ----------------------------------------------------

                markupin = types.InlineKeyboardMarkup()
                markupin.add(types.InlineKeyboardButton('Очистить корзину', callback_data='clearbox_' + str(message.from_user.id)))
                markupin.add(types.InlineKeyboardButton('Купить', callback_data='buybox_' + str(message.from_user.id) + '$' + str(message.id)))
                
                txt = "Сейчас в Вашей корзине:\n"
                total_sum = 0.0
                
                for b in bx:
                    game_name = b[0][0]
                    base_price = float(b[0][1])
                    
                    # Проверяем, действует ли скидка на эту игру
                    is_discounted = False
                    if promo_active:
                        game_name_low = bot.st_in_lowst(game_name)
                        for dg_norm in discounted_games_norm:
                            if game_name_low == dg_norm:
                                is_discounted = True
                                break

                    if is_discounted:
                        final_price = base_price * (1 - discount_pct / 100)
                        # Показываем зачеркнутую старую цену и новую со скидкой
                        txt += f"🎮 *{game_name}* ~~{base_price:.2f} ₽~~ **{final_price:.2f} ₽** 🔥 (-{discount_pct}%)\n"
                    else:
                        final_price = base_price
                        txt += f"🎮 *{game_name}* — {final_price:.2f} ₽\n"
                    
                    total_sum += final_price

                # Применяем скидку за объем (3+ игры), если она есть
                if len(bx) >= 3:
                    total_sum = round(total_sum * 0.95, 2)
                    txt += f"\n✅ *Применена дополнительная скидка 5% за 3+ игры!*"
                    
                txt += f"\n\n💰 *Итого к оплате:* **{total_sum:.2f} ₽**"
                
                bot.my_bot.send_message(message.from_user.id, txt, reply_markup=markupin, parse_mode='Markdown')
                        
                        
       # elif message.text=='/search_a' and str(message.from_user.id)  in bot.ids: bot.routes[message.from_user.id]['route']='a.start'; bot.pro_start(message); 
        
        
        elif "/get_order_wt" in message.text and str(message.from_user.id) in bot.ids:
            order=bot.great_dic.get(int(message.text.split()[1]),"")
            if order=="":
                bot.my_bot.send_message(message.from_user.id, "Заказ не найден")
            else:
                markupin=types.InlineKeyboardMarkup()
                markupin.add(types.InlineKeyboardButton('Написать уважаемому клиенту',callback_data='sendwtmessage_'+str(message.from_user.id)))
                markupin.add(types.InlineKeyboardButton('Взять заказ',callback_data='getwtorder_'+message.text.split()[1]))
                bot.my_bot.send_message(message.from_user.id, str(order), reply_markup=markupin)
                bot.routes[message.from_user.id]['sendwtid']=order['Клиент']



        
        elif message.text=='/back': route='start'; bot.pro_start(message)
        elif message.text=='/delete_photo' and str(message.from_user.id) in bot.ids: bot.rassu_photo2=-1; bot.au_photo(message);
        elif message.text=='/delete_all' and str(message.from_user.id) in bot.ids: bot.dgames=[];bot.routes[message.from_user.id]['route']='start'
        elif message.text=='/month_stat' and str(message.from_user.id) in bot.ids: bot.au_give_stat(message.from_user.id)               
        elif route=='sendwtmessage':
            bot.routes[message.from_user.id]['route']='start'
            bot.my_bot.send_message(bot.routes[message.from_user.id]['sendwtid'], message.text)
            bot.my_bot.send_message(message.from_user.id, "Сообщение успешно доставлено")

        
        elif route=='start': bot.pro_start(message)
        elif route=='search' or route=='a.search':
            if bot.validate_shopa(message.text):
                bot.pro_search(message)
            else:
                bot.my_bot.send_message(message.from_user.id, "Пожалуйста, введите название игры на английском")
        elif route=='a2.search': bot.pro2_search(message)
        elif route=='gamelist': bot.pro_gamelist(message)
        elif route=='au_rassu': bot.au_rassu3(message)
        elif route=='au_rassu2' and message.text=='/accept': bot.au_rassu2(message)
        elif route=='au_rassu2' and message.text=='/without_photo': bot.rassu_photo=-1; bot.au_rassu2(message)
        elif route=='au_rassu3' and message.text=='/accept': bot.au_rassu4(message)
        elif route=='au_game_add': bot.au_game_add2(message)
        elif route=='au_game_del': bot.au_game_del2(message)
        elif route=='au_ban': bot.au_ban2(message)
        elif route=='au_new_admin': bot.au_new_admin2(message)
        elif route=='au_new_admin2': bot.au_new_admin3(message)
        elif route=='au_del_admin': bot.au_del_admin2(message)
        elif route=='au_lpr' and message.text=='/accept': bot.au_lpr2(message)
        else: print(route)
        
        now=datetime.now()
        we=datetime.weekday(now)
        tm=int(str(now.time()).split(':')[0])+1
        
        if str(we)=='14' and time.time()-bot.alarm2>=24*60*60:
            bot.alarm2=time.time()
            bot.au_update()
            
        if str(we)=='15' and tm>=10 and tm<=20 and time.time()-bot.alarm3>=24*60*60:
            bot.alarm3=time.time()
            bot.au_lpr2(message)
        
            
    except Exception as e:
        bot.my_bot.send_message(for_reports, str(message.text)+traceback.format_exc())
        print(e)
        print('Crash in processing...')
        try:
            if route=='search': bot.my_bot.send_message(message.from_user.id,'Сбой в работе бота.\n Попробуйте перезапустить бота и повторить запрос или свяжитесь с нашим менеджером: http://t.me/bingupluss')
        except:
            pass
            print('Full crush')
    

@bot.my_bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    try:
        id1=callback.data[:callback.data.find('_')]

        if id1=="page":
            user_id = callback.from_user.id
    
            # Проверяем, есть ли данные для этого пользователя
            if user_id not in user_data:
                bot.my_bot.answer_callback_query(callback.id, "Сессия истекла. Начните поиск заново.")
                return
            
            # Извлекаем номер запрошенной страницы из callback_data
            requested_page = int(callback.data.split('_')[1])
            games_list = user_data[user_id]["games_list"] ##################################################
            
            # Проверяем, существует ли такая страница
            items_per_page = 5
            max_page = (len(games_list) - 1) // items_per_page
            
            if requested_page < 0 or requested_page > max_page:
                bot.answer_callback_query(callback.id)
                return
            
            # Обновляем текущую страницу
            user_data[user_id]["current_page"] = requested_page
            
            # Формируем новую клавиатуру и подпись
            new_keyboard = bot.build_keyboard(games_list, requested_page,callback.message)
            new_caption = bot.build_caption(games_list, requested_page)
            
            # Редактируем существующее сообщение
            try:
                #my_popug=bot.get_nice_popug()
                #with open(my_popug, 'rb') as photo:
                photo = callback.message.photo[-1].file_id  # берём самое большое по размеру фото
                bot.my_bot.edit_message_media(
                        chat_id=callback.message.chat.id,
                        message_id=callback.message.message_id,
                        media=types.InputMediaPhoto(
                            media=photo,  
                            caption=new_caption,
                            parse_mode='HTML'
                        ),
                        reply_markup=new_keyboard,
                        
                    )
            except Exception as e:
                # Если сообщение не изменяется (например, та же страница), просто игнорируем
                bot.my_bot.send_message(for_reports, traceback.format_exc())
            
            # Подтверждаем обработку callback
            bot.my_bot.answer_callback_query(callback.id)

        elif id1=="igonre":
            pass

                # 🔥 КНОПКА: СОЗДАТЬ ПРОМО
        elif id1 == "admincreatepromo":
            bot.my_bot.answer_callback_query(callback.id)
            bot.routes[callback.message.chat.id]['route'] = 'admin_promo_games'
            bot.my_bot.send_message(callback.message.chat.id, "🎟 *Создание промо- aссылки*\n\nВведите названия игр, на которые будет действовать скидка (через запятую).\nНапример: `Hollow Knight, Cuphead`", parse_mode='Markdown', reply_markup=bot.markup2)

        # 🔥 КНОПКА: СПИСОК ПРОМО
        elif id1 == "adminlistpromos":
            if not bot.promos:
                bot.my_bot.send_message(callback.message.chat.id, "Активных промокодов нет.")
            else:
              #  bot.my_bot.answer_callback_query(callback.id)
                # Отправляем каждое промо отдельным сообщением с кнопкой удаления
                for pid, p in bot.promos.items():
                    expires = datetime.fromtimestamp(p['expires_at']).strftime('%d.%m.%Y')
                    games = ", ".join(p['games_exact'])
                    uses = f"{p['current_uses']}/{p['max_uses']}" if p['max_uses'] > 0 else "Безлимит"
                    txt = f"🆔 `{pid}`\n🎮 Игры: {games}\n💸 Скидка: {p['discount_pct']}%\n🔄 Использований: {uses}\n⏳ До: {expires}"
                    
                    markup_del = types.InlineKeyboardMarkup()
                    markup_del.add(types.InlineKeyboardButton("🗑 Удалить промо", callback_data=f"admindelpromo_{pid}"))
                    
                    bot.my_bot.send_message(callback.message.chat.id, txt, parse_mode='Markdown', reply_markup=markup_del)

        # 🔥 КНОПКА: УДАЛИТЬ ПРОМО
        elif id1 == "admindelpromo":
            promo_id = callback.data.split("admindelpromo_")[1]
            if promo_id in bot.promos:
                del bot.promos[promo_id]
                bot.save_promos() # Сохраняем в shelve
                bot.my_bot.send_message(callback.id, "✅ Промокод успешно удален!")
                # Удаляем сообщение из чата, чтобы не засорять
                try:
                    bot.my_bot.delete_message(callback.message.chat.id, callback.message.message_id)
                except:
                    pass
            else:
                bot.my_bot.send_message(callback.id, "❌ Промокод не найден.")

        elif id1=="newpercent":
            num=callback.data[callback.data.find('_')+1:]
            txt568="Пожалуйста, введите новый процент (от 0 до 100)"
            bot.my_bot.send_message(callback.message.chat.id, txt568)
            bot.routes[callback.message.chat.id]['route']="newpercent"
            bot.routes[callback.message.chat.id]['mypopusk']=num

        elif id1=="cashcashcash":
            num=callback.data[callback.data.find('_')+1:]
            txt568="Пожалуйста, введите сумму (числом (цифрами (без буков)))"
            bot.my_bot.send_message(callback.message.chat.id, txt568)
            bot.routes[callback.message.chat.id]['route']="cashcashcash"
            bot.routes[callback.message.chat.id]['mypopusk']=num

        elif id1=='newgame':
            num=callback.data[callback.data.find('_')+1:]
            fv=bot.favo.get(str(num),[])
            if len(fv)>=10 and str(num) not in bot.ids:
                bot.my_bot.send_message(num, 'Максимальное количество игр в избранном - 10')
            else:
                st='search'
                txt568="Пожалуйста, введите название игры для Nintendo Switch на английском."
                bot.my_bot.send_message(num, txt568)
        
                bot.routes[int(num)]={'route':st}
                #bot.routes[int(num)]['route']='fv_newgame'
                #bot.my_bot.send_message(num, 'Название игры')
                
        elif id1=='delgame':
            num=callback.data[callback.data.find('_')+1:]
            bot.routes[int(num)]['route']='fv_delgame'
            bot.my_bot.send_message(num, 'Номер игры')
        elif id1=='clearbox':
             num=callback.data[callback.data.find('_')+1:]
             bot.great_box[int(num)]=[]
             
             bot.my_bot.send_message(num, 'Корзина очищена')
        elif id1 == 'buybox':
            user = int(callback.data[callback.data.find('_')+1:callback.data.find('$')])
            mid = callback.data[callback.data.find('$')+1:]
            bx = bot.great_box.get(user, [])
            
            if len(bx) == 0:
                bot.my_bot.send_message(user, "Ваша корзина пуста")
            else:
                stg = '💳 *Состав заказа:*\n'
                stga = '💳 *Детализация (для админа):*\n'
                stp = 0.0       # Итоговая цена для клиента
                allstp = 0.0    # Итоговый профит
                stpusa = 0.0    # Сумма в условных единицах
                
                # --- ЛОГИКА ПРОМОКОДА ---
                promo_id = bot.routes.get(user, {}).get('active_promo')
                promo_active = False
                discount_pct = 0
                discounted_games_norm = []
                
                if promo_id and promo_id in bot.promos:
                    p = bot.promos[promo_id]
                    if time.time() <= p['expires_at'] and (p['max_uses'] == 0 or p['current_uses'] < p['max_uses']):
                        promo_active = True
                        discount_pct = p['discount_pct']
                        discounted_games_norm = p['games_norm']
                # ------------------------

                arrord = {
                    'US': '$ (США)', 'GB': '£ (Великобритания)', 'UK': '£ (Великобритания)',
                    'CA': '$ (Канада)', 'MX': 'Peso (Мексика)', 'PL': 'zł (Польша)',
                    'AU': '$ (Австралия)', 'JP': '￥ (Япония)', 'NO': 'kr (Норвегия)',
                    'SE': 'kr (Швеция)', 'BR': 'R$ (Бразилия)', 'HK': 'HK$ (Гонконг)',
                    'KR': '₩ (Южная Корея)', 'TR': '₺ (Турция)', 'AR': '$ (Аргентина)',
                    'IN': '₹ (Индия)', 'UA': '₴ (Украина)', 'KZ': '₸ (Казахстан)',
                    'CN': '¥ (Китай)', 'NZ': '$ (Новая Зеландия)', 'CH': 'CHF (Швейцария)',
                    'DK': 'kr (Дания)', 'CZ': 'Kč (Чехия)', 'British Pound': '(Англия)',
                    'USD': '(США)', 'Canadian Dollar': '(Канада)', 'Mexican Peso': '(Мексика)',
                    'Polish Zloty': '(Польша)', 'Australian Dollar': '(Австралия)',
                    'Japanese Yen': '(Япония)', 'USD+': '(Мексика [PsPrices])',
                    'Norwegian Krone': '(Норвегия)', 'Swedish Krona': '(Швеция)'
                }
                
                for b in bx:
                    game_name = b[0][0]
                    marg = arrord.get(b[1][2], '')
                    base_price = float(b[0][1])
                    
                    # Проверяем скидку
                    is_discounted = False
                    if promo_active:
                        game_name_low = bot.st_in_lowst(game_name)
                        for dg_norm in discounted_games_norm:
                            if game_name_low == dg_norm:
                                is_discounted = True
                                break

                    final_price = base_price
                    discount_label = ""
                    
                    if is_discounted:
                        final_price = base_price * (1 - discount_pct / 100)
                        discount_label = f" 🔥 (-{discount_pct}%)"
                    
                    stp += final_price
                    # ВАЖНО: Профит считаем от РЕАЛЬНОЙ цены продажи (final_price), а не базовой!
                    allstp += bot.get_my_profit(final_price) 
                    
                    asus = "$"
                    if "Япония" in marg: asus = '￥'
                    if 'Бразилия' in marg: asus = 'R$'
                    if 'ХонгБонг' in marg or 'Гонконг' in marg: asus = 'HK$'
                    if 'Корея' in marg: asus = '₩'
                    
                    stg += f"🎮 *{game_name}* — `{final_price:.2f}` ₽{discount_label}\n"
                    stga += f"🎮 {game_name} — {final_price:.2f} ₽ ({float(b[1][1]):.2f} {asus} {marg})\n"
                    
                    if "Япония" in marg:
                        stpusa += float(b[1][1]) / bot.courses.get('Japanese Yen', 1)
                    else:
                        stpusa += float(b[1][1])

                # Применяем скидку 5% за 3+ игры (используем round вместо // 1, чтобы не терять копейки)
                if len(bx) >= 3:
                    stp = round(stp * 0.95, 2)
                    stpusa = round(stpusa * 0.95, 2)
                    allstp = round(allstp * 0.95, 2)
                    stga += "\n✅ Применена скидка 5% за заказ от 3 игр (учтена в итоговой сумме)"
                    stg += "\n✅ *Скидка 5% за заказ от 3 игр (уже учтена)*"

                # Формируем заказ
                bot.stack.append({
                    'Дата': bot.get_day(),
                    'Заказ': stg,
                    'Менеджер': '',
                    'Клиент': user,
                    'Статус': 'Создан',
                    'Цена': stp,
                    'Профит': allstp,
                    'stga': stga,
                    'stpusa': stpusa,
                    "Номер": bot.num
                })
                bot.num += 1
                
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('✅ Подтвердить заказ', callback_data='acceptorder_' + str(user) + '+' + str(len(bot.stack)-1) + '$' + str(mid)))
                markup.add(types.InlineKeyboardButton('❌ Отменить заказ', callback_data='breakorder_' + str(user)))
                
                bot.my_bot.send_message(user, stg, reply_markup=markup, parse_mode='Markdown')
        elif id1=='buybox':
             user=callback.data[callback.data.find('_')+1:callback.data.find('$')]
             mid=callback.data[callback.data.find('$')+1:]
             bx=bot.great_box.get(int(user),[])
             if len(bx)==0:
                 bot.my_bot.send_message(user, "Ваша корзина пуста")
             else:
                 stg='\n'
                 stga='\n'
                 stp=0
                 allstp=0
                 stpusa=0
                 arrord={
    # === ОФИЦИАЛЬНЫЕ ISO КОДЫ СТРАН (Alpha-2) ===
    'US': '$ (США)',
    'GB': '£ (Великобритания)',
    'UK': '£ (Великобритания)',  # Неофициальный, но часто встречается
    'CA': '$ (Канада)',
    'MX': 'Peso (Мексика)',
    'PL': 'zł (Польша)',
    'AU': '$ (Австралия)',
    'JP': '￥ (Япония)',
    'NO': 'kr (Норвегия)',
    'SE': 'kr (Швеция)',
    'BR': 'R$ (Бразилия)',
    'HK': 'HK$ (Гонконг)',
    'KR': '₩ (Южная Корея)',
    
    # === ДОП. ПОПУЛЯРНЫЕ РЕГИОНЫ (на всякий случай, для игр) ===
    'TR': '₺ (Турция)',
    'AR': '$ (Аргентина)',
    'IN': '₹ (Индия)',
    'UA': '₴ (Украина)',
    'KZ': '₸ (Казахстан)',
    'CN': '¥ (Китай)',
    'NZ': '$ (Новая Зеландия)',
    'CH': 'CHF (Швейцария)',
    'DK': 'kr (Дания)',
    'CZ': 'Kč (Чехия)','British Pound':'(Англия)','USD':'(США)','Canadian Dollar':'(Канада)','Mexican Peso':'(Мексика)','Polish Zloty':'(Польша)','Australian Dollar':'(Австралия)','Japanese Yen':'(Япония)','USD+':'(Мексика [PsPrices])','Norwegian Krone':'(Норвегия)','Swedish Krona':'(Швеция)'}
                 for b in bx:
                     marg=arrord.get(b[1][2],'')
                     stg+=b[0][0]+' - '+str(b[0][1])+' ₽\n'
                     asus="$"
                     if "Япония" in marg:
                        asus='￥'
                     if 'Бразилия' in marg:
                        asus='R$'
                     if 'ХонгБонг' in marg:
                        asus='HK$'
                     if 'Корея' in marg:
                        asus='₩'
                     stga+=b[0][0]+' - '+str(b[0][1])+' ₽ ('+str(float(b[1][1])*100//1/100)+f' {asus} '+str(marg)+'\n'
                     stp+=float(b[0][1])
                     if "Япония" in marg:
                        stpusa+=float(b[1][1])/bot.courses['Japanese Yen']
                     else:
                        stpusa+=float(b[1][1])
                     allstp+=bot.get_my_profit(b[0][1])
                 if len (bx)>=3:
                     stp=(stp*0.95)//1
                     stpusa=(stpusa*0.95)*100//1/100
                     allstp=(allstp*0.95)//1
                     stga+="\nСкидка в 5% за заказ от 3 игр (уже учтена)"
                     stg+="Скидка в 5% за заказ от 3 игр\n"
                 bot.stack.append({'Дата':bot.get_day(),'Заказ':stg,'Менеджер':'','Клиент':user,'Статус':'Создан','Цена':float(stp),'Профит':allstp,'stga':stga,'stpusa':stpusa,"Номер":bot.num})
                 bot.num+=1
                 markup=types.InlineKeyboardMarkup()
                 markup.add(types.InlineKeyboardButton('Отправить заказ',callback_data='acceptorder_'+str(user)+'+'+str(len(bot.stack)-1)+'$'+str(mid)))
                 markup.add(types.InlineKeyboardButton('Отменить заказ',callback_data='breakorder_'+str(user)))
                 #markup.add(types.InlineKeyboardButton('Отменить заказ',callback_data=str(user)+'_'+str(user)+'+'+str(bot.num+1)))
                 bot.my_bot.send_message(user, "🛍 Вы приобретаете:\n"+stg,reply_markup=markup)#✅ Ваш заказ отправлен! В ближайшее время будет назначен менеджер для исполнения заказа.",reply_markup=markup)
                 

            
        elif id1=="breakorder":
            user=int(callback.data[callback.data.find('_')+1:])
            bot.my_bot.delete_message(callback.message.chat.id, callback.message.message_id)
            if len(bot.routes[user]['gamelist'])!=[]:
                bot.handle_search(callback.message,bot.routes[user]['gamelist'],"")
                bot.routes[user]['route']='gamelist'
       
        elif id1=="ignore":
            pass
            
        elif id1=='acceptorder':
            user=callback.data[callback.data.find('_')+1:callback.data.find('+')]
            ind=int(callback.data[callback.data.find('+')+1:callback.data.find('$')])
            mid=callback.data[callback.data.find('$')+1:]

            if ind<len(bot.stack):
                order=bot.stack[ind]
                stg=order['Заказ']
                stp=order['Цена']
                stga=order['stga']
                stpusa=order['stpusa']
                
                url=bot.create_url_pally(float(stp),order["Номер"])
                if "Ошибка" in url:
                     bot.my_bot.send_message(for_reports,url)
                     kurl="К сожалению платежная ссылка сломалась... Оплатить заказ всё-таки придется, для этого свяжитесь с менеджером."
                else:
                     bot.stack[ind]["url"]=url
                     kurl="Оплатить заказ можно по ссылке:\n"+url+"\n\nПожалуйста, после оплаты нажмите на кнопку 'Я оплатил заказ'"
                
                markup=types.InlineKeyboardMarkup()  
                markup.add(types.InlineKeyboardButton('Я оплатил заказ',callback_data='acceptorder4_'+str(user)+'+'+str(ind)+'$'+str(mid)))
                markup.add(types.InlineKeyboardButton('Я не могу оплатить заказ (помогите)',callback_data='acceptorder3_'+str(user)+'+'+str(ind)+'$'+str(mid)))
                markup.add(types.InlineKeyboardButton('Отменить заказ',callback_data=str(user)+'_'+str(user)+'+'+str(order["Номер"])))
                bot.my_bot.send_message(user, kurl,reply_markup=markup)#",reply_markup=markup)
                bot.my_bot.delete_message(callback.message.chat.id, callback.message.message_id)
                     
            else:
                bot.my_bot.send_message(user, "К сожалению, Ваш заказ был удалён из памяти бота. Попробуйте отправить его заново!")
            bot.adbot_save()
        elif id1=="acceptorder4": ##!!
            #
            tm=bot.routes[callback.from_user.id].get('timer_aco4',0)
            if time.time()-tm<120:
                user=callback.data[callback.data.find('_')+1:callback.data.find('+')]
                bot.my_bot.send_message(user, "⌛️Пожалуйста, ожидайте, проверяем оплату. Это может занять несколько минут")
            else:
                #
                user=callback.data[callback.data.find('_')+1:callback.data.find('+')]
                ind=int(callback.data[callback.data.find('+')+1:callback.data.find('$')])
                mid=callback.data[callback.data.find('$')+1:]
                bot.my_bot.send_message(for_reports,"Крч, тип нажал на оплачено")
                if ind<len(bot.stack):
                    order=bot.stack[ind]
                    stg=order['Заказ']
                    stp=order['Цена']
                    stga=order['stga']
                    stpusa=order['stpusa']
                    bot.my_bot.send_message(user, "⌛️Ожидайте, проверяем оплату. Это может занять несколько минут")
                    bot.routes[callback.from_user.id]['timer_aco4']=time.time()
                    tms=[3,15,30,60,120]
                    tmm=["начинаем первую проверку","начинаем вторую проверку","начинаем третью проверку","начинаем четвертую проверку","начинаем пятую проверку"]
                    coll=0
                    kurl=""
                    for i in range(5):
                        if coll==1: break
                        time.sleep(tms[i])
                        bot.my_bot.send_message(for_reports,tmm[i])
                        kurl=bot.check_num(order["Номер"])
                        if "Оплачен" in kurl:
                            coll=1
                            break
                    
                    
                    if "Оплачен" not in kurl and "Неизвестно" not in kurl and coll!=1:
                        bot.my_bot.send_message(user, "Оплата не прошла. Попробуйте нажать кнопку через какое-то время или свяжитесь с поддержкой через вторую кнопку")
                    else:
                        markup=types.InlineKeyboardMarkup()
                        if coll!=1 and "Оплачен" not in kurl: markup.add(types.InlineKeyboardButton('Отменить заказ',callback_data=str(user)+'_'+str(user)+'+'+str(order["Номер"])))
                        bot.my_bot.send_message(user, "✅ Ваш заказ отправлен! В ближайшее время будет назначен менеджер для исполнения заказа.",reply_markup=markup)#",reply_markup=markup)
                   #     bot.num+=1
                        bot.great_dic[order["Номер"]]=order
                        btn=order["Номер"]+0

                        # Увеличиваем счетчик использований промокода
                        promo_id = bot.routes.get(int(user), {}).get('active_promo')
                        if promo_id and promo_id in bot.promos:
                            if bot.promos[promo_id]['max_uses'] > 0:
                                bot.promos[promo_id]['current_uses'] += 1
                            # Очищаем промо у пользователя после успешного заказа, чтобы он не применялся к следующим
                            if 'active_promo' in bot.routes[int(user)]:
                                del bot.routes[int(user)]['active_promo']
                           # bot.adbot_save()

                        


                        db=shelve.open(PARTNERS_DATA_SHELVE)
                        referals=db.get("referals",{})
                        db.close()
                        for kkkey in referals:
                            rem=referals[kkkey]
                            if str(callback.from_user.id) in rem and order["Номер"] not in rem[str(callback.from_user.id)]["orders"]:
                                uim=rem[str(callback.from_user.id)]
                                uim["sum"]+=order["Цена"]
                                uim["profit"]+=order["Профит"]
                                uim["orders"].append(order["Номер"])
                                rem[str(callback.from_user.id)]=uim
                                referals[kkkey]=rem
                                try:
                                    bot.my_bot.send_message(for_reports, f'Мы бы хотели начислить {float(order["Профит"]*15/100)} попуску {kkkey}')
                                    for kikey in bot.popuski:
                                        if bot.popuski[kikey]["key"]==kkkey:
                                            bot.popuski[kikey]["cash"]+=float(order["Профит"]*bot.popuski[kikey]["percent"]/100) 
                                    
                                except:
                                    bot.my_bot.send_message(for_reports, traceback.format_exc())

                        db=shelve.open(PARTNERS_DATA_SHELVE)
                        db["referals"]=referals
                        db.close()
    
                        for id1 in bot.ids:
                            try:
                                username="неизвестно"
                                userm = callback.from_user
                                if userm.username:  # Проверяем, есть ли username
                                    username = f"@{userm.username}"
                                markup=types.InlineKeyboardMarkup()
                                markup.add(types.InlineKeyboardButton('Взять заказ',callback_data=str(id1)+'_'+str(user)+'+'+str(btn)))
                                pmj="$"
                                if "Япония" in str(stga):
                                    pmj='￥'
                                
                                if 'Бразилия' in str(stga):
                                    pmj='R$'
                                if 'ХонгБонг' in str(stga):
                                    pmj='HK$'
                                if 'Корея' in str(stga):
                                    pmj='₩'
                                bot.my_bot.send_message(id1,f"Новый запрос(1) №"+str(btn)+f" от {username} (статус: "+kurl+"):\n"+str(stga)+"\nСтоимость: "+str(stp)+' рублей \n'+str(stpusa*100//1/100)+f' {pmj}',reply_markup=markup)
                                try:
                                    bot.my_bot.forward_message(id1, user, mid)
                                except:
                                    bot.my_bot.send_message(id1,f"Без сообщения от пользователя")
                                

                                bot.my_bot.send_message(id1, str(stga)+"\nСтоимость: "+str(stp)+' рублей \n'+str(stpusa*100//1/100)+f' {pmj}',reply_markup=markup)
                            except Exception as e:
                                pass
                        bot.adbot_save()
                        bot.great_box[int(user)]=[]
                        time.sleep(10)
                        order=bot.great_dic[btn]
                        if order['Статус']=='Создан':
                            bot.my_bot.send_message(user, "⌛️ В рабочее время (9:00 - 23:00) заказы принимаются в среднем в течение 10 минут. \n⚠️ Пожалуйста, не отправляйте тот же заказ повторно! Если ожидание длится более 3 часов, нажмите «📜 Другое», «Сообщить о проблеме».")
                   
                    
                else:
                    bot.my_bot.send_message(user, "К сожалению, Ваш заказ был удалён из памяти бота. Попробуйте отправить его заново!")
        elif id1=='acceptorder2' or id1=="acceptorder3":
            user=callback.data[callback.data.find('_')+1:callback.data.find('+')]
            ind=int(callback.data[callback.data.find('+')+1:callback.data.find('$')])
            mid=callback.data[callback.data.find('$')+1:]

            if ind<len(bot.stack):
                order=bot.stack[ind]
                stg=order['Заказ']
                stp=order['Цена']
                stga=order['stga']
                stpusa=order['stpusa']
                url=order.get("url","null")
                kurl=bot.check_num(order["Номер"])
                bot.my_bot.send_message(for_reports,str(callback.data))
                bot.my_bot.send_message(for_reports,str(order))
                
                if "Оплачен" not in kurl and "3" not in id1 and "Неизвестно" not in kurl:
                    bot.my_bot.send_message(user, "Оплата не прошла. Попробуйте нажать кнопку через какое-то время или свяжитесь с поддержкой через вторую кнопку")
                else:
                    markup=types.InlineKeyboardMarkup()
                    markup.add(types.InlineKeyboardButton('Отменить заказ',callback_data=str(user)+'_'+str(user)+'+'+str(order["Номер"])))
                    bot.my_bot.send_message(user, "✅ Ваш заказ отправлен! В ближайшее время будет назначен менеджер для исполнения заказа.",reply_markup=markup)#",reply_markup=markup)
               #     bot.num+=1
                    bot.great_dic[order["Номер"]]=order
                    btn=order["Номер"]+0


                    db=shelve.open(PARTNERS_DATA_SHELVE)
                    referals=db.get("referals",{})
                    db.close()
                    for kkkey in referals:
                        rem=referals[kkkey]
                        if str(callback.from_user.id) in rem and order["Номер"] not in rem[str(callback.from_user.id)]["orders"]:
                            uim=rem[str(callback.from_user.id)]
                            uim["sum"]+=order["Цена"]
                            uim["profit"]+=order["Профит"]
                            uim["orders"].append(order["Номер"])
                            rem[str(callback.from_user.id)]=uim
                            referals[kkkey]=rem
                            try:
                                bot.my_bot.send_message(for_reports, f'Мы бы хотели начислить {float(order["Профит"]*15/100)} попуску {kkkey}')
                                for kikey in bot.popuski:
                                    if bot.popuski[kikey]["key"]==kkkey:
                                        bot.popuski[kikey]["cash"]+=float(order["Профит"]*bot.popuski[kikey]["percent"]/100) 
                            except:
                                bot.my_bot.send_message(for_reports, traceback.format_exc())

                    db=shelve.open(PARTNERS_DATA_SHELVE)
                    db["referals"]=referals
                    db.close()
                    bot.my_bot.send_message(for_reports,str(id1)+'_'+str(user)+'+'+str(btn))
                    for id41 in bot.ids:
                        try:
                            
                            username="неизвестно"
                            userm = callback.from_user
                            if userm.username:  # Проверяем, есть ли username
                                username = f"@{userm.username}"
                            markup=types.InlineKeyboardMarkup()
                            markup.add(types.InlineKeyboardButton('Взять заказ',callback_data=str(id41)+'_'+str(user)+'+'+str(btn)))
                            pmj="$"
                            if "Япония" in str(stga):
                                pmj='￥'
                                
                            if 'Бразилия' in str(stga):
                                pmj='R$'
                            if 'ХонгБонг' in str(stga):
                                pmj='HK$'
                            if 'Корея' in str(stga):
                                pmj='₩'
                            bot.my_bot.send_message(id41,f"Новый запрос(2) №"+str(btn)+f" от {username} (статус: "+kurl+"):\n"+str(stga)+"\nСтоимость: "+str(stp)+' рублей \n'+str(stpusa*100//1/100)+f' {pmj}',reply_markup=markup)

                            try:
                                bot.my_bot.forward_message(id41, user, mid)
                            except:
                                bot.my_bot.send_message(id41,f"Без сообщения от пользователя")
                        
                            
                         #   self.my_bot.send_message(id1, str(arr[0])+". Стоимость: "+str(arr[1])+' '+dst,reply_markup=markup)
                            bot.my_bot.send_message(id41, str(stga)+"\nСтоимость: "+str(stp)+' рублей \n'+str(stpusa*100//1/100)+' $',reply_markup=markup)
                        except Exception as e:
                            pass
                          #  bot.my_bot.send_message(for_reports,traceback.format_exc())
                    bot.adbot_save()
                    bot.great_box[int(user)]=[]
                    time.sleep(10)
                    order=bot.great_dic[btn]
                    if order['Статус']=='Создан':
                        bot.my_bot.send_message(user, "⌛️ В рабочее время (9:00 - 23:00) заказы принимаются в среднем в течение 10 минут. \n⚠️ Пожалуйста, не отправляйте тот же заказ повторно! Если ожидание длится более 3 часов, нажмите «📜 Другое», «Сообщить о проблеме».")
                     
            else:
                print(ind,bot.stack)
                bot.my_bot.send_message(user, "К сожалению, Ваш заказ был удалён из памяти бота. Попробуйте отправить его заново!")
            bot.adbot_save()

        elif id1=='breaktorder':
            user=callback.data[callback.data.find('_')+1:callback.data.find('+')]
            bot.my_bot.send_message(user, "Вы отменили заказ...")
             
             
        elif id1=='buygame':
            
         #   message_time = callback.date
            #message_datetime = datetime.fromtimestamp(message_time)
            message_datetime = datetime.now()
            try:
                message_time = callback.message.date
                message_datetime = datetime.fromtimestamp(message_time)
            except:
                pass
            current_time = datetime.now()
            time_difference = current_time - message_datetime
            if time_difference > timedelta(hours=24):
                bot.my_bot.send_message(callback.message.chat.id, 'Это сообщение было отправлено более суток назад. Пожалуйста, проверьте цену товара через поиск')
                
            else:
                try:
                    bot.my_bot.delete_message(callback.message.chat.id, callback.message.message_id)
                except:
                    pass
                id2=callback.data[callback.data.find('_')+1:callback.data.find('+')]
                num=callback.data[callback.data.find('+')+1:callback.data.find('$')]
                mid=callback.data[callback.data.find('$')+1:]
                bot.pro_gamelist545(int(id2),int(num),int(mid))
                bot.adbot_save()
        elif id1=="selectgame":
            message_datetime = datetime.now()
            try:
                message_time = callback.message.date
                message_datetime = datetime.fromtimestamp(message_time)
            except:
                pass
            current_time = datetime.now()
            time_difference = current_time - message_datetime
            if time_difference > timedelta(hours=24):
                bot.my_bot.send_message(callback.message.chat.id, 'Это сообщение было отправлено более суток назад. Пожалуйста, проверьте цену товара через поиск')
                
            else:
                
                num=callback.data[callback.data.find('_')+1:callback.data.find('$')]
                mid=callback.data[callback.data.find('$')+1:]
                user=callback.message.chat.id
                try:
                    ind=int(num)
                except ValueError:
                    bot.my_bot.send_message(user, '''\n\n#️⃣ Укажите номер игры, которую вы хотите приобрести или добавить в Избранное
        
        (например: 1).
        
        ❗️Если вы хотите узнать цену на другую игру, нажмите на «Поиск игры» снова.''',reply_markup=bot.markup)
                    return 0
                try:
                    pass
                 #   bot.my_bot.delete_message(callback.message.chat.id, callback.message.message_id)
                except:
                    pass
                ind-=1
                results=bot.routes[user]['gamelist']
                if ind>=0 and ind<len(results):
                    arr=results[ind]
                    markupin=types.InlineKeyboardMarkup()
                    markupin.add(types.InlineKeyboardButton('💸 Купить игру сразу',callback_data='buygame_'+str(callback.message.chat.id)+'+'+str(ind)+'$'+str(mid)))
                    markupin.add(types.InlineKeyboardButton('🛒 Добавить игру в корзину',callback_data='boxgame_'+str(user)+'+'+str(ind)+'$'+str(mid)))
                    markupin.add(types.InlineKeyboardButton('🌟 Добавить в Избранное',callback_data='pingame_'+str(user)+'+'+str(ind)))
              
                    markupin.add(types.InlineKeyboardButton('Назад',callback_data='nbackgame_'+str(user)+'+'+str(ind)))
                    bot.my_bot.send_message(user, "Вы выбрали "+arr[0]+". Стоимость: "+str(arr[1])+" руб",reply_markup=markupin)
                else:
                    bot.my_bot.send_message(user, 'Пожалуйста, введите номер игры от 1 до '+str(len(results)),reply_markup=bot.markup)
                    
                    #
        elif id1=='boxgame':
            
         #   message_time = callback.date
            #message_datetime = datetime.fromtimestamp(message_time)
            message_datetime = datetime.now()
            try:
                message_time = callback.message.date
                message_datetime = datetime.fromtimestamp(message_time)
            except:
                pass
            current_time = datetime.now()
            time_difference = current_time - message_datetime
            if time_difference > timedelta(hours=24):
                bot.my_bot.send_message(callback.message.chat.id, 'Это сообщение было отправлено более суток назад. Пожалуйста, проверьте цену товара через поиск')
                
            else:
                try:
                    bot.my_bot.delete_message(callback.message.chat.id, callback.message.message_id)
                except:
                    pass
                id2=callback.data[callback.data.find('_')+1:callback.data.find('+')]
                num=callback.data[callback.data.find('+')+1:callback.data.find('$')]
                mid=callback.data[callback.data.find('$')+1:]
                bot.pro_gamelist545_boxgame(int(id2),int(num),int(mid))
        elif id1=='pingame':
            try:
                bot.my_bot.delete_message(callback.message.chat.id, callback.message.message_id)
            except:
                pass
            id2=callback.data[callback.data.find('_')+1:callback.data.find('+')]
            num=int(callback.data[callback.data.find('+')+1:])
            fv=bot.favo.get(str(id2),[])
            bot.routes[int(id2)]['route']='start'
            if len(fv)>=10 and str(id2) not in bot.ids:
                bot.my_bot.send_message(num, 'Максимальное количество игр в избранном - 10')
            else:
            
                results=bot.routes[int(id2)]['gamelist']
                arr=results[num]
                fv=bot.favo.get(str(id2),[])
                fv.append(arr[0])
                bot.favo[str(id2)]=fv
            # дбв1
                gm=arr[0]
                usd=-1
                val=arr[2]+""
                a=''
                if bot.st_in_lowst(arr[0])==bot.st_in_lowst(gm):
                    a=gm
                if a!='':
                    bot.favo_price[a]=[arr[1],arr[1],time.time(),usd,val]
                if arr[3]!=-1 and a!='': bot.favo_price[a][1]=bot.usd_to_rub(arr[3],arr[2])

            #
                markupin=types.InlineKeyboardMarkup()
                markupin.add(types.InlineKeyboardButton("🚫 Убрать из Избранного",callback_data='delpingame_'+str(id2)))
                markupin.add(types.InlineKeyboardButton("🔎 Найти ещё игру",callback_data='findgame_'+str(id2)))
                markupin.add(types.InlineKeyboardButton('Назад',callback_data='nbackgame_'+str(id2)+'+'+str(0)))
                bot.my_bot.send_message(id2, arr[0]+" успешно добавлена в 🌟 Избранное. Вы получите уведомление, когда на игру будет действовать скидка",reply_markup=markupin)
        elif id1=='delpingame':
            id2=int(callback.data[callback.data.find('_')+1:])
            fv=bot.favo.get(str(id2),[])
            if len(fv)==0:
                bot.my_bot.send_message(id2, "Ваш список Избранного пуст")
            else:
                game=fv[-1]
                fv.pop(-1)
                bot.favo[str(id2)]=fv
                bot.my_bot.send_message(id2, str(game)+" удалена из вашего списка избранного. Воспользуйтесь поиском, чтобы добавить в него интересующие игры")
        elif id1=='ndelgame':
            bot.my_bot.delete_message(callback.message.chat.id, callback.message.message_id)
        elif id1=="nbackgame":
            bot.my_bot.delete_message(callback.message.chat.id, callback.message.message_id)
          #  bot.handle_search(callback.message,bot.routes[callback.message.chat.id]['gamelist'],"")
            bot.routes[callback.message.chat.id]['route']='gamelist'
        elif id1=='sendwtmessage':
            num=int(callback.data[callback.data.find('_')+1:])
            bot.routes[num]['route']='sendwtmessage'
            txt568="Введите сообщение для пользователя"
            bot.my_bot.send_message(num, txt568)
        elif id1=="getwtorder":
            order_num=int(callback.data[callback.data.find('_')+1:])

            #
            manager=str(callback.from_user.id)
            customer=bot.great_dic[order_num]['Клиент']
            #
            bot.great_dic[order_num]['Статус']='Принят'
            bot.great_dic[order_num]['Менеджер']=bot.auth.get(manager,'')
            for i in bot.ids:
                try:
                    if str(i)==str(manager):
                        markup=types.InlineKeyboardMarkup()
                        markup.add(types.InlineKeyboardButton('Отменить заказ',callback_data='killz_'+str(customer)+'+'+str(order_num)))
                        bot.my_bot.send_message(i, 'Вы приняли заказ №'+str(order_num),reply_markup=markup)
                    else:
                        bot.my_bot.send_message(i, 'Заказ №'+str(order_num)+' принят менеджером: '+bot.auth.get(manager,''))
                except:
                    pass
            bot.my_bot.send_message(customer, 'Ваш заказ принят менеджером: '+bot.auth.get(manager,'')+'. Пожалуйста, свяжитесь с менеджером самостоятельно, если у вас закрыты сообщения')
                    
            #

        elif id1=='findgame':
            num=int(callback.data[callback.data.find('_')+1:])
            st='search'
            txt568="Пожалуйста, введите название игры для Nintendo Switch на английском для расчёта актуальной стоимости её покупки на ваш аккаунт."
            bot.my_bot.send_message(num, txt568)
        
            bot.routes[num]={'route':st}
        elif id1=='mybox':
            user=int(callback.data[callback.data.find('_')+1:callback.data.find('+')])
            mid=int(callback.data[callback.data.find('+')+1:])
            bx=bot.great_box.get(user,[])
            if len(bx)==0:
                bot.my_bot.send_message(user, 'Ваша корзина пуста')
            else:
                # 🔥 ПРОВЕРКА АКТИВНОГО ПРОМО
                promo_id = bot.routes.get(user, {}).get('active_promo')
                promo_active = False
                discount_pct = 0
                discounted_games_norm = []
                
                if promo_id and promo_id in bot.promos:
                    p = bot.promos[promo_id]
                    if time.time() <= p['expires_at'] and (p['max_uses'] == 0 or p['current_uses'] < p['max_uses']):
                        promo_active = True
                        discount_pct = p['discount_pct']
                        discounted_games_norm = p['games_norm']
                
                markupin=types.InlineKeyboardMarkup()
                markupin.add(types.InlineKeyboardButton('Очистить корзину',callback_data='clearbox_'+str(user)))
                markupin.add(types.InlineKeyboardButton('Купить',callback_data='buybox_'+str(user)+'$'+str(mid)))
                
                txt="Сейчас в Вашей корзине:\n"
                total_sum = 0
                
                for b in bx:
                    game_name = b[0][0]
                    game_name_norm = bot.st_in_lowst(game_name)
                    base_price = float(b[0][1])
                    
                    # 🔥 ЖЕЛЕЗОБЕТОННОЕ СРАВНЕНИЕ через нормализацию
                    is_discounted = False
                    if promo_active:
                        game_name_norm = bot.st_in_lowst(b[0][0])
                        for dg_norm in discounted_games_norm:
                            if game_name_norm == dg_norm:  # Только полное совпадение!
                                is_discounted = True
                                break
                    if is_discounted:
                        final_price = base_price * (1 - discount_pct / 100)
                        txt += f"🔥 {game_name} - {final_price:.2f} ₽ <s>{base_price:.2f}</s> ₽ (-{discount_pct}%)\n"
                    else:
                        final_price = base_price
                        txt += f"{game_name} - {final_price:.2f} ₽\n"
                    
                    total_sum += final_price
                    
                if promo_active:
                    txt += f"\n✅ Применена промо-скидка {discount_pct}% на выбранные игры!"
                    
                bot.my_bot.send_message(user, txt, reply_markup=markupin, parse_mode='HTML')
        
        elif id1=="codeofkpk":
            #
            num=int(callback.data[callback.data.find('_')+1:])
            
            regions=[]
            for arti in bot.popups:
                if bot.popups[arti]["Регион"] not in regions:
                    regions.append(bot.popups[arti]["Регион"])
         
            cdc=[]
            for arti in bot.popups:
                n=len(bot.popups_codes.get(arti,[]))
                dct=bot.popups[arti].copy()
                dct["Количество"]=n
                if n>=0 and bot.popups[arti]["Регион"]==regions[num]:
                    cdc.append(dct)

            #
            msg="По Вашему запросу найдено:\n\n"
            i=1
            markupin=types.InlineKeyboardMarkup()
            for offer in cdc:
                
                msg+=f"{i}. {offer['Наименование']} - {offer['Цена в рублях']} ₽\n"
                hj=f"{i}. {offer['Наименование']}"[:40]+f" - {offer['Цена в рублях']} ₽"
                markupin.add(types.InlineKeyboardButton(hj,callback_data='codebuy_'+offer['Артикул']))
                i+=1
            
            my_popug= BAD_POPUG_PNG
            with open(my_popug, 'rb') as photo:
                bot.my_bot.send_photo(
                    chat_id=callback.from_user.id,
                    photo=photo,  # Передаем файловый объект
                    caption=msg,
                    
                    reply_markup=markupin,
                    parse_mode='HTML'
                )

        elif id1=="codebuy":
            sku=callback.data[callback.data.find('_')+1:]
            item=bot.popups.get(sku,{})
            user=callback.from_user.id
            if len(item)==0:
                
                bot.my_bot.send_message(callback.from_user.id,"Нет сведений о наличии данного кода... Попробуйте поиск заново")
            else:
                kurl=f"🛍 Вы приобретаете:\n{item['Наименование']} - {item['Цена в рублях']} ₽"
                markup=types.InlineKeyboardMarkup()  
                markup.add(types.InlineKeyboardButton('Оплатить заказ',callback_data='acceptcdc_'+sku))
                markup.add(types.InlineKeyboardButton('Отменить заказ',callback_data='breakorder_'+str(user)))
                bot.my_bot.send_message(user, kurl,reply_markup=markup)#",reply_markup=markup)
        elif id1=="acceptcdc":
            sku=callback.data[callback.data.find('_')+1:]
            item=bot.popups.get(sku,{})
            if len(item)==0:
                bot.my_bot.send_message(callback.from_user.id,"Нет сведений о наличии данного кода... Попробуйте поиск заново")
            else:
                mid=bot.cdc_id
                url=bot.create_url_pally(float(item["Цена в рублях"]),mid)
                bot.cdc_id+=1
                bot.cdc_orders[mid]={"url":url,'item':item.copy(),'sku':sku,'user':callback.from_user.id,"status":"create"}
                bot.adbot_save()
                caption=f"Ваша ссылка для оплаты: {url}"
                markup=types.InlineKeyboardMarkup()  
                markup.add(types.InlineKeyboardButton('Я оплатил заказ',callback_data=f'finalcdc_{mid}'))
            #    markup.add(types.InlineKeyboardButton('Я не могу оплатить заказ (помогите)',callback_data=f'finalcdc_{mid}'))
                markup.add(types.InlineKeyboardButton('Отменить заказ',callback_data=f"killcdc_{mid}"))
                bot.my_bot.send_message(callback.from_user.id, caption,reply_markup=markup)#",reply_markup=markup)
                bot.my_bot.delete_message(callback.message.chat.id, callback.message.message_id)
        elif id1=="killcdc":
            mid=int(callback.data[callback.data.find('_')+1:])
            bot.cdc_orders[mid]["status"]="break by user"
            bot.adbot_save()
            bot.my_bot.send_message(callback.from_user.id, "Ваш заказ успешно отменен")
            bot.my_bot.delete_message(callback.message.chat.id, callback.message.message_id)

        elif id1=="finalcdc":
            mid=int(callback.data[callback.data.find('_')+1:])
            order=bot.cdc_orders[mid]
            coll=-1
            kurl=bot.check_num(mid)
          #  coll=1 ##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if "Оплачен" in kurl or callback.from_user.id==int(for_reports):
                coll=1
               # bot.my_bot.delete_message(callback.message.chat.id, callback.message.message_id)
            if "Оплачен" not in kurl and "Неизвестно" not in kurl and coll!=1:
                bot.my_bot.send_message(callback.from_user.id, "Оплата не прошла. Попробуйте нажать кнопку через какое-то время или свяжитесь с поддержкой через вторую кнопку")
            else:
                
                
                order2={'Дата':bot.get_day(),'Заказ':f"Код пополнения {order['item']['Наименование']}",'Менеджер':'','Клиент':callback.from_user.id,'Статус':'Создан','Цена':float(order["item"]["Цена в рублях"]),'Профит':float(order["item"]["Цена в рублях"])-float(order["item"]["Себестоимость в рублях"]),'stga':"",'stpusa':-1,"Номер":mid}

                db=shelve.open(PARTNERS_DATA_SHELVE)
                referals=db.get("referals",{})
                db.close()
                for kkkey in referals:
                    rem=referals[kkkey]
                    if str(callback.from_user.id) in rem and mid not in rem[str(callback.from_user.id)]["orders"]:
                        uim=rem[str(callback.from_user.id)]
                        uim["sum"]+=float(order2["Цена"])
                        uim["profit"]+=order2["Профит"]
                        uim["orders"].append(mid)
                        rem[str(callback.from_user.id)]=uim
                        referals[kkkey]=rem
                        try:
                            bot.my_bot.send_message(for_reports, f'Мы бы хотели начислить {float(order2["Профит"]*15/100)} попуску {kkkey}')
                            for kikey in bot.popuski:
                                if bot.popuski[kikey]["key"]==kkkey:
                                    bot.popuski[kikey]["cash"]+=float(order2["Профит"]*bot.popuski[kikey]["percent"]/100) 
                        except:
                            bot.my_bot.send_message(for_reports, traceback.format_exc())

                db=shelve.open(PARTNERS_DATA_SHELVE)
                db["referals"]=referals
                db.close()

                if len(bot.popups_codes.get(order["item"]["Артикул"],[]))>0:
                    try:
                        secret=bot.popups_codes[order["item"]["Артикул"]][0]
                        bot.closed_popups.append(bot.popups_codes[order["item"]["Артикул"]].pop(0))
                        caption=f"Поздравляем с покупкой!\nВаш код: {secret}"
                        bot.my_bot.send_message(callback.from_user.id, caption)
                        caption=f'''
    ❔Как активировать карту пополнения:

    Чтобы активировать карту пополнения на Nintendo Switch, зайдите в Nintendo eShop из главного меню, выберите учётную запись, а затем нажмите "Активировать код" (Redeem Code), чтобы ввести 16-значный код. Нажмите "ОК" или "Подтвердить", чтобы завершить процесс. 

    ❕Готово, приятных покупок!'''
                        bot.my_bot.send_message(callback.from_user.id, caption)
                        bot.cdc_orders[mid]["status"]="closed"
                        bot.check_popups()
                        bot.adbot_save()
                    except:
                        pass
                else:

                    #
                    order2={'Дата':bot.get_day(),'Заказ':f"Код пополнения {order["item"]["Наименование"]}",'Менеджер':'','Клиент':callback.from_user.id,'Статус':'Создан','Цена':float(order["item"]["Цена в рублях"]),'Профит':float(order["item"]["Цена в рублях"])-float(order["item"]["Себестоимость в рублях"]),'stga':"",'stpusa':-1,"Номер":mid}
   
                    stg=order2['Заказ']
                    stp=order2['Цена']
                    stga=order2['stga']
                    stpusa=order2['stpusa']
                    bot.great_dic[order2["Номер"]]=order2
                    
                    for id1 in bot.ids:
                        try:
                            
                            username="неизвестно"
                            userm = callback.from_user
                            if userm.username:  # Проверяем, есть ли username
                                username = f"@{userm.username}"
                            markup=types.InlineKeyboardMarkup()
                            markup.add(types.InlineKeyboardButton('Взять заказ',callback_data=str(id1)+'_'+str(callback.from_user.id)+'+'+str(mid)))
                            pmj="$"
                            bot.my_bot.send_message(id1,f"Новый запрос(3) №"+str(mid)+f" от {username} (статус: "+kurl+f"):\n{stg}\nСтоимость: "+str(stp)+' рублей \n',reply_markup=markup)
                            
                         #   self.my_bot.send_message(id1, str(arr[0])+". Стоимость: "+str(arr[1])+' '+dst,reply_markup=markup)
                           # bot.my_bot.send_message(id1, str(stga)+"\nСтоимость: "+str(stp)+' рублей \n'+str(stpusa*100//1/100)+' $')
                        except Exception as e:
                            pass
                            #bot.my_bot.send_message(for_reports,traceback.format_exc())
                    bot.my_bot.send_message(callback.from_user.id,f"Ваш заказ будет обработан менеджером")
                    bot.adbot_save()


                    #
                
                                # отправка кода


        elif id1=="subbuy":
            sku=callback.data[callback.data.find('_')+1:]
            item=bot.subs.get(sku,{})
            user=callback.from_user.id
            if len(item)==0:
                
                bot.my_bot.send_message(callback.from_user.id,"Нет сведений о наличии данного кода... Попробуйте поиск заново")
            else:
                display_price = item['Цена в рублях']
                if bot.has_big_walk_discount(callback.from_user.id) and bot.is_nso_1month(item):
                    display_price = NSO_1M_DISC_PRICE
                    kurl = f"🛍 Вы приобретаете:\n{item['Наименование']} - {display_price} ₽ <s>{item['Цена в рублях']}</s> ₽\n🔥 Скидка за покупку BIG WALK!"
                else:
                    kurl = f"🛍 Вы приобретаете:\n{item['Наименование']} - {display_price} ₽"
                # -------------------------
                markup=types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Оплатить заказ',callback_data='acceptsub_'+sku))
                markup.add(types.InlineKeyboardButton('Отменить заказ',callback_data='breakorder_'+str(user)))
                bot.my_bot.send_message(user, kurl, reply_markup=markup, parse_mode='HTML')
        elif id1=="acceptsub":
            sku=callback.data[callback.data.find('_')+1:]
            item=bot.subs.get(sku,{})
            if len(item)==0:
                bot.my_bot.send_message(callback.from_user.id,"Нет сведений о наличии данного кода... Попробуйте поиск заново")
            else:
                mid=bot.cdc_id
                # --- BIG WALK discount ---
                pay_amount = float(item["Цена в рублях"])
                if bot.has_big_walk_discount(callback.from_user.id) and bot.is_nso_1month(item):
                    pay_amount = float(NSO_1M_DISC_PRICE)
                # -------------------------
                url=bot.create_url_pally(pay_amount, mid)
                bot.cdc_id+=1
                bot.cdc_orders[mid]={"url":url,'item':item.copy(),'sku':sku,'user':callback.from_user.id,"status":"create","pay_amount":pay_amount}
                bot.adbot_save()
                caption=f"Ваша ссылка для оплаты: {url}"
                markup=types.InlineKeyboardMarkup()  
                markup.add(types.InlineKeyboardButton('Я оплатил заказ',callback_data=f'finalsub_{mid}'))
            #    markup.add(types.InlineKeyboardButton('Я не могу оплатить заказ (помогите)',callback_data=f'finalcdc_{mid}'))
                markup.add(types.InlineKeyboardButton('Отменить заказ',callback_data=f"killcdc_{mid}"))
                bot.my_bot.send_message(callback.from_user.id, caption,reply_markup=markup)#",reply_markup=markup)
                bot.my_bot.delete_message(callback.message.chat.id, callback.message.message_id)


        elif id1=="finalsub":
        #    bot.my_bot.delete_message(callback.message.chat.id, callback.message.message_id)
            mid=int(callback.data[callback.data.find('_')+1:])
            order=bot.cdc_orders[mid]
            coll=-1
            kurl=bot.check_num(mid)
          #  coll=1 ##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if "Оплачен" in kurl:
                coll=1
            if "Оплачен" not in kurl and "Неизвестно" not in kurl and coll!=1:
                bot.my_bot.send_message(callback.from_user.id, "Оплата не прошла. Попробуйте нажать кнопку через какое-то время или свяжитесь с поддержкой через вторую кнопку")
            else:     
                        # --- BIG WALK discount ---
                actual_price = order.get("pay_amount", float(order["item"]["Цена в рублях"]))
                # -------------------------
                order2={'Дата':bot.get_day(),'Заказ':f"Код пополнения {order['item']['Наименование']}",'Менеджер':'','Клиент':callback.from_user.id,'Статус':'Создан','Цена':actual_price,'Профит':actual_price - float(order["item"]["Себестоимость в рублях"]),'stga':"",'stpusa':-1,"Номер":mid}
                db=shelve.open(PARTNERS_DATA_SHELVE)
                referals=db.get("referals",{})
                db.close()
                for kkkey in referals:
                    rem=referals[kkkey]
                    if str(callback.from_user.id) in rem and mid not in rem[str(callback.from_user.id)]["orders"]:
                        uim=rem[str(callback.from_user.id)]
                        uim["sum"]+=float(order2["Цена"])
                        uim["profit"]+=order2["Профит"]
                        uim["orders"].append(mid)
                        rem[str(callback.from_user.id)]=uim
                        referals[kkkey]=rem
                        try:
                            bot.my_bot.send_message(for_reports, f'Мы бы хотели начислить {float(order2["Профит"]*15/100)} попуску {kkkey}')
                            for kikey in bot.popuski:
                                if bot.popuski[kikey]["key"]==kkkey:
                                    bot.popuski[kikey]["cash"]+=float(order2["Профит"]*bot.popuski[kikey]["percent"]/100) 
                        except:
                            bot.my_bot.send_message(for_reports, traceback.format_exc())

                db=shelve.open(PARTNERS_DATA_SHELVE)
                db["referals"]=referals
                db.close()
            
                if len(bot.popups_codes.get(order["item"]["Артикул"],[]))>0:
                    try:
                        secret=bot.popups_codes[order["item"]["Артикул"]][0]
                        bot.closed_popups.append(bot.popups_codes[order["item"]["Артикул"]].pop(0))
                        caption=f"Поздравляем с покупкой!\nВаш код: {secret}"
                        bot.my_bot.send_message(callback.from_user.id, caption)
                        if order["item"]["Артикул"] in ["sub_year"]:
                            caption=f'''
        ❔Как активировать подписку:

        1) Убедитесь, что вы вошли в аккаунт, на который активируете подписку NSO, со своей консоли Nintendo Switch.
        2) Через браузер откройте страницу учётной записи Nintendo (accounts.nintendo.com), поменяйте регион профиля на Соединенные Штаты Америки.
        3) Войдите в eShop на своей консоли через профиль, на котором сменили регион, введите пароль, если потребуется.
        4) Через браузер откройте страницу ec.nintendo.com/redeem и введите полученный код (коды), подтвердите активацию кода.
        5) Перейдите на страницу ec.nintendo.com/US/en/membership, выберите необходимый уровень подписки, нажмите Purchase
        5) При оплате выберите способ оплаты Funds Only, если необходим Postal (Zip) Code, используйте безналоговый индекс 97222 (любой город), подтвердите оплату.
        6) При необходимости отмените автопродление подписки на странице accounts.nintendo.com/portal/membership и верните нужный регион аккаунта

        ❕Готово, приятной игры! Для проверки срока окончания подписки используйте приложение Nintendo Switch Online на консоли.'''
                        else:
                            caption=f'''
        ❔Как активировать подписку

        1) Убедитесь, что вы вошли в аккаунт, на который активируете подписку NSO, со своей консоли Nintendo Switch.
        2) Через браузер откройте страницу учётной записи Nintendo (accounts.nintendo.com), поменяйте регион профиля на Японию.
        3) Войдите в eShop на своей консоли через профиль, на котором сменили регион, введите пароль, если потребуется.
        4) Через браузер откройте страницу ec.nintendo.com/redeem и введите полученный код, подтвердите активацию кода.
        5) Отмените автопродление подписки на странице accounts.nintendo.com/portal/membership и верните нужный регион аккаунта
        6) Снова перезайдите в eShop на консоли для подтверждения смены региона.

        ❕Готово, приятной игры! Для проверки срока окончания подписки используйте приложение Nintendo Switch Online на консоли.'''
                        bot.my_bot.send_message(callback.from_user.id, caption)

                        bot.cdc_orders[mid]["status"]="closed"

                        bot.check_popups()
                        bot.adbot_save()
                    except:
                        pass
                else:

                    #
                    order2={'Дата':bot.get_day(),'Заказ':f"Код пополнения {order["item"]["Наименование"]}",'Менеджер':'','Клиент':callback.from_user.id,'Статус':'Создан','Цена':order["item"]["Цена в рублях"],'Профит':float(order["item"]["Цена в рублях"])-float(order["item"]["Себестоимость в рублях"]),'stga':"",'stpusa':-1,"Номер":mid}
   
                    stg=order2['Заказ']
                    stp=order2['Цена']
                    stga=order2['stga']
                    stpusa=order2['stpusa']
                    bot.great_dic[order2["Номер"]]=order2
                    
                    for id1 in bot.ids:
                        try:
                            
                            username="неизвестно"
                            userm = callback.from_user
                            if userm.username:  # Проверяем, есть ли username
                                username = f"@{userm.username}"
                            markup=types.InlineKeyboardMarkup()
                            markup.add(types.InlineKeyboardButton('Взять заказ',callback_data=str(id1)+'_'+str(callback.from_user.id)+'+'+str(mid)))
                            pmj="$"
                            bot.my_bot.send_message(id1,f"Новый запрос(5) №"+str(mid)+f" от {username} (статус: "+kurl+f"):\n{stg}\nСтоимость: "+str(stp)+' рублей \n',reply_markup=markup)
                            
                         #   self.my_bot.send_message(id1, str(arr[0])+". Стоимость: "+str(arr[1])+' '+dst,reply_markup=markup)
                           # bot.my_bot.send_message(id1, str(stga)+"\nСтоимость: "+str(stp)+' рублей \n'+str(stpusa*100//1/100)+' $')
                        except Exception as e:
                            pass
                            #bot.my_bot.send_message(for_reports,traceback.format_exc())
                    bot.my_bot.send_message(callback.from_user.id,f"Ваш заказ будет обработан менеджером")
                    bot.adbot_save()
                                # отправка кода



        
        elif id1=="reorder":
            id2=callback.data[callback.data.find('_')+1:]
            bot.routes[int(callback.message.chat.id)]['route']='reorder'
            bot.routes[int(callback.message.chat.id)]['reorder']=id2
            bot.my_bot.send_message(callback.message.chat.id,"Напишите свой ответ")
        elif id1=="inorder":
            coll=-1
            for key in bot.great_dic:
                if str(bot.great_dic[key]["Клиент"])==str(callback.message.chat.id) and bot.great_dic[key]["Менеджер"]:
                    coll=key 
            if coll!=-1:
                bot.routes[callback.message.chat.id]['route']='chat_order'
                bot.routes[callback.message.chat.id]['chat_order']=coll
               # bot.my_bot.send_message(callback.message.chat.id, f"Вы перешли в чат по заказу {coll}. Ваш менеджер: {bot.great_dic[coll]["Менеджер"]}\nНапишите \"Закончить чат\", чтобы вернуться в основной режим работы бота")
                bot.my_bot.send_message(callback.message.chat.id, f"Вы перешли в чат по заказу {coll}. Ваш менеджер: {bot.great_dic[coll]["Менеджер"]}\n")
            else:
                bot.my_bot.send_message(callback.message.chat.id, "К сожалению, чат не найден")
        elif id1=='killz':
            bot.my_bot.delete_message(callback.message.chat.id, callback.message.message_id)
            id11=str(callback.message.chat.id)
            id2=callback.data[callback.data.find('_')+1:callback.data.find('+')]
            num=callback.data[callback.data.find('+')+1:]
            if int(num) in bot.great_dic:
            
                if id11 in bot.ids:
                    if bot.great_dic[int(num)]['Статус']=='Принят':
                        bot.great_dic[int(num)]['Статус']='Отменен менеджером'
                        bot.my_bot.send_message(id2, 'Ваш заказ был отозван менеджером: '+bot.auth.get(id11,'')+'. Пожалуйста, свяжитесь с менеджером для уточнения причин отмены заказа самостоятельно, если у вас закрыты сообщения')
                        bot.my_bot.send_message(id11, 'Вы отозвали заказ')
                        
        else:
            id2=callback.data[callback.data.find('_')+1:callback.data.find('+')]
            num=callback.data[callback.data.find('+')+1:]

            if int(num) in bot.great_dic:
            
                if id1 in bot.ids:
                    if bot.great_dic[int(num)]['Статус']=='Отменен пользователем':
                    #    bot.my_bot.send_message(id2, 'Заказ был отменен пользователем')
                        bot.my_bot.send_message(id1, 'Заказ был отменен пользователем')
                    elif bot.great_dic[int(num)]['Статус']=='Создан':
                     
                        bot.great_dic[int(num)]['Статус']='Принят'
                        bot.great_dic[int(num)]['Менеджер']=bot.auth.get(id1,'')
                        for i in bot.ids:
                            try:
                                if str(i)==str(callback.message.chat.id):
                                    markup=types.InlineKeyboardMarkup()
                                    markup.add(types.InlineKeyboardButton('Отменить заказ',callback_data='killz_'+str(id2)+'+'+str(num)))
                                    markup.add(types.InlineKeyboardButton("Написать покупателю",callback_data=f"reorder_{bot.great_dic[int(num)]['Клиент']}"))
                                    bot.my_bot.send_message(i, 'Вы приняли заказ №'+str(num),reply_markup=markup)
                                else:
                                    bot.my_bot.send_message(i, 'Заказ №'+str(num)+' принят менеджером: '+bot.auth.get(id1,''))
                            except:
                                pass
                        
                        markup=types.InlineKeyboardMarkup()
                        markup.add(types.InlineKeyboardButton("Написать менеджеру",callback_data=f"inorder_{bot.great_dic[int(num)]['Менеджер']}"))
                        bot.my_bot.send_message(id2, 'Ваш заказ принят менеджером: '+bot.auth.get(id1,'')+'. Пожалуйста, свяжитесь с менеджером самостоятельно, если у вас закрыты сообщения',reply_markup=markup)
                    
                    else:
                        if id1 in bot.ids: 
                            bot.my_bot.send_message(id1, f'Заказ №{num}: текущий статус {bot.great_dic[int(num)]['Статус']}')
                       
                else:
                    bot.great_dic[int(num)]['Статус']='Отменен пользователем'
                    for i in bot.ids:
                        bot.my_bot.send_message(i, 'Заказ №'+str(num)+' отозван пользователем')
                    bot.my_bot.send_message(id2, 'Ваш заказ успешно отменен')
            else:
                if id1 in bot.ids: 
                    bot.my_bot.send_message(id1, f'Заказ №{num} не обнаружен в базе')
    except Exception as e:
        bot.my_bot.send_message(for_reports, callback.data)
        bot.my_bot.send_message(for_reports, traceback.format_exc())




############################################



# ========== ЗАДАЧИ С ИНТЕРВАЛОМ (секунды) ==========
INTERVAL_TASKS = {
  #  'check_orders': 300,      # каждые 5 минут
  #  'fast_task': 6,           # каждые 6 секунд
 #   'medium_task': 3600,      # каждый час
}

# ========== ЗАДАЧИ ПО РАСПИСАНИЮ (время) ==========
# Формат: 'время' : 'название_функции'
# Время можно указывать в разных форматах
SCHEDULED_TASKS = {
    '00:05': 'adbot_save',
    '01:05': 'adbot_refresh',
    '02:05': 'adbot_reprice',
    '03:05': 'adbot_reprice2',
    '12:00': 'adbot_send2',
}

# Хранилище для статуса выполнения дневных задач (чтобы не дублировать)
daily_tasks_done = {}

def run_scheduled_task(task_name):
    """Выполняет запланированную задачу"""
    try:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Запуск: {task_name}")
        
        if task_name == 'adbot_save':
            bot.adbot_save()
        elif task_name == 'adbot_refresh':
            bot.adbot_refresh()
            bot.adbot_auto_dgames()
            bot.au_update()
        elif task_name == 'adbot_reprice':
            bot.adbot_reprice()
        elif task_name == 'adbot_reprice2':
            bot.fix_gms={}
            bot.adbot_reprice2()
        elif task_name == 'adbot_send2':
            bot.adbot_send2()


        elif task_name == 'adbot_send':
            bot.alarm3=time.time()
            bot.au_lpr2()

            
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Выполнено: {task_name}")
        
    except Exception as e:
        print(f"Ошибка в запланированной задаче {task_name}: {e}")





def setup_scheduled_jobs():
    """Настраивает все запланированные задачи"""
    for time_str, task_name in SCHEDULED_TASKS.items():
        # schedule использует format "HH:MM"
        schedule.every().day.at(time_str).do(run_scheduled_task, task_name)
        print(f"Запланировано: {task_name} в {time_str}")

    schedule.every().saturday.at("10:00").do(run_scheduled_task, "adbot_send")

def interval_worker():
    """Фоновый поток для задач с интервалом"""
    last_run = {task: 0 for task in INTERVAL_TASKS}
    
    while True:
        current_time = time.time()
        
        for task_name, interval in INTERVAL_TASKS.items():
            if current_time - last_run[task_name] >= interval:
                try:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Интервал: {task_name}")
                    
                    # Вызываем нужную функцию
                    if task_name == 'check_orders':
                        bot.check_orders()
                    elif task_name == 'fast_task':
                        bot.fast_task()  # замени на свою
                    elif task_name == 'medium_task':
                        bot.medium_task()
                    
                    last_run[task_name] = current_time
                    
                except Exception as e:
                    print(f"Ошибка в {task_name}: {e}")
        
        time.sleep(1)  # не жрем процессор

def scheduled_worker():
    """Фоновый поток для запланированных задач"""
    while True:
        schedule.run_pending()
        time.sleep(1)

# ========== ЗАПУСК ==========

# Запускаем интервальные задачи
interval_thread = threading.Thread(target=interval_worker, daemon=True)
interval_thread.start()
print("✓ Интервальные задачи запущены")

# Настраиваем и запускаем запланированные задачи
setup_scheduled_jobs()
scheduled_thread = threading.Thread(target=scheduled_worker, daemon=True)
scheduled_thread.start()
print("✓ Запланированные задачи запущены")

############################################



bot.my_bot.polling(none_stop=True, interval=0)
