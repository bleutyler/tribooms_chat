
#from contextlib import asynccontextmanager
#from fastapi import FastAPI
from flask import ctx
from twitchio.ext import commands


from dotenv import load_dotenv
from os import getenv

class WelcomeToTriboomChatBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            client_id=getenv('CLIENT_ID'),
            client_secret=getenv('CLIENT_SECRET'),
            bot_id=234,
            prefix='!',
            redirect_uri='http://localhost:4343/oauth/callback',
            channel="tribooms"

        )

        print(f"{self.__class__.__name__} initialized")

    async def event_ready(self):
        print(f'Logged into Twitch as {self}')

    async def get_status(self) -> str:
        return f"{self.__class__.__name__} is running in channels: {', '.join(self.channel_list)}"

    async def say_hi(self) -> None:
        print(f"Saying Hello")
        the_channel = await self.fetch_channel("tribooms")
        await the_channel.send( f"Hi Chat!" )

    @commands.command(name='hello')
    async def hello_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name} from {self.__class__.__name__}')

    @commands.command(name='tribothelp')
    async def tribothelp_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name} from {self.__class__.__name__}')

