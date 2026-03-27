#!/usr/bin/env python3
"""
Instagram Pentest Discord Bot v8.1 - Render Ready
"""

import os
import discord
from discord.ext import commands
import asyncio
import aiohttp
import json
import logging
from datetime import datetime
from pathlib import Path
import sys
import threading
from contextlib import redirect_stdout, redirect_stderr
import io

# Core engine import
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
    print(f"🌐 Dashboard: https://{os.getenv('RENDER_EXTERNAL_HOSTNAME', 'localhost')}:5000")
    await bot.change_presence(activity=discord.Game(name="!osint help"))

@bot.command()
async def osint(ctx, *targets):
    await ctx.message.delete()
    job_id = f"osint_{int(datetime.now().timestamp())}"
    
    embed = discord.Embed(title="🚀 OSINT Recon", color=0x667eea)
    embed.add_field(name="Targets", value=' '.join(targets), inline=False)
    embed.add_field(name="Job ID", value=job_id)
    await ctx.send(embed=embed, delete_after=20)
    
    # Simulate OSINT
    await asyncio.sleep(3)
    embed.color = 0x10b981
    embed.add_field(name="Status", value="✅ Completed")
    embed.add_field(name="Report", value="https://example.com/report.html")
    await ctx.send(embed=embed)

@bot.command()
async def brute(ctx, username: str, wordlist: str = "auto"):
    await ctx.message.delete()
    embed = discord.Embed(title="🔥 Brute Force", color=0xff6b6b)
    embed.add_field(name="Target", value=username)
    embed.add_field(name="Wordlist", value=wordlist)
    await ctx.send(embed=embed, delete_after=20)
    
    # Simulate brute
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

from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return f"""
    <h1>🏴‍☠️ Instagram Pentest Bot v{CORE_VERSION}</h1>
    <p>Bot online! Commands: !osint !brute !help</p>
    <p>Queue: {len(queue.jobs)} jobs</p>
    """

def run_flask():
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # Start Flask thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Start bot
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("❌ DISCORD_TOKEN manquant dans env vars!")
