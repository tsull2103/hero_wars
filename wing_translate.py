from discord.utils import get
from discord.ext import commands
from googletrans import Translator
import discord
import re
import pandas as pd

client = discord.Client()
translator = Translator()
flag_dict = {
    "🇰🇷": "ko"}

token_file_path = "C:/discord/token.txt"
token_file_df = pd.read_csv(token_file_path, sep=",", index_col=None, header=0)
keys = token_file_df['bot']
values = token_file_df['token']
token_file_dict = dict(zip(keys, values))
token = token_file_dict.get('wing_translate')

@client.event
async def on_reaction_add(reaction, user):

    if (reaction.emoji == "🇰🇷"):
        result = translator.translate(reaction.message.content, dest='ko')
        orig_message = reaction.message.content + "\n" + "------------------->" + "\n"
        with_user = result.text
        with_user = with_user.replace("<@! ", "<@!")
        await reaction.message.channel.send(orig_message + with_user)
    elif reaction.emoji == "🇨🇦" or reaction.emoji == "🇺🇸" or reaction.emoji == "🇬🇧":
        result = translator.translate(reaction.message.content, dest='en')
        orig_message = reaction.message.content + "\n" + "------------------->" + "\n"
        with_user = result.text
        with_user = with_user.replace("<@! ", "<@!")
        await reaction.message.channel.send(orig_message + with_user)


client.run(token)