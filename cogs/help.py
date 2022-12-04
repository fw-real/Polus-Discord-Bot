import discord
from utils import db
from discord import Option, Embed
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Help Cog has been connected successfully!")
    
    @commands.slash_command(description='Returns the help menu', guild_only=True)
    async def help(self, ctx, command: Option(str, 'A command you want to get more informations on', required=False)):
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
                if command:
                    await ctx.respond('this part is under work')
                else:
                    help_embed = Embed(title='Slash commands')
                    help_embed.add_field(name='Moderation', value='`ban`, `inviteblocker`, `kick`, `linkwarn`, `nuke`, `purge`, `tempchannel`')
                    help_embed.add_field(name='Fun', value='`dice`, `dontasktoask`, `flipacoin`, `infinitydice`, `nitrogen`, `nohello`, `tryitandsee`', inline=False)
                    help_embed.add_field(name='Tool', value='`shardcalc`', inline=False)
                    help_embed.add_field(name='Misc', value='`about`, `help`, `invite`, `license`, `links`, `ping`, `premium`, `support`', inline=False)
                    await ctx.respond(embed=help_embed)
    @help.error
    async def help_error(self, ctx, error):
        he_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=he_embed)
        raise error
        
def setup(bot):
    bot.add_cog(Help(bot))