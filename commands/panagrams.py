from commands.base_command  import BaseCommand
import subprocess
# Your friendly example event
# Keep in mind that the command name will be derived from the class name
# but in lowercase

# So, a command class named Random will generate a 'random' command
class Bee(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Provides hints to the NYT Spelling Bee"
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

        panagrams = subprocess.getoutput(['/Users/dianalin/mocking-spongebob/helpers/download_panagrams.sh']).split(' ')

        if panagrams == 'NULL':
            msg = f"Today's date does not match the Spelling Bee date."
        else:
            num_panagrams = len(panagrams)
            msg = f"There are {num_panagrams} panagrams:\n"

            for word in panagrams:
                answer = "# -"
                for letter in word:
                    answer = answer + f"   ||{letter}||"
                if len(word) == 7:
                    answer = answer + f"   (perfect)"
                msg = msg + answer +  "\n"

        await message.channel.send(msg)
