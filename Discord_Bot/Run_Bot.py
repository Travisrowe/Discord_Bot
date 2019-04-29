import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get
import asyncio
import random

# BOT_PREFIX = '?'
BOT_PREFIX = ('?', '!', '$')
TOKEN = open("token.txt","r").read()

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
    if "hello" in message.content.lower():
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
    await ctx.send("Starting join")
    channel = ctx.message.author.voice.channel
    await ctx.send(str(channel))
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
    source = FFmpegPCMAudio('1.m4a')
    player = voice.play(source)

async def leave(ctx):
    

@client.command()
async def airhorn(ctx):
    await ctx.send("Starting Airhorn")
    #server = ctx.message.server
    #gets the user that typed the message
    user = ctx.message.author
    
    await ctx.send(str(user))
    #get the voice channel user is in. this is currently not working!
    voice_channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(voice_channel)
    await ctx.send("voice channel name: " + str(voice_channel.name))
    await ctx.send("voice channel: " + str(voice_channel))
    channel = None
    #if user is in voice channel
    if voice_channel != None:
        channel = voice_channel.name
        await ctx.send('User is in channel: ' + channel)
        #join the voice channel
        vc = await client.join_voice_channel(voice_channel)
        #play the sound
        player = vc.create_ffmpeg_player('vuvuzela.mp3', after=lambda: print('done'))
        player.start()
        #wait until the sound is done before the bot disconnects
        while not player.is_done():
            await asyncio.sleep(1)
        player.stop()
        #bot disconnects
        await vc.disconnect()
    else:
        await ctx.send('User is not in a channel.')

#The bot joins the channel and awaits commands. This is neccessary!
client.run(TOKEN)