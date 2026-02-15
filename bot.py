import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import aiosqlite
import json
import os

# Load configuration
def load_config():
    config_path = "config.json"
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"{config_path} not found. Please create it with your settings.")
    
    with open(config_path, "r") as f:
        return json.load(f)

config = load_config()

# Initialize bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

async def init_db():
    """Initialize the database"""
    async with aiosqlite.connect(config["database"]) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS tiertests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ign TEXT,
            user_id INTEGER,
            gamemode TEXT,
            score TEXT,
            tier TEXT,
            comments TEXT,
            tester_id INTEGER
        )
        """)
        await db.commit()

def get_gamemode_choices():
    """Generate gamemode choices from config"""
    return [
        app_commands.Choice(name=gm["name"], value=gm["value"])
        for gm in config["gamemodes"]
    ]

def get_tier_choices():
    """Generate tier choices from config"""
    return [
        app_commands.Choice(name=tier, value=tier)
        for tier in config["tiers"]
    ]

@bot.event
async def on_ready():
    await init_db()
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")

    await bot.change_presence(
        activity=discord.Activity(
            name=config["bot_status"],
            type=discord.ActivityType.watching
        )
    )

    print(f"Logged in as {bot.user}")

@bot.tree.command(name="tiertest", description="Submit a tier test result")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(
    ign="The in-game name of the player",
    score="Final score (e.g. 3-0)",
    tier="Tier achieved",
    gamemode="Gamemode tested",
    comments="Tester comments"
)
@app_commands.choices(
    gamemode=get_gamemode_choices(),
    tier=get_tier_choices()
)
async def tiertest(
    interaction: discord.Interaction,
    ign: str,
    score: str,
    tier: app_commands.Choice[str],
    gamemode: app_commands.Choice[str],
    comments: str = "No comments"
):
    """Submit a tier test result to the database"""
    tester_id = interaction.user.id
    gamemode_value = gamemode.value
    tier_value = tier.value

    # Insert into database
    async with aiosqlite.connect(config["database"]) as db:
        await db.execute("""
        INSERT INTO tiertests (ign, user_id, gamemode, score, tier, comments, tester_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (ign, interaction.user.id, gamemode_value, score, tier_value, comments, tester_id))
        await db.commit()

    # Create embed with configurable emoji
    embed = discord.Embed(
        title=f"{config['emojis']['test_passed']} Tier Test Result",
        color=int(config["colors"]["embed"], 16)
    )
    embed.add_field(name="**IGN**", value=f"`{ign}`", inline=False)
    embed.add_field(name="**Gamemode**", value=gamemode_value.title(), inline=False)
    embed.add_field(name="**Score**", value=score, inline=False)
    embed.add_field(name="**Tier**", value=tier_value, inline=False)
    embed.add_field(name="**Comments**", value=comments, inline=False)
    embed.add_field(name="**Tester**", value=interaction.user.mention, inline=False)

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="tierlist", description="Show tier leaderboard for a gamemode")
@app_commands.describe(
    gamemode="The gamemode to show leaderboard for"
)
@app_commands.choices(
    gamemode=get_gamemode_choices()
)
async def tierlist(interaction: discord.Interaction, gamemode: app_commands.Choice[str]):
    """Display tier leaderboard and assign roles"""
    gamemode_value = gamemode.value
    
    # Fetch records from database
    async with aiosqlite.connect(config["database"]) as db:
        cursor = await db.execute("""
        SELECT ign, tier, score, user_id 
        FROM tiertests 
        WHERE gamemode = ?
        """, (gamemode_value,))
        rows = await cursor.fetchall()

    if not rows:
        return await interaction.response.send_message(
            f"No records found for **{gamemode_value.title()}**"
        )

    # Create embed with configurable emoji
    embed = discord.Embed(
        title=f"{config['emojis']['leaderboard']} {gamemode_value.title()} Tier List",
        color=int(config["colors"]["embed"], 16)
    )

    # Organize by tier
    tiers = {}
    for ign, tier, score, user_id in rows:
        if tier not in tiers:
            tiers[tier] = []
        tiers[tier].append({
            "ign": ign,
            "user_id": user_id,
            "emoji": config["emojis"]["tier_entry"]
        })

    # Assign roles to members
    for ign, tier, score, user_id in rows:
        try:
            member = interaction.guild.get_member(int(user_id))
            if member:
                role_name = f"{gamemode_value.title()} {tier}"
                role = discord.utils.get(interaction.guild.roles, name=role_name)

                if role and role not in member.roles:
                    await member.add_roles(role)
        except Exception as e:
            print(f"Error assigning role: {e}")

    # Add tier fields to embed in order
    for tier in config["tiers"]:
        if tier in tiers:
            tier_entries = "\n".join(
                f"{entry['emoji']} {entry['ign']}"
                for entry in tiers[tier]
            )
            embed.add_field(name=f"{tier} Tier", value=tier_entries, inline=False)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="reloadconfig", description="Reload the configuration file")
@app_commands.checks.has_permissions(administrator=True)
async def reloadconfig(interaction: discord.Interaction):
    """Reload the configuration file without restarting the bot"""
    global config
    try:
        config = load_config()
        await interaction.response.send_message("✅ Configuration reloaded successfully!")
    except Exception as e:
        await interaction.response.send_message(f"❌ Error loading config: {e}")

if __name__ == "__main__":
    # Validate config before running
    required_keys = ["token", "database", "emojis", "gamemodes", "tiers"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")
    
    bot.run(config["token"])