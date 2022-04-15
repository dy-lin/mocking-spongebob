from commands.base_command  import BaseCommand

# Your friendly example event
# Keep in mind that the command name will be derived from the class name
# but in lowercase

# So, a command class named Random will generate a 'random' command
class Sangria(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Scales sangria ingredients per cup"
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params' 
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = []
        super().__init__(description, params)

    # Override the handle() method
    # It will be called every time the command is received
    async def handle(self, params, message, client):
        schnapps = round(125/1500*500)
        wine = round(750/1500*500)
        oj = round(250/1500*500)
        peaches = round(45/1500*500)
        sprite = round(330/1500*500)
        msg = f"For 1 (500 mL) cup of Peach Sangria:\n\n**Peach schnapps:** {schnapps} mL \n**White wine:** {wine} mL\n**Orange juice:** {oj} mL\n**Sprite:** {sprite}\n**Peaches:** {peaches}"
        await message.channel.send(msg)
