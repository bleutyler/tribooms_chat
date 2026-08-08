""" 
Use FastAPI to be able to communicate to twitch channel in a threaded manner.
"""
from os import getenv
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from twitchio.utils import setup_logging as setup_twitchio_logging
from twitchio import Client as TwitchClient
import asyncio
import logging
import triboom_chat_bot

load_dotenv
setup_twitchio_logging(level=logging.INFO)

logging.basicConfig(encoding='utf-8', level=logging.DEBUG, filename="project.log",
                    format="%(asctime)s - %(levelname)s - %(message)s" )
logger = logging.getLogger(__name__)
print("logger is made")
logger.info("Logger initialized beep boop")
#logger = logging.getLogger("uvicorn.error")
bot = triboom_chat_bot.triboom_chat_bot()

def asyncio_create_task(temp_coroutine):
    "Helper function to avoid naming conflict with asyncio"
    return asyncio.create_task(temp_coroutine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    "Setup lifespan for FastAPI"
    print("Going to start bot")
    bot_task = asyncio_create_task(bot.start())
    print("Bot starting")
    await bot.start()
    print("Bot started")
    yield
    await bot.close()
    print("Bot Closed")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    "Root method for app "
    print(f"bot is made: {bot}")
    status_message = await bot.get_status()
    return {"status": status_message}


@app.get("/user_info")
async def user_info():
    "Display user information for owners of the Chatbot"
    status_message = ""
    async with TwitchClient(client_id=getenv('CLIENT_ID'), 
                            client_secret=getenv('CLIENT_SECRET')) as client:
        await client.login()
        print(f" Twitch client created {client}")
        twitch_users = await client.fetch_users(logins=["TriboomsChatBot", "onetwofiveeleven", 
                                                        "tribooms"])
        print(f"{len(twitch_users)} Twitch user(s) fetched for 'TriboomsChatBot'")
        logger.debug(f"{len(twitch_users)} Twitch user(s) fetched for 'TriboomsChatBot'")
        status_message = "0 Users found" if len(twitch_users) == 0 else ""
        for user in twitch_users:
            user_message = f"Twitch user fetched. name: {user.name} (ID: {user.id})"
            print(user_message)
            status_message += user_message + "\n"
            logger.debug(user_message)
    #bot_task = asyncio_create_task(bot.user_info())
    #await bot.user_info()
    return {"status": status_message}

@app.get("/say_hi")
async def say_hi():
    "Write to chat without a command from Twitch"
    bot_task = asyncio_create_task(bot.say_hi())
    await bot.say_hi()
    return {"status": "Said Hi Chat to chat" }

@app.get("/uh_oh")
async def uh_oh():
    "Get the bot to play a sound"
    bot_task = asyncio_create_task(bot.uh_oh())
    await bot.uh_oh()
    return {"status": "Audio Pinged played and logged"}
