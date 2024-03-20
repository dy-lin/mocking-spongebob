from commands.base_command  import BaseCommand
import subprocess
import re
import datetime
# Your friendly example event
# Keep in mind that the command name will be derived from the class name # but in lowercase

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
        if len(params) != 0 and params[0].startswith("2"):
            try:
                tmp = datetime.datetime.strptime(params[0], "%Y-%m-%d")
                today_unformatted = tmp.strftime("%Y-%m-%d")
                today = tmp.strftime("%A, %B %d, %Y")
                params = params[1:len(params)]
            except:
                await message.channel.send("Date must be YYYY-MM-DD.")
                return

        else:
            today_unformatted = datetime.date.today().strftime("%Y-%m-%d")
            today = datetime.date.today().strftime("%A, %B %d, %Y")

        # await message.channel.send(f"# {today}")
        msg = f"# {today}"
        if len(params) != 0:
            for start in params:
                start = re.sub("-[0-9]+$", "", start) # add suport for copying and pasting lines from built in hints
                if start.startswith("-"):
                    end = True
                else:
                    end = False

                hint = start.upper()
                words = subprocess.getoutput([f'/Users/dianalin/mocking-spongebob/helpers/download_panagrams.sh {today_unformatted} {hint}']).split('\n')
                if words == 'NULL':
                    msg = msg + "\n" + f"Today's date does not match the Spelling Bee date."
                elif len(words) == 1 and words[0] == '' and end == False:
                    msg = msg + "\n" + f"There are no words that start with **{hint}**."
                elif len(words) == 1 and words[0] == '' and end == True:
                    msg = msg + "\n" f"There are no words that end in **{hint}**."
                else:
                    num_words = len(words)
                    if end == True:
                        msg = msg + "\n" + f"There are {num_words} word(s) ending in **{hint[1:]}**:\n"
                    else:
                        msg = msg + "\n" + f"There are {num_words} word(s) starting with **{hint}**:\n"

                    for word in words:
                        answer = "# -"
                        i = 0
                        for letter in word:
                            # do not spoiler tag the first two letters
                            if end == True:
                                if len(word) == len(hint):
                                    if i >= len(word)-len(hint[1:]): # use len(hint[1:]) if only revealing hint instead of hint + 1 letter
                                        answer = answer + f"   {letter}"
                                    else:
                                        answer = answer + f"   ||{letter}||"
                                else:
                                    if i >= len(word)-len(hint): # use len(hint[1:]) if only revealing hint instead of hint + 1 letter
                                        answer = answer + f"   {letter}"
                                    else:
                                        answer = answer + f"   ||{letter}||"
                            else:
                                if len(word) == len(hint)+1:
                                    if i < len(hint): # use < if only revealing hint instead of hint + 1 letter
                                        answer = answer + f"   {letter}"
                                    else:
                                        answer = answer + f"   ||{letter}||"
                                else:
                                    if i <= len(hint): # use < if only revealing hint instead of hint + 1 letter
                                        answer = answer + f"   {letter}"
                                    else:
                                        answer = answer + f"   ||{letter}||"
                            i = i + 1
                        msg = msg + answer +  "\n"
            await message.channel.send(msg)
        else:
            panagrams = subprocess.getoutput([f'/Users/dianalin/mocking-spongebob/helpers/download_panagrams.sh {today_unformatted}']).split('\n')
            if panagrams == 'NULL':
                msg = msg + "\n" + f"Today's date does not match the Spelling Bee date."
            else:
                num_panagrams = len(panagrams)
                msg = msg + "\n" + f"There are {num_panagrams} panagram(s):\n"

                for word in panagrams:
                    answer = "# -"
                    for letter in word:
                        answer = answer + f"   ||{letter}||"
                    if len(word) == 7:
                        answer = answer + f"   (perfect)"
                    msg = msg + answer +  "\n"

            await message.channel.send(msg)
