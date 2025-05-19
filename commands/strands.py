from commands.base_command  import BaseCommand
import os
import subprocess

from datetime import date
# Your friendly example event # Keep in mind that the command name will be derived from the class name
# but in lowercase

# So, a command class named Random will generate a 'random' command
class Strands(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Provides hints for NYT Strands"
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

       strands = subprocess.getoutput(['C:/Users/Diana/mocking-spongebob/helpers/download_strands.sh']).split('\n')
       if len(strands) == 1 and strands[0] == "NULL":
           print(strands, flush=True)
           await message.channel.send("Please check today's URL.") 
           return
       today = date.today().strftime("%A, %B %d, %Y")
       theme = strands[0]
       theme_hint = strands[1]
       spangram, spangram_hint = strands[len(strands)-1].split(": ")
       spangram_censored = ""
       spangram_hint_censored = f"|| {spangram_hint} ||"
       for letter in spangram.upper():
           spangram_censored = spangram_censored + f"|| {letter} ||  "

       msg = f"# {today}\n## **THEME**: {theme}\n{theme_hint}\n## **SPANGRAM**: {spangram_censored}\n**Hint**: {spangram_hint_censored}"

       for i in strands[2:len(strands)-1]:
           word, hint = i.split(": ")
           word_censored = ""
           for letter in word.upper():
               word_censored = word_censored + f"|| {letter} ||  "

           hint_censored = f"|| {hint} ||"

           msg = msg + "\n" + f"## **Word**: {word_censored}\n**Hint**: {hint_censored}"

       await message.channel.send(msg) 


