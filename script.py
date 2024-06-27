"""
This script checks for the earliest available appointment for Global Entry interviews at a specific location.
It sends a message to a Discord webhook whenever an early appointment is found.

It should be run on a cron job every minute.
"""

import datetime
import os
import shelve

import requests

# Configure this section to match your location and discord webhook
location_id = 9200 # 9200 is the location id for Pittsburgh
discord_webhook = os.getenv("DISCORD_WEBHOOK_URL")

# Test mode will send a message to a webhook even if there is no update
test_mode = False
max_future_date ="2090-08-18T13:50"


def get_appointment_list():
  response = requests.get(f"https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=3&locationId=${location_id}&minimum=0")
  if response.status_code == 200:
    list = response.json()[0]
    return list
  else:
    return None

def send_message(msg):
    """
    Sends a message to a discord webhook
    """
    data = {"content": msg}
    requests.post(discord_webhook, json=data)

def main():
  list = get_appointment_list()

  with shelve.open("data") as db:
    stored_date = db.get("earliest", max_future_date)
    stored_date = datetime.datetime.strptime(stored_date, "%Y-%m-%dT%H:%M")

    api_earliest = datetime.datetime.strptime(list['startTimestamp'], "%Y-%m-%dT%H:%M")
    serialized_earliest = api_earliest.strftime("%Y-%m-%dT%H:%M")

    if api_earliest < stored_date:
      message = "New early date found " + str(api_earliest)
      db["earliest"] = serialized_earliest
    elif api_earliest > stored_date:
      message = "Lost early appoint of " + str(stored_date) + " newest date is " + str(api_earliest)
      db["earliest"] = serialized_earliest
    else:
      # Do nothing if they're equal
      message = "No changes to earliest date: " + str(stored_date)
      if not test_mode:
        return

    print(message)
    send_message(message)

if __name__ == "__main__":
  main()

