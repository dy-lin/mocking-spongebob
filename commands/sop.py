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

        # def create_sop(conn, sop):
        #     """
        #     Create a new sop into the sop table
        #     :param conn:
        #     :param sop:
        #     :return: sop id
        #     """
        #     sql = ''' INSERT INTO sop(food,mode,time,temperature)
        #               VALUES(?,?,?,?) '''
        #     cur = conn.cursor()
        #     cur.execute(sql, sop)
        #     conn.commit()
        #     return cur.lastrowid

        def select_sop_by_food(conn, food):
            """
            Query sop by food
            :param conn: the Connection object
            :param food:
            :return:
            """
            cur = conn.cursor()
            cur.execute("SELECT * FROM sop WHERE food LIKE ?", (food,))

            rows = cur.fetchall()
            keyword = food.replace("'", "").replace("%","").capitalize()
             
            if len(rows) == 0:
                # text = f"There is no {keyword} in our SOP."
                text = food
            else:
                degree_sign = u'\N{DEGREE SIGN}'
                msg = [ f"# :mag_right: Results for **{keyword}** :mag:" ]

                for row in rows:
                    id,name,mode,time,temp = row
                    name = name.title()
                    mode = mode.capitalize()
                    time_lower = round(int(time.replace(" ", "").split("-")[0]))
                    time_upper = round(int(time.replace(" ", "").split("-")[-1]))

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

        arg = " ".join(params)

        database = "/Users/diana/mocking-spongebob/files/sqlite.db"

        conn = create_connection(database)
        with conn:
            
            text = select_sop_by_food(conn, f"'%{arg}%'")
            await message.channel.send(text)
