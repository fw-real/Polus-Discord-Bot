import time
import random
import asyncio
import discord
import nest_asyncio
from utils import db
from discord import Option
from discord.ext import commands
from discord.ui import Button, View

nest_asyncio.apply()

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    def nuke_cooldown(ctx):
        premium_check = asyncio.run(db.check_premium(ctx.guild.id))
        if premium_check == True:
            return None
        else:
            return commands.Cooldown(1, 60)
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Admin Cog has been connected successfully!')
     
    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            blacklist = ['discord.gg/', 'discord.com/invite']
            check = await db.run_query(f'select exists(select * from inviteblocker where guild_id={message.guild.id})')
            if check[0]['exists'] == True:
                if message.author == self.bot.user:
                    pass
                else:
                    rcheck = await db.run_query(f'select whitelist_roles from inviteblocker where guild_id={message.guild.id}')
                    if rcheck[0]['whitelist_roles'] == None:
                        if any(word in message.content.lower() for word in blacklist):
                            try:
                                await message.delete()
                            except:
                                pass
                            await message.channel.send(f'{message.author.mention}, it seems like you sent an invite for a discord server. Please stop advertising.')
                    elif rcheck[0]['whitelist_roles'] == []:
                        if any(word in message.content.lower() for word in blacklist):
                            try:
                                await message.delete()
                            except:
                                pass
                            await message.channel.send(f'{message.author.mention}, it seems like you sent an invite for a discord server. Please stop advertising.')
                    else:
                        rsrc = rcheck[0]['whitelist_roles']
                        if any(role.id in rsrc for role in message.author.roles):
                            pass
                        else:
                            if any(word in message.content.lower() for word in blacklist):
                                try:
                                    await message.delete()
                                except:
                                    pass
                                await message.channel.send(f'{message.author.mention}, it seems like you sent an invite for a discord server. Please stop advertising.')
            else:
                pass
        except:
            pass
    @commands.Cog.listener('on_message')
    async def linkwarn_event(self, message):
        try:
            blacklist = ['https://', 'http']
            check = await db.run_query(f'select exists(select * from linkwarn where guild_id={message.guild.id})')
            if check[0]['exists'] == True:
                if message.author == self.bot.user:
                    pass
                else:
                    rcheck = await db.run_query(f'select whitelist_roles from linkwarn where guild_id = {message.guild.id}')
                    channelid = await db.run_query(f'select channel_id from linkwarn where guild_id = {message.guild.id}')
                    if rcheck[0]['whitelist_roles'] == None:
                        if any(word in message.content.lower() for word in blacklist):
                            pingrole = await db.run_query(f'select pingrole from linkwarn where guild_id = {message.guild.id}')
                            if pingrole[0]['pingrole'] == None:
                                linkwarnalert_embed = discord.Embed(title='Message infos', description=f'User: {message.author} | {message.author.id}\nChannel: {message.channel.mention}\nMessage content:\n{message.content}')
                                alertchannel = discord.utils.get(message.guild.channels, id=channelid[0]['channel_id'])
                                await alertchannel.send(f'Link warning\n{message.jump_url}', embed=linkwarnalert_embed)
                            else:
                                rlist = pingrole[0]['pingrole']
                                therlist = []
                                for ids in rlist:
                                    rid = discord.utils.get(message.guild.roles, id=ids)
                                    therlist.append(rid)
                                bro = [roles.mention for roles in therlist]
                                bro2 = ', '.join(bro)
                                linkwarnalert_embed = discord.Embed(title='Message infos', description=f'User: {message.author} | {message.author.id}\nChannel: {message.channel.mention}\nMessage content:\n{message.content}')
                                alertchannel = discord.utils.get(message.guild.channels, id=channelid[0]['channel_id'])
                                await alertchannel.send(f'{bro2}\nLink warning\n{message.jump_url}', embed=linkwarnalert_embed)
                    else:
                        rsrc = rcheck[0]['whitelist_roles']
                        if any(role.id in rsrc for role in message.author.roles):
                            pass
                        else:
                            if any(word in message.content.lower() for word in blacklist):
                                pingrole = await db.run_query(f'select pingrole from linkwarn where guild_id = {message.guild.id}')
                                if pingrole[0]['pingrole'] == None:
                                    linkwarnalert_embed = discord.Embed(title='Message infos', description=f'User: {message.author} | {message.author.id}\nChannel: {message.channel.mention}\nMessage content:\n{message.content}')
                                    alertchannel = discord.utils.get(message.guild.channels, id=channelid[0]['channel_id'])
                                    await alertchannel.send(f'Link warning\n{message.jump_url}', embed=linkwarnalert_embed)
                                else:
                                    rlist = pingrole[0]['pingrole']
                                    therlist = []
                                    for ids in rlist:
                                        rid = discord.utils.get(message.guild.roles, id=ids)
                                        therlist.append(rid)
                                    bro = [roles.mention for roles in therlist]
                                    bro2 = ', '.join(bro)
                                    linkwarnalert_embed = discord.Embed(title='Message infos', description=f'User: {message.author} | {message.author.id}\nChannel: {message.channel.mention}\nMessage content:\n{message.content}')
                                    alertchannel = discord.utils.get(message.guild.channels, id=channelid[0]['channel_id'])
                                    await alertchannel.send(f'{bro2}\nLink warning\n{message.jump_url}', embed=linkwarnalert_embed)
        except:
            pass
    
    @commands.Cog.listener('on_voice_state_update')
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def tempchannel_event(self, member, before, after):
        check = await db.run_query(f'select exists(select * from tempchannel where guildid = {member.guild.id})')
        if check[0]['exists'] == True:
            if after.channel != None:
                vcid = await db.run_query(f'select vcid from tempchannel where guildid = {member.guild.id}')
                if after.channel.id == vcid[0]['vcid']:
                    if after.channel.category:
                        tc_category = discord.utils.get(member.guild.categories, id=after.channel.category.id)
                        tempchannel = await member.guild.create_voice_channel(name=f'⌛ {member.display_name}', category=tc_category)
                        await tempchannel.set_permissions(member, connect=True, mute_members=True, manage_channels=True)
                        await member.move_to(tempchannel)
                    else:
                        tempchannel = await member.guild.create_voice_channel(name=f'⌛ {member.display_name}')
                        await tempchannel.set_permissions(member, connect=True, mute_members=True, manage_channels=True)
                        await member.move_to(tempchannel)
                    def check(x, y, z):
                        return len(tempchannel.members) == 0
                    await self.bot.wait_for('voice_state_update', check=check)
                    await tempchannel.delete()
        else:
            pass

    @commands.slash_command(description='Ban a user easily', guild_only=True)
    @discord.default_permissions(ban_members=True)
    async def ban(self, ctx, user: Option(discord.Member, 'The user you want to ban', required=True), reason: Option(str, 'The reason for banning the user', required=False), history: Option(str, 'Message history of user to delete', choices=['Delete none', 'Last 24 hours', 'Last 7 days'], required=False)):
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
                if ctx.me.guild_permissions.kick_members == True:            
                    check = ctx.guild.get_member(user.id)
                    if check == None:
                        be_resp = discord.Embed(description=f'Error banning user. Please check if the user is still on this server and my highest role is above their highest one.', colour=discord.Colour.red())
                        await ctx.respond(embed=be_resp)
                    elif user.id == ctx.guild.owner.id:
                        be_resp = discord.Embed(description=f'Error banning user. Please check if the user is still on this server and my highest role is above their highest one.', colour=discord.Colour.red())
                        await ctx.respond(embed=be_resp)
                    elif user.top_role >= ctx.me.top_role:
                        be_resp = discord.Embed(description=f'Error banning user. Please check if the user is still on this server and my highest role is above their highest one.', colour=discord.Colour.red())
                        await ctx.respond(embed=be_resp)
                    else:
                        if not reason:
                            b_reason = f'Initiated by {ctx.author} | ID: {ctx.author.id}'
                            b_resp = discord.Embed(description=f'Successfully banned {user.mention}.', colour=discord.Colour.green())
                        else:
                            b_reason = f'{reason} | Initiated by {ctx.author} | ID: {ctx.author.id}'
                            b_resp = discord.Embed(description=f'Successfully banned {user.mention} for reason `{reason}`.', colour=discord.Colour.green())
                        
                        if history == 'Last 24 hours':
                            msg_del = 86400
                        elif history == 'Last 7 days':
                            msg_del = 604800
                        else:
                            msg_del = 0
                        await user.ban(delete_message_seconds=msg_del, reason=b_reason)
                        await ctx.respond(embed=b_resp)
                else:
                    b_resp = discord.Embed(description='I need the **BAN MEMBERS** permission for doing that.', colour=discord.Colour.red())
                    await ctx.respond(embed=b_resp)
    @ban.error
    async def ban_error(self, ctx, error):
        be_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=be_embed)
        raise error
            
    @commands.slash_command(description='Kick a user easily', guild_only=True)
    @discord.default_permissions(kick_members=True)
    async def kick(self, ctx, user: Option(discord.Member, 'The user you want to kick', required=True), reason: Option(str, 'The reason for kicking the user', required=False)):
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
                if ctx.me.guild_permissions.kick_members == True:
                    check = ctx.guild.get_member(user.id)
                    if check == None:
                        ke_resp = discord.Embed(description=f'Error kicking user. Please check if the user is still on this server and my highest role is above their highest one.', colour=discord.Colour.red())
                        await ctx.respond(embed=ke_resp)
                    elif user.id == ctx.guild.owner.id:
                        ke_resp = discord.Embed(description=f'Error kicking user. Please check if the user is still on this server and my highest role is above their highest one.', colour=discord.Colour.red())
                        await ctx.respond(embed=ke_resp)
                    elif user.top_role >= ctx.me.top_role:
                        ke_resp = discord.Embed(description=f'Error kicking user. Please check if the user is still on this server and my highest role is above their highest one.', colour=discord.Colour.red())
                        await ctx.respond(embed=ke_resp)
                    else:
                        if not reason:
                            k_reason = f'Initiated by {ctx.author} | ID: {ctx.author.id}'
                            k_resp = discord.Embed(description=f'Successfully kicked {user.mention}.', colour=discord.Colour.green())
                        else:
                            k_reason = f'{reason} | Initiated by {ctx.author} | ID: {ctx.author.id}'
                            k_resp = discord.Embed(description=f'Successfully kicked {user.mention} for reason `{reason}`.', colour=discord.Colour.green())

                        await user.kick(reason=k_reason)
                        await ctx.respond(embed=k_resp)
                else:
                    k_resp = discord.Embed(description='I need the **KICK MEMBERS** permission for doing that.', colour=discord.Colour.red())
                    await ctx.respond(embed=k_resp)
    @kick.error
    async def kick_error(self, ctx, error):
        ke_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=ke_embed)
        raise error
    
    @commands.slash_command(description='Deletes a given amount of messages', guild_only=True)
    @discord.default_permissions(manage_messages=True)
    async def purge(self, ctx, amount: Option(int, 'The amount of messages to delete', required=True)):
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
                if amount > 10:
                    pcheck = await db.check_premium(ctx.guild.id)
                    if pcheck == True:
                        await ctx.channel.purge(limit=amount)
                        pembed = discord.Embed(description=f'Deleted {amount} messages.', colour=discord.Colour.green())
                        await ctx.send(embed=pembed)
                    else:
                        pembed = discord.Embed(description='The maximum amount for message purging in non-premium servers is 10.', colour=discord.Colour.red())
                        await ctx.respond(embed=pembed)
                else:
                    await ctx.channel.purge(limit=amount)
                    pembed = discord.Embed(description=f'Deleted {amount} messages.', colour=discord.Colour.green())
                    await ctx.send(embed=pembed)
    @purge.error
    async def purge_error(self, ctx, error):
        pe_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=pe_embed)
        raise error
    
    @commands.slash_command(description='Main command for nuking channels', guild_only=True)
    @discord.default_permissions(manage_channels=True, manage_guild=True)
    @commands.dynamic_cooldown(nuke_cooldown, commands.BucketType.user)
    async def nuke(self, ctx):
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
                if ctx.me.guild_permissions.manage_channels == True and ctx.me.guild_permissions.manage_roles == True:
                    class NukeView(View):
                        async def on_timeout(self):
                            try:
                                await self.message.delete()
                            except:
                                pass
                    yes_button = Button(label='Yes', style=discord.ButtonStyle.green)
                    no_button = Button(label='No', style=discord.ButtonStyle.red)
                    
                    async def yes_callback(interaction):
                        if interaction.user.id == ctx.author.id:
                            nuke_channel = interaction.channel
                            new_channel = await nuke_channel.clone()
                            await nuke_channel.delete()
                            premium_check = await db.check_premium(ctx.guild.id)
                            ads = ['If you like this bot, please star its repo at https://github.com/Nostorian/Polus-Discord-Bot', "If you need a premium license(it's free!), a custom made project for you or direct help, contact the developer at https://t.me/nostorian)", 'You can donate me some money at https://paypal.me/nostorian if you find my work good, thanks!']
                            if premium_check == True:
                                await new_channel.send('⚠️Nuked this channel⚠️')
                                await new_channel.send('https://i.imgur.com/TSAfgFO.gif')
                            else:
                                await new_channel.send('⚠️Nuked this channel⚠️')
                                await new_channel.send('https://i.imgur.com/TSAfgFO.gif')
                                await new_channel.send(f'**__Advertisement__**\n\n{random.choice(ads)}')
                        else:
                            nuke_deny = discord.Embed(description='Please use the command by yourself to nuke a channel.', colour=discord.Colour.red())
                            await interaction.response.send_message(embed=nuke_deny, ephemeral=True)
                    async def no_callback(interaction):
                        if interaction.user.id == ctx.author.id:
                            await interaction.message.delete()
                        else:
                            nuke_deny = discord.Embed(description='Please use the command by yourself to interact with this message.')
                            await interaction.response.send_message(embed=nuke_deny, ephemeral=True)
                    
                    yes_button.callback = yes_callback
                    no_button.callback = no_callback
                    nuke_embed = discord.Embed(description='Are you sure you want to nuke this channel?\nThis will also clear all webhooks and invites of this channel!', colour=discord.Colour.yellow())
                    nview = NukeView(timeout=10)
                    nview.add_item(yes_button)
                    nview.add_item(no_button)
                    bro = await ctx.respond(embed=nuke_embed, view=nview)
                else:
                    n_resp = discord.Embed(description='I need the **MANAGE ROLES** and the **MANAGE CHANNEL** permission for clearing this channel.', colour=discord.Colour.red())
                    await ctx.respond(embed=n_resp)
    @nuke.error
    async def nuke_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            ne_embed = discord.Embed(description='This command has a cooldown of 1 minute. If you want to remove the delay, you can request for a premium license key from the [developer](https://t.me/nostorian).', colour=discord.Colour.red())
            await ctx.respond(embed=ne_embed)
        else:
            ne_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
            await ctx.respond(embed=ne_embed)
            raise error
            
    inviteblocker = discord.SlashCommandGroup(name='inviteblocker', default_member_permissions=discord.Permissions(permissions=32), guild_only=True)
    
    @inviteblocker.command(description='Toggles the inviteblocker')
    async def toggle(self, ctx):
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
                check = await db.run_query(f'select exists(select * from inviteblocker where guild_id = {ctx.guild.id})')
                if check[0]['exists'] == True:
                    await db.run_query(f'delete from inviteblocker where guild_id = {ctx.guild.id}')
                    toggle_embed = discord.Embed(description='The inviteblocker has been disabled successfully.', colour=discord.Colour.green())
                    await ctx.respond(embed=toggle_embed)
                else:
                    await db.run_query(f'insert into inviteblocker(guild_id) values({ctx.guild.id})')
                    toggle_embed = discord.Embed(description='The inviteblocker has been enabled successfully.\nAdd roles to the whitelist by using **/inviteblocker whitelist add <role>**', colour=discord.Colour.green())
                    await ctx.respond(embed=toggle_embed)
    @toggle.error
    async def toggle_error(self, ctx, error):
        te_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=te_embed)
        raise error
            
    @inviteblocker.command(description='Manage the inviteblocker whitelist')
    async def whitelist(self, ctx, action: Option(str, 'Whether to add or remove a role from the whitelist', choices=['add', 'remove'], required=True), role: Option(discord.Role, 'The role you want to add / remove from the whitelist', required=True)):
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
                if action == 'add':
                    check = await db.run_query(f'select exists(select * from inviteblocker where guild_id = {ctx.guild.id})')
                    if check[0]['exists'] == True:
                        echeck = await db.run_query(f'select whitelist_roles from inviteblocker where guild_id = {ctx.guild.id}')
                        rlist = echeck[0]['whitelist_roles']
                        if rlist == None:
                            await db.run_query('update inviteblocker set whitelist_roles = whitelist_roles || '+"'{"+str(role.id)+"}'")
                            ibwembed = discord.Embed(description='The role has been added to the whitelist successfully', colour=discord.Colour.green())
                            await ctx.respond(embed=ibwembed)
                        elif role.id in rlist:
                            ibwembed = discord.Embed(description="Couldn't add the role because it's already added. Use **/inviteblocker status** for more infos.", colour=discord.Colour.red())
                            await ctx.respond(embed=ibwembed)
                        else:
                            await db.run_query('update inviteblocker set whitelist_roles = whitelist_roles || '+"'{"+str(role.id)+"}'")
                            ibwembed = discord.Embed(description='The role has been added to the whitelist successfully', colour=discord.Colour.green())
                            await ctx.respond(embed=ibwembed)
                    else:
                        ibwembed = discord.Embed(description="Couldn't manage the whitelist roles since inviteblocker is current disabled.\nEnable it by using **/inviteblocker toggle**", colour=discord.Colour.red())
                        await ctx.respond(embed=ibwembed)
                else:
                    check = await db.run_query(f'select exists(select * from inviteblocker where guild_id = {ctx.guild.id})')
                    if check[0]['exists'] == True:
                        echeck = await db.run_query(f'select whitelist_roles from inviteblocker where guild_id = {ctx.guild.id}')
                        rlist = echeck[0]['whitelist_roles']
                        if rlist == None:
                            ibwembed = discord.Embed(description="Couldn't remove the role because it's already removed. Use **/inviteblocker status** for more infos.", colour=discord.Colour.red())
                            await ctx.respond(embed=ibwembed)
                        elif role.id in rlist:
                            await db.run_query(f"update inviteblocker set whitelist_roles = array_remove(whitelist_roles, '{role.id}')")
                            ibwembed = discord.Embed(description='The role has been removed from the whitelist successfully', colour=discord.Colour.green())
                            await ctx.respond(embed=ibwembed)
                        else:
                            ibwembed = discord.Embed(description="Couldn't remove the role because it's already removed. Use **/inviteblocker status** for more infos.", colour=discord.Colour.red())
                            await ctx.respond(embed=ibwembed)
                    else:
                        ibwembed = discord.Embed(description="Couldn't manage the whitelist roles since inviteblocker is current disabled.\nEnable it by using **/inviteblocker toggle**", colour=discord.Colour.red())
                        await ctx.respond(embed=ibwembed)
    @whitelist.error
    async def whitelist_error(self, ctx, error):
        we_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=we_embed)
        raise error
    @inviteblocker.command(description='Shows the current status of the inviteblocker')
    async def status(self, ctx):
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
                check = await db.run_query(f'select exists(select * from inviteblocker where guild_id = {ctx.guild.id})')
                if check[0]['exists'] == True:
                    rsrc = await db.run_query(f'select whitelist_roles from inviteblocker where guild_id = {ctx.guild.id}')
                    if rsrc[0]['whitelist_roles'] == None:
                        ibsembed = discord.Embed(title=f'Inviteblocker status for {ctx.guild.name}', description='Status: true')
                        ibsembed.add_field(name='Whitelist roles', value='none')
                        await ctx.respond(embed=ibsembed)
                    elif rsrc[0]['whitelist_roles'] == []:
                        ibsembed = discord.Embed(title=f'Inviteblocker status for {ctx.guild.name}', description='Status: true')
                        ibsembed.add_field(name='Whitelist roles', value='none')
                        await ctx.respond(embed=ibsembed)
                    else:
                        rlist = rsrc[0]['whitelist_roles']
                        therlist = []
                        for ids in rlist:
                            rid = discord.utils.get(ctx.guild.roles, id=ids)
                            therlist.append(rid)
                        bro = [roles.mention for roles in therlist]
                        ibsembed = discord.Embed(title=f'Inviteblocker status for {ctx.guild.name}', description='Status: true')
                        ibsembed.add_field(name='Whitelist roles', value='\n'.join(map(str, bro)))
                        await ctx.respond(embed=ibsembed)
                else:
                    ibsembed = discord.Embed(title=f'Inviteblocker status for {ctx.guild.name}', description='Status: false')
                    await ctx.respond(embed=ibsembed)
    @status.error
    async def status_error(self, ctx, error):
        se_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=se_embed)
        raise error

    linkwarn = discord.SlashCommandGroup(name='linkwarn', default_member_permissions=discord.Permissions(permissions=32), guild_only=True)
    @linkwarn.command(description='Enable the linkwarn system')
    async def enable(self, ctx, warnchannel: Option(discord.TextChannel, 'The channel to recieve warn messages in', required=True)):
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
                check = await db.run_query(f'select exists(select * from linkwarn where guild_id = {ctx.guild.id})')
                if check[0]['exists'] == False:
                    await db.run_query(f'insert into linkwarn(channel_id, guild_id) values({warnchannel.id}, {ctx.guild.id})')
                    lwe_embed = discord.Embed(description=f'Successfully enabled link warnings.\nWarnings will be sent to {warnchannel.mention}.\nAdd ping roles using `/linkwarn pingrole add <role>`.\nWhitelist roles using `/linkwarn whitelist add <role>`.', colour=discord.Colour.green())
                    await ctx.respond(embed=lwe_embed)
                else:
                    lwe_embed = discord.Embed(description='Link warnings are already activated on this server. For updating the channel, please use `/linkwarn channel <channel>`.', colour=discord.Colour.red())
                    await ctx.respond(embed=lwe_embed)
    @enable.error
    async def enable_error(self, ctx, error):
        ee_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=ee_embed)
        raise error
    @linkwarn.command(name='channel', description='Set the channel to recieve the warns')
    async def channelcmd(self, ctx, channel: Option(discord.TextChannel, 'The channel for receiving warns', required=True)):
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
                check = await db.run_query(f'select exists(select * from linkwarn where guild_id = {ctx.guild.id})')
                if check[0]['exists'] == True:
                    await db.run_query(f'update linkwarn set channel_id = {channel.id}')
                    lwc_embed = discord.Embed(description=f'Link warnings channel updated to {channel.mention}.', colour=discord.Colour.green())
                    await ctx.respond(embed=lwc_embed)
                else:
                   lwc_embed = discord.Embed(description='You need to configure the link warning feature first using `/linkwarn enable <channel>`', colour=discord.Colour.red())
                   await ctx.respond(embed=lwc_embed)
    @channelcmd.error
    async def channelcmd_error(self, ctx, error):
        cce_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=cce_embed)
        raise error
    @linkwarn.command(description='Disable the linkwarn system')
    async def disable(self, ctx):
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
                check = await db.run_query(f'select exists(select * from linkwarn where guild_id = {ctx.guild.id})')
                if check[0]['exists'] == True:
                    await db.run_query(f'delete from linkwarn where guild_id = {ctx.guild.id}')
                    lwd_embed = discord.Embed(description='Successfully disabled link warnings', colour=discord.Colour.green())
                    await ctx.respond(embed=lwd_embed)
                else:
                    lwd_embed = discord.Embed(description="Link warnings aren't activated on this server. You can activate them using `/linkwarn enable <channel>`", colour=discord.Colour.red())
                    await ctx.respond(embed=lwd_embed)
    @disable.error
    async def disable_error(self, ctx, error):
        de_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=de_embed)
        raise error
    
    @linkwarn.command(name='whitelist', description='Add or remove roles from the whitelist')
    async def lwwhitelist(self, ctx, action: Option(str, 'The action to perform with the role', choices=['add', 'remove'], required=True), role: Option(discord.Role, 'The role to add / remove', required=True)):
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
                if action == 'add':
                    check = await db.run_query(f'select exists(select * from linkwarn where guild_id = {ctx.guild.id})')
                    if check[0]['exists'] == True:
                        echeck = await db.run_query(f'select whitelist_roles from linkwarn where guild_id = {ctx.guild.id}')
                        rlist = echeck[0]['whitelist_roles']
                        if rlist == None:
                            await db.run_query('update linkwarn set whitelist_roles = whitelist_roles || '+"'{"+str(role.id)+"}'")
                            lwwembed = discord.Embed(description=f'Successfully added {role.mention} to the link warning whitelist', colour=discord.Colour.green())
                            await ctx.respond(embed=lwwembed)
                        elif role.id in rlist:
                            lwwembed = discord.Embed(description="Couldn't add the role because it's already added. Use `/linkwarn status` for more infos.", colour=discord.Colour.red())
                            await ctx.respond(embed=lwwembed)
                        else:
                            await db.run_query('update linkwarn set whitelist_roles = whitelist_roles || '+"'{"+str(role.id)+"}'")
                            lwwembed = discord.Embed(description=f'Successfully added {role.mention} to the link warning whitelist', colour=discord.Colour.green())
                            await ctx.respond(embed=lwwembed)
                    else:
                        lwwembed = discord.Embed(description="You need to configure the link warning feature first using `/linkwarn enable <channel>`", colour=discord.Colour.red())
                        await ctx.respond(embed=lwwembed)
                else:
                    check = await db.run_query(f'select exists(select * from linkwarn where guild_id = {ctx.guild.id})')
                    if check[0]['exists'] == True:
                        echeck = await db.run_query(f'select whitelist_roles from linkwarn where guild_id = {ctx.guild.id}')
                        rlist = echeck[0]['whitelist_roles']
                        if rlist == None:
                            lwwembed = discord.Embed(description="Couldn't remove the role because it's already removed. Use `/linkwarn status` for more infos.", colour=discord.Colour.red())
                            await ctx.respond(embed=lwwembed)
                        elif role.id in rlist:
                            await db.run_query(f"update linkwarn set whitelist_roles = array_remove(whitelist_roles, '{role.id}')")
                            lwwembed = discord.Embed(description=f'Successfully removed {role.mention} from the link warning whitelist.', colour=discord.Colour.green())
                            await ctx.respond(embed=lwwembed)
                        else:
                            lwwembed = discord.Embed(description="Couldn't remove the role because it's already removed. Use `/linkwarn status` for more infos.", colour=discord.Colour.red())
                            await ctx.respond(embed=lwwembed)
                    else:
                        lwwembed = discord.Embed(description="You need to configure the link warning feature first using `/linkwarn enable <channel>`", colour=discord.Colour.red())
                        await ctx.respond(embed=lwwembed)
    @lwwhitelist.error
    async def disable_error(self, ctx, error):
        lww_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=lww_embed)
        raise error

    @linkwarn.command(description='Add or remove a role to ping on warning')
    async def pingrole(self, ctx, action: Option(str, 'The action to perform with the role', choices=['add', 'remove'], required=True), role: Option(discord.Role, 'The role to add / remove', required=True)):
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
                if action == 'add':
                    check = await db.run_query(f'select exists(select * from linkwarn where guild_id = {ctx.guild.id})')
                    if check[0]['exists'] == True:
                        echeck = await db.run_query(f'select pingrole from linkwarn where guild_id = {ctx.guild.id}')
                        rlist = echeck[0]['pingrole']
                        if rlist == None:
                            await db.run_query('update linkwarn set pingrole = pingrole || '+"'{"+str(role.id)+"}'")
                            lwpembed = discord.Embed(description=f'Successfully added {role.mention} to the roles to ping on warning.', colour=discord.Colour.green())
                            await ctx.respond(embed=lwpembed)
                        elif role.id in rlist:
                            lwpembed = discord.Embed(description="Couldn't add the role because it's already added. Use `/linkwarn status` for more infos.", colour=discord.Colour.red())
                            await ctx.respond(embed=lwpembed)
                        else:
                            await db.run_query('update linkwarn set pingrole = pingrole || '+"'{"+str(role.id)+"}'")
                            lwpembed = discord.Embed(description=f'Successfully added {role.mention} to the roles to ping on warning.', colour=discord.Colour.green())
                            await ctx.respond(embed=lwpembed)
                    else:
                        lwpembed = discord.Embed(description="You need to configure the link warning feature first using `/linkwarn enable <channel>`", colour=discord.Colour.red())
                        await ctx.respond(embed=lwpembed)
                else:
                    check = await db.run_query(f'select exists(select * from linkwarn where guild_id = {ctx.guild.id})')
                    if check[0]['exists'] == True:
                        echeck = await db.run_query(f'select pingrole from linkwarn where guild_id = {ctx.guild.id}')
                        rlist = echeck[0]['pingrole']
                        if rlist == None:
                            lwpembed = discord.Embed(description="Couldn't remove the role because it's already removed. Use `/linkwarn status` for more infos.", colour=discord.Colour.red())
                            await ctx.respond(embed=lwpembed)
                        elif role.id in rlist:
                            await db.run_query(f"update linkwarn set pingrole = array_remove(pingrole, '{role.id}')")
                            lwpembed = discord.Embed(description=f'Successfully removed {role.mention} from the roles to ping on warning.', colour=discord.Colour.green())
                            await ctx.respond(embed=lwpembed)
                        else:
                            lwpembed = discord.Embed(description="Couldn't remove the role because it's already removed. Use `/linkwarn status` for more infos.", colour=discord.Colour.red())
                            await ctx.respond(embed=lwpembed)
                    else:
                        lwpembed = discord.Embed(description="You need to configure the link warning feature first using `/linkwarn enable <channel>`", colour=discord.Colour.red())
                        await ctx.respond(embed=lwpembed)
    @pingrole.error
    async def pingrole_error(self, ctx, error):
        lwp_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=lwp_embed)
        raise error
        
   
    @linkwarn.command(description='Get the current status of the linkwarn system')
    async def status(self, ctx):
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
                check = await db.run_query(f'select exists(select * from linkwarn where guild_id = {ctx.guild.id})')
                if check[0]['exists'] == True:
                    wrsrc = await db.run_query(f'select whitelist_roles from linkwarn where guild_id = {ctx.guild.id}')
                    prsrc = await db.run_query(f'select pingrole from linkwarn where guild_id = {ctx.guild.id}')
                    channel = await db.run_query(f'select channel_id from linkwarn where guild_id = {ctx.guild.id}')
                    if wrsrc[0]['whitelist_roles'] == None and prsrc[0]['pingrole'] == None:
                        lwsembed = discord.Embed(title=f'LinkWarnings status for {ctx.guild.name}', description=f"Status enabled: true\nChannel for warns: <#{channel[0]['channel_id']}>")
                        lwsembed.add_field(name='Whitelisted roles', value='none')
                        lwsembed.add_field(name='Roles to ping', value='none')
                        await ctx.respond(embed=lwsembed)
                    elif wrsrc[0]['whitelist_roles'] == [] and prsrc[0]['pingrole'] == None:
                        lwsembed = discord.Embed(title=f'LinkWarnings status for {ctx.guild.name}', description=f"Status enabled: true\nChannel for warns: <#{channel[0]['channel_id']}>")
                        lwsembed.add_field(name='Whitelisted roles', value='none')
                        lwsembed.add_field(name='Roles to ping', value='none')
                        await ctx.respond(embed=lwsembed)
                    elif wrsrc[0]['whitelist_roles'] == None and prsrc[0]['pingrole'] == []:
                        lwsembed = discord.Embed(title=f'LinkWarnings status for {ctx.guild.name}', description=f"Status enabled: true\nChannel for warns: <#{channel[0]['channel_id']}>")
                        lwsembed.add_field(name='Whitelisted roles', value='none')
                        lwsembed.add_field(name='Roles to ping', value='none')
                        await ctx.respond(embed=lwsembed)
                    elif wrsrc[0]['whitelist_roles'] == [] and prsrc[0]['pingrole'] == []:
                        lwsembed = discord.Embed(title=f'LinkWarnings status for {ctx.guild.name}', description=f"Status enabled: true\nChannel for warns: <#{channel[0]['channel_id']}>")
                        lwsembed.add_field(name='Whitelisted roles', value='none')
                        lwsembed.add_field(name='Roles to ping', value='none')
                        await ctx.respond(embed=lwsembed)
                    elif wrsrc[0]['whitelist_roles'] == None and len(prsrc[0]['pingrole']) > 0:
                        rlist2 = prsrc[0]['pingrole']
                        therlist2 = []
                        for ids in rlist2:
                            rid2 = discord.utils.get(ctx.guild.roles, id=ids)
                            therlist2.append(rid2)
                        bro2 = [roles.mention for roles in therlist2]
                        lwsembed = discord.Embed(title=f'LinkWarnings status for {ctx.guild.name}', description=f"Status enabled: true\nChannel for warns: <#{channel[0]['channel_id']}>")
                        lwsembed.add_field(name='Whitelisted roles', value='none')
                        lwsembed.add_field(name='Roles to ping', value='\n'.join(map(str, bro2)))
                        await ctx.respond(embed=lwsembed)
                    elif wrsrc[0]['whitelist_roles'] == [] and len(prsrc[0]['pingrole']) > 0:
                        rlist2 = prsrc[0]['pingrole']
                        therlist2 = []
                        for ids in rlist2:
                            rid2 = discord.utils.get(ctx.guild.roles, id=ids)
                            therlist2.append(rid2)
                        bro2 = [roles.mention for roles in therlist2]
                        lwsembed = discord.Embed(title=f'LinkWarnings status for {ctx.guild.name}', description=f"Status enabled: true\nChannel for warns: <#{channel[0]['channel_id']}>")
                        lwsembed.add_field(name='Whitelisted roles', value='none')
                        lwsembed.add_field(name='Roles to ping', value='\n'.join(map(str, bro2)))
                        await ctx.respond(embed=lwsembed)
                    elif len(wrsrc[0]['whitelist_roles']) > 0 and prsrc[0]['pingrole'] == None:
                        rlist = wrsrc[0]['whitelist_roles']
                        therlist = []
                        for ids in rlist:
                            rid = discord.utils.get(ctx.guild.roles, id=ids)
                            therlist.append(rid)
                        bro = [roles.mention for roles in therlist]
                        lwsembed = discord.Embed(title=f'LinkWarnings status for {ctx.guild.name}', description=f"Status enabled: true\nChannel for warns: <#{channel[0]['channel_id']}>")
                        lwsembed.add_field(name='Whitelisted roles', value='\n'.join(map(str, bro)))
                        lwsembed.add_field(name='Roles to ping', value='none')
                        await ctx.respond(embed=lwsembed)
                    elif len(wrsrc[0]['whitelist_roles']) > 0 and prsrc[0]['pingrole'] == []:
                        rlist = wrsrc[0]['whitelist_roles']
                        therlist = []
                        for ids in rlist:
                            rid = discord.utils.get(ctx.guild.roles, id=ids)
                            therlist.append(rid)
                        bro = [roles.mention for roles in therlist]
                        lwsembed = discord.Embed(title=f'LinkWarnings status for {ctx.guild.name}', description=f"Status enabled: true\nChannel for warns: <#{channel[0]['channel_id']}>")
                        lwsembed.add_field(name='Whitelisted roles', value='\n'.join(map(str, bro)))
                        lwsembed.add_field(name='Roles to ping', value='none')
                        await ctx.respond(embed=lwsembed)
                    
                    else:
                        rlist = wrsrc[0]['whitelist_roles']
                        therlist = []
                        for ids in rlist:
                            rid = discord.utils.get(ctx.guild.roles, id=ids)
                            therlist.append(rid)
                        bro = [roles.mention for roles in therlist]
                        rlist2 = prsrc[0]['pingrole']
                        therlist2 = []
                        for ids in rlist2:
                            rid2 = discord.utils.get(ctx.guild.roles, id=ids)
                            therlist2.append(rid2)
                        bro2 = [roles.mention for roles in therlist2]
                        lwsembed = discord.Embed(title=f'LinkWarnings status for {ctx.guild.name}', description=f"Status enabled: true\nChannel for warns: <#{channel[0]['channel_id']}>")
                        lwsembed.add_field(name='Whitelisted roles', value='\n'.join(map(str, bro)))
                        lwsembed.add_field(name='Roles to ping', value='\n'.join(map(str, bro2)))
                        await ctx.respond(embed=lwsembed)
                else:
                    lwsembed = discord.Embed(title=f'LinkWarnings status for {ctx.guild.name}', description=f"Status enabled: false\nChannel for warns: none")
                    await ctx.respond(embed=lwsembed)
    @status.error
    async def status_error(self, ctx, error):
        lwse_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=lwse_embed)
        raise error

    @commands.slash_command(description='Sets a voice channel as creator for tempchannels', guild_only=True)
    @discord.default_permissions(manage_channels=True)
    async def tempchannel(self, ctx, action: Option(str, choices=['set', 'override', 'reset'], required=True)):
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
                if action=='set':
                    if not ctx.author.voice:
                        tc_embed = discord.Embed(description='You need to be in a voice channel for this command.', colour=discord.Colour.red())
                        await ctx.respond(embed=tc_embed)
                    else:
                        check = await db.run_query(f'select exists(select * from tempchannel where guildid = {ctx.guild.id})')
                        if check[0]['exists'] == True:
                            tc_embed = discord.Embed(description="You've already set a channel for creating tempchannels. To override it, please use **/tempchannel override.**", colour=discord.Colour.red())
                            await ctx.respond(embed=tc_embed)
                        else:
                            await db.run_query(f'insert into tempchannel(guildid, vcid) values({ctx.guild.id}, {ctx.author.voice.channel.id})')
                            tc_embed = discord.Embed(description='Current VC configured as creator. Rejoin for testing :)', colour=discord.Colour.green())
                            await ctx.respond(embed=tc_embed)
                elif action == 'override':
                    if not ctx.author.voice:
                        tc_embed = discord.Embed(description='You need to be in a voice channel for this command.', colour=discord.Colour.red())
                        await ctx.respond(embed=tc_embed)
                    else:
                        if ctx.author.voice.channel.name == f'⌛ {ctx.author.display_name}':
                            tc_embed = discord.Embed(description="You're already in a tempchannel.", colour=discord.Colour.red())
                            await ctx.respond(embed=tc_embed)
                        else:
                            check = await db.run_query(f'select exists(select * from tempchannel where guildid = {ctx.guild.id})')
                            if check[0]['exists'] == True:
                                await db.run_query(f'update tempchannel set vcid = {ctx.author.voice.channel.id}')
                                tc_embed = discord.Embed(description='Current VC configured as creator. Rejoin for testing :)', colour=discord.Colour.green())
                                await ctx.respond(embed=tc_embed)
                            else:
                                tc_embed = discord.Embed(description='Tempchannel has not been setup in this server. To setup this feature, please use **/tempchannel set.**', colour=discord.Colour.red())
                                await ctx.respond(embed=tc_embed)
                else:
                    check = await db.run_query(f'select exists(select * from tempchannel where guildid = {ctx.guild.id})')
                    if check[0]['exists'] == True:
                        await db.run_query(f'delete from tempchannel where guildid = {ctx.guild.id}')
                        tc_embed = discord.Embed(description='The previously assigned voice channel has been reset to its normal functionality.', colour=discord.Colour.green())
                        await ctx.respond(embed=tc_embed)
                    else:
                        tc_embed = discord.Embed(description='The tempchannel feature is currently not configured.', colour=discord.Colour.red())
                        await ctx.respond(embed=tc_embed)
    @tempchannel.error
    async def tempchannel_error(self, ctx, error):
        tce_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=tce_embed)
        raise error

def setup(bot):
    bot.add_cog(Moderation(bot))
