import io
import os
import sys
import rstr
import aiohttp
import asyncpg
import discord
import textwrap
import contextlib
from utils import db
from discord import Webhook
from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import Button, Select, View
from utils import packages
from traceback import format_exception

load_dotenv()
webhook_url = os.environ['WEBHOOK_LOGGER']

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Owner Cog has been connected successfully!')
    
    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title='Owner Commands', description='**Source Code: **[Github Repo](https://github.com/Nostorian/Polus-Discord-Bot)\n**Contact: **[Telegram](https://t.me/nostorian)\n**Support Me: **[PayPal](https://paypal.me/nostorian)\n\nNavigate through different sections of owner commands with the dropdown menu below.\n**⚠️ WARNING: Be mindful where you execute certain commands due to security reasons.**', colour=discord.Colour.blue())
        class OwnerView(View):
            async def on_timeout(self):
                view.remove_item(dropdown_menu)
                await bro.edit(view=self)
        dropdown_menu = Select(placeholder='Choose a category', min_values=1, max_values=1, options=[
            discord.SelectOption(emoji='🧩', label='Activity', description='Check out the activity commands.'),
            discord.SelectOption(emoji='🔃', label='Reload', description='Check out the reload commands.'),
            discord.SelectOption(emoji='🛠️', label='BotBan', description='Check out the botban commands.'),
            discord.SelectOption(emoji='🔐', label='License', description='Check out the license commands.'),
            discord.SelectOption(emoji='🗂️', label='Other', description='Check out the license commands.'),
        ])
        async def dropdown_callback(interaction):
            if dropdown_menu.values[0] == 'Activity':
                ac_embed = discord.Embed(title='Activity Commands', description=f"{ctx.me.mention} `activity [playing|streaming|listening|watching]`\n❯ changes the bot's activity to the desirable option.\n{ctx.me.mention} `activity reset`\n❯ resets the bot's activity to default.", colour=discord.Colour.blue())
                await interaction.response.edit_message(embed=ac_embed)
            elif dropdown_menu.values[0] == 'Reload':
                rc_embed = discord.Embed(title='Reload Commands', description=f"{ctx.me.mention} `reload all`\n❯ reloads all cogs of the bot.\n{ctx.me.mention} `reload cog 'cogname'`\n❯ reloads the given cog.", colour=discord.Colour.blue())
                await interaction.response.edit_message(embed=rc_embed)
            elif dropdown_menu.values[0] == 'BotBan':
                bc_embed = discord.Embed(title='BotBan Commands', description=f"{ctx.me.mention} `botban user [ban|unban] 'userid'`\n❯ ban or unban the given user from executing bot commands.\n{ctx.me.mention} `botban guild [ban|unban] 'userid'`\n❯ ban or unban the given guild from executing bot commands.", colour=discord.Colour.blue())
                await interaction.response.edit_message(embed=bc_embed)
            elif dropdown_menu.values[0] == 'License':
                lc_embed = discord.Embed(title='License Commands', description=f"{ctx.me.mention} `license create [lifetime|yearly|monthly|weekly]`\n❯ generates a license key which activates premium features in a guild.\n{ctx.me.mention} `license apply 'licensekey' 'userid'`\n❯ restricts a license key to be activated by one person only.\n{ctx.me.mention} `license delete 'licensekey'`\n❯ deletes the given license key.", colour=discord.Colour.blue())
                await interaction.response.edit_message(embed=lc_embed)
            elif dropdown_menu.values[0] == 'Other':
                oc_embed = discord.Embed(title='Other Commands', description=f"{ctx.me.mention} `shutdown`\n❯ logs out the bot.\n{ctx.me.mention} `eval 'code'`\n❯ evaluates the given python code, you can also wrap the code with codeblocks.\n{ctx.me.mention} `dm '@user' 'message'`\n❯ sends a message to the specified user.`", colour=discord.Colour.blue())
                await interaction.response.edit_message(embed=oc_embed)
        dropdown_menu.callback = dropdown_callback
        view = OwnerView(timeout=30)
        view.add_item(dropdown_menu)
        bro = await ctx.reply(embed=embed, view=view)
    @help.error
    async def help_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            pass
        else:
            await ctx.reply(f':x: Something went wrong while trying to execute this command! Please check terminal for more details...')
            raise error
        
    
    @commands.group()
    @commands.is_owner()
    async def activity(self, ctx):
        pass
    @activity.error
    async def activity_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            pass
    @activity.command()
    async def playing(self, ctx, *, activity):
        await self.bot.change_presence(activity=discord.Game(name=activity))
        await ctx.reply('The activity has been set successfully. Reset to normal by using the reset option.') 
    @playing.error
    async def playing_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"**The correct syntax to use this command is:**\n{ctx.me.mention}`activity playing 'activity_name'`")
        else:
            await ctx.reply(f':x: Something went wrong while trying to execute this command! Please check terminal for more details...')
            raise error
            
    @activity.command()
    async def streaming(self, ctx, stream_url, *, stream_name):
        await self.bot.change_presence(activity=discord.Streaming(name=stream_name, url=stream_url))
        await ctx.reply('The activity has been set successfully. Reset to normal by using the reset option.') 
    @streaming.error
    async def streaming_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"**The correct syntax to use this command is:**\n{ctx.me.mention}`activity streaming 'stream_url' 'stream_name'`")
        else:
            await ctx.reply(f':x: Something went wrong while trying to execute this command! Please check terminal for more details...')
            raise error
    
    @activity.command()
    async def listening(self, ctx, *, activity):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity))
        await ctx.reply('The activity has been set successfully. Reset to normal by using the reset option.') 
    @listening.error
    async def listening_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"**The correct syntax to use this command is:**\n{ctx.me.mention}`activity listening 'activity_name'`")
        else:
            await ctx.reply(f':x: Something went wrong while trying to execute this command! Please check terminal for more details...')
            raise error
    
    @activity.command()
    async def watching(self, ctx, *, activity):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity))
        await ctx.reply('The activity has been set successfully. Reset to normal by using the reset option.') 
    @watching.error
    async def watching_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"**The correct syntax to use this command is:**\n{ctx.me.mention}`activity watching 'activity_name'`")
        else:
            await ctx.reply(f':x: Something went wrong while trying to execute this command! Please check terminal for more details...')
            raise error
    @activity.command()
    async def reset(self, ctx):
        current_guilds = len(self.bot.guilds)
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=f"/help || {current_guilds}srv"))
        await ctx.reply('The activity has been reset successfully.')
    @reset.error
    async def reset_error(self, ctx, error):
        await ctx.reply(f':x: Something went wrong while trying to execute this command! Please check terminal for more details...')
        raise error
    @commands.group()
    @commands.is_owner()
    async def reload(self, ctx):
        pass
    @reload.error
    async def reload_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            pass
    @reload.command()
    async def all(self, ctx):
        for filename in os.listdir('./cogs'):    
            if filename.endswith('.py'):
                try:
                    self.bot.reload_extension(f'cogs.{filename[:-3]}')
                    print(f'Reloaded {filename} cog.')
                except Exception as err:
                    await ctx.reply(f"Couldn't reload {filename} cog, please check terminal for more details...")
                    print(f'Reloading failed for {filename} cog, error: {err}')
        await ctx.send('Finished reloading cogs, it may take a while for new slash commands to load.')
    @all.error
    async def cog_error(self, ctx, error):
        await ctx.reply(f':x: Something went wrong while trying to execute this command! Please check terminal for more details...')
        raise error
    
    @reload.command()
    async def cog(self, ctx, *, cog_name):
        cogs = os.listdir('./cogs')
        if f'{cog_name.lower()}.py' in cogs:
            try:
                self.bot.reload_extension(f'cogs.{cog_name.lower()}')
                await ctx.send(f'Finished reloading {cog_name.lower()} cog, it may take a while for new slash commands to load.')
            except Exception as err:
                await ctx.reply(f"Couldn't reload {cog_name.lower()} cog, please check terminal for more details...")
                print(f'Failed to reload {cog_name.lower()}.py cog, error: {err}')
        else:
            await ctx.reply(f"{cog_name.lower()}.py couldn't be reloaded as it doesn't exist.")
    @cog.error
    async def cog_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"**The correct syntax to use this command is:**\n{ctx.me.mention}`reload cog 'cog_name'`")
        else:
            await ctx.reply(f':x: Something went wrong while trying to execute this command! Please check terminal for more details...')
            raise error
            
    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.reply(f'**Shutting down bot...**')
        sys.exit()
    @shutdown.error
    async def shutdown_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            pass
    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx, *, code):
        code = packages.clean_code(code)

        local_variables = {
            "discord": discord,
            "commands": commands,
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message
        }

        stdout = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
                )

                obj = await local_variables["func"]()
                result = f"{stdout.getvalue()}\n-- {obj}\n"
                eval_embed = discord.Embed(title='Success', description=f'```\n{result}\n```', colour=discord.Colour.green())
        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))
            eval_embed = discord.Embed(title='Error', description=f'```\n{result}\n```', colour=discord.Colour.red())
        delete_button = Button(emoji='🗑️')
        async def delete_b_callback(interaction):
            if interaction.user.id == ctx.author.id:
                await interaction.message.delete()
            else:
                pass
        view = View()
        delete_button.callback = delete_b_callback
        view.add_item(delete_button)
        await ctx.reply(embed=eval_embed, view=view)
    @eval.error
    async def eval_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"**The correct syntax to use this command is:**\n{ctx.me.mention}`eval 'code'`")
        elif isinstance(error, commands.NotOwner):
            pass
        else:
            await ctx.reply(f':x: Something went wrong while trying to execute this command! Please check terminal for more details...')
            raise error
    @commands.command()
    @commands.is_owner()
    async def dm(self, ctx, user: discord.User, *, message):
        dm_embed = discord.Embed(title='New Message!', description=f'{message}\n-{ctx.author.name}#{ctx.author.discriminator}', colour=discord.Colour.blue())
        dm_embed.set_footer(text='This message was directly sent from the developer.')
        try:
            await user.send(f'{user.mention}', embed=dm_embed)
            success_embed = discord.Embed(title=f'Successfully sent the message to {user.name}#{user.discriminator} ({user.id}).', colour=discord.Colour.green())
            await ctx.reply(embed=success_embed)
        except:
            error_embed = discord.Embed(title=f"Couldn't message {user.name}#{user.discriminator} ({user.id}).", colour=discord.Colour.red())
            await ctx.reply(embed=error_embed)
    @dm.error
    async def dm_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"**The correct syntax to use this command is:**\n{ctx.me.mention}`dm '@user' 'message'`")
        elif isinstance(error, commands.NotOwner):
            pass
        else:
            await ctx.reply(f':x: Something went wrong while trying to execute this command! Please check terminal for more details...')
            raise error
    @commands.group()
    @commands.is_owner()
    async def botban(self, ctx):
        pass
    @botban.error
    async def botban_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            pass
    @botban.command()
    async def guild(self, ctx, action, guild_id, *, reason=None):
        if action == 'ban':
            if reason:
                await db.run_query(f"insert into blacklisted_guilds(guildid, reason) values({guild_id}, '{reason}')")
                bl_embed = discord.Embed(title=f'Guild with ID **{guild_id}** has successfully been banned from the bot for reason: **{reason}**.')
                await ctx.reply(embed=bl_embed)
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(webhook_url, session=session)
                    gbcreatewebhook_embed = discord.Embed(title=f'New Guild Banned', description=f'Guild ID: {guild_id}\nReason: {reason}\nBanned by: {ctx.author} || {ctx.author.id}', colour=discord.Colour.green())
                    await webhook.send(embed=gbcreatewebhook_embed, username='Blacklist Management')
            else:
                await db.run_query(f"insert into blacklisted_guilds(guildid, reason) values({guild_id}, 'No reason provided')")
                bl_embed = discord.Embed(title=f'Guild with ID **{guild_id}** has successfully been banned from the bot for reason: **No reason provided**.')
                await ctx.reply(embed=bl_embed)
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(webhook_url, session=session)
                    gbcreatewebhook_embed = discord.Embed(title=f'New Guild Banned', description=f'Guild ID: {guild_id}\nReason: No reason provided\nBanned by: {ctx.author} || {ctx.author.id}', colour=discord.Colour.green())
                    await webhook.send(embed=gbcreatewebhook_embed, username='Blacklist Management')
        elif action == 'unban':
            if reason:
                await db.run_query(f"delete from blacklisted_guilds where guildid = {guild_id}")
                bl_embed = discord.Embed(title=f'Guild with ID **{guild_id}** has successfully been unbanned from the bot for reason: **{reason}**.')
                await ctx.reply(embed=bl_embed)
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(webhook_url, session=session)
                    gubcreatewebhook_embed = discord.Embed(title=f'Guild Unbanned', description=f'Guild ID: {guild_id}\nReason: {reason}\nUnbanned by: {ctx.author} || {ctx.author.id}', colour=discord.Colour.green())
                    await webhook.send(embed=gubcreatewebhook_embed, username='Blacklist Management')
            else:
                await db.run_query(f"delete from blacklisted_guilds where guildid = {guild_id}")
                bl_embed = discord.Embed(title=f'Guild with ID **{guild_id}** has successfully been unbanned from the bot for reason: **No reason provided**.')
                await ctx.reply(embed=bl_embed)
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(webhook_url, session=session)
                    gubcreatewebhook_embed = discord.Embed(title=f'Guild Unbanned', description=f'Guild ID: {guild_id}\nReason: No reason provided\nUnbanned by: {ctx.author} || {ctx.author.id}', colour=discord.Colour.green())
                    await webhook.send(embed=gubcreatewebhook_embed, username='Blacklist Management')
        else:
            bl_embed = discord.Embed(title=f"Invalid option passed! Correct syntax is:\n{ctx.me.mention}`botban guild [ban|unban] 'guild_id'`")
            await ctx.reply(embed=bl_embed)
    @guild.error
    async def guild_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"**The correct syntax to use this command is:**\n{ctx.me.mention}`botban guild [ban|unban] 'guild_id'`")
        elif isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, asyncpg.exceptions.UniqueViolationError):
                bl_embed = discord.Embed(title=f'Guild is already blacklisted!')
                await ctx.reply(embed=bl_embed)
            else:
                await ctx.reply(f':x: Something went wrong while trying to execute this command! Please check terminal for more details...')
                raise error
        else:
            await ctx.reply(f':x: Something went wrong while trying to execute this command! Please check terminal for more details...')
            raise error
          
    @botban.command()
    async def user(self, ctx, action, user_id, *, reason=None):
        if action == 'ban':
            if reason:
                await db.run_query(f"insert into blacklisted_users(userid, reason) values({user_id}, '{reason}')")
                bl_embed = discord.Embed(title=f'User with ID **{user_id}** has successfully been banned from the bot for reason: **{reason}**.')
                await ctx.reply(embed=bl_embed)
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(webhook_url, session=session)
                    ubcreatewebhook_embed = discord.Embed(title=f'New User Banned', description=f'User ID: {user_id}\nReason: {reason}\nBanned by: {ctx.author} || {ctx.author.id}', colour=discord.Colour.red())
                    await webhook.send(embed=ubcreatewebhook_embed, username='Blacklist Management')
            else:
                await db.run_query(f"insert into blacklisted_users(userid, reason) values({user_id}, 'No reason provided')")
                bl_embed = discord.Embed(title=f'User with ID **{user_id}** has successfully been banned from the bot for reason: **No reason provided**.')
                await ctx.reply(embed=bl_embed)
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(webhook_url, session=session)
                    ubcreatewebhook_embed = discord.Embed(title=f'New User Banned', description=f'User ID: {user_id}\nReason: No reason provided\nBanned by: {ctx.author} || {ctx.author.id}', colour=discord.Colour.red())
                    await webhook.send(embed=ubcreatewebhook_embed, username='Blacklist Management')
        elif action == 'unban':
            if reason:
                await db.run_query(f"delete from blacklisted_users where userid = {user_id}")
                bl_embed = discord.Embed(title=f'User with ID **{user_id}** has successfully been unbanned from the bot for reason: **{reason}**.')
                await ctx.reply(embed=bl_embed)
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(webhook_url, session=session)
                    uubcreatewebhook_embed = discord.Embed(title=f'User Unbanned', description=f'User ID: {user_id}\nReason: {reason}\nUnbanned by: {ctx.author} || {ctx.author.id}', colour=discord.Colour.green())
                    await webhook.send(embed=uubcreatewebhook_embed, username='Blacklist Management')
            else:
                await db.run_query(f"delete from blacklisted_users where userid = {user_id}")
                bl_embed = discord.Embed(title=f'User with ID **{user_id}** has successfully been unbanned from the bot for reason: **No reason provided**.')
                await ctx.reply(embed=bl_embed)
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(webhook_url, session=session)
                    uubcreatewebhook_embed = discord.Embed(title=f'User Unbanned', description=f'User ID: {user_id}\nReason: No reason provided\nUnbanned by: {ctx.author} || {ctx.author.id}', colour=discord.Colour.green())
                    await webhook.send(embed=uubcreatewebhook_embed, username='Blacklist Management')
        else:
            bl_embed = discord.Embed(title=f"Invalid option passed! Correct syntax is:\n{ctx.me.mention}`botban user [ban|unban] 'user_id'`")
            await ctx.reply(embed=bl_embed)
    @user.error
    async def user_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"**The correct syntax to use this command is:**\n{ctx.me.mention}`botban user [ban|unban] 'user_id'`")
        elif isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, asyncpg.exceptions.UniqueViolationError):
                bl_embed = discord.Embed(title=f'User is already blacklisted!')
                await ctx.reply(embed=bl_embed)
            else:
                await ctx.reply(f':x: Something went wrong while trying to execute this command! Please check terminal for more details...')
                raise error
        else:
            await ctx.reply(f':x: Something went wrong while trying to execute this command! Please check terminal for more details...')
            raise error
            
    @commands.group()
    @commands.is_owner()
    async def license(self, ctx):
        pass
    @license.error
    async def license_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            pass
    @license.command()
    async def create(self, ctx, license_type):
        regex = '^[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}$'
        licensekey = rstr.xeger(regex)
        if license_type.lower() in ['yearly', 'monthly', 'weekly', 'lifetime']:
            await db.run_query(f"insert into unactivated_licenses(license_key, license_type) values('{licensekey}', '{license_type.lower()}')")
            await ctx.reply(licensekey)
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(webhook_url, session=session)
                lcreatewebhook_embed = discord.Embed(title=f'New License Created', description=f'License key: {licensekey}\nLicense type: {license_type.lower()}\nCreated by: {ctx.author} || {ctx.author.id}', colour=discord.Colour.green())
                await webhook.send(embed=lcreatewebhook_embed, username='License Management')
        else:
            await ctx.reply(f"{license_type} is not a valid license type!\n**The correct syntax to use this command is:**\n{ctx.me.mention}`license create [lifetime|yearly|monthly|weekly] 'user_id'`")
    @create.error
    async def create_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"**The correct syntax to use this command is:**\n{ctx.me.mention}`license create [lifetime|yearly|monthly|weekly] 'user_id'`")
        else:
            await ctx.reply(f':x: Something went wrong while trying to execute this command! Please check terminal for more details...')
            raise error
    @license.command()
    async def apply(self, ctx, license_key, user_id: int):
        check = await db.run_query(f"select exists(select * from unactivated_licenses where license_key = '{license_key}')")
        if check[0]['exists'] == True:
            lcheck = await db.run_query(f"select exists(select * from unactivated_licenses where license_key = '{license_key}' and userid is not null)")
            if lcheck[0]['exists'] == True:
                luser = await db.run_query(f"select userid from unactivated_licenses where license_key = '{license_key}'")
                la_embed = discord.Embed(title=f"License is already applied to user with ID: {luser[0]['userid']}", colour=discord.Colour.red())
                await ctx.reply(embed=la_embed)
            else:
                await db.run_query(f"update unactivated_licenses set userid = {user_id} where license_key = '{license_key}'")
                license_type = await db.run_query(f"select license_type from unactivated_licenses where license_key = '{license_key}'")
                await ctx.reply('Applied license successfully!')
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(webhook_url, session=session)
                    la_embed = discord.Embed(title='License Applied', description=f"License key: {license_key}\nLicense type: {license_type[0]['license_type']}\nApplied to: {user_id}\nApplied by: {ctx.author} || {ctx.author.id}", colour=discord.Colour.green())
                    await webhook.send(embed=la_embed, username='License Management')
        else:
            la_embed = discord.Embed(title=f"License ({license_key}) doesn't exist!", colour=discord.Colour.red())
            await ctx.reply(embed=la_embed)
    @apply.error
    async def apply_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"**The correct syntax to use this command is:**\n{ctx.me.mention}`license apply 'license_key' 'user_id'`")
        else:
            await ctx.reply(f':x: Something went wrong while trying to execute this command! Please check terminal for more details...')
            raise error
    @license.command()
    async def delete(self, ctx, license_key):
        check = await db.run_query(f"select exists(select * from unactivated_licenses where license_key = '{license_key}')")
        if check[0]['exists'] == True:
            license_type = await db.run_query(f"select license_type from unactivated_licenses where license_key = '{license_key}'")
            await db.run_query(f"delete from unactivated_licenses where license_key = '{license_key}'")
            await ctx.reply('Deleted license successfully!')
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(webhook_url, session=session)
                ld_embed = discord.Embed(title='License Deleted', description=f"License key: {license_key}\nLicense type: {license_type[0]['license_type']}\nDeleted by: {ctx.author} || {ctx.author.id}", colour=discord.Colour.red())
                await webhook.send(embed=ld_embed, username='License Management')
        else:
            ld_embed = discord.Embed(title=f"License ({license_key}) doesn't exist!", colour=discord.Colour.red())
            await ctx.reply(embed=ld_embed)
    @delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"**The correct syntax to use this command is:**\n{ctx.me.mention}`license delete 'license_key'`")
        else:
            await ctx.reply(f':x: Something went wrong while trying to execute this command! Please check terminal for more details...')
            raise error
    
def setup(bot):
    bot.add_cog(Owner(bot))
