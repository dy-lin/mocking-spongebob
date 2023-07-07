from commands.base_command  import BaseCommand
import json
import os.path
import random
# Your friendly example event
# Keep in mind that the command name will be derived from the class name
# but in lowercase

# So, a command class named Random will generate a 'random' command
class Eat(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Manages restaurants"
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
        savefile = "/Users/diana/mocking-spongebob/files/restaurants.json"
        if len(params) > 0: 
            subcommand = params[0].lower()

            if len(params) >= 2:
                sublist = params[1]
                if sublist != sublist.upper() and sublist != "all":
                    sublist = sublist.title()
            else:
                sublist = ""

            # will this be allowed for the bot if i specify 3 argument?
            # how do quotes work in discord bot input?
            # what is default type for params?
            if len(params) >= 3:
                item = " ".join(params[2:]).title()# .capitalize()
            else:
                item = ""

            if os.path.exists(savefile) == True:
                with open(savefile, "r") as f:
                    restaurant = json.load(f)
            else:
                restaurant = {}
#                 jsonfile = json.dumps(restaurant, indent = 4)
#                 with open(savefile, "w") as f:
#                     f.write(jsonfile)

            # will be called restaurant
            if subcommand not in ["add", "remove", "clear", "list", "delete", "edit", "append", "random"]:
                await message.channel.send(f"Unrecognized subcommand: *{subcommand}*")
            else:
                # CHECKBOX = u'\u2751'

                # check if the listname exists
                if sublist not in ["all"] + list(restaurant.keys()):
                    # create the list
                    if sublist == "" and subcommand != "list":
                        await message.channel.send(f"Missing list argument.")
                        return
                    if subcommand == "add":
                        restaurant[sublist] = []

                if subcommand == "add":
                    if item != "":
                        bulk = item.split(", ")
                        for i in bulk:
                            restaurant[sublist].append(i)
                        await message.channel.send(f"Added *{item}* to **{sublist}**.")
                        jsonfile = json.dumps(restaurant, indent = 4)
                        with open(savefile, "w") as f:
                            f.write(jsonfile)
                    else:
                        await message.channel.send(f"Missing item to be added.")
                elif subcommand in ["edit", "append"]:
                    if sublist not in list(restaurant.keys()):
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
                                if index not in range(1, len(restaurant[sublist])+1):
                                    await message.channel.send("Unrecognized index: *{index}*")
                                else:
                                    if subcommand == "edit":
                                        new_item = " ".join(string[1:])
                                        old_item = restaurant[sublist][index-1] 
                                        restaurant[sublist][index-1] = new_item
                                        await message.channel.send(f"Edited *{old_item}* to *{new_item}* in **{sublist}**.")
                                        jsonfile = json.dumps(restaurant, indent = 4)
                                        with open(savefile, "w") as f:
                                            f.write(jsonfile)
                                    elif subcommand == "append":
                                        old_item = restaurant[sublist][index-1] 
                                        new_item = " ".join(string[1:])
                                        restaurant[sublist][index-1] = old_item + " " + new_item
                                        await message.channel.send(f"Appended *{new_item}* to *{old_item}* in **{sublist}**.")
                                        jsonfile = json.dumps(restaurant, indent = 4)
                                        with open(savefile, "w") as f:
                                            f.write(jsonfile)
                            except ValueError as ve:
                                await message.channel.send(f"First item must be an index: {string[0]}")
                        else:
                            await message.channel.send(f"Missing item to {subcommand}.")

                elif subcommand == "remove":
                    if sublist not in list(restaurant.keys()):
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
                            copy = restaurant[sublist].copy()
                            removed = []
                            for i in indices:
                                try:
                                    index = int(i)
                                    if index not in range(1, len(copy)+1):
                                        await message.channel.send("Unrecognized index: *{index}*")
                                        continue
                                    else:
                                        item = copy[index-1] # get item from original list
                                        idx = restaurant[sublist].index(item) # get new index from new list using original item
                                        temp = restaurant[sublist].pop(idx) # use the new index to pop 
                                        removed.append(item)
                                        # await message.channel.send(f"Removed *{item}* from **{sublist}**.")
                                except ValueError as ve:
                                    if i not in restaurant[sublist]:
                                        await message.channel.send(f"Unrecognized item: *{i}*")
                                        continue
                                    else:
                                        # remove using name
                                        restaurant[sublist].remove(i)
                                        removed.append(i)
                                        # await message.channel.send(f"Removed *{item}* from **{sublist}**.")
                            text = ", ".join(removed)
                            await message.channel.send(f"Removed *{text}* from **{sublist}**.")
                            jsonfile = json.dumps(restaurant, indent = 4)
                            with open(savefile, "w") as f:
                                f.write(jsonfile)
                        else:
                            await message.channel.send(f"Missing item to be removed.")
                elif subcommand == "delete":
                    if sublist == "all":
                        restaurant = {}
                        await message.channel.send("Deleted all restaurants.")
                        jsonfile = json.dumps(restaurant, indent = 4)
                        with open(savefile) as f:
                            f.write(jsonfile)
                    else:
                        if sublist not in list(restaurant.keys()):
                            if sublist != "":
                                await message.channel.send(f"Unrecognized list: **{sublist}**")
                            else:
                                await message.channel.send(f"Missing list argument.")
                        else:
                            restaurant.pop(sublist)
                            await message.channel.send(f"Deleted **{sublist}**.")
                            jsonfile = json.dumps(restaurant, indent = 4)
                            with open(savefile, "w") as f:
                                f.write(jsonfile)
                elif subcommand == "clear":
                    if sublist == "all":
                        for i in list(restaurant.keys()):
                            restaurant[i] = []
                        jsonfile = json.dumps(restaurant, indent = 4)
                        with open(savefile, "w") as f:
                            f.write(jsonfile)
                    elif sublist not in list(restaurant.keys()):
                        if sublist != "":
                            await message.channel.send(f"Unrecognized list: **{sublist}**")
                        else:
                            await message.channel.send(f"Missing list argument.")
                    else:
                        restaurant[sublist] = []
                        await message.channel.send(f"Cleared **{sublist}**.")
                        jsonfile = json.dumps(restaurant, indent = 4)
                        with open(savefile, "w") as f:
                            f.write(jsonfile)
                elif subcommand == "random":
                    if sublist not in list(restaurant.keys()):
                        if sublist != "":
                            await message.channel.send(f"Unrecognized list: **{sublist}**")
                        else:
                            await message.channel.send(f"Missing list argument.")
                    else:
                        chosen = random.choice(restaurant[sublist])
                        await message.channel.send(f"You should watch *{chosen}*")
                elif subcommand == "list":
                    if sublist == "all" or sublist == "":
                        if len(restaurant) > 0:
                            msg = []
                            for i in list(restaurant.keys()):
                                items = []
                                if len(restaurant[i]) > 0:
                                    for index, j in enumerate(restaurant[i]):
                                        idx = index+1
                                        items.append(f"\t{idx : >2}. {j}")
                                    temp = [ f":fork_knife_plate: **{i}**" ] + items
                                    chunk = '\n'.join(temp)
                                    msg.append(chunk)
                                else:
                                    chunk = f":fork_knife_plate: **{i}**\n\t*No restaurant.*"
                                    msg.append(chunk)
                            text = '\n\n'.join(msg)
                            await message.channel.send(text)
                        else:
                            await message.channel.send("You have no restaurants.")
                    elif sublist not in list(restaurant.keys()):
                        if sublist != "":
                            await message.channel.send(f"Unrecognized list: **{sublist}**")
                        else:
                            await message.channel.send(f"Missing list argument.")
                    else:
                        if len(restaurant[sublist]) == 0:
                            await message.channel.send(f":fork_knife_plate: **{sublist}**\n*No restaurants.*")
                        else:
                            msg = [ f":fork_knife_plate: **{sublist}**" ]
                            items = []
                            for index, i in enumerate(restaurant[sublist]):
                                idx = index+1
                                items.append(f"\t{idx : >2}. {i}")
                            msg.extend(items)
                            text = '\n'.join(msg)
                            await message.channel.send(text) 
        else:
            if os.path.exists(savefile) == True:
                with open(savefile, "r") as f:
                    restaurant = json.load(f)
                if len(restaurant) > 0:
                    msg = []
                    for i in list(restaurant.keys()):
                        items = []
                        if len(restaurant[i]) > 0:
                            for index, j in enumerate(restaurant[i]):
                                idx = index+1
                                items.append(f"\t{idx : >2}. {j}")
                            temp = [ f":fork_knife_plate: **{i}**" ] + items
                            chunk = '\n'.join(temp)
                            msg.append(chunk)
                        else:
                            chunk = f":fork_knife_plate: **{i}**\n\t*No restaurants.*"
                            msg.append(chunk)
                    text = '\n\n'.join(msg)
                    await message.channel.send(text)
            else:
                await message.channel.send("You have no restaurants.")
