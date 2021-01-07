from discord.ext import commands


class UtilCog(commands.Cog, name='util'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', hidden=True)
    @commands.is_owner()
    async def ping(self, ctx):
        await ctx.send(f'Pong')

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'Failed to load module: {type(e).__name__} - {e}')
        else:
            await ctx.send(f'Successfully loaded module')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'Failed to load module: {type(e).__name__} - {e}')
        else:
            await ctx.send(f'Successfully loaded module')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'Failed to load module: {type(e).__name__} - {e}')
        else:
            await ctx.send(f'Successfully loaded module')


def setup(bot):
    bot.add_cog(UtilCog(bot))

