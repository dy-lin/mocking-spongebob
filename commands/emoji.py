from commands.base_command  import BaseCommand
import os
import string
# Your friendly example event
# Keep in mind that the command name will be derived from the class name
# but in lowercase

# So, a command class named Random will generate a 'random' command
class Emoji(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Converts letters into emojis"
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params' 
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ["message"]
        super().__init__(description, params)

    # Override the handle() method
    # It will be called every time the command is received
    async def handle(self, params, message, client):
        # 'params' is a list that contains the parameters that the command 
        # expects to receive, t is guaranteed to have AT LEAST as many
        # parameters as specified in __init__
        # 'message' is the discord.py Message object for the command to handle
        # 'client' is the bot Client object

        # try:
        #     lower_bound = int(params[0])
        #     upper_bound = int(params[1])
        # except ValueError:
        #     await client.send_message(message.channel,
        #                               "Please, provide valid numbers")
        #     return

        # if lower_bound > upper_bound:
        #     await client.send_message(message.channel,
        #                 "The lower bound can't be higher than the upper bound")
        #     return

        # rolled = randint(lower_bound, upper_bound)
        # msg = get_emoji(":game_die:") + f" You rolled {rolled}!"
        text = " ".join(params).upper().replace(" ", "  ")
        numbers = {
        "0": ":zero: ",
        "1": ":one: ",
        "2": ":two: ",
        "3": ":three: ",
        "4": ":four: ",
        "5": ":five: ",
        "6": ":six: ",
        "7": ":seven: ",
        "8": ":eight: ",
        "9": ":nine: "
        }

        for i in text:
            if i == "?":
                text = text.replace(i, ":question: ")
            elif i == "!":
                text = text.replace(i, ":exclamation: ")
            elif i == "#":
                text = text.replace(i, ":hash: ")
            elif i in string.punctuation:
                text = text.replace(i, "")
            elif i in string.digits:
                text = text.replace(i, numbers[i])
            elif i in string.ascii_uppercase:
                emoji = ":regional_indicator_" + i.lower() + ": "
                text = text.replace(i, emoji)

        text = text.replace(":exclamation: :exclamation:", ":bangbang:").replace(":exclamation: :question:", ":interrobang:")
        await message.channel.send(text)
