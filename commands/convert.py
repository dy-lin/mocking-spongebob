from commands.base_command  import BaseCommand
import string
import re

# Your friendly example event
# Keep in mind that the command name will be derived from the class name
# but in lowercase

# So, a command class named Random will generate a 'random' command
class Convert(BaseCommand):

    def __init__(self):
        degree_sign = u'\N{DEGREE SIGN}'
        # A quick description for the help message
        description = f"Converts oven instructions to airfryer instructions (-25{degree_sign}F, -30% time)"
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params' 
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ["temperature", "time (min)"]
        super().__init__(description, params)

    # Override the handle() method
    # It will be called every time the command is received
    async def handle(self, params, message, client):
        # if the temperature contains F, remove the F and do the math
        degree_sign = u'\N{DEGREE SIGN}'
        temperature = str(params[0].upper())
        if temperature.endswith("F") == True:
            fah = True
            temp_F = int(temperature.replace("F", ""))
            final_temp_F = f"{temp_F - 25}{degree_sign}F"
            temp_C = round((temp_F-25-32)*(5/9))
            final_temp_C = f"{temp_C}{degree_sign}C"
        elif temperature.endswith("C") == True:
            fah = False
            temp_C = int(temperature.replace("C", ""))
            temp_F = round((temp_C*9/5)+32)
            temp_C = round((temp_F-25-32)*(5/9))
            final_temp_F = f"{temp_F - 25}{degree_sign}F"
            final_temp_C = f"{temp_C}{degree_sign}C"
        else:
            # assume fahrenheit
            fah = True
            temp_F = int(temperature)
            final_temp_F = f"{temp_F - 25}{degree_sign}F"
            temp_C = round((temp_F-25-32)*(5/9))
            final_temp_C = f"{temp_C}{degree_sign}C"

        time = str(params[1]).lower().split("-")
        times = []
        for bound in time:
            num = int(re.findall('[0-9]+', bound)[0])
            times.append(round(num * 0.7))

        if len(times) == 1:
            final_time = f"{times[0]} min"
        else:
            if times[0] == times[1]:
                final_time = f"{times[0]} min"
            else:
                final_time = f"{times[0]}-{times[1]} min"

        if fah == True: 
            msg = f"Airfry at {final_temp_F} ({final_temp_C}) for {final_time}"
        else:
            msg = f"Airfry at {final_temp_C} ({final_temp_F}) for {final_time}"
        await message.channel.send(msg)
