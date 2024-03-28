from commands.base_command  import BaseCommand
import os
import re
# Your friendly example event # Keep in mind that the command name will be derived from the class name
# but in lowercase

# So, a command class named Random will generate a 'random' command
class Ig(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Embeds instagram links"
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params' 
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = [ "link" ]
        super().__init__(description, params)

    # Override the handle() method
    # It will be called every time the command is received
    async def handle(self, params, message, client):
        # 'params' is a list that contains the parameters that the command 
        # expects to receive, t is guaranteed to have AT LEAST as many
        # parameters as specified in __init__
        # 'message' is the discord.py Message object for the command to handle
        # 'client' is the bot Client object
        spoiler = False
        if len(params) > 1: 
            ig_index = [ i for i, item in enumerate(params) if re.search('instagram.com', item)][0]
            if ig_index+1 < len(params):
                if params[ig_index-1] == "||" and params[ig_index+1] == "||":
                    spoiler = True
            url = params.pop(ig_index)
            if spoiler == True:
                params.pop(ig_index)
                params.pop(ig_index-1)
                msg = " ".join(params) + "\n || " + url.replace(".instagram", ".ddinstagram") + " ||"
            else:
                msg = " ".join(params) + "\n" + url.replace(".instagram", ".ddinstagram")
            await message.channel.send(f"**{message.author.nick}**: {msg}")
        else:
            msg = params[0].replace(".instagram", ".ddinstagram")
            await message.channel.send(msg)
