import asyncio
import twitchio
from dotenv import load_dotenv
from os import getenv

load_dotenv()

CLIENT_ID: str = getenv('CLIENT_ID')
CLIENT_SECRET: str = getenv('CLIENT_SECRET')

async def main() -> None:
    async with twitchio.Client(client_id=CLIENT_ID, client_secret=CLIENT_SECRET) as client:
        await client.login()
        user = await client.fetch_users(logins=["onetwofiveeleven", "One2Five11"])
        for u in user:
            print(f"User: {u.name} - ID: {u.id}")

if __name__ == "__main__":
    asyncio.run(main())