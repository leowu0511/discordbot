import discord
import google.generativeai as genai
from discord.ext import commands

# 設定 Discord Bot Token 和 Gemini API Key
DISCORD_TOKEN = "MTI2MTY2MDMxNTg5MzEwODgyOA.GPYAW_.SnERQAw7hBaBYtt2_46sODQA-w_J1eBTjrJ4gQ"
GEMINI_API_KEY = "AIzaSyCgwvMRFOg331rOnTuK7TQXysSQE3LR-XE"

# 初始化 Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# 設定機器人權限
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# **只用 `bot`，不要 `client`**
bot = commands.Bot(command_prefix="!", intents=intents)

#tag
@bot.command()
async def tag(ctx: commands.Context, user_id: int, *, message: str):
    try:
        user = await bot.fetch_user(user_id)  # 嘗試取得使用者
        if user:
            await ctx.send(f"{user.mention} {message}")  # @使用者 並發送訊息
        else:
            await ctx.send("❌ 找不到此使用者")
    except discord.NotFound:
        await ctx.send("❌ 找不到此使用者")
    except discord.HTTPException:
        await ctx.send("⚠️ 無法標記該使用者，請稍後再試")




# **指令：hi**
@bot.command()
async def hi(ctx: commands.Context):
    embed = discord.Embed(
        title="👋 嗨！", 
        description="你好啊！有什麼需要幫忙的嗎？", 
        color=0x00ff00
    )
    embed.set_footer(text="Bot 為您服務！")
    
    await ctx.send(embed=embed)

# 用字典儲存每個伺服器的對話紀錄
conversation_histories = {}

@bot.event
async def on_ready():
    print(f'✅ 已登入 Discord，機器人名稱：{bot.user}')

@bot.event
async def on_message(message):
    # 允許機器人回應其他機器人
    # 但小心無窮回應問題


    if bot.user not in message.mentions:
        await bot.process_commands(message)  # **加上這行，讓指令能運行**
        return

    guild_id = str(message.guild.id)  # 取得伺服器 ID

    if guild_id not in conversation_histories:
        conversation_histories[guild_id] = []  # 初始化該伺服器的紀錄

    # 記錄對話，但不過度依賴
    new_entry = f"{message.author.name}: {message.content}"
    if new_entry not in conversation_histories[guild_id]:
        conversation_histories[guild_id].append(new_entry)

    # 只保留最近 50 條作為輔助
    conversation_histories[guild_id] = conversation_histories[guild_id][-50:]

    # **主要使用最新的一句話來生成回應**
    latest_message = message.content  # 只取當前訊息

    # **歷史對話只當輔助**
    history_text = "\n".join(conversation_histories[guild_id])

    # **建立 Prompt**
    prompt = f"""
        如果使用者對你用繁體中文，你會用繁體中文回應，如果使用者對你用簡體中文，你會用簡體中文回應，
        你是一個負責遊戲 一念逍遙，一個公會名稱叫「太初」機器人，你負責獲取一些官方的資料來幫成員們減輕壓力，你像是一個助手。
        最近一次仙魔決在兩周後的周五
    """

    safety_settings = [
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
    ]

    async with message.channel.typing():
        response = model.generate_content(prompt, safety_settings=safety_settings)

    await message.reply(response.text)    

# **改用 `bot.run()`**
bot.run(DISCORD_TOKEN)
