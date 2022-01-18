from commands.base_command  import BaseCommand

# Your friendly example event
# Keep in mind that the command name will be derived from the class name
# but in lowercase

# So, a command class named Random will generate a 'random' command
class Rickroll(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Rickrolls"
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

        # try:
        #     lower_bound = int(params[0])
        #     upper_bound = int(params[1])
        # except ValueError:
        #     await client.send_message(message.channel,
        #                               "Please, provide valid numbers")
        #     return

        # if lower_bound > upper_bound:
        #     await client.send_message(message.channel,
        #                 "The lower bound can't be higher than the upper bound")
        #     return

        # rolled = randint(lower_bound, upper_bound)
        # msg = get_emoji(":game_die:") + f" You rolled {rolled}!"
        
        await message.channel.send(":regional_indicator_n: :regional_indicator_e: :regional_indicator_v: :regional_indicator_e: :regional_indicator_r:   :regional_indicator_g: :regional_indicator_o: :regional_indicator_n: :regional_indicator_n: :regional_indicator_a:   :regional_indicator_g: :regional_indicator_i: :regional_indicator_v: :regional_indicator_e:   :regional_indicator_y: :regional_indicator_o: :regional_indicator_u:   :regional_indicator_u: :regional_indicator_p: :musical_note:\n:regional_indicator_n: :regional_indicator_e: :regional_indicator_v: :regional_indicator_e: :regional_indicator_r:   :regional_indicator_g: :regional_indicator_o: :regional_indicator_n: :regional_indicator_n: :regional_indicator_a:   :regional_indicator_l: :regional_indicator_e: :regional_indicator_t:   :regional_indicator_y: :regional_indicator_o: :regional_indicator_u:   :regional_indicator_d: :regional_indicator_o: :regional_indicator_w: :regional_indicator_n: :notes:\n:regional_indicator_n: :regional_indicator_e: :regional_indicator_v: :regional_indicator_e: :regional_indicator_r:   :regional_indicator_g: :regional_indicator_o: :regional_indicator_n: :regional_indicator_n: :regional_indicator_a:   :regional_indicator_r: :regional_indicator_u: :regional_indicator_n:   :regional_indicator_a: :regional_indicator_r: :regional_indicator_o: :regional_indicator_u: :regional_indicator_n: :regional_indicator_d:   :regional_indicator_a: :regional_indicator_n: :regional_indicator_d:   :regional_indicator_d: :regional_indicator_e: :regional_indicator_s: :regional_indicator_e: :regional_indicator_r: :regional_indicator_t:   :regional_indicator_y: :regional_indicator_o: :regional_indicator_u: :musical_note:\nhttps://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713")
