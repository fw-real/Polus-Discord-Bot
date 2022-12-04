import os
import json
import asyncio
import discord
from utils import db
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

with open('config.json', 'r') as f:
    data = json.load(f)

intents = discord.Intents.default()
intents.message_content = True
token = os.getenv('TOKEN')
ownerid = data['ownerid']

bot = commands.Bot(owner_id=ownerid, intents=intents, help_command=None, case_insensitive=True)

@bot.event
async def on_ready():
    print(f'Successfully logged into {bot.user} ({bot.user.id})!')
    current_guilds = len(bot.guilds)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=f"/help || {current_guilds}srv"))
    await db.setup_db()

@bot.event
async def on_guild_join(guild):
    current_guilds = len(bot.guilds)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=f"/help || {current_guilds}srv"))

@bot.event
async def on_guild_remove(guild):
    current_guilds = len(bot.guilds)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=f"/help || {current_guilds}srv"))


for filename in os.listdir('./cogs'):    
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'cogs.{filename[:-3]}')
        except Exception as err:
            print(f'Something went wrong while trying to load {filename} cog!')
            print(f'ERROR: {err}')

bot.run(token)