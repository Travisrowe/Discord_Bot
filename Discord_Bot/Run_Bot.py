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

#Global vars for playing audio
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

# Suppress noise about console usage from error
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

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
    # await ctx.send("Starting leave")
    await ctx.voice_client.disconnect()

# @client.command()
# async def airhorn(ctx):
#     await ctx.send("Starting Airhorn")

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
# @client.command(pass_context=True)
# async def play(ctx, url):
#     #join channel user is in
#     channel = ctx.message.author.voice.channel
#     #https://stackoverflow.com/questions/55321681/discord-py-voicestate-object-has-no-attribute-voice-channel
#     if not channel:
#         await ctx.send("You are not connected to a voice channel")
#         return
#     voice = get(client.voice_clients, guild=ctx.guild)
#     if voice and voice.is_connected():
#         await voice.move_to(channel)
#     else:
#         voice = await channel.connect()

#     #play audio
#     server = ctx.message.server
#     voice_client = client.voice_client_in(server)
#     player = await voice_client.create_ytdl_player(url)
#     players[server.id] = players
#     player.start()
#     # while not player.is_done(): #don't leave until player is done
#     #    await asyncio.sleep(1)
#     await asyncio.sleep(5)

#     #leave channel
#     await ctx.send("Starting leave")
#     await ctx.voice_client.disconnect()

'''
The following code directly from Discord.py's documentation.
https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py
'''
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(query))

    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        ctx.send("Starting ensure_voice")
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

client.add_cog(Music(client))
#The bot joins the channel and awaits commands. This is neccessary!
client.run(TOKEN)