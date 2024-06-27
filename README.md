# Global Entry Appointment Checker

This script is designed to check for the earliest available appointments for Global Entry interviews at a specific location and notify the user via a Discord webhook whenever an early appointment is found. It is intended to be run on a cron job every minute (or faster) to ensure timely updates.

I moved my appointment from months to a day using this.

## TLDR

- Checks for the earliest available Global Entry interview appointments.
- Sends notifications through Discord webhooks.

## Setup

1. **Create a discord server and a webhook for a channel you want alerts in**
2. **Create a .env file and add DISCORD_WEBHOOK_URL="my url"**
3. **Change location_id to the location you want. This defaults to Pittsburgh**
4. **Set it up on a cron to run every minute, otherwise you'll need to manually run the script to get an update**
