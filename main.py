import requests
import os
from datetime import datetime, timezone, timedelta

# --- DRAGON CONFIGURATION ---
CLUB_ID = 480838  # Basel Dragon Club ID
WAIT_MINUTES = 10 # Delay after activity ends
LOG_FILE = "praised_activities.txt"

# --- THE VIP LIST ---
# Add the Strava Athlete IDs of the specific people you want to praise here
DRAGON_VIPS = [
    75425755,  # Janne
    # 1234567, # Add more IDs here, separated by commas
]

def get_custom_comments(activity):
    """
    SIMPLE MODE: Every VIP gets this comment.
    """
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
    print(f"🐲 Dragon Bot scanning Club {CLUB_ID} for VIPs...")
    token = get_access_token()
    if not token: return
    headers = {'Authorization': f'Bearer {token}'}
    
    # Fetch club feed
    url = f"https://www.strava.com/api/v3/clubs/{CLUB_ID}/activities"
    res = requests.get(url, headers=headers)
    activities = res.json()
    
    if not isinstance(activities, list):
        print(f"⚠️ API Issue: {activities}")
        return

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f: processed = f.read().splitlines()
    else: processed = []

    for act in activities:
        act_id = str(act['id'])
        athlete_id = act.get('athlete', {}).get('id')

        # 1. VIP FILTER: Ignore anyone not in our list
        if athlete_id not in DRAGON_VIPS:
            continue

        # 2. DUPLICATE FILTER: Don't praise twice
        if act_id in processed: 
            continue

        # 3. 10-MINUTE TIMER LOGIC
        try:
            start_dt = datetime.strptime(act['start_date'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            duration = timedelta(seconds=act['elapsed_time'])
            finish_time = start_dt + duration
            now = datetime.now(timezone.utc)
            
            if now < (finish_time + timedelta(minutes=WAIT_MINUTES)):
                print(f"⏳ VIP activity {act_id} is too fresh. Waiting.")
                continue
        except KeyError:
            pass 

        # --- ACTION: KUDOS & COMMENTS FOR VIPS ONLY ---
        requests.post(f"https://www.strava.com/api/v3/activities/{act_id}/kudos", headers=headers)
        
        msgs = get_custom_comments(act)
        for msg in msgs:
            requests.post(f"https://www.strava.com/api/v3/activities/{act_id}/comments", 
                          headers=headers, data={'text': msg})
        
        with open(LOG_FILE, "a") as f: f.write(act_id + "\n")
        print(f"✅ VIP Praise sent for activity {act_id} (Athlete: {athlete_id})")

if __name__ == "__main__":
    run_bot()
