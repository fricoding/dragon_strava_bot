import requests
import os
import random
from datetime import datetime, timezone, timedelta

# --- CONFIGURATION ---
# Basel Dragon Club ID
CLUB_ID = 480838 
# Minutes to wait after an activity finishes before the bot acts
WAIT_MINUTES = 10 
LOG_FILE = "praised_activities.txt"

def get_custom_comments(activity):
    """
    MEMBERS: Customize your praise here!
    You can add logic for distance, elevation, or heart rate.
    """
    # Default simple praise
    return ["Great run!"] 

def get_access_token():
    res = requests.post('https://www.strava.com/oauth/token', data={
        'client_id': os.getenv('STRAVA_CLIENT_ID'),
        'client_secret': os.getenv('STRAVA_CLIENT_SECRET'),
        'refresh_token': os.getenv('STRAVA_REFRESH_TOKEN'),
        'grant_type': 'refresh_token'
    })
    return res.json().get('access_token')

def run_bot():
    print(f"🐲 Dragon Bot checking Club {CLUB_ID}...")
    token = get_access_token()
    if not token: 
        print("❌ Error: Could not get access token.")
        return
        
    headers = {'Authorization': f'Bearer {token}'}
    url = f"https://www.strava.com/api/v3/clubs/{CLUB_ID}/activities"
    res = requests.get(url, headers=headers)
    activities = res.json()
    
    if not isinstance(activities, list):
        print(f"⚠️ API issue: {activities}")
        return

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f: processed = f.read().splitlines()
    else: 
        processed = []

    for act in activities:
        act_id = str(act['id'])
        if act_id in processed: 
            continue

        # 10-Minute Delay Logic
        # Strava provides 'start_date' and 'elapsed_time' in the club feed
        try:
            start_dt = datetime.strptime(act['start_date'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            duration = timedelta(seconds=act['elapsed_time'])
            finish_time = start_dt + duration
            now = datetime.now(timezone.utc)
            
            if now < (finish_time + timedelta(minutes=WAIT_MINUTES)):
                print(f"⏳ Activity {act_id} is too fresh. Waiting for the {WAIT_MINUTES}m mark.")
                continue
        except KeyError:
            # If timing data is missing from the feed, we skip the delay for safety
            pass

        # 1. Give Kudos
        requests.post(f"https://www.strava.com/api/v3/activities/{act_id}/kudos", headers=headers)
        
        # 2. Add Comments
        msgs = get_custom_comments(act)
        for msg in msgs:
            requests.post(f"https://www.strava.com/api/v3/activities/{act_id}/comments", 
                          headers=headers, data={'text': msg})
        
        with open(LOG_FILE, "a") as f: f.write(act_id + "\n")
        print(f"✅ Dragon-fire praise sent for activity {act_id}!")

if __name__ == "__main__":
    run_bot()
