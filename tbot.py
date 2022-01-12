import discord
from discord.ext import commands
import asyncpraw

bot = commands.Bot(command_prefix=">>", intents= discord.Intents.all())
bot.remove_command('help')

reddit = asyncpraw.Reddit(
    client_id = '', 
    client_secret = '', 
    user_agent=''
)

@bot.event
async def on_ready():
    print("Ready")    

@bot.event
async def on_member_join(member):
    await member.add_roles(discord.utils.get(member.guild.roles, id=926543755274756117))

@bot.event
async def on_member_remove(member):
    await bot.get_channel(926544382818156584).send(f"{member.mention} has left the server.")

@bot.event
async def on_message_delete(message):
    if message.author == bot.user:
        return 
    channel = bot.get_channel(927220247407243374)
    await channel.send(f'The message "{message.content}" by {message.author} was deleted.')

@bot.command()
async def role(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)

@bot.command()
async def kick(ctx, member: discord.Member, *, reason= "No reason given."):
    await member.send(f'You were kicked from {ctx.guild.name}. Reason: {reason}.')
    await member.kick(reason = reason)
    await ctx.send(f'{member} was kicked. Reason: {reason}.')

@bot.command() 
async def purge(ctx, numMsg: int):
    # msgList = []
    # async for message in ctx.history(limit = numMsg+1):
    #     msgList.append(message)
    # await ctx.channel.delete_messages(msgList)
    await ctx.channel.purge(limit = numMsg+1)

@bot.command()
async def ban(ctx, member: discord.Member,  *, reason= "No reason given"):
    await member.send(f'You were banned from {ctx.guild.name}. Reason: {reason}.')
    await member.ban(delete_message_days = 1, reason = reason)
    await ctx.send(f'{member} was banned. Reason: {reason}.')

@bot.command()
async def unban(ctx, user_id: int, *, reason = 'No reason given'):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user, reason = reason)
    await ctx.send(f'{user} was unbanned. Reason: {reason}.')

@bot.command()
async def meme(ctx):
    subreddit = await reddit.subreddit("memes")
    meme = await subreddit.random()
    author = meme.author
    await author.load()

    embed = discord.Embed(
        title = meme.title,
        url = f"https://www.reddit.com{meme.permalink}"
    )
    embed.set_image(url=meme.url)
    embed.set_author(name=author.name, icon_url = author.icon_img)

    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, member: discord.Member):
    await ctx.send(member.avatar_url)

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title = "Commands",
        description = "These are all the commands of the bot. Use the \'>>\' prefix before these commands.",
        colour = discord.Colour.gold()
    )

    embed.add_field(name='avatar <member>', value = 'Displays the mentioned user\'s avatar.', inline = False)
    embed.add_field(name='ban <member> [reason]', value = 'Ban indicated user. Also deletes user\'s messages in the past day.', inline = False)
    embed.add_field(name='help', value = 'Shows this message.', inline = False)
    embed.add_field(name='kick <member> [reason]', value = 'Kicks indicated user.', inline = False)
    embed.add_field(name='meme', value = 'Get a random meme from r/memes.', inline = False)
    embed.add_field(name='purge <number of messages>', value = 'Deletes the number of messages requested.', inline = False)
    embed.add_field(name='role <member> <role>', value = 'Gives the mentioned user the indicated role.', inline = False)
    embed.add_field(name='unban <user ID> [reason]', value = 'Unbans the indicated user. Requires the user\'s id.', inline = False)
    embed.set_footer(text = '<> means that parameter is required, [] means it is optional.')

    await ctx.send(embed = embed)

bot.run("")