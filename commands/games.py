from commands.base_command  import BaseCommand
import os
import string
import pandas as pd
from random import randint

# Your friendly example event
# Keep in mind that the command name will be derived from the class name
# but in lowercase

# So, a command class named Random will generate a 'random' command
class Games(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Chooses a game from the list to play"
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params' 
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = [""]
        super().__init__(description, params)

    # Override the handle() method
    # It will be called every time the command is received
    async def handle(self, params, message, client):
        # 'params' is a list that contains the parameters that the command 
        # expects to receive, t is guaranteed to have AT LEAST as many
        # parameters as specified in __init__
        # 'message' is the discord.py Message object for the command to handle
        # 'client' is the bot Client object
        if len(params) == 0:
            arg = str(params[0]).capitalize()
        else:
            arg = "All"

        valid = ["Online", "Local"]
            
        df = pd.read_table("/data/Games.tsv")
        
        if arg not in valid:
            options = df
        else:
            condition = df.Coop.str.contains(arg)
            options = df[condition]

        lower_bound = 1
        upper_bound = options.shape[0]

        num = randint(lower_bound,upper_bound)
        selected = options.iloc[[num]][['Game']]

        final = selected.iloc[0]['Game']

        text = "You should play *" + str(final) + "* :video_game:"
        await message.channel.send(text)
