import discord
from datetime import datetime

intents = discord.Intents.default()
intents.voice_states = True

TOKEN = 'INSERT BOT TOKEN' #discord bot token
SERVER_ID = '' #insert discord server id
CHANNEL_ID = '' #insert discord server channel id
TARGET_USER_ID = '' #insert discord user id

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Eingeloggt als {client.user}')

@client.event
async def on_voice_state_update(member, before, after):
    if member.id == int(TARGET_USER_ID):
        if before.self_mute != after.self_mute or before.self_deaf != after.self_deaf:
            now = datetime.now()
            timestamp = now.strftime("%H:%M Uhr")
            if after.self_mute:
             message = f'{member.name} hat sich um {timestamp} gemuted.'
            elif after.self_deaf:
             message = f'{member.name} hat sich um {timestamp} full muted.'
            else:
             message = f'{member.name} hat sich um {timestamp} entmuted.'
        
            guild = client.get_guild(int(SERVER_ID))
            channel = guild.get_channel(int(CHANNEL_ID))

        await channel.send(message)

client.run(TOKEN)

