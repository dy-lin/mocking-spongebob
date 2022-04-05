from commands.base_command  import BaseCommand
import os
import string
import pandas as pd
from random import randint

# Your friendly example event
# Keep in mind that the command name will be derived from the class name
# but in lowercase

# So, a command class named Random will generate a 'random' command
class Lunch(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Chooses a place to eat lunch"
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
            
        df = pd.read_table("/app/data/Restaurants.tsv")
         

        lower_bound = 1
        upper_bound = df.shape[0]
        
        num = randint(lower_bound, upper_bound)

        selected = df.iloc[[num]][['Restaurant']]

        final = selected.iloc[0]['Restaurant']

        text = "You should have lunch at *" + str(final) + "* :fork_knife_plate:"
        await message.channel.send(text)
