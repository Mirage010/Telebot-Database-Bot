import asyncio
import time
from aiogram import types, Dispatcher
import logging
from create_bot import dp, bot
from aiogram.dispatcher import FSMContext
import schedule
import threading
import requests
from data_base import coins
import sqlite3 as sq
from keyboards import kb_client, kb_coins, kb_updown, kb_ethereum, kb_bitcoincash


def sql_client():
    global base, cur
    base = sq.connect('users_new.db')
    cur = base.cursor()




"შეტყობინების შემდეგ მონაცემთა ბაზაში შედის -1"
num = '-1'

def greeting():
    """ფასების API ბაინანსიდან"""
    try:
        global btcusdt, ethusdt, bch_usdt
        key = "https://fapi.binance.com/fapi/v1/ticker/24hr?symbol=btcusdt"
        data = requests.get(key)
        data = data.json()
        btcusdt = float(data['lastPrice'])



        key = "https://fapi.binance.com/fapi/v1/ticker/24hr?symbol=ethusdt"
        data = requests.get(key)
        data = data.json()
        ethusdt = float(data['lastPrice'])

        key = "https://fapi.binance.com/fapi/v1/ticker/24hr?symbol=bchusdt"
        data = requests.get(key)
        data = data.json()
        bch_usdt= float(data['lastPrice'])

        print(btcusdt, ethusdt, bch_usdt)


    except:
        return main1()


def main1():
    """ეს არის დაკავშირებულია greetin_თან და რთავს  ფასებს"""
    schedule.every(1).seconds.do(greeting)

    while True:
        schedule.run_pending()




#def get_db(uid):
 #   """ამ სკრიპტიდან ხდება შემოწმება, და ბოტის მუშაობის მომენტში გადმოდის user_id"""
  #  base = sq.connect('users_new.db')
   # cur = base.cursor()
    #user = cur.execute(f'SELECT * FROM coins_users WHERE user_id=?', (uid,)).fetchone()

   # if user is None:

    #    base.close()

     #   return None

   # else:
    #    base.close()
     #   user_id = user[0]
      #  btc_up = user[1]
       # btc_down = user[2]
        #eth_up = user[3]
       # return  user_id, btc_up, btc_down, eth_up




#async def asinsio(message: types.Message):
 #   """აქ ხდება user_id-ის დამახსოვრება"""
  #  global btc_up, btc_down, eth_up
   # user_id, btc_up, btc_down, eth_up= get_db(message.from_user.id)
    #if user_id:
     #   global BTC_up_h
      #  BTC_up_h = btc_up
       # btc_up = BTC_up_h

#        btc_down_h = btc_down
 #       btc_down = btc_down_h

  #      eth_up_h = eth_up
   #     eth_up = eth_up_h


 #   await bot.send_message(message.from_user.id, f'მოგივათ შეტყობინება{btc_up}')










#@dp.message_handler(commands=['start'])
async def start_command(message: types.Message, state: FSMContext):
    global ID
    ID = message.from_user.id
    """მისასალმებელი ფუნქცია სადაც ირთვება პირველი კლავიატურა"""
    await bot.send_message(message.from_id, f'მოგესალმებით, ეს არის Binance Futures-ს'
                                            f'ფასის შემახსენებლი ბოტი, შეგიძლიათ მიუთითოთ ფასი '
                                            f'და მოგივათ შეტყობინება ფასის გაზრდის ან კლების შესახებ', reply_markup=kb_client)
    print (ID, 'oooooooooooooooooooooooooooooooooo')



""""ფასის არჩევის შემდეგ აქ გადმოდის"""
async def back_home(message: types.Message):
    """მისასალმებელი ფუნქცია სადაც ირთვება პირველი კლავიატურა"""
    await bot.send_message(message.from_id, f'შეცვალეთ ან აირჩიეთ პარამეტრები', reply_markup=kb_client)




async def choose_start(message: types.Message):
    """მონეტების არჩევის ფუნქცია რომლის შემდეგ მიუთითებ ფასს"""
    await bot.send_message(message.from_id, f'აირჩიეთ სასურველი მონეტა ან მიწერეთ ბოტს, მაგ(BTC/USDT, ETH/BUSD)', reply_markup=kb_coins)


"""ზღვრების მითითება"""

async def btc_usdt_up_down_keyboard(message: types.Message):
    """ბიტკოინის ზღვარის არჩევა"""
    await bot.send_message(message.from_id, f'აირჩიეთ ქვედა ან ზედა ზღვარი შეტყობინების მისაღებად', reply_markup=kb_updown)


