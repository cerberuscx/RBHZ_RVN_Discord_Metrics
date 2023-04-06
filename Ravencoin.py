#!/usr/bin/env python3

import os
import discord
import requests
import asyncio
import json
import logging
import datetime
import aiohttp
from discord.ext import commands
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment
load_dotenv()
TOKEN = os.environ.get("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

# create a client object 
bot = commands.Bot(command_prefix="!", intents=intents)

URL = 'https://api.coingecko.com/api/v3/simple/price?ids=ravencoin&vs_currencies=usd'
url = 'https://api.coingecko.com/api/v3/coins/ravencoin'
thumbnail_url = os.environ.get("THUMBNAIL_URL")
image_url = os.environ.get("IMAGE_URL")
author_url = os.environ.get("AUTHOR_URL")
update_interval = os.environ.get("UPDATE_INTERVAL")
update_interval = int(update_interval)
description = os.environ.get("DESCRIPTION")
website_link = os.environ.get("WEBSITE_LINK")


#Event handler for when the bot is ready
@bot.event
async def on_ready():
    #Print a message indicating the bot is ready
    print('We have logged in as {0.user}'.format(bot))
    print(f'{bot.user.name} is online!')
    print(bot.user.id)
    print('----------------------------')

    bot.loop.create_task(update_statistics())

async def fetch_rvn_data(session):
    async with session.get(URL, timeout=120) as r:
        if r.status == 429:
            retry_after = int(r.headers.get('Retry-After', '1'))
            logger.warning(f'Rate limit exceeded. Retrying after {retry_after} seconds.')
            await asyncio.sleep(retry_after)
            return None
        r.raise_for_status()
        data = await r.json()
        price = data['ravencoin']['usd']
    return price

async def update_bot_activity(price):
    activity = discord.Activity(name=f'RVN: ${price:,.5f} USD', type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)

async def send_embed(embed_channel, embed):
    message = await embed_channel.send(embed=embed)
    return message

async def update_statistics():
    guild = bot.guilds[0]
    channel_id = os.environ.get("CHANNEL_ID")
    channel = bot.get_channel(int(channel_id))
    embed_id = os.environ.get("EMBED_ID")
    embed_channel = bot.get_channel(int(embed_id))

    message = None
    async for msg in embed_channel.history(limit=100):
        if msg.author == bot.user:
            await msg.delete()
            break

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                now = datetime.datetime.now()
                price = await fetch_rvn_data(session)

                if price is not None:
                    await update_bot_activity(price)
                    channel_name = f'RVN - ${price:,.5f} USD'
                    await channel.edit(name=channel_name)

                async with session.get(url, timeout=120) as response:
                    response.raise_for_status()
                    data = await response.json()
                    price = data['market_data']['current_price']['usd']
                    mcap = data['market_data']['market_cap']['usd']
                    supply = data['market_data']['circulating_supply']
                    volume = data['market_data']['total_volume']['usd']
                    change = data['market_data']['price_change_percentage_24h']
                    block_time = data['block_time_in_minutes']

                # embed RVN stats to discord embed_channel
                embed = discord.Embed(
                    title = 'Ravencoin Price & Statistics',
                    description = description,
                    colour = discord.Colour.orange()
                )
                # add the image as the thumbnail
                embed.set_thumbnail(url=thumbnail_url)
                embed.set_author(name='', icon_url=thumbnail_url)
                # add the image to the body of the embed
                embed.set_image(url=image_url)
                embed.add_field(name = 'Price', value = f'${price:,.5f}')
                embed.add_field(name = '24 Hour Change', value = f'{data["market_data"]["price_change_percentage_24h"]:,.2f}%')
                embed.add_field(name = '24 Hour Volume', value = f'${data["market_data"]["total_volume"]["usd"]:,.0f}')
                embed.add_field(name = 'Market Cap', value = f'${mcap:,.0f}')
                embed.add_field(name = 'Circulating Supply', value = f'{supply:,.0f} RVN')
                embed.add_field(name = 'Block Time (minutes)', value = f'{block_time}')
                embed.add_field(name = f'{guild.name} Website', value = f'[{website_link}]({website_link})\n\n'
                                            '[Asset Explorer](https://ravencoin.asset-explorer.net/)\n'
                                            '[RVN Dashboard](https://www.rvn-dashboard.com/)\n'
                                            '[Whitepaper](https://ravencoin.org/assets/documents/Ravencoin.pdf)',
                                            inline=False)
                embed.add_field(name='Source', value=f'[Coingecko](https://www.coingecko.com/en/coins/ravencoin)')
                embed.set_footer(text=f'Last updated on {now.strftime("%B %d, %Y at %H:%M")}\nby RVN Bounty HunterZ', icon_url=author_url)

                if message:
                        await message.edit(embed=embed)
                else:
                        message = await send_embed(embed_channel, embed)

                await asyncio.sleep(update_interval)

            except aiohttp.ClientError as e:
                logger.error("An error occurred while getting market data", exc_info=True)
                await asyncio.sleep(30)
                message = None
            except Exception as e:
                logger.error("An unexpected error occurred", exc_info=True)
                await asyncio.sleep(30)
                message = None
            else:
                logger.info("RVN stats were successfully updated.")

@bot.event
async def on_disconnect():
    logger.warning("The bot has been disconnected")

@bot.command()
async def price(ctx):
    async with aiohttp.ClientSession() as session:
        price = await fetch_rvn_data(session)
        if price is not None:
            await ctx.send(f"Current RVN price: ${price:,.5f} USD")
        else:
            await ctx.send("Failed to fetch RVN price. Please try again later.")

try:
    bot.run(TOKEN)
except Exception as e:
    logger.error("An unexpected error occurred", exc_info=True)