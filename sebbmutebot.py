import discord
from datetime import datetime
import pytz

intents = discord.Intents.default()
intents.voice_states = True

TOKEN = 'INSERT BOT TOKEN' #discord bot token
SERVER_ID = '' #insert discord server id
CHANNEL_ID = '' #insert discord server channel id
TARGET_USER_ID = '' #insert discord user id

client = discord.Client(intents=intents)
german_timezone = pytz.timezone('Europe/Berlin')

@client.event
async def on_ready():
    print(f'Eingeloggt als {client.user}')

@client.event
async def on_voice_state_update(member, before, after):
    if member.id == int(TARGET_USER_ID):
        if before.self_mute != after.self_mute or before.self_deaf != after.self_deaf:
            now_utc = datetime.now(pytz.utc) #aktuelle UTC-Zeit abrufen
            now_germany = now_utc.replace(tzinfo=pytz.utc).astimezone(german_timezone) #Zeit in DE abrufen
            timestamp = now_germany.strftime("%H:%M Uhr") #Zeit im gewünschten Format abrufen
 
            if after.self_deaf:
             message = f'{member.name} hat sich um {timestamp} full muted.'
            elif after.self_mute:
             message = f'{member.name} hat sich um {timestamp} gemuted.'
            else:
             message = f'{member.name} hat sich um {timestamp} entmuted.'
        
            guild = client.get_guild(int(SERVER_ID))
            channel = guild.get_channel(int(CHANNEL_ID))

        await channel.send(message)

client.run(TOKEN)

