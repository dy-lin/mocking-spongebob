from commands.base_command  import BaseCommand
import os
# Your friendly example event
# Keep in mind that the command name will be derived from the class name
# but in lowercase

# So, a command class named Random will generate a 'random' command
class Fix(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Fixes lowercase L's when adjacent to uppercase i's"
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params' 
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ["on/off"]
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
        if params[0].lower() == "on":
            f = open("C:/Users/Diana/mocking-spongebob/files/fixl", "w")
            f.write("on")
            f.close()
            await message.channel.send("L's will be uppercase and i's will be lowercase when adjacent.")
        elif params[0].lower() == "off":
            f = open("C:/Users/Diana/mocking-spongebob/files/fixl", "w")
            f.write("off")
            f.close()
            await message.channel.send("L's will be randomized.")
        else:
            await message.channel.send("!fix should be used with <on> or <off>.")
