import discord
from datetime import datetime
import pytz
from datetime import timedelta
import time
import asyncio
import pandas as pd
import os

client = discord.Client()
guild_path = "C:/discord/guild.txt"
guild_champ_path = "C:/discord/guild_champs.txt"
guild_b_map_path = "C:/discord/guild_b_map.txt"
guild_a_champ_assignment_path = "C:/discord/guild_a_assignment.txt"
guild_a_champ_recommend_path = "C:/discord/guild_a_champ_recommend.txt"

channel_id = 774112256924975137

token_file_path = "C:/discord/token.txt"
token_file_df = pd.read_csv(token_file_path, sep=",", index_col=None, header=0)
keys = token_file_df['bot']
values = token_file_df['token']
token_file_dict = dict(zip(keys, values))
token = token_file_dict.get('war_planner')

@client.event
async def on_message(message):
    author_username = message.author.name
    author_user_id = str(message.author.id)
    message.content = ' '.join(message.content.split())
    if message.content.startswith("+help"):
        await message.channel.send('+show plan <your guild name(m)> <opponent guild name(m)>')
        await message.channel.send('+show guild')
        await message.channel.send('+show champ <guild name(m)>')
        await message.channel.send('+show map name')
        await message.channel.send('+show map <opponent guild name(m)>')
        await message.channel.send('+add guild <guild name(m)> <server(o)> <note(o)>')
        await message.channel.send('+remove guild <guild name(m)>')
        await message.channel.send('+add champ <guild name(m)> <champ(m)> <hero_team(o)> <hero_power(o)> <titan_power(o)> <note(o)>')
        await message.channel.send('+remove champ <guild name(m)> <champ(m)>')
        await message.channel.send('+add map <opponent guild name(m)> <opponent champ(m)> <building(m)> <position(m)>')
        await message.channel.send('+remove map <opponent guild name(m)> <opponent champ(m)>')
        await message.channel.send('+add assignment <your guild name(m)> <champ(m)> <opponent guild name(m)> <opponent champ(m)> <note(o)> "first attack / cleanup(o)"')
        await message.channel.send('+remove assignment <your guild name(m)> <champ(m)>')
        await message.channel.send('+add recommend')
        await message.channel.send('+remove recommend')

    elif message.content.startswith("+add guild"):
        is_command_valid = validate_command(message.content, "addguild")
        if "Error" in is_command_valid:
            await message.channel.send(is_command_valid)
            return 1
        else:
            message_tokenized = message.content.split(' ', 4)
            guild_name = str(message_tokenized[2])
            server = str(message_tokenized[3])
            note = str(message_tokenized[4])
            remove_from_file(guild_name, guild_path)
            add_to_file(','.join([guild_name, server, note]), guild_path)

    elif message.content.startswith("+remove guild"):
        await message.channel.send('currently not supported yet')
    elif message.content.startswith("+add champ"):
        is_command_valid = validate_command(message.content, "addchamp")
        if "Error" in is_command_valid:
            await message.channel.send(is_command_valid)
            return 1
        else:
            message_tokenized = message.content.split(' ', 7)
            guild_name = str(message_tokenized[2])
            champ = str(message_tokenized[3])
            hero_team = str(message_tokenized[4])
            hero_power = str(message_tokenized[5])
            titan_power = str(message_tokenized[6])
            note = str(message_tokenized[7])
            remove_from_file(','.join([guild_name, champ]), guild_champ_path)
            add_to_file(','.join([guild_name, champ, hero_team, hero_power, titan_power, note]), guild_champ_path)
    elif message.content.startswith("+remove champ"):
        await message.channel.send('currently not supported yet')
    elif message.content.startswith("+add map"):
        # add map <opponent guild name(m)> <opponent champ(m)> <building(m)> <position(m)>
        is_command_valid = validate_command(message.content, "addmap")
        if "Error" in is_command_valid:
            await message.channel.send(is_command_valid)
            return 1
        else:
            message_tokenized = message.content.split(' ', 5)
            guild_name = str(message_tokenized[2])
            opponent_champ = str(message_tokenized[3])
            building = str(message_tokenized[4])
            position = str(message_tokenized[5])
            remove_from_file(','.join([guild_name, champ]), guild_champ_path)
            add_to_file(','.join([guild_name, opponent_champ, building, position]), guild_champ_path)
    elif message.content.startswith("+remove map"):
        return 1
    elif message.content.startswith("+add assignment"):
        return 1
    elif message.content.startswith("+remove assignment"):
        return 1
    elif message.content.startswith("+add recommend"):
        return 1
    elif message.content.startswith("+remove recommend"):
        return 1