async def eth_usdt_up_down_keyboard(message: types.Message):
    """ეთერიუმის ზღვრის არჩევა"""
    await bot.send_message(message.from_id, f'აირჩიეთ ქვედა ან ზედა ზღვარი შეტყობინების მისაღებად-', reply_markup=kb_ethereum )


async def bch_usdt_up_down_keyboard(message: types.Message):
    """ბიტკოინ ქეშის ზღვრების არჩევა"""
    await bot.send_message(message.from_id, f'აირჩიეთ ქვედა ან ზედა ზღვარი შეტყობინების მისაღებად-',
                           reply_markup=kb_bitcoincash)


"""BTC/USDT"""
###########################################################
#@dp.message_handler(commands=['remind'])
"""ბიტკოინის ფასის მაღლა აწევის ფუნქცია"""
async def reminder_coins(message : types.Message, state: FSMContext):
    """"აქ ირთვება ციკლი, ეს ციკლი რო ჩართულია მაშინ მოდის შეტყობინება"""
    ID = message.from_user.id
    if message.from_user.id == ID:
        """ბიტკოინის უსდტ-ს ზედა ზღვრის მითითება"""
        while True:
            await asyncio.sleep(1)
            base = sq.connect('users_new.db')
            cur = base.cursor()
            user = cur.execute(f'SELECT * FROM coins_users WHERE user_id=?', (ID,)).fetchone()
            if user is None:

                base.close()

                return None
            else:
                base.close()
                btc_up = user[1]

                if btcusdt >= float(btc_up) and float(btc_up) > float(num):
                    async with state.proxy() as data:
                        data['user_id'] = ID
                        delete = '-2'
                    async with state.proxy() as data:
                        data['btcusdt_up'] = delete
                    await bot.send_message(message.from_user.id, f'ფასი აიწია და მივიდა თქვენს ნიშნულთან \n'
                                                f'BTC/USDT - {btcusdt} \n'
                                                f'ჩემი მითითებული ფასი {btc_up}')
                    await coins.sql_add_command_delete_bitcoin(state)
                    break



async def reminder_btc_down(message: types.Message, state: FSMContext):
    """ბიტკოინის ქვედა ზღვარი"""
    ID = message.from_user.id
    if message.from_user.id == ID:
        while True:
            await asyncio.sleep(1)
            while True:
                await asyncio.sleep(1)
                base = sq.connect('users_new.db')
                cur = base.cursor()
                user = cur.execute(f'SELECT * FROM coins_users WHERE user_id=?', (ID,)).fetchone()
                if user is None:

                    base.close()

                    return None
                else:
                    base.close()
                    btc_down = user[2]

                    if btcusdt <= float(btc_down) and float(btc_down) > float(num):
                        async with state.proxy() as data:
                            data['user_id'] = ID
                            delete_btc_down = '-2'
                        async with state.proxy() as data:
                            data['btcusdt_down'] = delete_btc_down
                        await message.answer(f'ფასი დაიწია და მივიდა თქვენს ნიშნულთან \n'
                                     f'BTC/USDT - {btcusdt} $\n'
                                     f'ჩემი მითითებული ფასი {btc_down} $')
                        await coins.sql_add_command_delete_bitcoin_lower(state)
                        break



"""ETH/USDT"""
##########################
async def reminder_eth_usdt(message : types.Message, state: FSMContext):
    """"აქ ირთვება ციკლი, ეს ციკლი რო ჩართულია მაშინ მოდის შეტყობინება"""
    ID = message.from_user.id
    if message.from_user.id == ID:
        """ზედა ზღვრის მითითება"""
        while True:
            await asyncio.sleep(1)
            base = sq.connect('users_new.db')
            cur = base.cursor()
            user = cur.execute(f'SELECT * FROM coins_users WHERE user_id=?', (ID,)).fetchone()
            if user is None:

                base.close()

                return None
            else:
                base.close()
                eth_up = user[3]

                if ethusdt >= float(eth_up) and float(eth_up) > float(num):
                    async with state.proxy() as data:
                        """ბაზაში მიდის ნო მესიჯი"""
                        data['user_id'] = ID
                        delete = '-2'
                    async with state.proxy() as data:
                        data['ethusdt_up'] = delete
                    await message.answer(f'ფასი აიწია და მივიდა თქვენს ნიშნულთან \n'
                                                f'ETH/USDT - {ethusdt} $\n'
                                                f'ჩემი მითითებული ფასი {eth_up} $')
                    await coins.sql_add_command_delete_eth_usdt(state)
                    break


