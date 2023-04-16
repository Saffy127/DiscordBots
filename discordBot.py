import os
import time
import requests
from bs4 import BeautifulSoup
from discord.ext import commands, tasks

TOKEN = 'your_bot_token'  # Replace with your bot token
BOUNTY_URL = 'https://replit.com/bounties'
CHANNEL_ID = 123456789012345678  # Replace with the target Discord channel ID

bot = commands.Bot(command_prefix='!')

last_bounties = []

def get_bounties():
    response = requests.get(BOUNTY_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    bounty_elements = soup.select('.bounty-post')
    bounties = []

    for bounty in bounty_elements:
        title = bounty.select_one('.bounty-post-title').text.strip()
        link = BOUNTY_URL + bounty.select_one('.bounty-post-title')['href']
        amount = bounty.select_one('.bounty-post-amount').text.strip()
        bounties.append({'title': title, 'link': link, 'amount': amount})

    return bounties

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    check_bounties.start()

@tasks.loop(minutes=10)
async def check_bounties():
    global last_bounties

    new_bounties = get_bounties()

    if last_bounties:
        for bounty in new_bounties:
            if bounty not in last_bounties:
                channel = bot.get_channel(CHANNEL_ID)
                await channel.send(f"New Replit bounty: {bounty['title']} - {bounty['amount']} - {bounty['link']}")

    last_bounties = new_bounties

bot.run(TOKEN)
