
from dotenv import load_dotenv
from os import getenv

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
#from twitchio.ext import commands

import WelcomeToTriboomChatBot 

load_dotenv
#bot = WelcomeToTriboomChatBot.WelcomeToTriboomChatBot("12", "34")
bot = WelcomeToTriboomChatBot.WelcomeToTriboomChatBot(getenv('ACCESS_TOKEN'), 'tribooms', getenv('CLIENT_ID'))

# Helper function to avoid naming conflict with asyncio
def asyncio_create_task(temp_coroutine):
    return asyncio.create_task(temp_coroutine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    bot_task = asyncio_create_task(bot.start())
    yield
    await bot.close()

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    status_message = await bot.get_status()
    return {"status": status_message}

@app.get("/sayhi")
async def say_hi():
    await bot.say_hi()


