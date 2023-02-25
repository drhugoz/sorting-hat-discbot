from random import choice

import discord

from settings import token, HOUSES, HAT_CHANNEL
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)


@bot.command()
async def rehouse(ctx: discord.ext.commands.Context):
    author = ctx.author
    guild: discord.Guild = ctx.guild
    old_role = discord.utils.find(lambda r: r.id in HOUSES, author.roles)
    houses = HOUSES
    if old_role:
        houses.remove(old_role.id)
        await author.remove_roles(old_role)
    new_role: discord.Role = discord.utils.get(guild.roles, id=choice(houses))
    await author.add_roles(new_role)
    info_ch = guild.get_channel(HAT_CHANNEL)
    await info_ch.send(f"{author.mention}, тебя переопределило в {new_role.mention}!!!")


@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    guild: discord.Guild = member.guild
    if before.channel is None and after.channel is not None:
        house_role = discord.utils.find(lambda r: r.id in HOUSES, member.roles)
        if not house_role:
            house_role: discord.Role = discord.utils.get(guild.roles, id=choice(HOUSES))
            await member.add_roles(house_role)
            info_ch = guild.get_channel(HAT_CHANNEL)
            await info_ch.send(f"{member.mention}, тебя определило в {house_role.mention}!!!")


bot.run(token)


