import datetime
from discord.ext import commands, tasks
import discord
import pytz

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="%", intents=intents)

WEEKDAY_CHANNEL_ID = 1346088213382696991
WEEKEND_CHANNEL_ID = 1346088213382696991
ROLE_ID = 1350507122844237866

def create_embed(title, description, color):
    """建立 Discord Embed 訊息"""
    return discord.Embed(title=title, description=description, color=color)

@bot.event
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")
    send_message.start()

@tasks.loop(seconds=60)
async def send_message():
    try:
        tz = pytz.timezone('Asia/Shanghai')
        now = datetime.datetime.now(tz)

        role_mention = f"<@&{ROLE_ID}>"

        if now.weekday() in range(5):  # 周一至周五
            channel = bot.get_channel(WEEKDAY_CHANNEL_ID)
            if isinstance(channel, discord.TextChannel):
                messages = {
                    (0, 19, 50): ("鎮魔提醒", "還有10分鐘8點鎮魔", 0x3498db),
                    (2, 19, 50): ("鎮魔 & 宗門對決提醒", "還有10分鐘8點鎮魔，宗門對決的記得去打", 0x3498db),
                    (4, 19, 50): ("鎮魔提醒", "還有10分鐘8點鎮魔", 0x3498db),
                }
                if (now.weekday(), now.hour, now.minute) in messages:
                    title, description, color = messages[(now.weekday(), now.hour, now.minute)]
                    await channel.send(content=f"{role_mention} {title}", embed=create_embed(title, description, color))

        else:  # 週末
            channel = bot.get_channel(WEEKEND_CHANNEL_ID)
            if isinstance(channel, discord.TextChannel):
                messages = {
                    (5, 20, 50): ("亂鬥準備", "還有10分鐘開始亂鬥。", 0x2ecc71),
                    (6, 20, 50): ("八荒準備", "還有10分鐘開始八荒。", 0x2ecc71),
                    (6, 21, 20): ("天下準備", "還有10分鐘開始天下。", 0x2ecc71),
                }
                if (now.weekday(), now.hour, now.minute) in messages:
                    title, description, color = messages[(now.weekday(), now.hour, now.minute)]
                    await channel.send(content=f"{role_mention} {title}", embed=create_embed(title, description, color))

    except Exception as e:
        print(f"Error sending message: {e}")

@bot.command()
async def timelist(ctx: commands.Context):
    embed = discord.Embed(title="📅 時間表", description="以下是各活動的時間安排", color=0x3498db)

    embed.add_field(name="周一", value="> **19:50** 沒打鎮魔的記得去打", inline=False)
    embed.add_field(name="周三", value="> **19:50** 沒打鎮魔以及宗門對決的記得去打", inline=False)
    embed.add_field(name="周五", value="> **19:50** 沒打鎮魔的記得去打", inline=False)
    embed.add_field(name="周六", value="> **20:50** 準備亂鬥", inline=False)
    embed.add_field(name="周日", value="> **20:50** 準備八荒\n> **21:20** 準備天下", inline=False)

    embed.set_footer(text="請努力準時參加活動！")

    await ctx.send(embed=embed)

send_message.before_loop(bot.wait_until_ready)

bot.run('MTI2MTY2MDMxNTg5MzEwODgyOA.GPYAW_.SnERQAw7hBaBYtt2_46sODQA-w_J1eBTjrJ4gQ')  # Bot Token

#leowu做的小人機for太初群
