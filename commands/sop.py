from commands.base_command  import BaseCommand
import sqlite3
from sqlite3 import Error
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


        def create_connection(db_file):
            """ create a database connection to the SQLite database
                specified by db_file
            :param db_file: database file
            :return: Connection object or None
            """
            conn = None
            try:
                conn = sqlite3.connect(db_file)
                return conn
            except Error as e:
                print(e)

            return conn 

        def create_sop(conn, sop):
           """
           Create a new sop into the sop table
           :param conn:
           :param sop:
           :return: sop id
           """

           # TODO
           # add support for different units of time
           # ends in m means minutes
           # ends in h means hours, convert this to minutes for storage in database
           # ends in number, assume minutes unless the mode is sous vide?
           sql = ''' INSERT INTO sop(food,mode,time,temperature)
           VALUES(?,?,?,?) '''
           cur = conn.cursor()
           cur.execute(sql, sop)
           conn.commit()
           return cur.lastrowid
        def select_sop_by_food(conn, food):
            """
            Query sop by food
            :param conn: the Connection object
            :param food:
            :return:
            """
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM sop WHERE food LIKE '%{food}%'")

            rows = cur.fetchall()
            keyword = food.replace("'", "").replace("%","").title()
             
            if len(rows) == 0:
                text = f"There is no {keyword} in our SOP."
            else:
                degree_sign = u'\N{DEGREE SIGN}'
                msg = [ f"# :mag_right: Results for {keyword} :mag:" ]
                for row in rows:
                    id,name,mode,time,temp = row
                    name = name.title()
                    mode = mode.capitalize()
                    try:
                        time_lower = int(time.replace(" ", "").split("-")[0])
                        time_upper = int(time.replace(" ", "").split("-")[-1])
                    except ValueError:
                        time_lower = float(time.replace(" ", "").split("-")[0])
                        time_upper = float(time.replace(" ", "").split("-")[-1])

                    if time_lower == time_upper:
                        time = time_lower
                    elif time_lower < time_upper:
                        time = f"{time_lower}-{time_upper}"
                    elif time_upper < time_lower:
                        time = f"{time_upper}-{time_lower}"
                    temperature = round(temp)
                    celsius = round((temperature-32)*5/9)

                    msg.append(f"- **{name}:** {mode} at {temperature}{degree_sign}F ({celsius}{degree_sign}C) for {time} min.")

                text = '\n'.join(msg)
            return(text)
        if params[0].lower() == "add":
            arg = params[-3:]
            name = " ".join(params[1:len(params)-3]).title()
            # TODO: currently mode is inferred positionally but sous vide is two words so its incompatible
        else:
            arg = " ".join(params)

        database = "C:/Users/Diana/mocking-spongebob/files/sqlite.db"

        conn = create_connection(database)
        with conn:
            if params[0].lower() == "add":
               sop = (name, arg[0].capitalize(), str(arg[1]), int(arg[2]))
               create_sop(conn, sop)
               await message.channel.send(f"SOP for {name} added to the database.")
               text = select_sop_by_food(conn, name)
               await message.channel.send(text, delete_after = 5)
            else:
                text = select_sop_by_food(conn, arg)
                await message.channel.send(text)
