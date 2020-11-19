from discord.utils import get
from discord.ext import commands
from googletrans import Translator
import discord
import re
import pandas as pd

client = discord.Client()

flag_dict = {
    "🇰🇷": "ko"}

token_file_path = "C:/discord/token.txt"
token_file_df = pd.read_csv(token_file_path, sep=",", index_col=None, header=0)
keys = token_file_df['bot']
values = token_file_df['token']
token_file_dict = dict(zip(keys, values))
token = token_file_dict.get('wing_translate')

max_try = 10

# @client.event
# async def on_reaction_add(reaction, user):
#     print(reaction)
#     translator = Translator()
#     if (reaction.emoji == "🇰🇷"):
#         result = translator.translate(reaction.message.content, dest='ko')
#         orig_message = reaction.message.content + "\n" + "------------------->" + "\n"
#         with_user = result.text
#         with_user = with_user.replace("<@! ", "<@!")
#         await reaction.message.channel.send(orig_message + with_user)
#     elif reaction.emoji == "🇨🇦" or reaction.emoji == "🇺🇸" or reaction.emoji == "🇬🇧":
#         result = translator.translate(reaction.message.content, dest='en')
#         orig_message = reaction.message.content + "\n" + "------------------->" + "\n"
#         with_user = result.text
#         with_user = with_user.replace("<@! ", "<@!")
#         await reaction.message.channel.send(orig_message + with_user)

@client.event
async def on_raw_reaction_add(payload):
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if (payload.emoji.name == "🇰🇷"):
        print("KR")
        for curr_try in range(max_try):
            try:
                translator = Translator()
                result = translator.translate(message.content, dest='ko')
                break
            except Exception as e:
                print('Exception, Retry : ' + str(curr_try))
                if curr_try == max_try - 1:
                    return 1
                continue

        orig_message = message.content + "\n" + "------------------->" + "\n"
        with_user = result.text
        with_user = with_user.replace("<@! ", "<@!")
        await message.channel.send(orig_message + with_user)
    elif payload.emoji.name == "🇨🇦" or payload.emoji.name == "🇺🇸" or payload.emoji.name == "🇬🇧":
        print("EN")
        for curr_try in range(max_try):
            try:
                translator = Translator()
                result = translator.translate(message.content, dest='en')
                break
            except Exception as e:
                print('Exception, Retry : ' + str(curr_try))
                if curr_try == max_try - 1:
                    return 1
                continue
        orig_message = message.content + "\n" + "------------------->" + "\n"
        with_user = result.text
        with_user = with_user.replace("<@! ", "<@!")
        await message.channel.send(orig_message + with_user)

client.run(token)