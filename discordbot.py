#
from distutils import errors
from multiprocessing.sharedctypes import Value
import random

from click import pass_context
import discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
import praw
import youtube_dl
# from steam.client import SteamClient
# from dota2.client import Dota2Client
from mytoken import MYTOKEN 
import pandas as pd
import numpy as np
import os
import time
from threading import Thread, Timer
import sys
from decimal import Decimal
import regex
import csv
import datetime
import requests



TOKEN = MYTOKEN
global timer
timer = 120 #seconds
BOT_PREFIX = ('.')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = BOT_PREFIX, intents=intents)
bot.remove_command('help')

bet_df = pd.DataFrame(columns=("guild","id", "wl", "points"))
BET_ACTIVE = False

BET_CLOSED = True

# sclient = SteamClient()
# dota = Dota2Client(sclient)

# @sclient.on('logged_on')
# def start_dota():
#     dota.launch()

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
    print('ID: ' + str(bot.user.id))
    # msg = '*beep*'
    # for server in bot.servers:
    #     for channel in server.channels:
    #         if channel.name == 'bot':
    #             message = await bot.send_message(channel, msg)
    #             await asyncio.sleep(3)
    #             await bot.delete_message(message)
    #             await asyncio.sleep(4)
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('Cyberpunk 2077'))
    # await isinbulldogstream.start()

@bot.command()
# async def on_message(message):
#     if message.content.startswith('ping'):
#         channel = message.channel
#         await channel.send('pong!')
async def ping(ctx):
    channel = ctx.message.channel
    await channel.send('Pong!')

@bot.command()
async def quit(ctx):
    await bot.logout()

@bot.command(pass_context=True)
async def permission(ctx):
    author = ctx.message.author
    if 'rockerboy' in [y.name.lower() for y in author.roles]:
        await bot.say('You have permission.')
    elif 'corporate' in [x.name.lower() for x in author.roles]:
        await bot.say('You have permission.')
    elif 'nomad' in [z.name.lower() for z in author.roles]:
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
    # embed.add_field(name='.join', value='Joins the channel invoker is currently in.', inline=False)
    # embed.add_field(name='.leave', value='Leaves the current voice channel.', inline=False)
    embed.add_field(name='.points', value='Returns your current points.', inline="False")
    embed.add_field(name='.roulette', value='Play a game of chance.', inline=False)
    embed.add_field(name='.startbet', value=f'Starts a bet and accepts bets for {timer} seconds.', inline=False)
    embed.add_field(name='.bet [win/lose] [amount]', value='Place a bet (if active). Amount must be an Integer.', inline=False)
    embed.add_field(name='.endbet [win/lose]', value='End the current bet and distribute results.', inline=False)
    embed.add_field(name='.ban [mention]', value="Restricts the mentioned user's ability to chat via voice for 5 minutes. Costs 150,000 points.", inline=False)
    embed.add_field(name='.leaderboard', value='Returns a Leaderboard with their current points.', inline=False)
    await ctx.author.send(embed=embed)

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

async def global_df(df):
    global bet_df
    if bet_df is not None:
        bet_df = pd.concat([bet_df, df], axis=0)
    return bet_df

@bot.command(pass_context=True)
async def bet(ctx, *args):
    if BET_ACTIVE == False:
        await ctx.channel.send("No active bets. Please try again later.")
        return
    if len(args) > 2:
        await ctx.channel.send(f"Unkown command, please type {BOT_PREFIX}bet win/lose #.")
        return
    wl = args[0]
    if wl not  in ['win','lose']:
        await ctx.channel.send(f"Unkown command {wl}. Please type either 'win' or 'lose'.")
        return
    betpoints = args[1]
    df = pd.read_csv(f'database-{str(ctx.guild)}.csv', index_col=False)
    df_numpy = df.to_numpy()
    member = hex(ctx.message.author.id)
    guild = ctx.message.guild
    match = df[df["id"]==member]["id"]
    if member in bet_df['id'].values:
        await ctx.author.send('You have already bet on this game.')
        return
    try:
        betpoints = int(betpoints)
        if betpoints < 1:
            await ctx.channel.send("Invalid betting amount. Must be greater than 0.")
            return
        for i in df_numpy:
            if i[0] == member:
                points = i[-1]
        if points < betpoints:
            await ctx.channel.send(f"You only have {int(df.iloc[(match.index, 2)])} points available.")
            return
    except (TypeError, ValueError):
        if betpoints == 'all':
            betpoints = int(df.loc[df['id'] == member].values[0][2])
        else:
            await ctx.channel.send("Amount must be either 'all' or an Integer greater than 0.")
            return
    df_temp = pd.DataFrame(data=[[guild, member, wl, betpoints]], columns=("guild", "id", "wl","points"))
    bet_df1 = await global_df(df_temp)
    await ctx.author.send(f"You have bet {betpoints} points on this game resulting in a {wl}.")
    return

