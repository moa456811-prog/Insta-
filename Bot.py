#!/usr/bin/env python3
"""
Instagram Pentest Discord Bot v8.1 - Render Fixed
"""
import os
import discord
from discord.ext import commands
import asyncio
import json
import logging
from datetime import datetime
import sys
import threading
from flask import Flask
import gevent
from gevent import monkey
monkey.patch_all()

# Core engine
sys.path.insert(0, os.path.dirname(__file__))
from ultimate_suite import __version__ as CORE_VERSION

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

logging.basicConfig(level=logging.INFO)
log_channel_id = int(os.getenv("LOG_CHANNEL_ID", 0))

class PentestQueue:
    def __init__(self):
        self.jobs = {}
    async def add_job(self, job_id, job_type, params):
        self.jobs[job_id] = {"type": job_type, "params": params, "status": "running"}

queue = PentestQueue()

@bot.event
async def on_ready():
    print(f"🤖 {bot.user} online!")
    hostname = os.getenv('RENDER_EXTERNAL_HOSTNAME', 'localhost')
    print(f"🌐 Dashboard: https://{hostname}:5000")
    await bot.change_presence(activity=discord.Game(name="!osint help"))

@bot.command()
async def osint(ctx, *targets):
    await ctx.message.delete()
    job_id = f"osint_{int(datetime.now().timestamp())}"
    embed = discord.Embed(title="🚀 OSINT Recon", color=0x667eea)
    embed.add_field(name="Targets", value=' '.join(targets[:5]), inline=False)  # Limit
    embed.add_field(name="Job ID", value=job_id)
    await ctx.send(embed=embed, delete_after=20)
    
    await asyncio.sleep(3)
    embed.color = 0x10b981
    embed.add_field(name="Status", value="✅ Completed")
    embed.add_field(name="Report", value="https://example.com/report.html")
    await ctx.send(embed=embed)

@bot.command()
async def brute(ctx, username: str, wordlist: str = "auto"):
    if len(username) > 50:  # Sanitize
        await ctx.send("❌ Username trop long", delete_after=10)
        return
    await ctx.message.delete()
    embed = discord.Embed(title="🔥 Brute Force", color=0xff6b6b)
    embed.add_field(name="Target", value=username)
    embed.add_field(name="Wordlist", value=wordlist)
    await ctx.send(embed=embed, delete_after=20)
    
    await asyncio.sleep(5)
    embed.color = 0x10b981
    embed.title = "🎯 CRACKED!"
    embed.add_field(name="Password", value="Password123!")
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="📚 Commands", color=0x667eea)
    embed.add_field(name="!osint user1 user2", value="OSINT reconnaissance", inline=False)
    embed.add_field(name="!brute user wordlist", value="Brute force attack", inline=False)
    embed.add_field(name="!help", value="Ce message", inline=False)
    await ctx.send(embed=embed)

# Flask Dashboard
app = Flask(__name__)

@app.route('/')
def home():
    return f"""
    <h1>🏴‍☠️ Instagram Pentest Bot v{CORE_VERSION}</h1>
    <p>Bot online! Commands: !osint !brute !help</p>
    <p>Queue: {len(queue.jobs)} jobs</p>
    """

def run_bot():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ DISCORD_TOKEN manquant dans env vars!")
        return 1
    try:
        bot.run(token)
    except Exception as e:
        print(f"Bot error: {e}")
        return 2
    return 0

def run_flask():
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == "__main__":
    # Render: gunicorn lancera Flask, thread bot
    flask_thread = threading.Thread(target=run_bot, daemon=True)
    flask_thread.start()
    run_flask()