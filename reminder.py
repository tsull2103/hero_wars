import discord
from datetime import datetime
import pytz
from datetime import timedelta
import time
import asyncio
import pandas as pd
import os

client = discord.Client()
reminder_file_path = "C:/discord/reward_time.txt"

timezone_dict = {
    "GMT": "Etc/GMT",
    "GMT-1": "Etc/GMT+1",
    "GMT-10": "Etc/GMT+10",
    "GMT-11": "Etc/GMT+11",
    "GMT-12": "Etc/GMT+12",
    "GMT-2": "Etc/GMT+2",
    "GMT-3": "Etc/GMT+3",
    "GMT-4": "Etc/GMT+4",
    "GMT-5": "Etc/GMT+5",
    "GMT-6": "Etc/GMT+6",
    "GMT-7": "Etc/GMT+7",
    "GMT-8": "Etc/GMT+8",
    "GMT-9": "Etc/GMT+9",
    "GMT+1": "Etc/GMT-1",
    "GMT+10": "Etc/GMT-10",
    "GMT+11": "Etc/GMT-11",
    "GMT+12": "Etc/GMT-12",
    "GMT+13": "Etc/GMT-13",
    "GMT+14": "Etc/GMT-14",
    "GMT+2": "Etc/GMT-2",
    "GMT+3": "Etc/GMT-3",
    "GMT+4": "Etc/GMT-4",
    "GMT+5": "Etc/GMT-5",
    "GMT+6": "Etc/GMT-6",
    "GMT+7": "Etc/GMT-7",
    "GMT+8": "Etc/GMT-8",
    "GMT+9": "Etc/GMT-9"
}

time_zone_gmt_dict = dict((timezone_dict[k], k) for k in timezone_dict)

timezone_ran_today_dict = {}

timezone_list = [
    "GMT","GMT-1","GMT-10",
    "GMT-11","GMT-12","GMT-2","GMT-3","GMT-4",
    "GMT-5","GMT-6","GMT-7","GMT-8","GMT-9",
    "GMT+1","GMT+10","GMT+11","GMT+12","GMT+13",
    "GMT+14","GMT+2","GMT+3","GMT+4","GMT+5",
    "GMT+6","GMT+7","GMT+8","GMT+9"
]


channel_id = 775078801633050644

next_reminder = "No champs got reward in next reward time"

async def my_background_task():
    await client.wait_until_ready()
    timezone_ran_today_dict = timezone_dict.copy()
    for curr_tz in timezone_ran_today_dict:
        timezone_ran_today_dict[curr_tz] = "N"
    channel = client.get_channel(channel_id)
    while not client.is_closed():
        if os.path.getsize(reminder_file_path) > 0:
            reward_df = pd.read_csv(reminder_file_path, sep=",", header=None, dtype=str)
            reward_df.columns = ['username','userid', 'timezone_gmt', 'timezone_pytz']
            for curr_timezone_pytz in reward_df['timezone_pytz'].unique():
                current_timezone_time = datetime.now(pytz.timezone(curr_timezone_pytz))
                today8pm = current_timezone_time.replace(hour=20, minute=00, second=0, microsecond=0)
                today7pm = current_timezone_time.replace(hour=19, minute=00, second=0, microsecond=0)
                curr_gmt_timezone = time_zone_gmt_dict[curr_timezone_pytz]

                if current_timezone_time >= today7pm and current_timezone_time <= today8pm and timezone_ran_today_dict[curr_gmt_timezone] == "N":
                    timezone_ran_today_dict[curr_gmt_timezone] = "Y"
                    curr_reward_df = reward_df[reward_df['timezone_pytz'] == curr_timezone_pytz]

                    await channel.send("Reminder reward for timezone : " + curr_gmt_timezone)
                    await channel.send("Please do not attack the following Soul members in the next 1 hour:")
                    await channel.send(curr_reward_df['userid'].apply(message_string_userid).to_string(index=False))

                elif current_timezone_time > today8pm:
                    timezone_ran_today_dict[curr_gmt_timezone] = "N"

        await asyncio.sleep(20)  # task runs every 20 seconds


