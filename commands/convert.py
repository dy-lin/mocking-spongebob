from commands.base_command  import BaseCommand
import string
import re

# Your friendly example event
# Keep in mind that the command name will be derived from the class name
# but in lowercase

# So, a command class named Random will generate a 'random' command
class Convert(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Converts oven instructions to airfryer instructions"
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params' 
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ["temperature (F)", "time (min)"]
        super().__init__(description, params)

    # Override the handle() method
    # It will be called every time the command is received
    async def handle(self, params, message, client):
        # if the temperature contains F, remove the F and do the math
        degree_sign = u'\N{DEGREE SIGN}'
        temp_F = str(params[0]).upper()
        temp = int(temp_F.replace("F", ""))
        final_temp = f"{temp - 25}{degree_sign}F"

        time = str(params[1]).lower().split("-")
        
        times = []
        for bound in time:
            num = int(re.findall('[0-9]+', bound)[0])
            times.append(round(num * 0.8))

        if len(times) == 1:
            final_time = f"{times[0]} min"
        else:
            if times[0] == times[1]:
                final_time = f"{times[0]} min"
            else:
                final_time = f"{times[0]}-{times[1]} min"
        
        msg = f"Airfry at {final_temp} for {final_time}"
        await message.channel.send(msg)
