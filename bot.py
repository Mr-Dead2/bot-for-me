import os
import asyncio
import discord
import sys
import json
import random
import requests
from discord.ext import commands


with open('./config.json') as f:
  data = json.load(f)
  for c in data['botConfig']:
     print('token: ' + c['token'])


intent = discord.Intents.default()
intent.members = True
intent.message_content = True

activity = discord.Activity(type=discord.ActivityType.listening, name="nigga ")
bot = commands.Bot(command_prefix=["+", "ax", "axiom"], activity=activity, intents=intent,  help_command=None)
bot.remove_command('help')

curseWord = ['fuck', 'nigga', 'kill']


@bot.event
async def on_ready():
    print(f'Logged on as {bot.user} and ready for work!')


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1073605242547097752)
    embed = discord.Embed(
        title="New member",
        description=f"Member {member.name} has been joined!",
        color=discord.Color.random())
    embed.set_thumbnail(url=f"{member.avatar}")
    embed.set_footer(text="Thanks for joining to Dead Squad!")
    await channel.send(embed=embed)
    print(f"new member join {member.name}!")


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1073605242547097752)
    embed = discord.Embed(
        title="Member levae",
        description=f"Member {member.name} has been leave the server.",
        color=discord.Color.random())
    await channel.send(embed=embed)
    print(f"Member leave server {member.name}!")
        

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author.id == bot.user.id:
        return
    msg_content = message.content.lower()
    if any(word in msg_content for word in curseWord):
        msg = await message.channel.send(f'{message.author} was using banned words `{message.content}`',reference=message)
        await asyncio.sleep(10)
        await message.delete()
        await msg.delete()
        

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member} has been kicked.')
# Ban command


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member} has been banned.')


@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user} has been unbanned.')
            return

# Mute command


@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.add_roles(role, reason=reason)
    await ctx.send(f'{member} has been muted.')

# Unmute command


@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.remove_roles(role)
    await ctx.send(f'{member} has been unmuted.')

# Clear command


@bot.command(aliases=["cl"])
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)
    msg = await ctx.send(f'{amount} messages have been cleared.')
    await asyncio.sleep(30)
    await msg.delete()


# Ticket tool commands


@bot.command()
async def ticket(ctx):
    channel = await ctx.guild.create_text_channel(f'ticket-{ctx.author.name}')
    category = discord.utils.get(ctx.guild.categories, name='Tickets')
    await channel.edit(category=category)

    await channel.set_permissions(ctx.guild.default_role, read_messages=False)
    await channel.set_permissions(ctx.author, read_messages=True, send_messages=True)

    await ctx.send(f'Your ticket has been created at {channel.mention}!')
    await ctx.channel.send()


@bot.command()
async def close(ctx):
    channel = ctx.channel
    await channel.delete()


@bot.command()
@commands.has_permissions(manage_roles=True)
async def giverole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"{member.name} has been given the {role.name} role.")


@bot.command(aliases=["sl"])
@commands.has_permissions(administrator=True)
async def serverlist(ctx):
    msg = "\n".join(f"{x}" for x in bot.guilds)
    embed = discord.Embed(
        title="Server list",
        description="Serverl list where bot are joined!",

    )
    embed.add_field(name="All bots guilds", value=f"```\n{msg}\n```")
    await ctx.send(embed=embed)


@bot.command(aliases=["sd"])
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
    await ctx.send(f"Bot is turned off.")




@bot.command(aliases=['sv', 'info'])
async def serverinfo(ctx):
    membros = len(ctx.guild.members)
    cargos = len(ctx.guild.roles)
    x = discord.Embed(title='**Server Info:**', color=discord.Color.random())
    x.add_field(name='Server name:', value=ctx.guild.name, inline=False)
    x.add_field(name='Server ID:', value=ctx.guild.id, inline=False)
    x.add_field(name='Server Owner:', value=ctx.guild.owner.mention, inline=False)
    x.add_field(
        name='Server Create Date:',
        value=ctx.guild.created_at.strftime('Data: %d/%m/%Y Hour: %H:%M:%S %p'),
        inline=False)
    x.add_field(name='Server Members:', value=f'`{membros}`', inline=False)
    x.add_field(name=f'Server Roles:', value=f'`{cargos}`', inline=False)
    await ctx.send(embed=x)


@bot.command()
async def pool(ctx, *, message):
    channel = bot.get_channel('1119253879721308191')
    mess = ctx.message
    e = discord.Embed(title="pool", description=f"{message}", color=discord.Color.random())
    await mess.delete()
    msg = await channel.send(embed=e)
    await msg.add_reaction("✔")
    await msg.add_reaction("❌")





@bot.command()
@commands.has_permissions(administrator=True)
async def invite(ctx):
    invite = "https://discord.com/api/oauth2/authorize?client_id=1091438564388114545&permissions=8&scope=bot"
    msg = await ctx.send(f"there is bot invite link {invite} ")
    await asyncio.sleep(50)
    await msg.delete()


