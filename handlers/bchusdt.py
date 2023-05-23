from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from data_base import coins
from handlers import client
from keyboards import kb_home

import re

ID = None


class FSMAdmin_bch_up(StatesGroup):
    bchusdt_up = State()



# @dp.message_handler(commands=['moderator'],is_chat_admin=True)


# dialogis dacyebis menius punkti
# @dp.message_handler(command='chatvirtva', state=None)
async def cm_start_bch_usdt(message: types.Message):
    global ID
    ID = message.from_user.id
    await FSMAdmin_bch_up.next()
    await message.reply("შეიყვანეთ ფასი")



async def bch_usdt(message: types.Message, state: FSMContext):
    try:
        ID = message.from_user.id
        if re.match(r"^[+-]?([0-9]*[.])?[0-9]+", message.text):
            async with state.proxy() as data:
                data['user_id'] = ID
                bchusdtup_message = message.text
            async with state.proxy() as data:
                data['bchusdt_up'] = bchusdtup_message

            await message.reply("თქვენი მოთხოვნა დაფიქსირებულია, ფასის ნიშნულთან მისვლის "
                                    "შემთხვევაში მიიღებთ შეტყობინებას", reply_markup=kb_home)

            await coins.sql_add_bch_usdt(state)
            await client.reminder_bch_usdt(message, state)
            await state.finish()
        elif message.text == 'Back':
            await client.back_home(message)
            await state.finish()

        else:
            return await message.reply("შეიყვანეთ კორექტული მონაცემები")

    except Exception as e:
        print(e)


"""ქვედა ზღვარი"""
class FSM_bch_lower(StatesGroup):
    bchusdt_down = State()



# @dp.message_handler(commands=['moderator'],is_chat_admin=True)


# dialogis dacyebis menius punkti
# @dp.message_handler(command='chatvirtva', state=None)
async def cm_bch_lower_start(message: types.Message):
    global ID
    ID = message.from_user.id
    await FSM_bch_lower.next()
    await message.reply("შეიყვანეთ ფასი")



async def cm_bch_lower_load_name(message: types.Message, state: FSMContext):
    try:
        ID = message.from_user.id
        if re.match(r"^[+-]?([0-9]*[.])?[0-9]+", message.text):
            async with state.proxy() as data:
                    data['user_id'] = ID
                    bchusdtdown_message = message.text
            async with state.proxy() as data:
                    data['bchusdt_down'] = bchusdtdown_message

            await message.reply("თქვენი მოთხოვნა დაფიქსირებულია, ფასის ნიშნულთან მისვლის "
                                    "შემთხვევაში მიიღებთ შეტყობინებას", reply_markup=kb_home)



            await coins.sql_add_command_bch_usdt_lower(state)

            await client.reminder_bch_usdt_down(message, state)
            await state.finish()
        elif message.text == 'Back':
            await client.back_home(message)
            await state.finish()

        else:
            return await message.reply("შეიყვანეთ კორექტული მონაცემები. \n"
                                           "მაგ: 10100, 10100.40")

    except Exception as e:
        print(e)







def register_handlers_bchusdt(dp: Dispatcher):
    dp.register_message_handler(cm_start_bch_usdt, text=['BCH/USDT Upper Limit'], state=None)
    dp.register_message_handler(bch_usdt, state=FSMAdmin_bch_up.bchusdt_up)

    dp.register_message_handler(cm_bch_lower_start, text=['BCH/USDT Lower Limit'], state=None)
    dp.register_message_handler(cm_bch_lower_load_name, state=FSM_bch_lower.bchusdt_down)