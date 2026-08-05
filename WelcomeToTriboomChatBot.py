
#from contextlib import asynccontextmanager
#from fastapi import FastAPI
from twitchio.ext import commands

class WelcomeToTriboomChatBot(commands.Bot):
    def __init__(self, **kwargs: Any) -> None:
        channel_list = []
        channel_list.append(Any)

        super().__init__(
            token=f"oauth:{access_token}",
            prefix='!',
            initial_channels=channel_list
        )

    async def event_ready(self):
        print(f'Logged into Twitch as | {self.nick}')

    @commands.command(name='hello')
    async def hello_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name} from {self.__class__}')