async def reminder_eth_usdt_down(message : types.Message, state: FSMContext):
    """"აქ ირთვება ციკლი, ეს ციკლი რო ჩართულია მაშინ მოდის შეტყობინება"""
    ID = message.from_user.id
    if message.from_user.id == ID:
        """ზედა ზღვრის მითითება"""
        while True:
            await asyncio.sleep(1)
            base = sq.connect('users_new.db')
            cur = base.cursor()
            user = cur.execute(f'SELECT * FROM coins_users WHERE user_id=?', (ID,)).fetchone()
            if user is None:

                base.close()

                return None
            else:
                base.close()
                eth_down = user[4]

                if ethusdt <= float(eth_down) and float(eth_down) > float(num):
                    async with state.proxy() as data:
                        """ბაზაში მიდის ნო მესიჯი"""
                        data['user_id'] = ID
                        delete = '-2'
                    async with state.proxy() as data:
                        data['ethusdt_down'] = delete
                    await message.answer(f'ფასი აიწია და მივიდა თქვენს ნიშნულთან \n'
                                                f'ETH/USDT - {ethusdt} $\n'
                                                f'ჩემი მითითებული ფასი - {eth_down} $')
                    await coins.sql_add_command_delete_eth_usdt_lower(state)
                    break



#bchusdt
##########################################################
"""bchusdt ზედა ზღვარი"""
async def reminder_bch_usdt(message : types.Message, state: FSMContext):
    """"აქ ირთვება ციკლი, ეს ციკლი რო ჩართულია მაშინ მოდის შეტყობინება"""
    ID = message.from_user.id
    if message.from_user.id == ID:
        """ზედა ზღვრის მითითება"""
        while True:
            await asyncio.sleep(1)
            base = sq.connect('users_new.db')
            cur = base.cursor()
            user = cur.execute(f'SELECT * FROM coins_users WHERE user_id=?', (ID,)).fetchone()
            if user is None:

                base.close()

                return None
            else:
                base.close()
                bch_up = user[5]

                if bch_usdt >= float(bch_up) and float(bch_up) > float(num):
                    async with state.proxy() as data:
                        """ბაზაში მიდის ნო მესიჯი"""
                        data['user_id'] = ID
                        delete = '-2'
                    async with state.proxy() as data:
                        data['bchusdt_up'] = delete
                    await message.answer(f'ფასი აიწია და მივიდა თქვენს ნიშნულთან \n'
                                                f'BCH/USDT - {bch_usdt} $ \n'
                                                f'ჩემი მითითებული ფასი {bch_up} $')
                    await coins.sql_add_command_delete_bch_usdt(state)
                    break


##### BCH_Down
async def reminder_bch_usdt_down(message : types.Message, state: FSMContext):
    """bchusdts-ს ქვედა ზღვარი"""
    """"აქ ირთვება ციკლი, ეს ციკლი რო ჩართულია მაშინ მოდის შეტყობინება"""
    ID = message.from_user.id
    if message.from_user.id == ID:
        """ზედა ზღვრის მითითება"""
        while True:
            await asyncio.sleep(1)
            base = sq.connect('users_new.db')
            cur = base.cursor()
            user = cur.execute(f'SELECT * FROM coins_users WHERE user_id=?', (ID,)).fetchone()
            if user is None:

                base.close()

                return None
            else:
                base.close()
                eth_down = user[4]

                if bch_usdt <= float(bch_down) and float(bch_down) > float(num):
                    async with state.proxy() as data:
                        """ბაზაში მიდის ნო მესიჯი"""
                        data['user_id'] = ID
                        delete = '-2'
                    async with state.proxy() as data:
                        data['ethusdt_down'] = delete
                    await message.answer(f'ფასი აიწია და მივიდა თქვენს ნიშნულთან \n'
                                                f'ETH/USDT - {bchusdt} $\n'
                                                f'ჩემი მითითებული ფასი - {eth_down} $')
                    await coins.sql_add_command_delete_eth_usdt_lower(state)
                    break




def register_handlers_client(dp : Dispatcher):
    """რეგისტრირებული ჰენდლერები"""
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(choose_start, text=['Add/change Coins'])
    dp.register_message_handler(btc_usdt_up_down_keyboard, text=['BTC/USDT'])
    dp.register_message_handler(eth_usdt_up_down_keyboard, text=['ETH/USDT'])
    dp.register_message_handler(bch_usdt_up_down_keyboard, text=['BCH/USDT'])
    dp.register_message_handler(back_home, text=['Back'])





"""ეს კოდი რთავს ეგრევე ფასების ციკლს main1-ს"""

t2 = threading.Thread(target=main1)
t2.start()