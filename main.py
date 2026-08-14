""" 
Use FastAPI to be able to communicate to twitch channel in a threaded manner.
"""
from os import getenv
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from twitchio.utils import setup_logging as setup_twitchio_logging
from twitchio import Client as TwitchClient, user
import asyncio
import logging
import triboom_chat_bot
import twitchio

load_dotenv
setup_twitchio_logging(level=logging.INFO)


### SETUP ####
output_file = "project.log"
file_handler = logging.FileHandler(filename=output_file, encoding='utf-8', mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
twitchio.utils.setup_logging(level=logging.DEBUG, handler=file_handler)

logger = logging.getLogger(__name__)
logger.addHandler(file_handler)
logger.info(f"Logger initialized beep {logger}")
#logger = logging.getLogger("uvicorn.error")
bot = triboom_chat_bot.triboom_chat_bot(logger)

### FastAPI Endpoints ###

def asyncio_create_task(temp_coroutine):
    "Helper function to avoid naming conflict with asyncio"
    return asyncio.create_task(temp_coroutine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    "Setup lifespan for FastAPI"
    logger.info("Going to start bot")
    bot_task = asyncio_create_task(bot.start())
    logger.info("Bot starting")
    await bot.start()
    logger.info("Bot started")
    #user = bot.create_partialuser(user_id=getenv('STREAMER_ID'), user_login="OneTwoFiveEleven")
    #await user.send_message(sender=bot.user, message="Hello World!")
    yield
    #await bot.close()
   # logger.info("Bot Closed")

logger.info("Starting the FastAPI app")
app = FastAPI(lifespan=lifespan)
logger.info("FastAPI app Started")

@app.get("/")
async def root():
    "Root method for app"
    logger.info("Root URL called - get bot status")
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
        twitch_users = await client.fetch_users(logins=["onetwofiveeleven",
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