@client.event
async def on_message(message):
    author_username = message.author.name
    author_user_id = str(message.author.id)
    message.content = ' '.join(message.content.split())
    if message.content.startswith(".help"):
        await message.channel.send('Commend 1: .add @<user> <timezone>. This will also UPDATE if user is already in the system. <timezone> in gmt+/-"hour" or gmt for gmt+0')
        await message.channel.send('Comment 2: .remove @<user>')
        await message.channel.send('Comment 3: .ask @<user>')
        await message.channel.send('Comment 4: .next. This show the champs for the next timezone.')
        await message.channel.send('Comment 5: .help')
        await message.channel.send('Example: .add @Wing GMT-5')
    elif message.content.startswith(".add"):
        is_command_valid = validate_command(message.content, "add")

        if "Error" in is_command_valid:
            await message.channel.send(is_command_valid)
            return 1
        else:

            message_tokenized = message.content.split(' ', 2)
            userid = to_int_userid(message_tokenized[1])
            timezone = message_tokenized[2].upper()

            if not is_valid_user(userid):
                await message.channel.send('Error: Invalid user')
                return 1

            curr_user = client.get_user(int(userid))
            remove_user_reward(curr_user.id)
            print(curr_user.name + "," + str(userid) + "," + timezone.upper() + "," + timezone_dict[timezone.upper()] + "\n")

            f = open(reminder_file_path, "a", encoding="utf-8")
            f.write(curr_user.name + "," + str(userid) + "," + timezone.upper() + "," + timezone_dict[timezone.upper()] + "\n")
            f.close()
            await message.channel.send('Successfully added : ' + message_string_userid(userid))
    elif message.content.startswith(".remove"):
        is_command_valid = validate_command(message.content, "remove")
        if "Error" in is_command_valid:
            await message.channel.send(is_command_valid)
            return 1
        else:
            message_tokenized = message.content.split(' ', 1)
            userid = to_int_userid(message_tokenized[1])

            if not is_valid_user(userid):
                await message.channel.send('Error: Invalid user')
                return 1

            remove_user_reward(userid)
            await message.channel.send('Successfully removed' + message_string_userid(userid))
    elif message.content.startswith(".ask"):
        is_command_valid = validate_command(message.content, "remove")
        if "Error" in is_command_valid:
            await message.channel.send(is_command_valid)
            return 1
        else:
            message_tokenized = message.content.split(' ', 1)
            userid = to_int_userid(message_tokenized[1])

            if not is_valid_user(userid):
                await message.channel.send('Error: Invalid user')
                return 1

            curr_user = client.get_user(int(userid))

            if os.path.getsize(reminder_file_path) > 0:
                reward_df = pd.read_csv(reminder_file_path, sep=",", header=None, dtype=str)
                reward_df.columns = ['username', 'userid', 'timezone_gmt', 'timezone_pytz']
                user_reward_df = reward_df[reward_df['userid'] == str(userid)]
                if len(user_reward_df) == 0:
                    await message.channel.send('User ' + message_string_userid(userid) + ' does not have recorded reward time')
                else:
                    await message.channel.send('User ' + message_string_userid(userid) + ' reward timezone is ' + user_reward_df['timezone_gmt'].iloc[0])
            else:
                await message.channel.send('User ' + message_string_userid(userid) + ' does not have recorded reward time')
    elif message.content.startswith(".show"):
        f = open(reminder_file_path, "r")
        all_content = f.read()
        await message.channel.send(all_content)
        f.close()
    elif message.content.startswith(".next"):
        if os.path.getsize(reminder_file_path) > 0:
            reward_df = pd.read_csv(reminder_file_path, sep=",", header=None, dtype=str)
            reward_df.columns = ['username', 'userid', 'timezone_gmt', 'timezone_pytz']
            for curr_timezone_pytz in reward_df['timezone_pytz'].unique():
                current_timezone_time = datetime.now(pytz.timezone(curr_timezone_pytz))
                today6pm = current_timezone_time.replace(hour=18, minute=00, second=0, microsecond=0)
                today7pm = current_timezone_time.replace(hour=19, minute=00, second=0, microsecond=0)
                curr_gmt_timezone = time_zone_gmt_dict[curr_timezone_pytz]

                if current_timezone_time >= today6pm and current_timezone_time <= today7pm:
                    curr_reward_df = reward_df[reward_df['timezone_pytz'] == curr_timezone_pytz]
                    await message.channel.send("Reward for next timezone : " + curr_gmt_timezone)
                    await message.channel.send(curr_reward_df['username'].to_string(index=False))
                    return 1
            await message.channel.send("No champs for the next reward timezone")


def is_valid_user(userid):
    curr_user = client.get_user(int(userid))
    return not curr_user is None

def remove_user_reward(userid):
    old_file = open(reminder_file_path, "r")
    lines = old_file.readlines()
    old_file.close()
    new_file = open(reminder_file_path, "w")
    for line in lines:
        if not str(userid) in line.strip("\n"):
            new_file.write(line)
    new_file.close()

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
            return "Good"

client.loop.create_task(my_background_task())
client.run('Nzc0MTAzMjE2Njk4MDMyMTM5.X6S5zQ.qx1MWRkvOD6t02_XRa1S-IEKXho')
