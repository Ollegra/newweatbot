from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='🌤 Получить прогноз погоды', callback_data='namcity')
    builder.adjust(1)
    key_main = builder.as_markup()
    return key_main

def weat_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='☀ Сегодня', callback_data='oneday')
    builder.button(text='🌡 5 дней', callback_data='fiveday')
    # builder.button(text='📊 ', callback_data='grafics')
    builder.button(text='🚫 отмена', callback_data='konec')
    builder.adjust(3)
    key_weat = builder.as_markup()
    return key_weat

def stat_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='📈 stat_1', callback_data='stat')
    builder.button(text='📉 stat_2', callback_data='statx')
    builder.button(text='📊 stat_3', callback_data='statn')
    builder.button(text='🚫 отмена', callback_data='konec')
    builder.adjust(3)
    key_stat = builder.as_markup()
    return key_stat

def data_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='⬆', callback_data='expo')
    builder.button(text='⬇', callback_data='save')
    builder.button(text='🔙', callback_data='konec')
    builder.adjust(2)
    key_data = builder.as_markup()
    return key_data

print('Keyboards created', '.' * 23)