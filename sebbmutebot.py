import discord

TOKEN = 'MTIyODA0MTcxMDE5MDQ2NTA5NQ.G1efdl.eXHrrmzTSUCqgDdvFDZRKnodtdalug-0XBJ1ik' #discord bot token
SERVER_ID = '372827135594725376' #discord server id
CHANNEL_ID = '1227333701554143252' #discord server kanal id
TARGET_USER_ID = '424232360960196621' #discord nutzer id

client = discord.Client()

@client.event
async def on_ready():
    print(f'Eingeloggt als {client.user}')

@client.event
async def on_voice_state_update(member, before, after):
    if before.self_mute != after.self_mute or before.self_deaf != after.self_deaf
        if after.self_mute:
            message = f'{member.name} ist nun muted.'
        elif after.self_deaf:
            message = f'{member.name} ist nun full mute.'
        else:
            message = f'{member.name} ist nun wieder entmuted.'
        
        guild = client.get_guild(int(SERVER_ID))
        channel = guild.get_channel(int(CHANNEL_ID))

        await channel.send(message)

client.run(TOKEN)