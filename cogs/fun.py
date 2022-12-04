import random
import discord
from utils import db
from discord.ui import View, Button
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Fun Cog has been connected successfully!')
        
    @commands.slash_command(description='Rolls a virtual dice', guild_only=True)
    async def dice(self, ctx):
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
                dice_probability = random.choice([1, 2, 3, 4, 5, 6])
                if dice_probability == 1:
                    one_embed = discord.Embed(title="It's a 1")
                    one_embed.set_thumbnail(url='https://i.imgur.com/xMhv4JA.png')
                    await ctx.respond(embed=one_embed)
                elif dice_probability == 2:
                    two_embed = discord.Embed(title="It's a 2")
                    two_embed.set_thumbnail(url='https://i.imgur.com/gwNy90E.png')
                    await ctx.respond(embed=two_embed)
                elif dice_probability == 3:
                    three_embed = discord.Embed(title="It's a 3")
                    three_embed.set_thumbnail(url='https://i.imgur.com/9eMCmkn.png')
                    await ctx.respond(embed=three_embed)
                elif dice_probability == 4:
                    four_embed = discord.Embed(title="It's a 4")
                    four_embed.set_thumbnail(url='https://i.imgur.com/i8sPLxY.png')
                    await ctx.respond(embed=four_embed)
                elif dice_probability == 5:
                    five_embed = discord.Embed(title="It's a 5")
                    five_embed.set_thumbnail(url='https://i.imgur.com/OgZBCvq.png')
                    await ctx.respond(embed=five_embed)
                elif dice_probability == 6:
                    six_embed = discord.Embed(title="It's a 6")
                    six_embed.set_thumbnail(url='https://i.imgur.com/S5wN14e.png')
                    await ctx.respond(embed=six_embed)
    @dice.error
    async def dice_error(self, ctx, error):
        de_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=de_embed)
        raise error

    @commands.slash_command(description='Rolls a virtual dice with configurable amount of sides', guild_only=True)
    async def infinitydice(self, ctx, sides: discord.Option(int, 'Amount of sides', required=True)):
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
                if sides > 1000000:
                    id_embed = discord.Embed(title='Please use a smaller number', colour=discord.Colour.red())
                    await ctx.respond(embed=id_embed)
                else:
                    dice_probability = random.randint(0, sides)
                    id_embed = discord.Embed(title=f"It's a {dice_probability}")
                    await ctx.respond(embed=id_embed)
    @infinitydice.error
    async def infinitydice_error(self, ctx, error):
        ide_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=ide_embed)
        raise error
    
    @commands.slash_command(description='Advices to not ask to ask but to ask instead', guild_only=True)
    async def dontasktoask(self, ctx, user: discord.Option(discord.Member, 'The user to ping', required=False)):
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
                if user:
                    await ctx.respond(f'{user.mention} https://dontasktoask.com/')
                else:
                    await ctx.respond('https://dontasktoask.com/')
    @dontasktoask.error
    async def dontasktoask_error(self, ctx, error):
        datae_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=datae_embed)
        raise error
        
    @commands.slash_command(description='Advices to not just say hello', guild_only=True)
    async def nohello(self, ctx, user: discord.Option(discord.Member, 'The user to ping', required=False)):
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
                if user:
                    await ctx.respond(f'{user.mention} https://nohello.net/')
                else:
                    await ctx.respond('https://nohello.net/')
    @nohello.error
    async def nohello_error(self, ctx, error):
        nhe_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=nhe_embed)
        raise error

    @commands.slash_command(description='Advices to try and see', guild_only=True)
    async def tryitandsee(self, ctx, user: discord.Option(discord.Member, 'The user to ping', required=False)):
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
                if user:
                    await ctx.respond(f'{user.mention} https://tryitands.ee/')
                else:
                    await ctx.respond('https://tryitands.ee/')
    @tryitandsee.error
    async def tryitandsee_error(self, ctx, error):
        tiase_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=tiase_embed)
        raise error
    
    @commands.slash_command(description='A simple coin flip', guild_only=True)
    async def flipacoin(self, ctx):
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
                coin_probability = random.choice(['heads', 'tails'])
                if coin_probability == 'heads':
                    ch_embed = discord.Embed(title='Heads')
                    ch_embed.set_thumbnail(url='https://i.imgur.com/JbmyE5U.png')
                    await ctx.respond(embed=ch_embed)
                elif coin_probability == 'tails':
                    ct_embed = discord.Embed(title='Tails')
                    ct_embed.set_thumbnail(url='https://i.imgur.com/PcWrtdl.png')
                    await ctx.respond(embed=ct_embed)
    @flipacoin.error
    async def flipacoin_error(self, ctx, error):
        face_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=face_embed)
        raise error
        
    @commands.slash_command(description='Generates discord nitro', guild_only=True)
    async def nitrogen(self, ctx):
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
                class NitroView(View):
                    async def on_timeout(self):
                        expire_button = Button(label='Claim', style=discord.ButtonStyle.gray, disabled=True)
                        view.add_item(expire_button)
                        view.remove_item(accept_button)
                        nitroexpire_embed = discord.Embed(title="You've been gifted a subscription!", description='Hmm, it seems someone already claimed this gift.')
                        nitroexpire_embed.set_thumbnail(url='https://i.imgur.com/wI9q2Md.png')
                        await bro.edit(view=self, embed=nitroexpire_embed)
                accept_button = Button(label='Claim', style=discord.ButtonStyle.green)
                async def accept_callback(interaction):
                    await interaction.response.send_message('https://tenor.com/bItJt.gif', ephemeral=True)
                nitro_embed = discord.Embed(title="You've been gifted a subscription!", description=f'{ctx.author} gifted you nitro for **1 month!**')
                nitro_embed.set_thumbnail(url='https://i.imgur.com/wI9q2Md.png')
                accept_button.callback = accept_callback
                view = NitroView(timeout=120)
                view.add_item(accept_button)
                bro = await ctx.respond(view=view, embed=nitro_embed)
                
    @nitrogen.error
    async def nitrogen_error(self, ctx, error):
        nge_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=nge_embed)
        raise error
def setup(bot):
    bot.add_cog(Fun(bot))