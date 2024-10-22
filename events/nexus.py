from events.base_event      import BaseEvent
from utils                  import get_channel

import os
import sys
from datetime import datetime, timedelta

import requests

# Your friendly example event
# You can name this class as you like, but make sure to set BaseEvent
# as the parent class
class NexusEvent(BaseEvent):

    def __init__(self):
        interval_minutes = 1  # Set the interval for this event
        super().__init__(interval_minutes)

    # Override the run() method
    # It will be called once every {interval_minutes} minutes
    async def run(self, client):
        # CREDIT: https://github.com/arosu/NexusInterview
        start_delta = 1 # days from today to start scanning
        channel = get_channel(client, "nexus-bot")

        WEEK_DELTA = 12  # Weeks
#         LOCATIONS = [
#                     ("Blaine Global Entry Enrollment Center", 5020),
#                     ]
        location_name = "Blaine Global Entry Enrollment Center"
        location_code = 5020
        SCHEDULER_API_URL = "https://ttp.cbp.dhs.gov/schedulerapi/locations/{location}/slots?startTimestamp={start}&endTimestamp={end}"  # noqa
        TTP_TIME_FORMAT = "%Y-%m-%dT%H:%M"

        NOTIF_MESSAGE = "New appointment slot open at {location}: {date}"
        MESSAGE_TIME_FORMAT = "%A, %B %d, %Y at %I:%M %p"


        start = datetime.now() + timedelta(days = start_delta)
        end = start + timedelta(weeks=WEEK_DELTA)

        url = SCHEDULER_API_URL.format(
            location=location_code,
            start=start.strftime(TTP_TIME_FORMAT), end=end.strftime(TTP_TIME_FORMAT)
        )
        # print(f"Fetching data from {url}", flush = True)

        try:
            results = requests.get(url).json()
            # DEBUG: results = [ { "active": 1, "timestamp": "2024-10-23T11:00" }, { "active": 0, "timestamp": "2024-10-23T11:10" } ]
        except requests.ConnectionError:
            # print("Could not connect to scheduler API")
            pass
           
        for result in results:
            if result["active"] > 0:
                print(f"Opening found for {location_name}", flush = True)

                timestamp = datetime.strptime(result["timestamp"], TTP_TIME_FORMAT)
                weekday = int(timestamp.strftime("%w"))
                hour = int(timestamp.strftime("%-H"))

                message = NOTIF_MESSAGE.format(
                    location=location_name,
                    date=timestamp.strftime(MESSAGE_TIME_FORMAT)
                )
                
                # if weekend, notify everyone
                if weekday == 0 or weekday == 6:
                    msg = f":bangbang: **ATTENTION** @everyone :bangbang: {message}"
                else:
                # if weekday
                    # if weekday between hours of workdays
                    # TODO: consider different workdays for di, wfh vs onsite?
                    if hour > 8 and hour < 16:
                        msg = f":bangbang: **ATTENTION** @di.lyn :bangbang: {message}"
                    # if outside of these hours, then ping everyone
                    else:
                        msg = f":bangbang: **ATTENTION** @everyone :bangbang: {message}"
            
                await channel.send(msg)
                return  # Halt on first match
                # TODO: return every match but use an embed? 
                # if scanning every minute, do not return previous one??

        print(f"No openings for {location_name}", flush = True)

