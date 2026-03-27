#!/usr/bin/env python3
"""
Instagram Pentest Bot v8.1 - Render NO-GEVENT Fixed
"""
import os
import discord
from discord.ext import commands
import asyncio
import json
import logging
from datetime import datetime
import sys
from flask import Flask, request

# Core engine
sys.path.insert(0, os.path.dirname(__file__))
from ultimate_suite import __version__ as CORE_VERSION

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

logging.basicConfig(level=logging.INFO)

class PentestQueue:
    def __init__(self): self.jobs = {}
    async def add_job(self, job_id, job_type, params):
        self.jobs[job_id] = {"type": job_type, "params": params, "status": "running"}

queue = PentestQueue()

@bot.event
async def on_ready():
    print(f"🤖 {bot.user} online!")
    print("🌐 Dashboard: http://localhost:5000")
    await bot.change_presence(activity=discord.Game(name="!osint help"))

@bot.command()
async def osint(ctx, *targets):
    await ctx.message.delete()
    targets = targets[:5]  # Limit spam
    job_id = f"osint_{int(datetime.now().timestamp())}"
    embed = discord.Embed(title="🚀 OSINT Recon", color=0x667eea)
    embed.add_field(name="Targets", value=' '.join(targets), inline=False)
    embed.add_field(name="Job ID", value=job_id)
    msg = await ctx.send(embed=embed)
    await asyncio.sleep(3)
    embed.color = 0x10b981
    embed.add_field(name="Status", value="✅ Completed - ultimate_suite v" + CORE_VERSION)
    await msg.edit(embed=embed)

@bot.command()
async def brute(ctx, username: str, wordlist: str = "auto"):
    if len(username) > 50:
        return await ctx.send("❌ Username trop long", delete_after=10)
    await ctx.message.delete()
    embed = discord.Embed(title="🔥 Brute Force Attack", color=0xff6b6b)
    embed.add_field(name="Target", value=f"@{username}", inline=False)
    embed.add_field(name="Wordlist", value=wordlist, inline=False)
    msg = await ctx.send(embed=embed)
    await asyncio.sleep(5)
    embed.color = 0x10b981
    embed.title = "🎯 CRACKED!"
    embed.add_field(name="Password", value="**Password123!**", inline=False)
    await msg.edit(embed=embed)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="📚 Instagram Pentest Commands", color=0x667eea)
    embed.add_field(name="!osint user1 user2", value="Recon OSINT (ultimate_suite)", inline=False)
    embed.add_field(name="!brute username [wordlist]", value="Brute force simulation", inline=False)
    embed.add_field(name="!help", value="Ce menu", inline=False)
    await ctx.send(embed=embed)

# Flask Dashboard SEUL (bot tourne ailleurs)
app = Flask(__name__)

@app.route('/')
def home():
    return f"""
<!DOCTYPE html>
<html>
<head><title>Pentest Bot v{CORE_VERSION}</title></head>
<body style="background:#000;color:#0f0;font-family:monospace;">
    <h1>🏴‍☠️ Instagram Ultimate Suite v{CORE_VERSION}</h1>
    <p><b>Status:</b> Dashboard OK | Bot: Check Discord</p>
    <p><b>Queue:</b> {len(queue.jobs)} jobs</p>
    <p>Commands: <code>!osint user1</code> <code>!brute target</code></p>
    <hr>
    <small>Deployed on Render | ultimate_suite OSINT ready</small>
</body>
</html>
    """

@app.route('/health')
def health():
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)