import os
import psycopg2
import discord
import logging
from discord.ext import commands
from database.database import Postgres

# ==============================================================================
# ==============================================================================

def get_prefix(bot, message):
    default_prefix = 'wp;'

    if not message.guild:
        return commands.when_mentioned_or(*default_prefix)(bot, message)

    with Postgres() as db:
        prefix = db.query('SELECT prefix FROM prefixes WHERE guild_id = %s', (message.guild.id,))

        if prefix:
            return commands.when_mentioned_or(str(*prefix[0]))(bot, message)
    return commands.when_mentioned_or(*default_prefix)(bot, message)

# ==============================================================================

initial_cogs = ['cogs.ironworks']

# ==============================================================================

bot = commands.Bot(command_prefix=get_prefix, description='Wolf's Child')


@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f':ping_pong:⠀⠀**Pong!**⠀{round(bot.latency, 3)}ms')

@bot.command(name='server')
async def server(ctx):
    await ctx.send("This command isn't ready yet!")

@bot.command(name='credits')
async def credits(ctx):
    embed = discord.Embed(title='Development Credits', description='...', colour=0xffff33)
    embed.set_thumbnail(url=bot.user.avatar_url)
    await ctx.send(content=None, embed=embed)
                   
@bot.group(name='prefix', pass_context=True)
async def prefix(ctx):
    # check that we're not in a subcommand
    if ctx.invoked_subcommand is None:
        await ctx.send(f'Current prefix set to: `{get_prefix(bot, ctx.message)[2]}`')

@prefix.command(name='set', no_pm=True, hidden=True, pass_context=True, aliases=['change'])
                   
@commands.has_guild_permissions(administrator=True)
                   
# ==============================================================================
                   
async def set(ctx, new_prefix):
    # instantiate database
    with Postgres() as db:
        # check if there's already an entry for this guild
        entry_exists = db.query('SELECT prefix FROM prefixes WHERE guild_id = %s', (ctx.guild.id,))

        # if there is, then update the entry
        if entry_exists:
            db.execute('UPDATE prefixes SET prefix=%s WHERE guild_id = %s', (new_prefix, ctx.guild.id))
        # else create a new entry for this guild
        else:
            db.execute('INSERT INTO prefixes VALUES (%s, %s)', (ctx.guild.id, new_prefix))

        # check to see if we successfully wrote to the database by checking if a row was modified
        if db.cursor.rowcount == 1:
            await ctx.send(f':white_check_mark:⠀⠀**Success!**⠀my prefix is now `{new_prefix}`')
        # else something went wrong
        else:
            await ctx.send('<:wrong:742105251271802910>⠀⠀**Error!!**⠀my prefix couldn\'t be changed because of something Kaito did...')
                   
# ==============================================================================

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_cogs:
        bot.load_extension(extension)

    with Postgres() as db:
        db.create_tables()


@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    print(f'Successfully logged in and booted...!')


bot.run(os.environ.get("TOKEN"), bot=True, reconnect=True)
