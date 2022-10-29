from commands.base_command  import BaseCommand
import os
import string
import pandas as pd
from random import randint

# Your friendly example event
# Keep in mind that the command name will be derived from the class name
# but in lowercase

# So, a command class named Random will generate a 'random' command
class Jackbox(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Generates a random Jackbox game to play"
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params' 
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = []
        super().__init__(description, params)

    # Override the handle() method
    # It will be called every time the command is received
    async def handle(self, params, message, client):
        # 'params' is a list that contains the parameters that the command 
        # expects to receive, t is guaranteed to have AT LEAST as many
        # parameters as specified in __init__
        # 'message' is the discord.py Message object for the command to handle
        # 'client' is the bot Client object

        sheet_id = "1yR90EC3fvSD9jdHqGVkixAZ_ZtC0-mA12HkIQV0KIyg"
        sheet_name = "Sheet1"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"    
        df = pd.read_csv(url)
        if len(params) == 0:
            # generate the random game
            lower_bound = 1
            upper_bound = df.shape[0]
            num = randint(lower_bound,upper_bound)
            selected = df.iloc[[num]]
            final = selected.iloc[0]['Game']
            pack = selected.iloc[0]['Pack']
            text = "You should play *" + str(final) + "* from **" + str(pack) + "** :video_game:"
            await message.channel.send(text)
        else:
            valid = ["1", "2", "3", "4", "5", "6", "7", "8"]
            if str(params[0]) in valid:
                # grab from that pack
                condition = df.Pack.str.contains(str(params[0]))
                options = df[condition]
                msg = ["**" + options.Pack.iloc[0] + ":**"] + list(options.Game)
                text = '\n• '.join(msg)
                await message.channel.send(text)
            elif str(params[0]).lower() == "all":
                packs = []
                valid = ["1", "2", "3", "4", "5", "6", "7", "8"]
                for i in valid:
                    condition = df.Pack.str.contains(i)
                    options = df[condition]
                    msg = ["**" + options.Pack.iloc[0] + ":**"] + list(options.Game)
                    chunk = '\n• '.join(msg)
                    packs.append(chunk)
                text = '\n\n'.join(packs)
                await message.channel.send(text)
            else:
                # use it as regex
                args = " ".join(params).lower()
                condition = df.Game.str.contains(args, case=False)
                options = df[condition]
                msg = []
                for index, row in options.iterrows():
                    pack = row['Pack']
                    game = row['Game']
                    msg.append(f"**{pack}:**\n{game}")
                text = '\n\n'.join(msg)
                await message.channel.send(text)
