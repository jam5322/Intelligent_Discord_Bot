import discord
import os
from discord.ext import commands, tasks
import random
from itertools import cycle
import json
import contentM

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix= get_prefix)
status = cycle(['Zelda Simulator v4.0.0', 'Melee Sucks', 'My Internet is Trash'])
on_status = cycle([discord.Status.do_not_disturb, discord.Status.idle])

@client.event
async def on_ready():
    change_play_status.start()
    #await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('Zelda Simulator v4.0.0'))
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '$'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

#@client.event
#async def on_message(message):
#    if message.author == client.user:
#        return

 #   if message.content.startswith('$hello'):
 #       await message.channel.send('Hello!')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Bruh.\nYou're Missing a Required Command Argument.\nGit Gud.")

def is_it_me(ctx):
    return ctx.author.id == 376060560153903104

@tasks.loop(minutes=3)
async def change_play_status():
    await client.change_presence( activity=discord.Game(next(status)),status=(next(on_status)))

@client.command()
@commands.check(is_it_me)
async def change_prefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

    await ctx.send(f"Prefix changed to '{prefix}'.")

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
@commands.check(is_it_me)
async def bot_credits(ctx):
    await ctx.send(f'Hi!, I am BassBot, the first bot created by {ctx.author}')

@client.command(name='ping')
async def ping(ctx):
    await ctx.send(f'Pong! - Your ping is roughly {round(client.latency * 1000)}ms')

@client.command(aliases = ['8ball', 'ball'])
async def _8ball(ctx, *, question):
    responses = [
        'It is certain.',
        'It is decidedly so.',
        'Without a doubt',
        'Yes, definitely.',
        'You may rely on it',
        'As I see it, yes.',
        'Most likely',
        'Outlook good.',
        'Yes.',
        'Signs point to yes',
        'Reply hazy, try again.',
        'Ask again later.',
        'Better not tell you now.',
        'Cannot predict now.',
        'Concentrate and ask again',
        "Don't count on it.",
        'My reply is no.',
        'My sources say no.',
        'Outlook not so good.',
        'Very doubtful.'
    ]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

#@client.command()
#async def clear(ctx, amount=5):
#    await ctx.channel.purge(limit = amount)
"""
The function below loads all of the functions, commands, etc from the bots' associated cog files.
"""
for filename in os.listdir('./admin'):
    if filename.endswith('.py'):
        client.load_extension(f'admin.{filename[:-3]}')

@client.event
async def on_message(message):
    if client.user.mentioned_in(message) and message.mention_everyone is False:                                                       #When the Bot is mentioned in a message, but it isn't through an @everyone
        #res = any(ele in contentM.Greetings for ele in contentM.Greetings)
        for res in contentM.Greetings:                                                                                                #The bot goes through its dictionary of possible greetings
            if res in message.content:                                                                                        #If the message someone sent to the bot uses one of the greeting strings in their message
                                                                                                                                      #  at all, the bot knows to respond with one of the two following "greeting" response paths
                temp_id = message.author.id
                if str(temp_id) in contentM.Known_Friends.keys():                                                                     #If the sender's ID matches that of one of Bass's personal friends on Discord:

                    mention = '{0.author.mention} Hello '.format(message) + contentM.Known_Friends.get(str(message.author.id)) + '!'  #Hello's for Jonah's Known Friends
                    await message.channel.send(mention)

                else:
                    mention = '{0.author.mention} Hello!'.format(message)                                                             #Hello's for "random people"/unknown/forgotten friends
                    await message.channel.send(mention)
    await client.process_commands(message)

client.run('NjkyMjE4MzYxMzUzOTk0MjUx.XnriwQ.r7f-kJomH_LFGSyJTIq3icFl-yc')
