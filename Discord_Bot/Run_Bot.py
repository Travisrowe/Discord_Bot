import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get
import youtube_dl
import asyncio
import random

# BOT_PREFIX = '?'
BOT_PREFIX = ('?', '!', '$')
curse_words = ['fuck', 'bitch', 'shit', 'ass', 'damn']
offensive_words = ['nigga', "nigger", 'cunt', 'whore', 'hoe', 'damn', 'cunt']
TOKEN = open("token.txt","r").read()
players = {}

client = commands.Bot(command_prefix=BOT_PREFIX, description='A bot that greets the user back.')
# bot = commands.Bot(command_prefix=BOT_PREFIX, description='A bot that greets the user back.')

@client.event
async def on_ready():
    print("The Bot is ready!")
    await client.change_presence(game=discord.Game(name="Helping dumbasses"))

#client events do not look for BOT_PREFIX
@client.event
async def on_message(message):
    #don't want the bot responding to itself
    if message.author == client.user:
        return
    
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    if message.content.lower() in curse_words:
        # player = await create_ytdl_player("https://www.youtube.com/watch?v=25f2IgIrkD4")
        await message.channel.send("https://media1.tenor.com/images/a051059c7642e9a474a13e1ab7191fb6/tenor.gif?itemid=5600117")
        #await message.channel.send('Hi!')

    elif message.content.lower() in offensive_words:
        # player = await create_ytdl_player("https://www.youtube.com/watch?v=25f2IgIrkD4")
        await message.channel.send("https://media0.giphy.com/media/70orEIVDASzXW/giphy.gif")
        await message.channel.send("Woah...")

    elif "hello" in message.content.lower():
        await message.channel.send('Hi!')
    
    #Not putting this line at the end of the on_message function can block all other events from being processed
    #source https://discordpy.readthedocs.io/en/rewrite/faq.html#commands-extension
    await client.process_commands(message)

'''
bot commands. These look for messages that start with characters in the
BOT_PREFIX tuple

type ?help or !help or $help to list commands in the discord
'''

@client.command()
async def add(ctx, a: int, b: int):
    await ctx.channel.send(a+b)

@client.command()
async def multiply(ctx, a: int, b: int):
    await ctx.send(a*b)

@client.command()
async def greet(ctx):
    await ctx.send(":smiley: :wave: Hello, there!")

@client.command()
async def cat(ctx):
    await ctx.send("https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif")

@client.command()
async def eight_ball(ctx):
    possible_responses = [
        'That is a resounding no',
        'Hell to the nah-nah-nah',
        #TODO: Add more responses
    ]
    await ctx.send(random.choice(possible_responses))

'''
Voice chat functions
'''
@client.command(pass_context=True)
async def join(ctx):
    #await ctx.send("Starting join")
    channel = ctx.message.author.voice.channel
    #await ctx.send(str(channel))

    #outdated methods
    #await client.join_voice_channel(channel)
    #await ctx.voice_client.move_to(channel)

    #https://stackoverflow.com/questions/55321681/discord-py-voicestate-object-has-no-attribute-voice-channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    # source = FFmpegPCMAudio('1.m4a')
    # player = voice.play(source)

@client.command(pass_context=True)
async def leave(ctx):
    await ctx.send("Starting leave")
    await ctx.voice_client.disconnect()

@client.command()
async def airhorn(ctx):
    await ctx.send("Starting Airhorn")

    #currently not working!
    #TODO: use code from join to join channel

    #use source = FFmpegPCMAudio('1.m4a')
        # player = voice.play(source)
    #as well as youtube_dl
    #to play audio
    #while not player.is_done():
    #    await asyncio.sleep(1)
    #use code from leave to disconnect

# I found this and tried to test it but I can't get the bot to
# join the voice channel
# In order to do this you must install ffmpeg, add it to you path, and pip install -U youtube_dl
# I can show you these steps or you can just follow this video https://www.youtube.com/watch?v=MbhXIddT2YY
@client.command(pass_context=True)
async def play(ctx, url):
    #join channel user is in
    channel = ctx.message.author.voice.channel
    #https://stackoverflow.com/questions/55321681/discord-py-voicestate-object-has-no-attribute-voice-channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    #play audio
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = players
    player.start()
    # while not player.is_done(): #don't leave until player is done
    #    await asyncio.sleep(1)
    await asyncio.sleep(5)

    #leave channel
    await ctx.send("Starting leave")
    await ctx.voice_client.disconnect()

#The bot joins the channel and awaits commands. This is neccessary!
client.run(TOKEN)