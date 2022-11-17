from commands.base_command  import BaseCommand
import json
import os.path
# Your friendly example event
# Keep in mind that the command name will be derived from the class name
# but in lowercase

# So, a command class named Random will generate a 'random' command
class Gro(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Manages grocery lists"
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
        # await message.channel.send(f"{os.getcwd()}")
        savefile = "/Users/brian/mocking-spongebob/files/groceries.json"
        if len(params) > 0: 
            subcommand = params[0].lower()

            if len(params) >= 2:
                # if it starts with quotes then split it into quotes
                # if params[1].startswith('"'):
                #     temp = " ".join(params)
                #     temp.split('"')[2].remove(" $").remove("^ ")
                sublist = params[1] # how to account for two words?

                if sublist != sublist.upper() and sublist != "all":
                    sublist = sublist.capitalize()
                if sublist == "Ikea":
                    sublist = "IKEA"
                if sublist == "T&t":
                    sublist = "T&T"
                if sublist == "Tnt" or sublist == "TNT":
                    sublist = "T&T"
                if sublist == "Ct":
                    sublist = "Canadian Tire"
                if sublist == "Canadiantire":
                    sublist = "Canadian Tire"
                    
            else:
                sublist = ""

            # will this be allowed for the bot if i specify 3 argument?
            # how do quotes work in discord bot input?
            # what is default type for params?
            if len(params) >= 3:
                item = " ".join(params[2:]).lower()# .capitalize()
            else:
                item = ""

            if os.path.exists(savefile) == True:
                with open(savefile, "r") as f:
                    groceries = json.load(f)
            else:
                groceries = {}

            # will be called groceries
            if subcommand not in ["add", "remove", "clear", "list", "delete", "edit", "append"]:
                await message.channel.send(f"Unrecognized subcommand: *{subcommand}*")
            else:
                # CHECKBOX = u'\u2751'

                # check if the listname exists
                if sublist not in ["all"] + list(groceries.keys()):
                    # create the list
                    if sublist == "" and subcommand != "list":
                        await message.channel.send(f"Missing list argument.")
                        return
                    if subcommand == "add":
                        groceries[sublist] = []
                if subcommand == "add":
                    if item != "":
                        bulk = item.split(", ")
                        for i in bulk:
                            groceries[sublist].append(i)
                        await message.channel.send(f"Added *{item}* to **{sublist}**.")
                        jsonfile = json.dumps(groceries, indent = 4)
                        with open(savefile, "w") as f:
                            f.write(jsonfile)
                    else:
                        await message.channel.send(f"Missing item to be added.")
                elif subcommand in ["edit", "append"]:
                    if sublist not in list(groceries.keys()):
                        if sublist == "":
                            await message.channel.send(f"Unrecognized list: **{sublist}**")
                        else:
                            await message.channel.send("Missing list argument.")
                    else:
                        if item != "":
                            string = item.split()
                            try:
                                # SPLIT BACK TO individual
                                index = int(string[0])
                                if index not in range(1, len(groceries[sublist])+1):
                                    await message.channel.send("Unrecognized index: *{index}*")
                                else:
                                    if subcommand == "edit":
                                        new_item = " ".join(string[1:])
                                        old_item = groceries[sublist][index-1] 
                                        groceries[sublist][index-1] = new_item
                                        await message.channel.send(f"Edited *{old_item}* to *{new_item}* in **{sublist}**.")
                                        jsonfile = json.dumps(groceries, indent = 4)
                                        with open(savefile, "w") as f:
                                            f.write(jsonfile)
                                    elif subcommand == "append":
                                        old_item = groceries[sublist][index-1] 
                                        new_item = " ".join(string[1:])
                                        groceries[sublist][index-1] = old_item + " " + new_item
                                        await message.channel.send(f"Appended *{new_item}* to *{old_item}* in **{sublist}**.")
                                        jsonfile = json.dumps(groceries, indent = 4)
                                        with open(savefile, "w") as f:
                                            f.write(jsonfile)
                            except ValueError as ve:
                                await message.channel.send(f"First item must be an index: {string[0]}")
                        else:
                            await message.channel.send(f"Missing item to {subcommand}.")

                elif subcommand == "remove":
                    if sublist not in list(groceries.keys()):
                        indices = sublist.split(", ")
                        try:
                            x = int(indices[0])
                            await message.channel.send(f"Missing list argument.")
                        except ValueError as ve:
                            if indices[0] == "":
                                await message.channel.send(f"Missing list argument.")
                            else:
                                await message.channel.send(f"Unrecognized list: **{sublist}**")
                    else:
                        if item != "":
                            indices = item.split(", ")
                            copy = groceries[sublist].copy()
                            removed = []
                            for i in indices:
                                try:
                                    index = int(i)
                                    if index not in range(1, len(copy)+1):
                                        await message.channel.send("Unrecognized index: *{index}*")
                                        continue
                                    else:
                                        item = copy[index-1] # get item from original list
                                        idx = groceries[sublist].index(item) # get new index from new list using original item
                                        temp = groceries[sublist].pop(idx) # use the new index to pop 
                                        removed.append(item)
                                        # await message.channel.send(f"Removed *{item}* from **{sublist}**.")
                                except ValueError as ve:
                                    if i not in groceries[sublist]:
                                        await message.channel.send(f"Unrecognized item: *{i}*")
                                        continue
                                    else:
                                        # remove using name
                                        groceries[sublist].remove(i)
                                        removed.append(i)
                                        # await message.channel.send(f"Removed *{item}* from **{sublist}**.")
                            text = ", ".join(removed)
                            await message.channel.send(f"Removed *{text}* from **{sublist}**.")
                            jsonfile = json.dumps(groceries, indent = 4)
                            with open(savefile, "w") as f:
                                f.write(jsonfile)
                        else:
                            await message.channel.send(f"Missing item to be removed.")
                elif subcommand == "delete":
                    if sublist == "all":
                        groceries = {}
                        await message.channel.send("Deleted all grocery lists.")
                        jsonfile = json.dumps(groceries, indent = 4)
                        with open(savefile, "w") as f:
                            f.write(jsonfile)
                    else:
                        if sublist not in list(groceries.keys()):
                            if sublist != "":
                                await message.channel.send(f"Unrecognized list: **{sublist}**")
                            else:
                                await message.channel.send(f"Missing list argument.")
                        else:
                            groceries.pop(sublist)
                            await message.channel.send(f"Deleted **{sublist}**.")
                            jsonfile = json.dumps(groceries, indent = 4)
                            with open(savefile, "w") as f:
                                f.write(jsonfile)
                elif subcommand == "clear":
                    if sublist == "all":
                        for i in list(groceries.keys()):
                            groceries[i] = []
                        jsonfile = json.dumps(groceries, indent = 4)
                        with open(savefile, "w") as f:
                            f.write(jsonfile)
                    elif sublist not in list(groceries.keys()):
                        if sublist != "":
                            await message.channel.send(f"Unrecognized list: **{sublist}**")
                        else:
                            await message.channel.send(f"Missing list argument.")
                    else:
                        groceries[sublist] = []
                        await message.channel.send(f"Cleared **{sublist}**.")
                        jsonfile = json.dumps(groceries, indent = 4)
                        with open(savefile, "w") as f:
                            f.write(jsonfile)
                elif subcommand == "list":
                    if sublist == "all" or sublist == "":
                        if len(groceries) > 0:
                            msg = []
                            for i in list(groceries.keys()):
                                items = []
                                if len(groceries[i]) > 0:
                                    for index, j in enumerate(groceries[i]):
                                        idx = index+1
                                        items.append(f"\t{idx : >2}. {j.capitalize()}")
                                    temp = [ f":shopping_cart: **{i}**" ] + items
                                    chunk = '\n'.join(temp)
                                    msg.append(chunk)
                                else:
                                    chunk = f":shopping_cart: **{i}**\n\t*No groceries.*"
                                    msg.append(chunk)
                            text = '\n\n'.join(msg)
                            await message.channel.send(text)
                        else:
                            await message.channel.send("You have no grocery lists.")
                    elif sublist not in list(groceries.keys()):
                        if sublist != "":
                            await message.channel.send(f"Unrecognized list: **{sublist}**")
                        else:
                            await message.channel.send(f"Missing list argument.")
                    else:
                        msg = [ f":shopping_cart: **{sublist}**" ]
                        items = []
                        for index, i in enumerate(groceries[sublist]):
                            idx = index+1
                            items.append(f"\t{idx : >2}. {i.capitalize()}")
                        msg.extend(items)
                        text = '\n'.join(msg)
                        await message.channel.send(text) 
        else:
            if os.path.exists(savefile) == True:
                with open(savefile, "r") as f:
                    groceries = json.load(f)
                if len(groceries) > 0:
                    msg = []
                    for i in list(groceries.keys()):
                        items = []
                        if len(groceries[i]) > 0:
                            for index, j in enumerate(groceries[i]):
                                idx = index+1
                                items.append(f"\t{idx : >2}. {j.capitalize()}")
                            temp = [ f":shopping_cart: **{i}**" ] + items
                            chunk = '\n'.join(temp)
                            msg.append(chunk)
                        else:
                            chunk = f":shopping_cart: **{i}**\n\t*No groceries.*"
                            msg.append(chunk)
                    text = '\n\n'.join(msg)
                    await message.channel.send(text)
            else:
                await message.channel.send("You have no grocery lists.")
