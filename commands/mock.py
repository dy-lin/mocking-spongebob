from commands.base_command  import BaseCommand
from random                 import randint
import string
import os
import re

# Your friendly example event
# Keep in mind that the command name will be derived from the class name
# but in lowercase
# TODO
# get a 'bot is typing' message

# So, a command class named Random will generate a 'random' command
class Mock(BaseCommand):

    def __init__(self):
        # A quick description for the help message description = "Mocks the given message."
        # A list of parameters that the command will take as input
        description = "Mocks message given"
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

        # use pop to remove the param that starts with an http or a www or contains a .com/
        # add it to the end of the message after mocking
        r = re.compile("^http.*|.*\.com/?.*|^www\..*")
        links = list(filter(r.match, params))

        for i in links:
            params.remove(i)

        # TODO enable spoiler with space support here 
        # need to grab value of previous item in list and one after it too if they are ||. 
        # how to grab indices of regex matches? 
        # or how to grab index of item given its value? how does this handle repeats?
        # need to set spoiler = True after detection complete
        spoiler = False

        text = " ".join(params).lower()
        # except ValueError:
           #  await client.send_message(message.channel,
                                #      "Please, provide valid numbers")
           # return
        mocked = "*"
        alternate = open("/Users/dianalin/mocking-spongebob/files/alternate", "r").read()
        fix = open("/Users/dianalin/mocking-spongebob/files/fixl", "r").read()
        instafix = open("/Users/dianalin/mocking-spongebob/files/instafix", "r").read()
        if alternate == "on":
            if text[0] == "i":
                count = 0
            else:
                count = randint(0,1)

            for idx in range(len(text)):
                if text[idx] == " ":
                    mocked = mocked + text[idx]
                    count += 2
                elif text[idx] == "*" or text[idx] == "_":
                    continue
                elif text[idx] in string.punctuation:
                    mocked = mocked + text[idx]
                    count += 2
                elif not count % 2 :
                    mocked = mocked + text[idx].lower()
                    count += 1
                else:
                    mocked = mocked + text[idx].upper()
                    count += 1
        else:
            if text[0] == "i":
                start = 1
                mocked = mocked + text[0]
            else:
                start = 0
            for idx in range(start, len(text)):
                roll = randint(0,1)
                if text[idx] == "*" or text[idx] == "_":
                    continue
                elif roll == 0:
                    mocked = mocked + text[idx].lower()
                else:
                    mocked = mocked + text[idx].upper()
        mocked = mocked + "*"
         
        if fix == "on":
            mocked = mocked.replace("IlI", "iLi").replace("Il", "iL").replace("lI", "Li")
        
        if instafix == "on":
            if len(links) > 0: 
                ig_index = [ i for i, item in enumerate(links) if re.search('instagram.com', item)][0]
                url = links.pop(ig_index)
                if spoiler == True:
                    links.pop(ig_index)
                    links.pop(ig_index-1)
                    msg = " ".join(links) + "\n || " + url.replace(".instagram", ".ddinstagram") + " ||"
                    mocked = mocked + " " + msg
                else:
                    msg = " ".join(links) + "\n" + url.replace(".instagram", ".ddinstagram")
                    mocked = mocked + " " + msg
        await message.channel.send(f"**{message.author.nick}**: {mocked}")
