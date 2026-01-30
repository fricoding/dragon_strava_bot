🐉 Basel Dragon Support Bot: The Setup Guide
Hey Dragon! If you want to automate some love for your running buddies, you're in the right place. This bot watches our club feed and drops a kudo and a "Great run!" comment exactly 10 minutes after your favorite people finish their workout.

🛡️ First: Is it safe?
Yes. Your Strava "keys" (the codes that let the bot talk to your account) are never written in the actual code. We use GitHub Secrets, which act like a digital vault. Only you can put keys in, and GitHub hides them with asterisks (***) whenever the bot is running.

🚀 Step-by-Step Instructions
1. Copy the Project
At the top of this page, click the green "Use this template" button.

Give your new project a cool name (like Support-Bot-For-The-Team) and click "Create repository".

2. Get your Strava "Passport"
Go to the Strava API Dashboard.

You’ll need three things from here: your Client ID, your Client Secret, and a Refresh Token.

Tip: If you don't have a Refresh Token yet, you might need to run a quick authorization step to get one with activity:write permissions.

3. Lock your Keys in the Vault
In your new GitHub project, go to Settings (the gear icon at the top).

On the left sidebar, click Secrets and variables > Actions.

Click New repository secret for each of these:

Name: STRAVA_CLIENT_ID | Value: (Your numeric ID)

Name: STRAVA_CLIENT_SECRET | Value: (Your secret code)

Name: STRAVA_REFRESH_TOKEN | Value: (Your refresh token)

4. Pick your VIPs
Open the main.py file in your project and click the pencil icon to edit.

Look for the DRAGON_VIPS list. Replace the numbers there with the Athlete IDs of the friends you want to cheer on.

How to find an ID? Open their Strava profile in a web browser; the number is at the end of the URL.

5. Turn it On
Go to the Actions tab at the top of your repository.

Click the big blue button that says "I understand my workflows, go ahead and enable them".

That's it! The bot will now wake up every 30 minutes to check if your VIPs have been running.
