from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import bot
from data_base import coins
from handlers import client
from keyboards import kb_home

import re

ID = None






class FSMAdmin(StatesGroup):
    btcusdt_up = State()



# @dp.message_handler(commands=['moderator'],is_chat_admin=True)


# dialogis dacyebis menius punkti
# @dp.message_handler(command='chatvirtva', state=None)
async def cm_start(message: types.Message):
    global ID
    ID = message.from_user.id
    await FSMAdmin.next()
    await bot.send_message(message.from_user.id, "შეიყვანეთ ფასი")



async def load_name(message: types.Message, state: FSMContext):
    try:
        ID = message.from_user.id
        if re.match(r"^[+-]?([0-9]*[.])?[0-9]+", message.text):
            async with state.proxy() as data:
                data['user_id'] = ID
                btcusdtup_message = message.text
            async with state.proxy() as data:
                data['btcusdt_up'] = btcusdtup_message

            await bot.send_message(message.from_user.id, "თქვენი მოთხოვნა დაფიქსირებულია, ფასის ნიშნულთან მისვლის "
                                    "შემთხვევაში მიიღებთ შეტყობინებას", reply_markup=kb_home)

            await coins.sql_add_command(state)
            await client.reminder_coins(message, state)
            await state.finish()
        elif message.text == 'Back':
            await client.back_home(message)
            await state.finish()

        else:
            return await message.reply("შეიყვანეთ კორექტული მონაცემები")

    except Exception as e:
        print(e)





"""""ბიტკოინის ქვედა ზღვარი"""""

class FSM_btc_lower(StatesGroup):
    btcusdt_down = State()



# @dp.message_handler(commands=['moderator'],is_chat_admin=True)


# dialogis dacyebis menius punkti
# @dp.message_handler(command='chatvirtva', state=None)
async def cm_btc_lower_start(message: types.Message):
    global ID
    ID = message.from_user.id
    await FSM_btc_lower.next()
    await message.reply("შეიყვანეთ ფასი")



async def cm_btc_lower_load_name(message: types.Message, state: FSMContext):
    try:
        ID = message.from_user.id
        if re.match(r"^[+-]?([0-9]*[.])?[0-9]+", message.text):
            async with state.proxy() as data:
                data['user_id'] = ID
                btcusdtdown_message = message.text
            async with state.proxy() as data:
                data['btcusdt_down'] = btcusdtdown_message

            await message.reply("თქვენი მოთხოვნა დაფიქსირებულია, ფასის ნიშნულთან მისვლის "
                                    "შემთხვევაში მიიღებთ შეტყობინებას", reply_markup=kb_home)

            print(btcusdtdown_message)

            await coins.sql_add_command_btc_lower(state)
            await client.reminder_btc_down(message, state)
            await state.finish()
        elif message.text == 'Back':
            await client.back_home(message)
            await state.finish()

        else:
            return await message.reply("შეიყვანეთ კორექტული მონაცემები. \n"
                                           "მაგ: 10100, 10100.40")

    except Exception as e:
        print(e)











"""ჰენდლერის რეგისტრაცია"""
def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(cm_start, text=['BTC/USDT Upper Limit'], state=None)
    dp.register_message_handler(load_name, state=FSMAdmin.btcusdt_up)

    dp.register_message_handler(cm_btc_lower_start, text=['BTC/USDT Lower Limit'], state=None)
    dp.register_message_handler(cm_btc_lower_load_name, state=FSM_btc_lower.btcusdt_down)




