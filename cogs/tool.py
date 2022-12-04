import discord
from discord.ext import commands
from utils import db

class Tool(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Fun Cog has been connected successfully!')
    
    @commands.slash_command(description='Allows to calculate the shard of a server', guild_only=True)
    async def shardcalc(self, ctx, serverid: discord.Option(str, 'The ID of the server', required=True), shardcount: discord.Option(int, 'The total amount of Shards', required=True)):
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
                if serverid.isdigit() == False:
                    sc_embed = discord.Embed(description='Please provide a valid server ID', colour=discord.Colour.red())
                    await ctx.respond(embed=sc_embed)
                else:
                    server_id = int(serverid)
                    shard_id = (server_id >> 22) % shardcount
                    sc_embed = discord.Embed(description=f'The server would be in the shard with ID `{shard_id}`.\nThat would be shard `{shard_id + 1}/{shardcount}`', colour=discord.Colour.dark_blue())
                    await ctx.respond(embed=sc_embed)
    @shardcalc.error
    async def shardcalc_error(self, ctx, error):
        sc_embed = discord.Embed(description='Something went wrong from the backend, you can either contact the [developer](https://t.me/nostorian) directly or open an issue in the [official repo](https://github.com/Nostorian/Polus-Discord-Bot).', colour=discord.Colour.red())
        await ctx.respond(embed=sc_embed)
        raise error

def setup(bot):
    bot.add_cog(Tool(bot))