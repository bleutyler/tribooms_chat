"""
This is a simple Twitch Chat Bot for the Tribooms Twitch Channel.
Emphasis on using FastAPI for threaded processing and async calls to TwitchIO
"""
import logging
import winsound
import twitchio
from os import getenv
from dotenv import load_dotenv
from flask import ctx
from twitchio.ext import commands

class triboom_chat_bot(commands.Bot):
    def __init__(self, new_logger: logging.Logger | None = None) -> None:
        self.login_name = "TriboomsChatBot"
        self.logger = new_logger or logging.getLogger(__name__)
        super().__init__(
            client_id=getenv('CLIENT_ID'),
            client_secret=getenv('CLIENT_SECRET'),
            bot_id=1226671483,
            owner_id="tribooms",
            prefix='!',
            redirect_uri='https://twitchtokengenerator.com/oauth/callback',
            channel="tribooms"
        )

        self.logger.info(f"{self.__class__.__name__} initialized")

    async def event_ready(self):
        "Simple Ready method to make sure bot is alive"
        self.logger.info('Logged into Twitch !')

    async def get_status(self) -> str:
        "State the status of the Bot"
        return f"{self.__class__.__name__} is running"

    async def say_hi(self) -> None:
        "This is a command to say Hi Chat! from a FastAPI endpoint "
        self.logger.info("Saying Hello")
        the_channel = await self.fetch_channel("tribooms")
        await the_channel.send( "Hi Chat!" )

    @commands.command(name='hello')
    async def hello_command(self, ctx):
        "Say Hello back to the user"
        await ctx.send(f"Hello {ctx.author.name}",
                       f" from {self.__class__.__name__}")

    @commands.command(name="user_info")
    async def user_info(self, ctx):
        "Get simple twitch user details"
        with twitchio.Client(client_id=getenv('CLIENT_ID'),
                             client_secret=getenv('CLIENT_SECRET')) as client:
            await client.login()
            twitch_users = await client.fetch_users(logins=[ctx.author.name])
            for user in twitch_users:
                self.logger.debug(f"Twitch user '{self.login_name}' fetched.",
                                   f"name: {user.name} (ID: {user.id})")

    @commands.command(name='uh_oh')
    async def uh_oh(self, ctx):
        "Play the ICQ uh oh sound"
        winsound.PlaySound("audio/icq-uh-oh.mp3", winsound.SND_FILENAME)
        await ctx.send(f"User {ctx.author.name} used Audio Ping")