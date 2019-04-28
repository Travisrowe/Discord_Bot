import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
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

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    if "hello" in message.content.lower():
        await message.channel.send('Hi!')
    
    #Not putting this line at the end of the on_message function can block all other events from being processed
    #source https://discordpy.readthedocs.io/en/rewrite/faq.html#commands-extension
    await client.process_commands(message)

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

@client.command()
async def airhorn(context):
    await context.send("Starting Airhorn")
    user = context.message.author
    await context.send(str(user))
    await context.send(str(user.voice.voice_channel))
    voice_channel = user.voice.voice_channel
    await context.send(str(voice_channel.name))
    channel = None
    if voice_channel != None:
        channel = voice_channel.name
        await client.say('User is in channel: ' + channel)
        vc = await client.join_voice_channel(voice_channel)
        player = vc.create_ffmpeg_player('vuvuzela.mp3', after=lambda: print('done'))
        player.start()
        while not player.is_done():
            await asyncio.sleep(1)
        player.stop()
        await vc.disconnect()
    else:
        await client.say('User is not in a channel.')

client.run(TOKEN)