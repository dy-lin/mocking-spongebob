from commands.base_command  import BaseCommand

# Your friendly example event
# Keep in mind that the command name will be derived from the class name
# but in lowercase

# So, a command class named Random will generate a 'random' command
class Angry(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Adds to or displays the current angry balance"
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
        filename = "/Users/dianalin/mocking-spongebob/files/angry.txt"

        infile = open(filename, 'r')

        balance = float(infile.read().replace("$", ""))
        infile.close()

        if len(params) > 0:
            if params[0] != "clear":
                to_add = float(params[0].replace("$", ""))
                new_balance = balance + to_add
                format_balance = "${:.2f}".format(new_balance) 

                outfile = open(filename, 'w')
                outfile.write(format_balance)
                outfile.close()

                msg = f":face_with_symbols_over_mouth: Your updated angry balance is: **{format_balance}** :face_with_symbols_over_mouth:"
            else:
                outfile = open(filename, 'w')
                outfile.write("$0.00")
                outfile.close()
                msg = ":face_with_symbols_over_mouth: Your updated angry balance is: **$0.00** :face_with_symbols_over_mouth:"
        else:
            format_balance = "${:.2f}".format(balance) 
            msg = f":face_with_symbols_over_mouth: Your current angry balance is: **{format_balance}** :face_with_symbols_over_mouth:"

        await message.channel.send(msg)