@bot.command()
async def help(ctx):
    ban_help = 'Ban member from server.'
    kick_help = 'Kick member from server.'
    unban_help = 'Unban member from server.'
    mute_help = 'Mute member from server.'
    unmute_help = 'Unmute member from server.'
    clear_help = 'Clear messeges from any channel.'
    ticket_help = 'Make new ticket.'
    close_help = 'Close or delete any channel.'
    giverole_help = 'Giverole to member.'
    serverlist_help = 'Show all server where bot are joined.'
    shutdown_help = 'Shutdown the bot.'
    server_help = 'Show info about server.'
    pool_help = 'Make pool.'
    info_help = 'Show info about any member.'
    invite_help = 'Bot invite link.'
    help_embed = discord.Embed(title="All bot supported commands.", color=discord.Color.random())
    help_embed.add_field(name='`ban`', value=ban_help, inline=False)
    help_embed.add_field(name='`kick`', value=kick_help, inline=False)
    help_embed.add_field(name='`unban`', value=unban_help, inline=False)
    help_embed.add_field(name='`mute`', value=mute_help, inline=False)
    help_embed.add_field(name='`unmute`', value=unmute_help, inline=False)
    help_embed.add_field(name='`clear`', value=clear_help, inline=False)
    help_embed.add_field(name='`ticket`', value=ticket_help, inline=False)
    help_embed.add_field(name='`close`', value=close_help, inline=False)
    help_embed.add_field(name='`giverole`', value=giverole_help, inline=False)
    help_embed.add_field(name='`serverlist`', value=serverlist_help, inline=False)
    help_embed.add_field(name='`shutdown`', value=shutdown_help, inline=False)
    help_embed.add_field(name='`server`', value=server_help, inline=False)
    help_embed.add_field(name='`pool`', value=pool_help, inline=False)
    help_embed.add_field(name='`info`', value=info_help, inline=False)
    help_embed.add_field(name='invate', value=invite_help, inline=False)
    await ctx.send(embed=help_embed)


@bot.command()
async def map(ctx):
    r = requests.get("https://fortnite-api.com/v1/map")
    res =  r.json()
    data = res["data"]
    images = data["images"]
    em = discord.Embed(title="Fortnite Map.", color=discord.Color.random())
    em.set_image(url=f"{images['pois']}")
    await ctx.reply(embed=em)
    print(res["status"])



@bot.command()
async def code(ctx, code):
    r = requests.get(f"https://fortnite-api.com/v2/creatorcode/?name={code}")
    res= r.json()
    status= res["status"]
    data = res["data"]
    if status == 200:
        print (f"{res['status']}")
        await ctx.reply(f"{data['status']}")

    else:
        await ctx.reply(f"{data['status']}")


@bot.command()
async def stats(ctx, name):
    headers = {"Authorization": 'de2caa62-205f-4955-95cb-72dec8e1e075'}
    r = requests.get(f"https://fortnite-api.com/v2/stats/br/v2/?name={name}", headers=headers)
    res = r.json()
    status= res["status"]
    data = res["data"]
    account=data["account"]
    stats=data["stats"]
    all=stats["all"]
    overall=all["overall"]
    e= discord.Embed(title=(f"Account {account['name']} statistics"), description=(f"User id `{account['id']}`"), color=discord.Color.random())
    e.add_field(name=("Wnis"), value=(f"{overall['wins']}"), inline=False)
    e.add_field(name=("Top10"), value=(f"{overall['top10']}"), inline=False)
    e.add_field(name=("Top25"), value=(f"{overall['top25']}"), inline=False)
    e.add_field(name=("Kills"), value=(f"{overall['kills']}"), inline=False)
    e.add_field(name=("Deaths"), value=(f"{overall['deaths']}"), inline=False)
    e.add_field(name=("Matches"), value=(f"{overall['matches']}"), inline=False)
    e.add_field(name=("Win Rate"), value=(f"{overall['winRate']}"), inline=False)
    
    if status == 200:
        await ctx.send(embed=e)

    else:
        await ctx.reply(f"{res['error']}")





@bot.event
async def on_command_error(ctx, error):
    missingperms = discord.Embed(
        title="        ❌Missing Permissions❌",
        description="You do not have the required permissions to run this command.",
        color=discord.Color.red())
    missingreq = discord.Embed(
        title="    ❌Missing Required Argument❌",
        description="Please pass in all required arguments.",
        color=discord.Color.red())
    missmember = discord.Embed(
        title="❌Missing Member❌",
        description="Member does not exist or canou't find.",
        colour=discord.Color.red())
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=missingreq)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=missingperms)
    if isinstance(error, commands.BadArgument):
        await ctx.send(embed=missmember)
    else:
        print(error)


bot.run(c['token'])
