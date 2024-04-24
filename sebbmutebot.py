import discord # type: ignore
from datetime import datetime
import pytz # type: ignore
import sqlite3

# Discord Bot mit Python
intents = discord.Intents.default()
intents.voice_states = True

# Discord Bot Token und IDs
TOKEN = 'INSERT BOT TOKEN' #discord bot token
SERVER_ID = '' #insert discord server id
CHANNEL_ID = '' #insert discord server channel id
TARGET_USER_ID = '' #insert discord user id
COMMAND_PREFIX = '!' #insert command prefix

# SQL-Datenbank verbinden
conn = sqlite3.connect('mute_tracker.db')
c = conn.cursor()

# SQL-Tabelle erstellen, sofern noch nicht existiert
c.execute('''CREATE TABLE IF NOT EXISTS mute_tracker
          (user_id TEXT, mute_time TEXT, mute_status TEXT)''')
conn.commit()

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
             message = f'{member.name} hat sich um {timestamp} full muted. <:muted:1217086196543520818> '
            elif after.self_mute:
             message = f'{member.name} hat sich um {timestamp} gemuted. <:muted:1217086196543520818> '
            else:
             message = f'{member.name} hat sich um {timestamp} entmuted. <:muted:1217086196543520818> '
        
            guild = client.get_guild(int(SERVER_ID))
            channel = guild.get_channel(int(CHANNEL_ID))

        await channel.send(message)

        c.execute("INSERT INTO mute_tracker VALUES (?, ?, ?)", (member.id, timestamp, 'muted' if after.self_mute else 'unmuted'))
        conn.commit()

async def on_message(message):
   if message.content.startswith(COMMAND_PREFIX + 'mutetime'):
        user_id = TARGET_USER_ID
        total_mute_time = get_total_mute_time(user_id) #USER_ID eintragen

        hours = int(total_mute_time // 3600)
        minutes = int((total_mute_time % 3600) // 60)
        seconds = int(total_mute_time % 60)

        await message.channel.send(f"Sebb war insgesamt {hours} Stunden, {minutes} Minuten und {seconds} Sekunden stumm.")


def get_total_mute_time(user_id):
    c.execute("SELECT * FROM mute_history WHERE user_id=?", (user_id,))
    rows = c.fetchall()
    total_mute_time = 0
    last_timestamp = None 

    for row in rows:
        if row[2] == 'muted':
            last_timestamp = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
        elif row[2] == 'unmuted' and last_timestamp is not None:
            total_mute_time += (datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S") - last_timestamp).total_seconds()
            last_timestamp = None

    return total_mute_time


client.run(TOKEN)

