from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
import config
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage=MemoryStorage()

bot = Bot(config.token)
dp = Dispatcher(bot, storage=storage)