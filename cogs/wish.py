import asyncio
from datetime import datetime

import discord
from discord.ext import commands
from discord.utils import get

WISHWALL_CHANNEL = 746220388866064474
WISHWALL_BOT_ID = 795749771289690152
WHITELIST_ROLES = {"The Boss / Admin", "Enforcers / Moderator", "Ringleaders / Officer", "Gigi Dev Team"}


class WishWall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='wish')
    async def commission(self, ctx, platform=None, *args):
        ps_emote = get(ctx.message.guild.emojis, name='ps4')
        xb_emote = get(ctx.message.guild.emojis, name='xbox')
        pc_emote = get(ctx.message.guild.emojis, name='pc')
        alias_list = {f'{ps_emote} Playstation': {'playstation', 'ps'},
                      f'{xb_emote} Xbox': {'xbox', 'xb'},
                      f'{pc_emote} PC': {'pc', 'steam'}}
        wish = ' '.join(args)
        if platform:
            for i in alias_list:
                if platform.lower() in alias_list[i]:
                    platform = i
                    break
                else:
                    platform = None
        if ctx.channel.id == WISHWALL_CHANNEL:
            if not platform:
                new_embed = discord.Embed(title="Error",
                                          description="*Please specify your platform.*\n"
                                                      "***w^wish __<platform>__ <wish>***",
                                          color=0xff0209)
            elif len(wish) == 0:
                new_embed = discord.Embed(title="Error",
                                          description="*Please include a full description of you wish.*\n"
                                                      "***w^wish <platform> __<wish>__***",
                                          color=0xff0209)
            else:
                if ctx.message.author.nick:
                    comm_author = str(ctx.message.author.nick)
                else:
                    comm_author = str(ctx.message.author)[:-5]
                new_embed = discord.Embed(title="__***{}***__ *has made a new wish!*".format(comm_author),
                                          description="{}".format(wish),
                                          color=0xff0209)
                new_embed.set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/767568459939708950/800966534956318720/destiny_icon_grey.png")
                new_embed.add_field(name="**Platform:**",
                                    value=platform,
                                    inline=True)
                new_embed.add_field(name="**Accepted by:**",
                                    value="N/A",
                                    inline=True)
                new_embed.set_footer(text="Created by: {}".format(ctx.message.author))
                new_embed.timestamp = datetime.utcnow()
            await ctx.channel.send(embed=new_embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        user = await self.bot.fetch_user(message.author.id)
        if message.channel.id == WISHWALL_CHANNEL:
            if user.bot and user.id == WISHWALL_BOT_ID:
                try:
                    if 'Error' in str(message.embeds[0].title):
                        await asyncio.sleep(3)
                        await discord.Message.delete(message)
                    else:
                        reactions = ['\U00002705', '\U0000274E']
                        for emoji in reactions:
                            await discord.Message.add_reaction(message, emoji)
                except Exception:
                    pass
            elif str(message.content[:6]) == 'w^wish':
                await discord.Message.delete(message)
        elif message.channel.id == WISHWALL_CHANNEL:
            await discord.Message.delete(message)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = await self.bot.fetch_channel(payload.channel_id)
        member = channel.guild.get_member(payload.user_id)
        message = await channel.fetch_message(payload.message_id)
        try:
            old_embed = message.embeds[0]
        except IndexError:
            old_embed = discord.Embed()
        if old_embed.footer:
            comm_owner = old_embed.footer.text[12:]
        if channel.id == WISHWALL_CHANNEL and not member.bot:
            if payload.emoji.name == '✅':
                if not (member.name + '#' + member.discriminator) == comm_owner:
                    for i, field in enumerate(old_embed.fields):
                        new_embed = discord.Embed(title=old_embed.title,
                                                  description=old_embed.description,
                                                  color=old_embed.color,
                                                  timestamp=old_embed.timestamp)
                        new_embed.set_thumbnail(
                            url="https://cdn.discordapp.com/attachments/767568459939708950/800966534956318720/destiny_icon_grey.png")
                        new_embed.set_footer(text=old_embed.footer.text)
                        for react in message.reactions:
                            async for user in react.users():
                                if react.emoji == '✅' and not user.bot:
                                    if field.value == 'N/A':
                                        field.value = str(user.mention) + '\n'
                                    elif user.mention not in field.value:
                                        field.value = field.value + '\n' + str(user.mention)
                                    else:
                                        new_embed = discord.Embed(title="Error",
                                                                  description="*You already accepted this wish.*",
                                                                  color=0xff0209)
                                        await channel.send(embed=new_embed)
                        new_embed.add_field(name=field.name,
                                            value=field.value,
                                            inline=True)
                    await message.edit(embed=new_embed)
                else:
                    new_embed = discord.Embed(title="Error",
                                              description="*You cannot grant your own wish.*",
                                              color=0xff0209)
                    await channel.send(embed=new_embed)
            elif payload.emoji.name == '❎':
                if str(member.name) == comm_owner:
                    await discord.Message.delete(message)
                else:
                    for w_role in WHITELIST_ROLES:
                        role = discord.utils.find(lambda r: r.name == w_role, channel.guild.roles)
                        if role in member.roles:
                            await discord.Message.delete(message)
                            return
                    for i, field in enumerate(old_embed.fields):
                        new_embed = discord.Embed(title=old_embed.title,
                                                  description=old_embed.description,
                                                  color=old_embed.color,
                                                  timestamp=old_embed.timestamp)
                        field.value = field.value.replace(str(member.mention), '')
                        try:
                            field.value = field.value.replace('\n\n', '\n')
                        finally:
                            if field.value == '':
                                field.value = 'N/A'
                            new_embed.add_field(name=field.name,
                                                value=field.value,
                                                inline=True)
                            # new_embed.set_thumbnail(
                            #     url="https://cdn.discordapp.com/attachments/532380077896237061/786762838789849139/Cid_ARR.jpg")
                            new_embed.set_footer(text=old_embed.footer.text)
                            await message.edit(embed=new_embed)
        try:
            for react in message.reactions:
                async for user in react.users():
                    if not user.bot:
                        await react.remove(user)
        finally:
            return


def setup(bot):
    bot.add_cog(WishWall(bot))
