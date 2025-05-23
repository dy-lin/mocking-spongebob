import sys

import settings
import discord
import message_handler

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from events.base_event              import BaseEvent
from events                         import *
from multiprocessing                import Process

# Set to remember if the bot is already running, since on_ready may be called
# more than once on reconnects
this = sys.modules[__name__]
this.running = False

# Scheduler that will be used to manage events
sched = AsyncIOScheduler()


###############################################################################

def main():
    # Initialize the client
    print("Starting up...")
    client = discord.Client()

    # Define event handlers for the client
    # on_ready may be called multiple times in the event of a reconnect,
    # hence the running flag
    @client.event
    async def on_ready():
        if this.running:
            return

        this.running = True

        # Set the playing status
        if settings.NOW_PLAYING:
            print("Setting NP game", flush=True)
            await client.change_presence(
                activity=discord.Game(name=settings.NOW_PLAYING))
        print("Logged in!", flush=True)

        # Load all events
        print("Loading events...", flush=True)
        n_ev = 0
        for ev in BaseEvent.__subclasses__():
            event = ev()
            sched.add_job(event.run, 'interval', (client,), 
                          minutes=event.interval_minutes)
            n_ev += 1
        sched.start()
        print(f"{n_ev} events loaded", flush=True)

    # The message handler for both new message and edits
    async def common_handle_message(message):
        text = message.content
        embed = open("C:/Users/Diana/mocking-spongebob/files/embed", "r").read()
        # possible values be "dd", "ez", "off" if text.startswith(settings.COMMAND_PREFIX) and text != settings.COMMAND_PREFIX:
        if message.author.name != "Mocking Spongebob":
            if text.startswith(settings.COMMAND_PREFIX) and text != settings.COMMAND_PREFIX:
                cmd_split = text[len(settings.COMMAND_PREFIX):].split()
                try:
                    await message_handler.handle_command(cmd_split[0].lower(), 
                                          cmd_split[1:], message, client)
                except Exception as error:
                    print("Error while handling message", error, flush=True)
                    raise
            elif "instagram.com" in text:
                try:
                    if embed == "dd":
                        await message_handler.handle_command("dd", 
                                              text.split(), message, client)
                    elif embed == "ez":
                        await message_handler.handle_command("ez", 
                                              text.split(), message, client)
                except Exception as error:
                    print("Error while handling message", error, flush=True)
                    print("Use `!embed` `dd|ez|current|off`", flush = True)
                    raise
            # elif "tiktok.com" in text:
            #     try:
            #         await message_handler.handle_command("tt", 
            #                               text.split(), message, client)
            #     except Exception as error:
            #         print("Error while handling message", error, flush=True)
            #         raise

                    
        # else:
        #    print(f"{message.author.name}: {text}", flush = True)

    @client.event
    async def on_message(message):
        await common_handle_message(message)

    @client.event
    async def on_message_edit(before, after):
        await common_handle_message(after)

    # Finally, set the bot running
    client.run(settings.BOT_TOKEN)

###############################################################################


if __name__ == "__main__":
    main()
