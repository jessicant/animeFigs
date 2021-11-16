import discord, random, time, sys
from discord.ext import commands
from amiami import checkPreowned

#globals
client = commands.Bot(command_prefix = '!')
mainUser:discord.Member = None
myinput = True

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command()
async def message(ctx, user:discord.Member, *, message=None):
    message = "Hello"
    print(user)
    embed = discord.Embed(title=message)
    await user.send(embed=embed)

@client.command()
async def hello(ctx):
    await ctx.send("Testing")
    await ctx.send("Main user:")
    await ctx.send(mainUser)
    await mainUser.send("Hi!")

@client.command()
async def defineMainUser(ctx,  user:discord.Member):
    global mainUser
    await ctx.send("command is calling")
    mainUser = user
    await ctx.send(user)
    await ctx.send(mainUser)

@client.command()
async def botCheckPreowned(ctx):
    await checkingPreowned(ctx)
    while(True):
        random_wait_time = random.randrange(5, 10) #900, 1200
        time.sleep(random_wait_time)
        await checkPreowned(ctx)


@client.command()
async def checkingPreowned(ctx):
    preownedFigs = checkPreowned("https://www.amiami.com/eng/search/list/?s_st_condition_flg=1&s_sortkey=preowned&pagecnt=")
    if (preownedFigs):
        await mainUser.send(preownedFigs)


client.run(sys.argv[1])
