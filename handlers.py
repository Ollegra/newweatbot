from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import default_state
from tg_analytic import db_add, csv_to_db, out_stat, user_stat, exp_db_txt, user_xname
import requests
import datetime
# import time
from kbrd import main_keyboard, weat_keyboard, stat_keyboard, data_keyboard
from config import OW_TOKEN, COD_SM, FIL3
import logging
import speedtest
# aiogram==3.0.0b7

logger2 = logging.getLogger(__name__)
logger2.setLevel(logging.INFO)
handler2 = logging.FileHandler(f"{__name__}.log")
formatter2 = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler2.setFormatter(formatter2)
logger2.addHandler(handler2)

logger2.info(f'Handlers created for module {__name__}...')

gorod = ''
router = Router()

class FSMFillForm(StatesGroup):
    city_name = State()

#@router.message(Command("start"))
#async def start_handler(msg: Message):
#    await msg.answer("Привет! Я помогу тебе узнать твой ID, просто отправь мне любое сообщение")

#@router.message()
#async def message_handler(msg: Message):
#    await msg.answer(f"Твой ID: {msg.from_user.id}")

@router.message(Command('start'))
async def start_command(message: Message):
    db_add(message.chat.id, message.text, message.from_user.first_name)
    await message.answer(text=f'<b>{message.from_user.first_name}</b> напиши мне название города и я расскажу тебе о погоде')



@router.message(Command('help'))
async def help_command(message: Message):
    db_add(message.chat.id, message.text, message.from_user.first_name)
    await message.answer(text=f'🪧 <b>{message.from_user.first_name}</b> название города пишем так:\nDubai или dubai или Дубай или дубай ')

@router.message(Command('zakoma'))
async def zakoma_command(message: Message):
    await message.answer_photo(FIL3)

@router.message(Command('admin'))
async def remontdb(message: Message):
    db_add(message.chat.id, message.text, message.from_user.first_name)
    await message.answer('⚠ Режим работы с базой данных', reply_markup=data_keyboard())
    logger3.info(f'Database mode ON...')


@router.callback_query(lambda c: c.data == 'expo')
async def start_export(callback: CallbackQuery):
    await callback.answer()
    csv_to_db()
    logger2.info(f'Data export from csv to database completed...')
    await callback.answer('ℹ Data export from csv to database completed...', show_alert=True)


@router.callback_query(lambda c: c.data == 'save')
async def start_download(callback: CallbackQuery):
    exp_db_txt()
    await callback.answer('ℹ Data export from database to file csv completed...', show_alert=True)
    await callback.message.answer_document(document=FSInputFile('db_old.csv'))
    logger2.info(f'Data export from database to file csv completed...')
    await callback.message.delete()

@router.message(Command('users'))
async def stats_db(message: Message):
    db_add(message.chat.id, message.text, message.from_user.first_name)
    await message.answer('⚠ Режим работы со статистикой', reply_markup=stat_keyboard())
    logger2.info(f'Mode of working with statistics ON...')

@router.callback_query(lambda c: c.data == 'stat')
async def stat_stat(callback: CallbackQuery):
    await callback.answer()
    messages = out_stat()
    await callback.message.edit_text(text=messages, reply_markup=stat_keyboard())


@router.callback_query(lambda c: c.data == 'statx')
async def stat_statx(callback: CallbackQuery):
    await callback.answer()
    messages = user_stat()
    await callback.message.edit_text(text=messages, reply_markup=stat_keyboard())


@router.callback_query(lambda c: c.data == 'statn')
async def stat_statn(callback: CallbackQuery):
    await callback.answer()
    messages = user_xname()
    await callback.message.edit_text(text=messages, reply_markup=stat_keyboard())


@router.callback_query(lambda c: c.data == 'konec')
async def start_cancel(callback: CallbackQuery):
    await callback.answer(text='')
    logger2.info(f'Mode of working with statistics Off...')
    await callback.message.delete()


@router.message(F.photo)
async def send_photo(message: Message):
    print(message.photo[-1].file_id)
    await message.reply_photo(message.photo[-1].file_id)
    photo = max(message.photo, key=lambda x: x.height)
    file_id = photo.file_id
    print(file_id)
    logger2.info(f'Mode of working with Photo...')


@router.message(Command('speed'))
async def get_speed(message: Message):
    st = speedtest.Speedtest()
    sd = st.download() / (2 ** 20)
    su = st.upload() / (2 ** 20)
    mesage = f'Скорость вашего соединения:\n\n' \
              f'⬇  <b>DL</b> <i>{sd:.2f} Mb/s</i>, ⬆  <b>UL</b> <i>{su:.2f} Mb/s</i>'
    await message.answer(text=mesage)
    logger2.info(f'Determination of Internet connection speed completed...')

@router.message(Command('calcip'))
async def canip_command(message: Message):
    db_add(message.chat.id, message.text, message.from_user.first_name)
    textout = f'Информация по вашему IP адрессу:\n'
    try:
      response = requests.get(url=f'http://ip-api.com/json/?lang=ru&fields=status,message,continent,country,countryCode,region,regionName,city,zip,lat,lon,timezone,currency,isp,org,as,asname,query').json()
      #print(response)
      data = {
          '[IP]': response.get('query'),
          '[Провайдер]': response.get('isp'),
          '[Организация]': response.get('org'),
          '[Континент]': response.get('continent'),
          '[Страна]': response.get('country'),
          '[Область]': response.get('regionName'),
          '[Город]': response.get('city'),
          '[Индекс]': response.get('zip'),
          '[Широта]': response.get('lat'),
          '[Долгота]': response.get('lon'),
          '[Часовой пояс]': response.get('timezone'),
          '[Валюта]': response.get('currency'),
      }

      for k, v in data.items():
          textout += f'{k} : {v}\n'
          #print(f'{k} : {v}')    
      await message.answer(text=textout)
    except requests.exceptions.ConnectionError:
        print('Please check your connection!')


