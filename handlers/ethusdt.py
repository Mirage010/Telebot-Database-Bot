from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from data_base import coins
from handlers import client
from keyboards import kb_home

import re

ID = None






class FSMAdmin_eth_up(StatesGroup):
    ethusdt_up = State()



# @dp.message_handler(commands=['moderator'],is_chat_admin=True)


# dialogis dacyebis menius punkti
# @dp.message_handler(command='chatvirtva', state=None)
async def cm_start_eth_usdt(message: types.Message):
    global ID
    ID = message.from_user.id
    await FSMAdmin_eth_up.next()
    await message.reply("შეიყვანეთ ფასი")



async def eth_usdt(message: types.Message, state: FSMContext):
    try:
        ID = message.from_user.id
        if re.match(r"^[+-]?([0-9]*[.])?[0-9]+", message.text):
            async with state.proxy() as data:
                data['user_id'] = ID
                ethusdtup_message = message.text
            async with state.proxy() as data:
                data['ethusdt_up'] = ethusdtup_message

            await message.reply("თქვენი მოთხოვნა დაფიქსირებულია, ფასის ნიშნულთან მისვლის "
                                    "შემთხვევაში მიიღებთ შეტყობინებას", reply_markup=kb_home)

            await coins.sql_add_eth_usdt(state)
            await client.reminder_eth_usdt(message, state)
            await state.finish()
        elif message.text == 'Back':
            await client.back_home(message)
            await state.finish()

        else:
            return await message.reply("შეიყვანეთ კორექტული მონაცემები")

    except Exception as e:
        print(e)


"""ქვედა ზღვარი"""
class FSM_eth_lower(StatesGroup):
    ethusdt_down = State()



# @dp.message_handler(commands=['moderator'],is_chat_admin=True)


# dialogis dacyebis menius punkti
# @dp.message_handler(command='chatvirtva', state=None)
async def cm_eth_lower_start(message: types.Message):
    global ID
    ID = message.from_user.id
    await FSM_eth_lower.next()
    await message.reply("შეიყვანეთ ფასი")



async def cm_eth_lower_load_name(message: types.Message, state: FSMContext):
    try:
        ID = message.from_user.id
        if re.match(r"^[+-]?([0-9]*[.])?[0-9]+", message.text):
            async with state.proxy() as data:
                    data['user_id'] = ID
                    ethusdtdown_message = message.text
            async with state.proxy() as data:
                    data['ethusdt_down'] = ethusdtdown_message

            await message.reply("თქვენი მოთხოვნა დაფიქსირებულია, ფასის ნიშნულთან მისვლის "
                                    "შემთხვევაში მიიღებთ შეტყობინებას", reply_markup=kb_home)



            await coins.sql_add_command_eth_usdt_lower(state)

            await client.reminder_eth_usdt_down(message, state)
            await state.finish()
        elif message.text == 'Back':
            await client.back_home(message)
            await state.finish()

        else:
            return await message.reply("შეიყვანეთ კორექტული მონაცემები. \n"
                                           "მაგ: 10100, 10100.40")

    except Exception as e:
        print(e)







def register_handlers_ethusdt(dp: Dispatcher):
    dp.register_message_handler(cm_start_eth_usdt, text=['ETH/USDT Upper Limit'], state=None)
    dp.register_message_handler(eth_usdt, state=FSMAdmin_eth_up.ethusdt_up)

    dp.register_message_handler(cm_eth_lower_start, text=['ETH/USDT Lower Limit'], state=None)
    dp.register_message_handler(cm_eth_lower_load_name, state=FSM_eth_lower.ethusdt_down)


