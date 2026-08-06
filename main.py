
from dotenv import load_dotenv
from os import getenv

import asyncio
import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI
#from twitchio.ext import commands

from twitchio.utils import setup_logging

import WelcomeToTriboomChatBot 

load_dotenv

setup_logging(level=logging.DEBUG)

logger = logging.getLogger("uvicorn.error")
bot = WelcomeToTriboomChatBot.WelcomeToTriboomChatBot()

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

@app.get("/say_hi")
async def say_hi():
    bot_task = asyncio_create_task(bot.say_hi())
    await bot.say_hi()
    return {"status": "Said hello to chat" }


