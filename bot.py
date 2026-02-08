# bot.py
"""Spud Snarking Bot — Discord personality bot for Radiospiral."""

import logging
import os
from pathlib import Path

import discord
from dotenv import load_dotenv

logger = logging.getLogger("spud")

from handlers import MatchResult, dispatch
from responses import get_random, load_pool

load_dotenv()

DATA_DIR = Path(__file__).parent / "data"

# Load all response pools at startup
POOLS = {
    MatchResult.OBLIQUE: load_pool(DATA_DIR / "strategies.yml"),
    MatchResult.GREETING: load_pool(DATA_DIR / "greetings.yml"),
    MatchResult.GOODNIGHT: load_pool(DATA_DIR / "goodnight.yml"),
    MatchResult.THANKS: load_pool(DATA_DIR / "thanks.yml"),
    MatchResult.SNARK: load_pool(DATA_DIR / "snark.yml"),
}

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    logger.info(f"Spud is lurking as {client.user}")


@client.event
async def on_message(message: discord.Message):
    # Never respond to ourselves
    if message.author == client.user:
        return

    text = message.content
    bot_name = client.user.display_name.lower() if client.user else "spud"
    is_mentioned = (
        client.user in message.mentions
        or isinstance(message.channel, discord.DMChannel)
        or bot_name in text.lower()
    )

    logger.debug(f"MSG [{message.channel}] {message.author}: {text!r} (mentioned={is_mentioned})")

    result = dispatch(text, is_mentioned)
    if result is None:
        return

    response = get_random(POOLS[result])
    logger.info(f"RESPOND [{result.name}]: {response!r}")
    if response:
        await message.channel.send(response)


def main():
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("Error: DISCORD_BOT_TOKEN not set in .env")
        raise SystemExit(1)
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)-8s %(name)s %(message)s")
    client.run(token)


if __name__ == "__main__":
    main()
