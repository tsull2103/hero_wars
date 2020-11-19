from discord.utils import get
from discord.ext import commands
from googletrans import Translator
import discord
import re

client = discord.Client()
translator = Translator()
flag_dict = {
    "🇰🇷": "ko"}

@client.event
async def on_reaction_add(reaction, user):

    if (reaction.emoji == "🇰🇷"):
        result = translator.translate(reaction.message.content, dest='ko')
        orig_message = reaction.message.content + "\n" + "-------------------" + "\n"
        with_user = result.text
        with_user = with_user.replace("<@! ", "<@!")
        await reaction.message.channel.send(orig_message + with_user)
    elif reaction.emoji == "🇨🇦" or reaction.emoji == "🇺🇸" or reaction.emoji == "🇬🇧":
        result = translator.translate(reaction.message.content, dest='en')
        orig_message = reaction.message.content + "\n" + "------------------->" + "\n"
        with_user = result.text
        with_user = with_user.replace("<@! ", "<@!")
        await reaction.message.channel.send(orig_message + with_user)


client.run('Nzc5MDA4NTkxNDY1OTM5MDI0.X7aSSQ.z9Y4zEmbiwBqpOJaVLYyGjgXEDw')