
#from contextlib import asynccontextmanager
#from fastapi import FastAPI
from flask import ctx

from twitchio.ext import commands

class WelcomeToTriboomChatBot(commands.Bot):
    def __init__(self, access_token: str, channel: str, client_id: str) -> None:
        self.channel_list = []
        self.channel_list.append(channel)

        super().__init__(
            token=f"oauth:{access_token}",
            client_id=client_id,
            prefix='!',
            initial_channels=self.channel_list
        )

        print(f"{self.__class__.__name__} initialized with channel: {channel}")

    async def event_ready(self):
        print(f'Logged into Twitch as | {self.nick}')

    async def get_status(self) -> str:
        return f"{self.__class__.__name__} is running in channels: {', '.join(self.channel_list)}"

    async def say_hi(self) -> None:
        the_channel = await self.fetch_channel(self.channel_list[0])
        await the_channel.send( f"Hi Chat!" )

    @commands.command(name='hello')
    async def hello_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name} from {self.__class__.__name__}')

