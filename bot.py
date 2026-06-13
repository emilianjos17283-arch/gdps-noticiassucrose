import discord
from discord.ext import commands
import os

# --- CONFIGURACIÓN ---
TOKEN = os.getenv("DISCORD_TOKEN")          # Tu token del bot
CANAL_ID = int(os.getenv("CANAL_ID", "0"))  # ID del canal donde funciona !revivir

# --- BOT ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

@bot.command(name="revivir")
async def revivir(ctx):
    # Solo funciona en el canal específico
    if ctx.channel.id != CANAL_ID:
        await ctx.send("❌ Este comando solo funciona en el canal designado.")
        return

    # Obtener todos los miembros (excepto bots)
    miembros = [m for m in ctx.guild.members if not m.bot]

    if not miembros:
        await ctx.send("No hay miembros para mencionar.")
        return

    # Dividir en grupos de 20 para no hacer mensajes enormes
    chunk_size = 20
    for i in range(0, len(miembros), chunk_size):
        grupo = miembros[i:i + chunk_size]
        menciones = " ".join(m.mention for m in grupo)
        await ctx.send(menciones)

    await ctx.send("🔔 ¡Todos han sido notificados!")

bot.run(TOKEN)
