import asyncio
import os
import sys

sys.path.append("./scihub.py/scihub")

from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from scihub import SciHub

sh = SciHub()
storage = MemoryStorage()
bot = Bot(token=os.environ[BOT_TOKEN])
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
@dp.message_handler(commands=['help'])
async def start(message):
	text =  "/help|/start - shows this message;\n"
	text += "/get - find and get paper in pdf by DOI, PMID or URL;\n"
	text += "/multi_get - for downloading more than 1 paper;\n"
	text += "/search - for searching in Google Scholar\n"
	text += "/donate - information for found/support projects"
	text += "\n"
	text += "This bot uses a submodule scihub.py from zaytoun(https://github.com/zaytoun/scihub.py)"
	await bot.send_message(message.from_user.id, text, reply_markup=buttons.main)

@dp.message_handler(commands=['get'])
@dp.callback_query_handler(text=['get'])
async def get(callback):
	await bot.send_message(callback.from_user.id, "Send DOI, PMID or URL")
	@dp.message_handler()
	async def fetch(message):
		paper = sc.fetch(message.text)
		await bot.send_message(message.from_user.id, paper['name'])
		await bot.send_document(message.from_user.id, paper['pdf'])

@dp.message_handler(commands=['multi_get'])
@dp.callback_query_handler(text=['multi_get'])
async def multi_get(callback):
	await bot.send_message(callback.from_user.id, "Send DOIs, PMIDs or URLs separated by semicolon(;)")
	dp@.message_handler()
	async def get_list(message):
		list = message.text.strip().split(";")
		for string in list:
			paper = sc.fetch(string)
			await bot.send_message(message.from_user.id, paper['name'])
			await bot.send_document(message.from_user.id, paper['pdf'])

@dp.message_handler(commands=['search'])
@dp.callback_query_handler(text=['search'])
async def search(callback):
	await bot.send_message(callback.from_user.id, "Send DOI, PMID or URL")
	@dp.message_handler()
	async def search(message):
		result = sh.search("message.text", 5)
	if result['err'] not Null or "":
		await bot.send_message(message.from_user.id, result['err'])
		return
	for paper in result['papers']:
		await bot.send_message(message.from_user.id, f"Name: {{paper[\'name\']}}\nURL: {{paper[\'url\']}}")




