import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

postgres_url = os.environ['POSTGRESQL_URL']

async def run_query(query):
    """
    run a query to postgresql via asyncpg
    """
    conn = await asyncpg.connect(postgres_url)
    return await conn.fetch(query)

    

async def check_premium(guild_id):
    """
    check if the author's guild is premium or not
    """
    pcheck = await run_query(f'select exists(select * from activated_guilds where guild_id = {guild_id} and expire_at > NOW())')
    if pcheck[0]['exists'] == True:
        return True
    else:
        return False

async def user_bl_check(user_id):
    """
    check if the author is blacklisted or not
    """
    check = await run_query(f'select exists(select * from blacklisted_users where userid = {user_id})')
    if check[0]['exists'] == True:
        return True
    else:
        return False

async def guild_bl_check(guild_id):
    """
    check if the author's guild is blacklisted or not
    """
    check = await run_query(f'select exists(select * from blacklisted_guilds where guildid = {guild_id})')
    if check[0]['exists'] == True:
        return True
    else:
        return False        

async def user_bl_reason(user_id):
    reason = await run_query(f'select reason from blacklisted_users where userid = {user_id}')
    return reason[0]['reason']

async def guild_bl_reason(guild_id):
    reason = await run_query(f'select reason from blacklisted_guilds where guildid = {guild_id}')
    return reason[0]['reason']

    


async def setup_db():
    try:
        print('Intializing database...')
        await run_query("create table if not exists unactivated_licenses(license_key varchar(25) primary key, license_type varchar(10) not null, userid bigint);")
        await run_query("create table if not exists activated_guilds(guild_id bigint primary key, license_key varchar(25) not null, user_id bigint not null, expire_at date not null);")
        await run_query("create table if not exists inviteblocker(guild_id bigint primary key, whitelist_roles bigint[]);")
        await run_query("create table if not exists linkwarn(channel_id bigint primary key, guild_id bigint not null, pingrole bigint[], whitelist_roles bigint[]);")
        await run_query("create table if not exists blacklisted_users(userid bigint primary key, reason varchar(500) not null);")
        await run_query("create table if not exists blacklisted_guilds(guildid bigint primary key, reason varchar(500) not null);")
        await run_query("create table if not exists tempchannel(guildid bigint primary key, vcid bigint not null);")
        print('Successfully initialized database!')
    except Exception as err:
        print('Database initialization failed! Please check the logs below.')
        raise err