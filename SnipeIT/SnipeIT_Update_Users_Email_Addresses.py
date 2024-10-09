#!/usr/bin/env python

###########################################################################################
#
# Note:     This changes the email domain for existing users in Snipe
#
#
###########################################################################################

import config
import requests
import csv
import json
from datetime import datetime
import logging
import time

# Set some parameters for this run
api_url = config.API_URL
api_token = config.API_TOKEN
input_file = config.INPUT_FILE
output_file = config.OUTPUT_FILE
license_id = config.LICENSE_ID
initial_seat = config.INITIAL_SEAT

###################### Set up Logging
logfile = config.LOGFILE

# get Date and time
dt_object = datetime.now()
# Create time format for Logging
modified = dt_object.strftime('_%Y-%m-%d_%H_%M')
logfile = logfile + modified + ".log"

# configure logging
FORMAT = '%(asctime)-20s %(levelname)-8s %(message)s'
logging.basicConfig(filename=logfile, level=logging.INFO, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

###################### End of Logging Setup


# Configuration
SNIPE_IT_URL = 'https://your-snipe-it-url.com'  # Your Snipe-IT instance URL
API_TOKEN = 'your-api-token'  # Your Snipe-IT API token
HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}

def get_users(page=1):
    """Fetch all users from Snipe-IT."""
    url = f'{SNIPE_IT_URL}/api/v1/users?page={page}'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching users: {response.status_code} - {response.text}")

def update_user_email(user_id, new_email):
    """Update a user's email address."""
    url = f'{SNIPE_IT_URL}/api/v1/users/{user_id}'
    data = {
        'email': new_email
    }
    response = requests.put(url, headers=HEADERS, json=data)
    if response.status_code == 200:
        print(f"Updated user {user_id}: {new_email}")
    else:
        print(f"Failed to update user {user_id}: {response.status_code} - {response.text}")

def main():
    page = 1
    while True:
        users_data = get_users(page)
        users = users_data['rows']

        if not users:
            break

        for user in users:
            current_email = user['email']
            user_id = user['id']

            # Check if email belongs to the old domain
            if 'pinnacle-oa.com' in current_email:
                # Replace domain
                new_email = current_email.replace('pinnacle-oa.com', 'harborglobal.com')
                update_user_email(user_id, new_email)

        page += 1

if __name__ == "__main__":
    main()
