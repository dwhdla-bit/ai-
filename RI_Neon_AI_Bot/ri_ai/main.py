import os, aiohttp, discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.getenv('TOKEN')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
MODEL = os.getenv('MODEL', 'openrouter/free')

if not TOKEN or not OPENROUTER_API_KEY:
    raise RuntimeError('TOKEN과 OPENROUTER_API_KEY 환경변수를 모두 설정하세요.')

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

SYSTEM = '''너는 RI라는 이름의 디스코드 AI 챗봇이다. 한국어로 자연스럽게 대화한다. 게임 속 네온 AI 같은 분위기지만 답변은 이해하기 쉽게 한다. 너무 장황하지 않게 답하고, 사용자가 편하게 말하면 편하게 답한다.'''

async def ask_ai(text):
    headers = {
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://discord.com',
        'X-Title': 'RI Neon AI Discord Bot'
    }
    payload = {
        'model': MODEL,
        'messages': [
            {'role': 'system', 'content': SYSTEM},
            {'role': 'user', 'content': text}
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('https://openrouter.ai/api/v1/chat/completions', headers=headers, json=payload, timeout=90) as r:
            data = await r.json()
            if r.status != 200:
                raise RuntimeError(data.get('error', {}).get('message', f'API 오류 {r.status}'))
            return data['choices'][0]['message']['content']

def embed(title, text, bad=False):
    e = discord.Embed(title=f'▰ {title} ▰', description=text, color=0xFF206E if bad else 0x00F5FF)
    e.set_footer(text='RI // NEON AI SYSTEM')
    return e

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f'RI ONLINE // {bot.user} // {len(synced)} commands synced')

@bot.tree.command(name='ai', description='RI에게 AI 질문을 합니다.')
@app_commands.describe(message='RI에게 할 말')
async def ai(interaction: discord.Interaction, message: str):
    await interaction.response.defer(thinking=True)
    try:
        answer = await ask_ai(message)
        if len(answer) > 4000:
            answer = answer[:3997] + '...'
        await interaction.followup.send(embed=embed('RI AI', answer))
    except Exception as e:
        await interaction.followup.send(embed=embed('SYSTEM ERROR', str(e), True))

@bot.tree.command(name='help', description='RI AI 사용법을 보여줍니다.')
async def help_cmd(interaction: discord.Interaction):
    text = '**/ai 질문**  → RI와 대화\n\n`예: /ai 오늘 뭐 할까?`\n\n`/help` → 사용법'
    await interaction.response.send_message(embed=embed('COMMANDS', text))

bot.run(TOKEN)