@bot.command(pass_context=True)
async def points(ctx):
    df = pd.read_csv(f'database-{str(ctx.guild)}.csv', index_col=False)
    member = hex(ctx.message.author.id)
    points = int(df.loc[df['id'] == member].values[0][2])
    await ctx.author.send(f"You have {int(points)} points.")
    return

@bot.command(pass_context=True)
@commands.cooldown(1, timer, commands.BucketType.guild)
async def startbet(ctx):
    global BET_ACTIVE, BET_CLOSED, bet_df
    BET_ACTIVE = True
    BET_CLOSED = False
    bet_df = pd.DataFrame(columns=("guild","id", "wl", "points"))
    guild = ctx.guild
    try:
        df = pd.read_csv(f'database-{str(ctx.guild)}.csv', index_col=False)
    except FileNotFoundError:
        members = ctx.guild.members
        data_arr = np.zeros(shape=(1,3))
        for i in members:
            temp_df = np.asarray([[str(hex(i.id)), i.name, int(5000)]])
            data_arr = np.append(data_arr,temp_df, axis=0)
        df = pd.DataFrame(data=data_arr, columns=['id', 'name', 'totalpoints'])
        df['name'] = df['name'].str.replace('[^\w\s#@/:%.,_-]', '', flags=regex.UNICODE)
        header = ['id', 'name', 'totalpoints']
        dfnp = df.to_numpy()
        with open(f"database-{str(ctx.guild)}.csv", 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(dfnp)
        await ctx.channel.send('Database created.')
        
    await ctx.channel.send("Betting is open, you have 60 seconds.")
    await closebet(ctx)
    BET_ACTIVE = False
    if len(bet_df) == 0:
        await ctx.channel.send("No bets were placed.")
        return
    filter_df = bet_df.loc[bet_df['guild'] == guild]
    filter_numpy = filter_df.to_numpy()
    username = np.empty((len(filter_numpy), 3), dtype='object')
    for index, value in enumerate(filter_numpy):
        value[1] = int(value[1], 0)
        member = await guild.fetch_member(value[1])
        username[index][0] = member.name
        username[index][1] = value[2]
        username[index][2] = value[3]
    filternp_id = filter_numpy[:,1]
    try:
        num_win = filter_df['wl'].value_counts()['win']
    except KeyError:
        num_win = 1
    try:
        num_lose = filter_df['wl'].value_counts()['lose']
    except KeyError:
        num_lose = 1
    odds_w = num_win/(num_win+num_lose)
    odds_l = num_lose/(num_win+num_lose)
    embed = discord.Embed(
        title = '//current bet info',
        colour = 0xff0075
    )
    uname = username[:,0]
    bet = username[:,1]
    bpoints = username[:,2]
    joined_uname = '\n'.join([str(elem) for elem in uname])
    joined_bet = '\n'.join([str(elem) for elem in bet])
    joined_bpoints = '\n'.join([str(elem) for elem in bpoints])
    embed.set_thumbnail(url = bot.user.avatar_url)
    embed.set_author(name = '//alt-cunningham')#bot.user.name)#, icon_url=bot.user.avatar_url)
    embed.add_field(name='//created at', value=datetime.datetime.now().time(), inline=True)
    embed.add_field(name='Odds for Winning', value = odds_w, inline=True)
    embed.add_field(name='Odds for Losing', value=odds_l, inline=True)
    embed.add_field(name='Payout for Win Bettors', value=1/odds_w, inline=True)
    embed.add_field(name='Payout for Lose Bettors', value=1/odds_l, inline=True)
    embed.add_field(name='Number of Bettors', value = len(filter_df), inline=True)
    embed.add_field(name = 'Username', value=joined_uname, inline = True)
    embed.add_field(name = 'Bet', value=joined_bet, inline = True)
    embed.add_field(name = 'Amount', value=joined_bpoints, inline=True)
    await ctx.channel.send(embed=embed)

# 196955792304242690
async def closebet(ctx):
    await asyncio.sleep(timer)
    BET_ACTIVE = False
    await ctx.channel.send("Betting is now closed.")
    return

@bot.command(pass_context=True)
async def leaderboard(ctx):
    guild = ctx.guild
    df = pd.read_csv(f'database-{str(ctx.guild)}.csv', index_col=False)
    df = df.loc[(df != 0).all(axis=1),:]
    df = df.sort_values(by=['totalpoints'])
    dfnp = df.to_numpy()
    dfnp = dfnp[dfnp[:,1].argsort()]
    username = np.empty((len(dfnp), 2), dtype='object')
    for index, value in enumerate(dfnp):
        value[0] = int(value[0], 0)
        role = get(guild.roles, id=332710290804178945)
        memlist = [i.id for i in role.members]
        if int(value[0]) in memlist:
            username[index][0] = value[1]
            username[index][1] = int(value[2])
        else:
            username[index][0] = np.nan
            username[index][1] = np.nan
    usernamedf = pd.DataFrame(data=username, columns=['username', 'points']).dropna().sort_values(by=['points'], ascending=False)
    uname = usernamedf['username'].values
    points = usernamedf['points'].values
    joined_uname = '\n'.join([str(elem) for elem in uname])
    joined_points = '\n'.join([str(elem) for elem in points])
    embed = discord.Embed(
        title = '//leaderboard',
        colour = 0xff0075
    )
    embed.add_field(name = 'Username', value=joined_uname, inline = True)
    embed.add_field(name = 'Amount', value=joined_points, inline=True)
    await ctx.channel.send(embed=embed)
    
@bot.command(pass_context=True)
async def endbet(ctx, *args):
    global BET_CLOSED
    if BET_ACTIVE == True:
        await ctx.channel.send("Currently taking bets.")
        return
    if BET_CLOSED == True:
        await ctx.channel.send("No active bets to end.")
        return
    if len(args) != 1:
        await ctx.channel.send("Only pass one argument, 'win' or 'lose'.")
        return
    if args[0] not in ['win', 'lose']:
        await ctx.channel.send("Can only pass 'win' or 'lose'.")
        return
    guild = ctx.message.guild
    filter_df = bet_df.loc[bet_df['guild'] == guild]
    filter_numpy = filter_df.to_numpy()
    df = pd.read_csv(f'database-{str(ctx.guild)}.csv', index_col=False)
    dfnp = df.to_numpy()
    if len(filter_numpy) > 0:
        await ctx.channel.send(f"The game resulted in a {args[0]}.")
        try:
            num_win = filter_df['wl'].value_counts()['win']
        except KeyError:
            num_win = 1
        try:
            num_lose = filter_df['wl'].value_counts()['lose']
        except KeyError:
            num_lose = 1
        odds_w = num_win/(num_win+num_lose)
        odds_l = num_lose/(num_win+num_lose)
        if args[0] == 'win':
            payout = 1/odds_w
            for i in filter_df.values:
                user = bot.get_user(int(i[1], 0))
                for j in dfnp:
                    if j[0] == i[1]:
                        before_total_points = j[-1]
                betpoints = i[3]
                bet = i[2]
                if bet == args[0]:
                    st = 'won'
                    prize_points = int(payout*betpoints)
                    final_points = prize_points + before_total_points
                    await user.send(f"Your {bet} bet of {int(betpoints)} points, resulted in {args[0]}. You have {st} {int(prize_points)} points, and your total points are {int(final_points)} points.")
                else:
                    st = 'lost'
                    points = int(df.loc[df['id'] == hex(user.id)].values[0][2])
                    await user.send(f"Your {bet} bet of {int(betpoints)} points, resulted in {args[0]}. You have {st} {int(betpoints)} points, and your remaining points are {int(before_total_points-betpoints)} points.")
            filter_df.loc[filter_df['wl'] == 'win', 'points'] *= payout
            filter_df.loc[filter_df['wl'] == 'lose', 'points'] *= -1
        else:
            payout = 1/odds_l
            for i in filter_df.values:
                user = bot.get_user(int(i[1], 0))
                for j in dfnp:
                    if j[0] == i[1]:
                        before_total_points = j[-1]
                betpoints = i[3]
                bet = i[2]
                if bet == args[0]:
                    st = 'won'
                    prize_points = int(payout*betpoints)
                    final_points = prize_points + before_total_points
                    await user.send(f"Your {bet} bet of {int(betpoints)} points, resulted in {args[0]}. You have {st} {int(prize_points)} points, and your total points are {int(final_points)} points.")
                else:
                    st = 'lost'
                    points = int(df.loc[df['id'] == hex(user.id)].values[0][2])
                    await user.send(f"Your {bet} bet of {int(betpoints)} points, resulted in {args[0]}. You have {st} {int(betpoints)} points, and your remaining points are {int(before_total_points-betpoints)} points.")
            filter_df.loc[filter_df['wl'] == 'lose', 'points'] *= payout
            filter_df.loc[filter_df['wl'] == 'win', 'points'] *= -1
        df = pd.merge(df, filter_df, how='left', on='id')
        df = df.drop(columns=['wl'])
        df = df.fillna(0)
        df['totalpoints'] += df['points']
        df = df.drop(columns=['points', 'guild'])
        header = ['id', 'name', 'totalpoints']
        dfnp = df.to_numpy()
        with open(f"database-{str(ctx.guild)}.csv", 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(dfnp)
            await clear_bet_df(bet_df)
        BET_CLOSED = True
    else:
        await ctx.channel.send("No active bets.")
    filter_df = filter_df.drop(index=range(len(filter_df)))
    return
    
async def clear_bet_df(bet_df):
    bet_df = bet_df.drop(index=range(len(bet_df)))
    return bet_df

@commands.cooldown(1, 5, commands.BucketType.member)
@bot.command(pass_context = True)
async def roulette(ctx):
    df = pd.read_csv(f'database-{str(ctx.guild)}.csv', index_col=False)
    dfnp = df.to_numpy()
    multiplier = (0, 1, 10, 100, 1000, 'ban')
    value = random.randint(-10, 10)
    value2 = random.random()
    member = hex(ctx.message.author.id)
    ban_member = ctx.message.author
    rand_multi = random.choice(multiplier)
    bantime = 60
    guild = ctx.guild
    alt = guild.get_member(459614241939259404)
    role = get(ctx.guild.roles, id=965151168470868018)
    if rand_multi == 'ban':
        await ctx.channel.send(f"{alt.name} has banned {ctx.author.name} for {int(bantime/60)} minutes. <a:kekbye:965154556424118283>")
        await ban_member.add_roles(role)
        await asyncio.sleep(bantime)
        await ban_member.remove_roles(role)
        return
    for i in dfnp:
        if i[0] == member:
            points = i[-1]
    prize = value*value2
    total_prize = int(prize*rand_multi)
    if total_prize < 0:
        wl = 'lost'
        if total_prize > points:
            await ctx.channel.send(f"{ctx.author.name} has {wl} {abs(total_prize)} points. But you did not enough in you bank. <:kekl:965152443459592212>")
            return
        await ctx.channel.send(f"{ctx.author.name} has {wl} {abs(total_prize)} points. <:jebaited:466411622785613825>")
        for i in dfnp:
            if i[0] == member:
                # print(i[-1])
                i[-1] += total_prize
        return
    wl = 'won'
    await ctx.channel.send(f"{ctx.author.name} has {wl} {int(total_prize)} points. <:ez:480186243741909002>")
    for i in dfnp:
        if i[0] == member:
            # print(i[-1])
            i[-1] += total_prize
            total_points = i[-1]
            await ctx.author.send(f"Your points are {int(total_points)} points.")
            # print(i[-1])
    header = ['id', 'name', 'totalpoints']
    dfnp = df.to_numpy()
    with open(f"database-{str(ctx.guild)}.csv", 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(dfnp)
    return

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.add_reaction('<:pepeg:654197378772893706>')
        await ctx.channel.send("Unkown command you <:pepeg:654197378772893706>. Too many of these will get you banned.")
        return
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.channel.send("Command on cooldown, try again after {:.2f}s".format(error.retry_after))
        return
    raise error

@bot.command(pass_context = True)
async def si(ctx, *args):
    list1 = ['dn', 'deez', 'nuts']
    check = all(item.lower() in list1 for item in list(args))
    if check:
        await ctx.message.add_reaction('<:gottem:964794458765926430>')
    else:
        await ctx.message.add_reaction('<:pepeg:654197378772893706>')
    return

@bot.command(pass_context = True)
async def sendcomms(ctx):
    await ctx.channel.send('.points')

@bot.command(pass_context = True)
async def refund(ctx):
    await ctx.channel.send('No refunds. <:elegiggle:466411622647463946>')

# @commands.cooldown(1, 60*60*24, commands.BucketType.member)
@bot.command(pass_context = True)
async def ban(ctx, *args):
    if len(args) != 1:
        await ctx.channel.send("Please mention only one user.")
        return
    if type(args[0]) != str:
        await ctx.channel.send("Please mention only one user.")
        return
    df = pd.read_csv(f'database-{str(ctx.guild)}.csv', index_col=False)
    dfnp = df.to_numpy()
    member = hex(ctx.message.author.id)
    points = int(df.loc[df['id'] == member].values[0][2])
    bantime = 5
    cost = 10000
    guild = ctx.guild
    ban_member = ctx.message.raw_mentions[0]
    ban_member_name = guild.get_member(ban_member)
    role = get(ctx.guild.roles, id=965151168470868018)
    if points < cost:
        await ctx.channel.send(f"You do not have enough points to ban {ban_member_name.name}. <:kekl:965152443459592212>")
    else:
        if role not in ban_member_name.roles:
            for i in dfnp:
                if i[0] == member:
                    print(i[-1])
                    i[-1] -= cost
                    print(i[-1])
            await ctx.author.send(f"You have used {cost} points to ban {ban_member_name.name}. You have {int(points-cost)} points remaining.")
            header = ['id', 'name', 'totalpoints']
            with open(f"database-{str(ctx.guild)}.csv", 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(dfnp)
            await clear_bet_df(bet_df)
            await ban_member_name.add_roles(role)
            await ctx.channel.send(f"{ban_member_name.name} has been banned by {ctx.author.name} for 5 minutes. <a:kekbye:965154556424118283>")
            await ban_member_name.send(f"You have been banned by {ctx.author.name} for 5 minutes.")
            await asyncio.sleep(bantime)
            role_get = get(ban_member_name.guild.roles, id=965151168470868018)
            await ban_member_name.remove_roles(role_get)
        else:
            await ctx.channel.send(f"{ban_member_name} is already banned and will be back soon. <:pausechamp:965155561295462400>")
        return

@bot.event
async def on_voice_state_update(member, before, after):
    guild = bot.get_guild(305352819894910986)
    role = get(guild.roles, id=965151168470868018)
    if role in member.roles:
        if before.channel is None and after.channel is not None:# and after.channel.id in [305352819894910988, 368731230981718016, 471107780539842560, 447353741482524673]:
            await member.edit(mute=True)
            return
        elif before.channel is not None and after.channel is None:
            await member.edit(mute=False)
    return

@bot.event
async def on_member_update(before, after):
    if len(before.roles) < len(after.roles):
        banrole = next(role for role in after.roles if role not in before.roles)
        if banrole.name == 'ban' and after.voice is not None:
            await after.edit(mute=True)
            return
    if after.voice is not None:
        await after.edit(mute=False)



@tasks.loop(minutes=10)
# @bot.command(pass_context=True)
async def isinbulldogstream():
    guild = bot.get_guild(305352819894910986)
    bazba = guild.get_member(136431788980568064)
    bulldog_tag = ' (watching AdmiralBulldog)'
    nickname = bazba.display_name
    if is_in_bulldog_stream():
        if not nickname.endswith(bulldog_tag):
            await bazba.edit(nick=nickname + bulldog_tag)
    else:
        if nickname.endswith(bulldog_tag):
            await bazba.edit(nick=nickname.removesuffix(bulldog_tag))
    return


def is_in_bulldog_stream():
    url = "https://tmi.twitch.tv/group/user/admiralbulldog/chatters"
    r = requests.get(url)
    viewers = r.json()['chatters']['viewers']
    if 'quacktheduck' in viewers:
        return True
    return False
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