from aiogram.utils import executor
from create_bot import dp, bot
from data_base import coins


async def on_startup(_):
    print("ბოტი ონლაინშია")
    coins.sql_start()



from handlers import client, admin, ethusdt, bchusdt
client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
ethusdt.register_handlers_ethusdt(dp)
bchusdt.register_handlers_bchusdt(dp)






executor.start_polling(dp, skip_updates=True, on_startup=on_startup)