def is_valid_user(userid):
    curr_user = client.get_user(int(userid))
    return not curr_user is None

def is_valid_guild(guild_name):
    guild_name_df = pd.read_csv(guild_path, sep=",", dtype=str)
    guild_list = guild_name_df['guild'].unique()
    if guild_name not in guild_list:
        return "Error: guild name does not exist. Current guild name created : " + ', '.join(guild_list).upper()
    else:
        return "Pass"

def is_valid_champ(guild_name, champ_name):
    #Assume guild_name is validated
    guild_champ_df = pd.read_csv(guild_champ_path, sep=",", dtype=str)
    curr_guild_champ_df = guild_champ_df[guild_champ_df['guild'] == guild_name]
    curr_guild_champ_list = curr_guild_champ_df['champ'].unique()
    if champ_name not in curr_guild_champ_list:
        return "Error: champ does not exist. Current guild champ created : " + ', '.join(curr_guild_champ_list).upper()
    else:
        return "Pass"

def is_valid_building(building, position):
    building_list = ['BRIDGE', 'MAGE', 'BARRACK', 'LH', 'FOUNDRY', 'BOF', 'BOI', 'GON', 'CITADEL', 'SPRING']
    position_dict = {'BRIDGE': [1, 2, 3, 4],
                    'MAGE': [1, 2, 3],
                     'BARRACK': [1, 2, 3],
                     'LH': [1, 2, 3],
                     'FOUNDRY': [1, 2, 3, 4],
                     'BOF': [1, 2, 3, 4],
                     'BOI': [1, 2, 3, 4],
                     'GON': [1, 2, 3, 4],
                     'CITADEL': [1, 2, 3, 4, 5, 6, 7],
                     'SPRING': [1, 2, 3, 4]
         }
    if building not in building_list:
        return 'Error: building must be in one of the following : ' + ', '.join(building_list).upper()
    else:
        building_pos_list = position_dict[building.lower()]
        if position not in building_pos_list:
            return 'Error: ' + building + ' position must be one of the following : ' + ', '.join([str(elem) for elem in building_pos_list])
        else:
            return "Pass"

def add_guild(guild_name):
    remove_from_file(guild_name)
    return 1

def remove_from_file(remove_string, file_path):
    old_file = open(file_path, "r")
    lines = old_file.readlines()
    old_file.close()
    new_file = open(file_path, "w")
    for line in lines:
        if not str(remove_string) in line.strip("\n"):
            new_file.write(line)
    new_file.close()

def add_to_file(add_string, file_path):
    f = open(file_path, "a", encoding="utf-8")
    f.write(add_string + "\n")
    f.close()



def to_int_userid(userid):
    return int(userid.replace("<","").replace(">","").replace("@","").replace("!",""))

def message_string_userid(userid):
    return "<@!" + str(userid) + ">"

def validate_command(command, command_type):
    if command_type == "add":
        count = command.count(' ')
        if count != 2:
            return "Error: must have 2 spaces. However " + str(count) + " are found"
        else:
            message_tokenized = command.split(' ', 2)
            timezone = message_tokenized[2].upper()
            if timezone in timezone_list:
                return "Good"
            else:
                return "Error: Timezone must be in the format of GMT<+/-><hours>. Use GMT is you are GMT+/-0 Example: GMT+3, GMT"
    else:
        count = command.count(' ')
        if count != 1:
            return "Error: must have 1 space. However " + str(count) + " are found"
        else:
            return "Goo"

client.run(token)