@router.message()
async def get_weather(message: Message):
    db_add(message.chat.id, message.text, message.from_user.first_name)
    global gorod
    gorod = message.text
    await message.answer(text=f'🏖 требуется выбрать вариант прогноза для {gorod}:', reply_markup=weat_keyboard())
    logger2.info(f'Choice of weather forecast for the {gorod} city...')


@router.callback_query(lambda c: c.data == 'oneday')
async def out_weather(callback: CallbackQuery):
    await callback.answer(text='прогноз на сегодня, период 3 часа')
    try:
        r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={gorod}&APPID={OW_TOKEN}&lang=ru&units=metric")
        #rrc = r.status_code
        #rrs = r.raise_for_status()
        #print(rrc, rrs)
        r_hourly = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?q={gorod}&APPID={OW_TOKEN}&lang=ru&units=metric")
        data = r.json()

        d_img = data.get("weather")[0].get("icon")
        if d_img in COD_SM:
            wd = COD_SM[d_img]
        else:
            wd = "\U0001f914"

        dcity = data.get("name")
        descript = data.get("weather")[0].get("description")
        temp = data.get("main").get("temp")
        feel = data.get("main").get("feels_like")
        hum = data.get("main").get("humidity")
        press = int(data.get('main').get('pressure')) / 1.33
        wind_speed = data.get("wind").get("speed")

        textout = f'<b>Погода в городе {dcity} сегодня</b>\n\n<u>Сейчас</u>\n' \
                  f'{wd} <i>{descript}</i>\n' \
                  f'🌡 <i>{temp}</i> \N{DEGREE CELSIUS}, ощущается <i>{feel}</i> \N{DEGREE CELSIUS}\n' \
                  f'🔻 атмосферное давл. {press:.2f} мм. рт. ст.,\n💦 влажность {hum} %, 💨 ветер {wind_speed}м/с\n\n'
        #print(textout)
        forecast = r_hourly.json().get('list')[1:]
        # print(2, forecast)
        count = 0
        for i in forecast:
            count += 1
            #idata = i.get('dt_txt')
            if count < 6:
                s_img = i.get("weather")[0].get("icon")
                if s_img in COD_SM:
                    wd1 = COD_SM[s_img]
                else:
                    wd1 = "\U0001f914"

                textout += f'<u>{datetime.datetime.strptime(i.get("dt_txt"), "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%y (%H:%M)")}</u>\n' \
                       f'{wd1} <i>{i.get("weather")[0].get("description")}</i>\n' \
                       f'🌡  <i>{i.get("main").get("temp")}</i> \N{DEGREE CELSIUS},  💦  <i>{i.get("main").get("humidity")}</i> %,  💨  <i>{i.get("wind").get("speed")}</i> м/с\n\n'
            else:
                break
        await callback.message.edit_text(text=textout, reply_markup=weat_keyboard())
        logger2.info(f'Weather forecast received for today for the {gorod} city...')
    except Exception as err:
        logger2.exception(err)
        await callback.message.edit_text('\U00002620 Неверное название города \U00002620 \n/help')
        


@router.callback_query(lambda c: c.data == 'fiveday')
async def out_weather(callback: CallbackQuery):
    await callback.answer(text='краткий прогноз на 5 дней')

    try:
        #r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={gorod}&APPID={OW_TOKEN}&lang=ru&units=metric")
        r_hourly = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?q={gorod}&APPID={OW_TOKEN}&lang=ru&units=metric")

        data = r_hourly.json().get('city')
        dcity = data.get("name")
        textout = f'<b>Погода в городе {dcity} на 5 дней</b>\n\n'
        forecast = r_hourly.json().get('list')[0:]
        # print(2, forecast)
        for i in forecast:
            idata = i.get('dt_txt')
            if idata[11:] == "12:00:00" and int(idata[8:10]) != int(datetime.datetime.now().strftime('%d')):
                s_img = i.get("weather")[0].get("icon")
                if s_img in COD_SM:
                    wd1 = COD_SM[s_img]
                else:
                    wd1 = "\U0001f914"

                textout += f'<u>{datetime.datetime.strptime(i.get("dt_txt"), "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%y")}</u>\n' \
                           f'{wd1} <i>{i.get("weather")[0].get("description")}</i>\n' \
                           f'🌡  <i>{i.get("main").get("temp")}</i> \N{DEGREE CELSIUS},  💦  <i>{i.get("main").get("humidity")}</i> %,  💨  <i>{i.get("wind").get("speed")}</i> м/с\n\n'

        await callback.message.edit_text(text=textout, reply_markup=weat_keyboard())
        logger2.info(f'Weather forecast received for five days for the {gorod} city...')
    except Exception as err:
        logger2.exception(err)
        await callback.message.edit_text('\U00002620 Неверное название города \U00002620 \n/help')
