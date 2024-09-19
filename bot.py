import os
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment variables for GitHub and Discord
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME')
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
REPO_OWNER = os.environ.get('REPO_OWNER')  # e.g., 'prabinpanta0'
REPO_NAME = os.environ.get('REPO_NAME')    # e.g., 'F-U'

headers = {'Authorization': f'token {GITHUB_TOKEN}'}

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
tree = bot.tree  # Access the application commands (slash commands) tree


def get_following():
    following = []
    page = 1
    while True:
        url = f'https://api.github.com/users/{GITHUB_USERNAME}/following?per_page=100&page={page}'
        response = requests.get(url, headers=headers)
        data = response.json()
        if not data:
            break
        following.extend([user['login'] for user in data])
        page += 1
    return following


def get_followers():
    followers = []
    page = 1
    while True:
        url = f'https://api.github.com/users/{GITHUB_USERNAME}/followers?per_page=110&page={page}'
        response = requests.get(url, headers=headers)
        data = response.json()
        if not data:
            break
        followers.extend([user['login'] for user in data])
        page += 1
    return followers


# Event: When the bot is ready
@bot.event
async def on_ready():
    await tree.sync()  # Sync slash commands with Discord
    print(f'{bot.user} is ready and online!')


# Slash Command: View the number of followers
@tree.command(name="viewfollowers", description="Shows the number of followers on GitHub")
async def viewfollowers(interaction: discord.Interaction):
    await interaction.response.send_message(f"You have {len(get_followers())} followers.")


# Slash Command: View the number of following
@tree.command(name="viewfollowing", description="Shows the number of users you are following on GitHub")
async def viewfollowing(interaction: discord.Interaction):
    await interaction.response.send_message(f"You are following {len(get_following())} users.")


# Slash Command: List n followers
@tree.command(name="listfollowers", description="Lists the first n followers")
async def listfollowers(interaction: discord.Interaction, n: int):
    # Defer the interaction to avoid timing out
    await interaction.response.defer(thinking=True)

    # Fetch the followers
    followers = get_followers()

    # Send the final message after fetching the data
    await interaction.followup.send(f"First {n} followers: {', '.join(followers[:n])}")



# Slash Command: List n following
@tree.command(name="listfollowing", description="Lists the first n users you are following")
async def listfollowing(interaction: discord.Interaction, n: int):
    await interaction.response.defer(thinking=True)
    following = get_following()
    await interaction.followup.send(f"First {n} following: {', '.join(following[:n])}")


# Slash Command: Manually trigger the follow-unfollow GitHub Action
@tree.command(name="runfu", description="Runs the Follow-Unfollow bot")
async def runfu(interaction: discord.Interaction):
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/main.yml/dispatches'
    payload = {
        "ref": "main"  # Branch to run the action on
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 204:
        await interaction.response.send_message('GitHub action triggered successfully.')
    else:
        await interaction.response.send_message(f'Failed to trigger action. Status code: {response.status_code}')


# Error handling for unknown commands
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Please check the command and try again.")


# Start the bot
bot.run(DISCORD_TOKEN)
