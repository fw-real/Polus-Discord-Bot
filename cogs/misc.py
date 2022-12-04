import os
import json
import aiohttp
import discord
from utils import db, packages
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands
from discord import Option, Webhook
from dateutil.relativedelta import relativedelta

load_dotenv()
webhook_url = os.environ['WEBHOOK_LOGGER']
with open('config.json', 'r') as f:
    data = json.load(f)
success_emoji = data['success_emoji']
error_emoji = data['error_emoji']

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        print('Misc Cog has been connected successfully!')
    
    @commands.slash_command(description='Displays informations about the bot', guild_only=True)
    async def about(self, ctx):
        await ctx.defer(ephemeral=True)
        guild_check = await db.guild_bl_check(ctx.guild.id)
        if guild_check == True:
            blreason = await db.guild_bl_reason(ctx.guild.id)
            gbl_embed = discord.Embed(title=f'This guild has been blacklisted from the bot for reason: **{blreason}**', colour=discord.Colour.red())
            await ctx.respond(embed=gbl_embed)
        elif guild_check == False:
            user_check = await db.user_bl_check(ctx.author.id)
            if user_check == True:
                blreason = await db.user_bl_reason(ctx.author.id)
                ubl_embed = discord.Embed(title=f'You have been blacklisted from the bot for reason: **{blreason}**', colour=discord.Colour.red())
                await ctx.respond(embed=ubl_embed)
            else:
                pcheck = await db.check_premium(ctx.guild.id)
                if pcheck == True:
                    about_embed = discord.Embed(title='__About__', description=f"Current server's premium status: true\n**Owner:** [Nostorian](https://t.me/nostorian)\n**Servercount:** {len(self.bot.guilds)}\n**Created:** 09.10.2022\n**Language:** Python\n**API:** [py-cord v{discord.__version__}](https://github.com/Nostorian/Polus-Discord-Bot/Pycord-Development/pycord)")
                else:
                    about_embed = discord.Embed(title='__About__', description=f"Current server's premium status: false\n**Owner:** [Nostorian](https://t.me/nostorian)\n**Servercount:** {len(self.bot.guilds)}\n**Created:** 09.10.2022\n**Language:** Python\n**API:** [py-cord v{discord.__version__}](https://github.com/Nostorian/Polus-Discord-Bot/Pycord-Development/pycord)")
                about_embed.set_thumbnail(url=ctx.me.display_avatar.url)
                await ctx.respond(embed=about_embed)
    @about.error
    async def about_error(self, ctx, error):
        ae_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=ae_embed)
        raise error
        
    @commands.slash_command(description='Sends the invite link for the bot', guild_only=True)
    async def invite(self, ctx):
        await ctx.defer(ephemeral=True)
        guild_check = await db.guild_bl_check(ctx.guild.id)
        if guild_check == True:
            blreason = await db.guild_bl_reason(ctx.guild.id)
            gbl_embed = discord.Embed(title=f'This guild has been blacklisted from the bot for reason: **{blreason}**', colour=discord.Colour.red())
            await ctx.respond(embed=gbl_embed)
        elif guild_check == False:
            user_check = await db.user_bl_check(ctx.author.id)
            if user_check == True:
                blreason = await db.user_bl_reason(ctx.author.id)
                ubl_embed = discord.Embed(title=f'You have been blacklisted from the bot for reason: **{blreason}**', colour=discord.Colour.red())
                await ctx.respond(embed=ubl_embed)
            else:
                invite_embed = discord.Embed(description=f"Here's the link for inviting this bot 👉 [Click Me](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=285698135&scope=bot%20applications.commands)", colour=discord.Colour.green())
                await ctx.respond(embed=invite_embed)
    @invite.error
    async def invite_error(self, ctx, error):
        ie_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=ie_embed)
        raise error
    
    @commands.slash_command(description="Returns the bot's useful links", guild_only=True)
    async def links(self, ctx):
        await ctx.defer(ephemeral=True)
        guild_check = await db.guild_bl_check(ctx.guild.id)
        if guild_check == True:
            blreason = await db.guild_bl_reason(ctx.guild.id)
            gbl_embed = discord.Embed(title=f'This guild has been blacklisted from the bot for reason: **{blreason}**', colour=discord.Colour.red())
            await ctx.respond(embed=gbl_embed)
        elif guild_check == False:
            user_check = await db.user_bl_check(ctx.author.id)
            if user_check == True:
                blreason = await db.user_bl_reason(ctx.author.id)
                ubl_embed = discord.Embed(title=f'You have been blacklisted from the bot for reason: **{blreason}**', colour=discord.Colour.red())
                await ctx.respond(embed=ubl_embed)
            else:
                links_embed = discord.Embed(title='Useful links', description=f'📰 [Official Github Repo](https://github.com/Nostorian/Polus-Discord-Bot)\n🔗 [Bot Invite](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=285698135&scope=bot%20applications.commands)\n💰 [Donation Link](https://paypal.me/nostorian)\n📞 [Developer Contact](https://t.me/nostorian)')
                await ctx.respond(embed=links_embed)
    @links.error
    async def links_error(self, ctx, error):
        le_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=le_embed)
        raise error
        
    @commands.slash_command(description = "Shows the bot's latency!", guild_only=True)
    async def ping(self, ctx):
        ping_embed = discord.Embed(title=f'**Pong!** `{round(self.bot.latency * 1000)}ms`', colour=discord.Colour.green())
        await ctx.respond(embed=ping_embed)
    @ping.error
    async def ping_error(self, ctx, error):
        pe_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=pe_embed)
        raise error
    
    
    @commands.slash_command(description='Informations about NukeBot premium', guild_only=True)
    async def premium(self, ctx):
        await ctx.defer(ephemeral=True)
        guild_check = await db.guild_bl_check(ctx.guild.id)
        if guild_check == True:
            blreason = await db.guild_bl_reason(ctx.guild.id)
            gbl_embed = discord.Embed(title=f'This guild has been blacklisted from the bot for reason: **{blreason}**', colour=discord.Colour.red())
            await ctx.respond(embed=gbl_embed)
        elif guild_check == False:
            user_check = await db.user_bl_check(ctx.author.id)
            if user_check == True:
                blreason = await db.user_bl_reason(ctx.author.id)
                ubl_embed = discord.Embed(title=f'You have been blacklisted from the bot for reason: **{blreason}**', colour=discord.Colour.red())
                await ctx.respond(embed=ubl_embed)
            else:
                premium_embed = discord.Embed(title='**NukeBot Premium**', description="As a premium server you have exclusive rights.\n- No advertisements after clearing a channel\n- No cooldown for channel nuking\n- No limited amount of messages when using the purge command\n- and more coming soon\n If you're interested contact [me](https://t.me/nostorian) for gaining a license key.\n**We say thank you for support in the name of the whole NukeBot-Team**")
                premium_embed.add_field(name='Important Notice', value="Note: This bot is actually 100% free and you don't need to pay to gain access for premium features.\nProbably if you are running your own instance of my bot you can just change all of this stuff and put your own policies or smthing\nIf you actually want to support me, please donate to my [paypal](https://paypal.me/nostorian)")
                await ctx.respond(embed=premium_embed)
    @premium.error
    async def premium_error(self, ctx, error):
        pre_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=pre_embed)
        raise error
    
    license = discord.SlashCommandGroup(name='license', guild_only=True)
    
    @license.command(description='Activates the given license on a server')
    async def activate(self, ctx, licensekey: Option(str, 'Your license key', required=True)):
        await ctx.defer()
        guild_check = await db.guild_bl_check(ctx.guild.id)
        if guild_check == True:
            blreason = await db.guild_bl_reason(ctx.guild.id)
            gbl_embed = discord.Embed(title=f'This guild has been blacklisted from the bot for reason: **{blreason}**', colour=discord.Colour.red())
            await ctx.respond(embed=gbl_embed)
        elif guild_check == False:
            user_check = await db.user_bl_check(ctx.author.id)
            if user_check == True:
                blreason = await db.user_bl_reason(ctx.author.id)
                ubl_embed = discord.Embed(title=f'You have been blacklisted from the bot for reason: **{blreason}**', colour=discord.Colour.red())
                await ctx.respond(embed=ubl_embed)
            else:
                guild_p_check = await db.check_premium(ctx.guild.id)
                if guild_p_check == True:
                    ler_embed = discord.Embed(description=f'{error_emoji} This guild is already a premium server!', colour=discord.Colour.red())
                    await ctx.respond(embed=ler_embed)
                else:
                    first_check = await db.run_query(f"select exists(select * from activated_guilds where license_key = '{licensekey}')")
                    if first_check[0]['exists'] == True:
                        fc_embed = discord.Embed(description=f'{error_emoji} The license you entered has already been activated.', colour=discord.Colour.red())
                        await ctx.respond(embed=fc_embed)
                    else:
                        second_check = await db.run_query(f"select exists(select * from unactivated_licenses where license_key = '{licensekey}')")
                        if second_check[0]['exists'] == True:
                            licensetype = await db.run_query(f"select license_type from unactivated_licenses where license_key = '{licensekey}'")
                            third_check = await db.run_query(f"select exists(select * from unactivated_licenses where license_key = '{licensekey}' and userid is not null)")
                            if third_check[0]['exists'] == True:
                                applied_userid = await db.run_query(f"select userid from unactivated_licenses where license_key = '{licensekey}'")
                                if ctx.author.id == applied_userid[0]['userid']:
                                    if licensetype[0]['license_type'] == 'yearly':
                                        date_after_year = datetime.today()+ relativedelta(years=1)
                                        expirydate = date_after_year.strftime('%Y-%m-%d')
                                        await db.run_query(f"delete from unactivated_licenses where license_key = '{licensekey}'")
                                        await db.run_query(f"insert into activated_guilds(guild_id, license_key, user_id, expire_at) values({ctx.guild.id}, '{licensekey}', {ctx.author.id}, '{expirydate}')")
                                    elif licensetype[0]['license_type'] == 'lifetime':
                                        await db.run_query(f"delete from unactivated_licenses where license_key = '{licensekey}'")
                                        await db.run_query(f"insert into activated_guilds(guild_id, license_key, user_id, expire_at) values({ctx.guild.id}, '{licensekey}', {ctx.author.id}, 'infinity')")
                                    elif licensetype[0]['license_type'] == 'monthly':
                                        date_after_month = datetime.today()+ relativedelta(months=1)
                                        expirydate = date_after_month.strftime('%Y-%m-%d')
                                        await db.run_query(f"delete from unactivated_licenses where license_key = '{licensekey}'")
                                        await db.run_query(f"insert into activated_guilds(guild_id, license_key, user_id, expire_at) values({ctx.guild.id}, '{licensekey}', {ctx.author.id}, '{expirydate}')")
                                    elif licensetype[0]['license_type'] == 'weekly':
                                        date_after_week = datetime.today()+ relativedelta(weeks=1)
                                        expirydate = date_after_week.strftime('%Y-%m-%d')
                                        await db.run_query(f"delete from unactivated_licenses where license_key = '{licensekey}'")
                                        await db.run_query(f"insert into activated_guilds(guild_id, license_key, user_id, expire_at) values({ctx.guild.id}, '{licensekey}', {ctx.author.id}, '{expirydate}')")
                                    lsc_embed = discord.Embed(description=f'{success_emoji} License key **{licensekey}** has been activated for the guild **{ctx.guild.id}**.', colour=discord.Colour.green())
                                    await ctx.respond(embed=lsc_embed)
                                    async with aiohttp.ClientSession() as session:
                                        webhook = Webhook.from_url(webhook_url, session=session)
                                        lcreatewebhook_embed = discord.Embed(title=f'License Activated', description=f"License key: {licensekey}\nLicense type: {licensetype[0]['license_type']}\nActivated at: {ctx.guild.name} | {ctx.guild.id}\nActivated by: {ctx.author} | {ctx.author.id}", colour=discord.Colour.green())
                                        await webhook.send(embed=lcreatewebhook_embed, username='License Management')                                
                                else:
                                    ler_embed = discord.Embed(description=f"{error_emoji} This license key can only be activated by user with ID: {applied_userid[0]['userid']}", colour=discord.Colour.red())
                                    await ctx.respond(embed=ler_embed)
                            else:
                                if licensetype[0]['license_type'] == 'yearly':
                                    date_after_year = datetime.today()+ relativedelta(years=1)
                                    expirydate = date_after_year.strftime('%Y-%m-%d')
                                    await db.run_query(f"delete from unactivated_licenses where license_key = '{licensekey}'")
                                    await db.run_query(f"insert into activated_guilds(guild_id, license_key, user_id, expire_at) values({ctx.guild.id}, '{licensekey}', {ctx.author.id}, '{expirydate}')")
                                elif licensetype[0]['license_type'] == 'lifetime':
                                    await db.run_query(f"delete from unactivated_licenses where license_key = '{licensekey}'")
                                    await db.run_query(f"insert into activated_guilds(guild_id, license_key, user_id, expire_at) values({ctx.guild.id}, '{licensekey}', {ctx.author.id}, 'infinity')")
                                elif licensetype[0]['license_type'] == 'monthly':
                                    date_after_month = datetime.today()+ relativedelta(months=1)
                                    expirydate = date_after_month.strftime('%Y-%m-%d')
                                    await db.run_query(f"delete from unactivated_licenses where license_key = '{licensekey}'")
                                    await db.run_query(f"insert into activated_guilds(guild_id, license_key, user_id, expire_at) values({ctx.guild.id}, '{licensekey}', {ctx.author.id}, '{expirydate}')")
                                elif licensetype[0]['license_type'] == 'weekly':
                                    date_after_week = datetime.today()+ relativedelta(weeks=1)
                                    expirydate = date_after_week.strftime('%Y-%m-%d')
                                    await db.run_query(f"delete from unactivated_licenses where license_key = '{licensekey}'")
                                    await db.run_query(f"insert into activated_guilds(guild_id, license_key, user_id, expire_at) values({ctx.guild.id}, '{licensekey}', {ctx.author.id}, '{expirydate}')")
                                lsc_embed = discord.Embed(description=f'{success_emoji} License key **{licensekey}** has been activated for the guild **{ctx.guild.id}**.', colour=discord.Colour.green())
                                await ctx.respond(embed=lsc_embed)
                                async with aiohttp.ClientSession() as session:
                                    webhook = Webhook.from_url(webhook_url, session=session)
                                    lcreatewebhook_embed = discord.Embed(title=f'License Activated', description=f"License key: {licensekey}\nLicense type: {licensetype[0]['license_type']}\nActivated at: {ctx.guild.name} | {ctx.guild.id}\nActivated by: {ctx.author} | {ctx.author.id}", colour=discord.Colour.green())
                                    await webhook.send(embed=lcreatewebhook_embed, username='License Management')
                        else:
                            sc_embed = discord.Embed(description=f"{error_emoji} Incorrect license key. Please make sure you've entered it correctly.", colour=discord.Colour.red())
                            await ctx.respond(embed=sc_embed)
    @activate.error
    async def activate_error(self, ctx, error):
        acte_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=acte_embed)
        raise error
    
    @license.command(description='Lists your owned licenses')
    async def list(self, ctx):
        await ctx.defer(ephemeral=True)
        guild_check = await db.guild_bl_check(ctx.guild.id)
        if guild_check == True:
            blreason = await db.guild_bl_reason(ctx.guild.id)
            gbl_embed = discord.Embed(title=f'This guild has been blacklisted from the bot for reason: **{blreason}**', colour=discord.Colour.red())
            await ctx.respond(embed=gbl_embed)
        elif guild_check == False:
            user_check = await db.user_bl_check(ctx.author.id)
            if user_check == True:
                blreason = await db.user_bl_reason(ctx.author.id)
                ubl_embed = discord.Embed(title=f'You have been blacklisted from the bot for reason: **{blreason}**', colour=discord.Colour.red())
                await ctx.respond(embed=ubl_embed)
            else:
                check = await db.run_query(f"select license_key from unactivated_licenses where userid = {ctx.author.id}")
                check2 = await db.run_query(f"select license_key from activated_guilds where user_id = {ctx.author.id}")
                if len(check) == 0 and len(check2) == 0:
                    llist_embed = discord.Embed(title='Your NukeBot Premium licenses', description=f"You don't own a premium license. You can read everything about licenses by using the `/premium` command.")
                    llist_embed.set_thumbnail(url=ctx.me.display_avatar.url)
                    await ctx.respond(embed=llist_embed)
                elif len(check) > 0 and len(check2) > 0:
                    unlic = packages.get_list(check)
                    alic = packages.get_list(check2)
                    llist_embed = discord.Embed(title='Your NukeBot Premium licenses', description=f'Get information on each license key, by using the `/license info` command.')
                    llist_embed.add_field(name='Activated Licenses', value='\n'.join(map(str, alic)))
                    llist_embed.add_field(name='Unactivated Licenses', value='\n'.join(map(str, unlic)))
                    llist_embed.set_thumbnail(url=ctx.me.display_avatar.url)
                    await ctx.respond(embed=llist_embed)
                elif len(check) == 0 and len(check2) > 0:
                    alic = packages.get_list(check2)
                    llist_embed = discord.Embed(title='Your NukeBot Premium licenses', description=f'Get information on each license key, by using the `/license info` command.')
                    llist_embed.add_field(name='Activated Licenses', value='\n'.join(map(str, alic)))
                    llist_embed.add_field(name='Unactivated Licenses', value='none')
                    llist_embed.set_thumbnail(url=ctx.me.display_avatar.url)
                    await ctx.respond(embed=llist_embed)
                elif len(check) > 0 and len(check2) == 0:
                    unlic = packages.get_list(check)
                    llist_embed = discord.Embed(title='Your NukeBot Premium licenses', description=f'Get information on each license key, by using the `/license info` command.')
                    llist_embed.add_field(name='Activated Licenses', value='none')
                    llist_embed.add_field(name='Unactivated Licenses', value='\n'.join(map(str, unlic)))
                    llist_embed.set_thumbnail(url=ctx.me.display_avatar.url)
                    await ctx.respond(embed=llist_embed)
    @list.error
    async def list_error(self, ctx, error):
        le_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=le_embed)
        raise error
        
    @license.command(description='Returns information on the given license')
    async def info(self, ctx, licensekey: Option(str, 'Your license key', required=True)):
        await ctx.defer(ephemeral=True)
        guild_check = await db.guild_bl_check(ctx.guild.id)
        if guild_check == True:
            blreason = await db.guild_bl_reason(ctx.guild.id)
            gbl_embed = discord.Embed(title=f'This guild has been blacklisted from the bot for reason: **{blreason}**', colour=discord.Colour.red())
            await ctx.respond(embed=gbl_embed)
        elif guild_check == False:
            user_check = await db.user_bl_check(ctx.author.id)
            if user_check == True:
                blreason = await db.user_bl_reason(ctx.author.id)
                ubl_embed = discord.Embed(title=f'You have been blacklisted from the bot for reason: **{blreason}**', colour=discord.Colour.red())
                await ctx.respond(embed=ubl_embed)
            else:
                existence_check = await db.run_query(f"select exists(select * from unactivated_licenses where license_key = '{licensekey}')")
                if existence_check[0]['exists'] == True:
                    ownership_check = await db.run_query(f"select exists(select * from unactivated_licenses where license_key = '{licensekey}' and userid is not null)")
                    if ownership_check[0]['exists'] == True:
                        userid = await db.run_query(f"select userid from unactivated_licenses where license_key = '{licensekey}'")
                        if ctx.author.id == userid[0]['userid']:
                            ultype = await db.run_query(f"select license_type from unactivated_licenses where license_key = '{licensekey}'")
                            ulid = await db.run_query(f"select userid from unactivated_licenses where license_key = '{licensekey}'")
                            ul_embed = discord.Embed(title='License Information', description=f"**License Key: **{licensekey}\n**License Type: **{ultype[0]['license_type']}\n**License Owner ID: **{ulid[0]['userid']}")
                            ul_embed.set_thumbnail(url=ctx.me.display_avatar.url)
                            await ctx.respond(embed=ul_embed)
                        else:
                            ul_embed = discord.Embed(description=f"{error_emoji} You aren't authorized to view information on this license.", colour=discord.Colour.red())
                            await ctx.respond(embed=ul_embed)
                    else:
                        ultype = await db.run_query(f"select license_type from unactivated_licenses where license_key = '{licensekey}'")
                        ul_embed = discord.Embed(title='License Information', description=f"**License Key: **{licensekey}\n**License Type: **{ultype[0]['license_type']}")
                        ul_embed.set_thumbnail(url=ctx.me.display_avatar.url)
                        await ctx.respond(embed=ul_embed)
                else:
                    existence_check2 = await db.run_query(f"select exists(select * from activated_guilds where license_key = '{licensekey}')")
                    if existence_check2[0]['exists'] == True:
                        alid = await db.run_query(f"select user_id from activated_guilds where license_key = '{licensekey}'")
                        algid = await db.run_query(f"select guild_id from activated_guilds where license_key = '{licensekey}'")
                        alea = await db.run_query(f"select expire_at from activated_guilds where license_key = '{licensekey}'")
                        if ctx.author.id == alid[0]['user_id']:
                            guild = self.bot.get_guild(algid[0]['guild_id'])
                            al_embed = discord.Embed(title='License Information', description=f"**License Key: **{licensekey}\n**Activated At: **{guild.name} || {guild.id}\n**Activated By: **{ctx.author.mention}\n**Expires At: **{alea[0]['expire_at']}")
                            al_embed.set_thumbnail(url=ctx.me.display_avatar.url)
                            await ctx.respond(embed=al_embed)
                        else:
                            al_embed = discord.Embed(description=f"{error_emoji} You aren't authorized to view information on this license.", colour=discord.Colour.red())
                            await ctx.respond(embed=al_embed)
                    else:
                        al_embed = discord.Embed(description=f"{error_emoji} **{licensekey}** doesn't exist, please recheck your license key.", colour=discord.Colour.red())
                        await ctx.respond(embed=al_embed)
                        await ctx.respond(embed=al_embed)
    @info.error
    async def info_error(self, ctx, error):
        linfo_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=linfo_embed)
        raise error
        
def setup(bot):
    bot.add_cog(Misc(bot))