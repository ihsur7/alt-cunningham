#
import random
import discord
from discord.ext import commands
import asyncio
import praw
import youtube_dl

TOKEN = 'NDU5NjE0MjQxOTM5MjU5NDA0.Dg4w7Q.u_bVogw0I5awXw_WNavop083_uU'

BOT_PREFIX = ('.')

bot = commands.Bot(command_prefix = BOT_PREFIX)
bot.remove_command('help')

players = {}
queues = {}

def check_queues(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()

reddit = praw.Reddit(client_id='3_2IOgyYY7TXHQ',
                     client_secret='Nmema0LT5M4xsNz8kPyktB-u4Lc',
                     user_agent='praw-discord')

@bot.event
async def on_ready():
    print('Running on ' + bot.user.name)
    print('ID: ' + bot.user.id)
    # msg = '*beep*'
    # for server in bot.servers:
    #     for channel in server.channels:
    #         if channel.name == 'bot':
    #             message = await bot.send_message(channel, msg)
    #             await asyncio.sleep(3)
    #             await bot.delete_message(message)
    #             await asyncio.sleep(4)
    await bot.change_presence(game = discord.Game(name = 'Cyberpunk 2077'))

@bot.command()
async def ping():
    await bot.say('Pong!')

@bot.command(pass_context=True)
async def permission(ctx):
    author = ctx.message.author
    if 'rockerboy' in [y.name.lower() for y in author.roles]:
        await bot.say('You have permission.')
    elif 'corporate' in [x.name.lower() for x in author.roles]:
        await bot.say('You have permission.')
    else: 
        await bot.say('No, you do not have permission.')

@bot.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await bot.say(output)

# @bot.command(pass_context=True)
# async def clear(ctx, amount=100):
#     channel = ctx.message.channel
#     messages = []
#     async for message in bot.logs_from(channel, limit = int(amount)):
#         messages.append(message)
#     await bot.delete_messages(messages)
#     await bot.say('Messages deleted.')

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name = 'solo')
    await bot.add_roles(member, role)

@bot.command(pass_context=True)
async def info(ctx):
    embed = discord.Embed(
        title = '//information',
        description = 'Developer of Soulkiller (Beta). Murdered by Saburo Arasaka, my ghost now roams the Net.',
        colour = 0xff0075
    )
    embed.set_thumbnail(url = bot.user.avatar_url)
    embed.set_author(name = '//cunningham-alt')#bot.user.name)#, icon_url=bot.user.avatar_url)
    embed.add_field(name='//created at', value=bot.user.created_at, inline=True)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        color = 0xff0075
    )
    embed.set_author(name='Help')
    embed.add_field(name='.info', value='Returns Bot Information', inline=False)
    embed.add_field(name='.ping', value='Returns Pong!', inline=False)
    embed.add_field(name='.join', value='Joins the channel invoker is currently in.', inline=False)
    embed.add_field(name='.leave', value='Leaves the current voice channel.', inline=False)

    await bot.send_message(author, embed=embed)

@bot.command(pass_context=True)
async def join(ctx):
    while True:
        try:
            channel = ctx.message.author.voice.voice_channel
            await bot.join_voice_channel(channel)
            break
        except discord.errors.InvalidArgument:
            await bot.send_message(ctx.message.channel, '<@%s>, call me after joining a voice channel.' %ctx.message.author.id)
            break
        except discord.errors.ClientException:
            await bot.send_message(ctx.message.channel, '<@%s>, I am already in a channel.' %ctx.message.author.id)
            break

@bot.command(pass_context=True)
async def leave(ctx):
    while True:
        try:
            server = ctx.message.server
            voice_client = bot.voice_client_in(server)
            await voice_client.disconnect()
            break
        except AttributeError:
            await bot.send_message(ctx.message.channel, '<@%s>, I have already left voice-chat.' %ctx.message.author.id)
            break

@bot.command(pass_context=True)
async def play(ctx, url):
    while True:
        try:
            server = ctx.message.server
            voice_client = bot.voice_client_in(server)
            player = await voice_client.create_ytdl_player(url, after=lambda: check_queues(server.id))
            players[server.id] = player
            player.start()
            break
        except AttributeError:
            await bot.send_message(ctx.message.channel, '<@%s>, add me to a channel first.' %ctx.message.author.id)
            break

@bot.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()

@bot.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()

@bot.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()

@bot.command(pass_context=True)
async def queue(ctx, url):
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queues(server.id))
    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await bot.say('Video queued.')

@bot.command(pass_context=True)
async def playlist(ctx):
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    embed = discord.Embed(
        color = 0xff0075
    )
    embed.set_author(name='Help')
    embed.add_field(name='.info', value='Returns Bot Information', inline=False)
    embed.add_field(name='.ping', value='Returns Pong!', inline=False)
    embed.add_field(name='.join', value='Joins the channel invoker is currently in.', inline=False)
    embed.add_field(name='.leave', value='Leaves the current voice channel.', inline=False)

    await bot.send_message(ctx.message.channel, embed=embed)

# @bot.command(pass_context=True)
# async def next(ctx):
#     id = ctx.message.server.id
#     print(players)
#     print(queues)
    # players[id].next()
    

# @bot.event
# async def on_message_delete(message):
#     if message.author == bot.user:
#         return
#     else:
#         author = message.author
#         content = message.content
#         channel = message.channel
#         await bot.send_message(channel, '{}: {}'.format(author, content))

#@bot.command(name='hi')
#async def bot():
#    message = 'Hey {0.author.mention}!'.format(message)
#    await bot.send_message(message.channel, message)

#@bot.event
#async def on_message(message):
#    if message.author == client.user:
#        return
#    if message.content.startswith('.hello'):
#        message = 'Hello {0.author.mention}'.format(message)
#        await client.send_message(message.channel, message)

bot.run(TOKEN)
