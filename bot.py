import discord
from discord.ext import commands


def get_prefix(bot, message):
    prefixes = ['w^']
    if not message.guild:
        return 'w^'
    return commands.when_mentioned_or(*prefixes)(bot, message)


initial_cogs = ['util', 'cogs.ironworks']
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=get_prefix, description='Wolf\'s Child', intents=intents)
if __name__ == '__main__':
    for extension in initial_cogs:
        print('Loading '+str(extension))
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    print(f'Successfully logged in and booted...!')


token = open("token.txt", "r").readline()
bot.run(token, bot=True, reconnect=True)
