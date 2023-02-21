from commands.base_command  import BaseCommand
import pandas as pd

# Your friendly example event
# Keep in mind that the command name will be derived from the class name
# but in lowercase

# So, a command class named Random will generate a 'random' command
class Sop(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Fetches the airfryer protocol"
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params' 
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = [ "food" ]
        super().__init__(description, params)

    # Override the handle() method
    # It will be called every time the command is received
    async def handle(self, params, message, client):
        # 'params' is a list that contains the parameters that the command 
        # expects to receive, t is guaranteed to have AT LEAST as many
        # parameters as specified in __init__
        # 'message' is the discord.py Message object for the command to handle
        # 'client' is the bot Client object

        arg = " ".join(params).lower()
        sheet_id = "1b489bA2PW1XVHAH8H6qcrcBzxBiOeGE8g7WWfe7ASGo"
        sheet_name = "Sheet1"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

        df = pd.read_csv(url)
        condition = df.Keywords.str.contains(arg)
        options = df[condition]
        if options.shape[0] == 0:
            await message.channel.send(f"There is no {arg} in our SOP.")
        else:
            degree_sign = u'\N{DEGREE SIGN}'
            msg = []
            for index, row in options.iterrows():
                name = row['Food']
                mode = row['Mode'].capitalize()
                tmp = row['Time']
                if isinstance(tmp, str):
                    time_lower = round(int(row['Time'].replace(" ", "").split("-")[0]))
                    time_upper = round(int(row['Time'].replace(" ", "").split("-")[-1]))
                    if time_lower == time_upper:
                        time = time_lower
                    elif time_lower < time_upper:
                        time = f"{time_lower}-{time_upper}"
                    elif time_upper < time_lower:
                        time = f"{time_upper}-{time_lower}"
                elif isinstance(tmp, float):
                    time = round(tmp)
                temperature = round(row['Temperature'])
                celsius = round((temperature-32)*5/9)
                preset = row['Preset']
                notes = row['Notes']
                msg.append(f"**{name}:** {mode} at {temperature}{degree_sign}F ({celsius}{degree_sign}C) for {time} min.")
            text = '\n'.join(msg)
            await message.channel.send(text)
