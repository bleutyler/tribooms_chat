
#from contextlib import asynccontextmanager
#from fastapi import FastAPI
from dotenv import load_dotenv
from flask import ctx
from os import getenv
import twitchio
from twitchio.ext import commands

import logging

class WelcomeToTriboomChatBot(commands.Bot):
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
        self.logger.info(f'Logged into Twitch !')

    async def get_status(self) -> str:
        return f"{self.__class__.__name__} is running"

    async def say_hi(self) -> None:
        self.logger.info(f"Saying Hello")
        print(f"Saying Hello")
        the_channel = await self.fetch_channel("tribooms")
        await the_channel.send( f"Hi Chat!" )

    @commands.command(name='hello')
    async def hello_command(self, ctx):
        await ctx.send(f"Hello {ctx.author.name} from {self.__class__.__name__}")

    @commands.command(name="user_info")
    async def user_info(self, ctx):
        # Only need to run once taken from twitchio docs
        with twitchio.Client(client_id=getenv('CLIENT_ID'), client_secret=getenv('CLIENT_SECRET')) as client:
            await client.login()
            twitch_users = await client.fetch_users(logins=[ctx.author.name])
            for user in twitch_users:
                self.logger.debug(f"Twitch user '{self.login_name}' fetched. name: {user.name} (ID: {user.id})")
        

    @commands.command(name='uh_oh')
    async def uh_oh(self, ctx):
        import winsound
        winsound.PlaySound("audio/", winsound.SND_FILENAME)
        await ctx.send(f"User {ctx.author.name} used Audio Ping")

