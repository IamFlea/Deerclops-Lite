import settings
import asyncio
import datetime as dt
import multiprocessing as mp 
import discord
import re
from deerclops import Deerclops
from hooks import ProxyBot

# Transfers stdout to specific files 
if settings.release_version:
    import sys
    sys.stdout = open("/tmp/carrat_main.out", "w")
    sys.stderr = open("/tmp/carrat_main.err", "w")


# Creates manager for shared memory
manager = mp.Manager()
shared_memory = manager.list(range(1)) # TODO more servers on the same machine

# Editting at #dst-info
async def listener(client, shared_memory):
    await asyncio.sleep(5) 
    async def sendMsg(msg, val):
        while True:
            try:
                await msg.edit(content=val)
            except discord.errors.HTTPException:
                await asyncio.sleep(0.5)
                continue
            return

    time_counter = 0
    total_players = ""
    # Get channel for edit
    channel = client.get_channel(settings.channel_id)
    while channel is None:
        channel = client.get_channel(settings.channel_id)
    # Get message for edit
    msg = await channel.fetch_message(settings.message_id)
    while msg is None:
        msg = await channel.fetch_message(settings.message_id)
    
    while 1:
        updated = -1
        for i, val in enumerate(shared_memory):
            if type(val) is str:
                shared_memory[i] = False
                timestamp_obj = dt.datetime.now()
                client.last_time = timestamp_obj.strftime('*Last update %-d. %B at %H:%M*')
                val = f"{val}\n{client.last_time}"
                client.last_msg = val
                
                if len(val) < 2000:
                    await sendMsg(msg, val)
                else:
                    await sendMsg(msg, f"{val[:1950]}...\nAnd more...\n{client.last_time}")
                x = re.findall(r"Total players: (\d+)/(\d+)", val, re.MULTILINE)
                try:
                    total_players = x[0][0]
                except:
                    pass
        await asyncio.sleep(1)

        if total_players == "":
            continue
        time_counter = (time_counter + 1) % (settings.status_change_speed*len(settings.status_suffixes))
        response = settings.status_suffixes[time_counter//settings.status_change_speed]
        
        if int(total_players) == 1:
            activity_str = f"{total_players} player{response}"
        else:
            activity_str = f"{total_players} players{response}"
        # update status for endless
        game = discord.Game(activity_str, type=discord.ActivityType.playing)
        try:
            await client.change_presence(activity=game)
        except Exception as inst:
            print("Couldnt update status")
            print("---------------------")
            print(inst, file=sys.stderr)
            print("---------------------")




# Creates the bot
client = Deerclops()


@client.event
async def on_message(message):
    await client.parseCommands(message)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')
    print('------')



bot = ProxyBot(shared_memory, client)
#print("BOT ID", id(bot))
client.the_bot = bot
p_hooks = mp.Process(target=bot.run, args=())
p_hooks.start()

client.loop.create_task(listener(client, shared_memory))
client.shared_memory = shared_memory



client.run(settings.token)


p_hooks.join()
p_hooks.close()

