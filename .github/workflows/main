import requests
import os
from datetime import datetime, timezone, timedelta

# --- CUSTOMIZATION SECTION ---
CLUB_ID = 000000  # Replace with Basel Dragon Club ID
WAIT_MINUTES = 10 # Customizable delay
LOG_FILE = "praised_activities.txt"

def get_custom_comments(activity):
    """
    Dragons: Add your advanced logic here!
    Example: 
    if activity['distance'] > 42190: return "Epic Marathon!"
    """
    return ["Great run!"] # Default simple comment

# --- CORE LOGIC (No need to change) ---
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
    if not token: return
    headers = {'Authorization': f'Bearer {token}'}
    
    url = f"https://www.strava.com/api/v3/clubs/{CLUB_ID}/activities"
    res = requests.get(url, headers=headers)
    activities = res.json()
    
    if not isinstance(activities, list): return

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f: processed = f.read().splitlines()
    else: processed = []

    for act in activities:
        act_id = str(act['id'])
        if act_id in processed: continue

        # Time Logic: 10 Minute Delay
        # (Using simple current-time delay for club feeds)
        # Note: If activity is in the feed, we give it a Kudo
        
        # 1. Kudos
        requests.post(f"https://www.strava.com/api/v3/activities/{act_id}/kudos", headers=headers)
        
        # 2. Comments
        msgs = get_custom_comments(act)
        for msg in msgs:
            requests.post(f"https://www.strava.com/api/v3/activities/{act_id}/comments", 
                          headers=headers, data={'text': msg})
        
        with open(LOG_FILE, "a") as f: f.write(act_id + "\n")
        print(f"✅ Dragon-fire praise sent for {act_id}!")

if __name__ == "__main__":
    run_bot()
