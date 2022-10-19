import discord
from discord import app_commands
import config
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)



@client.event
async def on_ready():
    await sync_commands()


@tree.command(name="todaysplan", description="Displays today's meal plan", guild=discord.Object(id=config.discord_object_id))
async def displays_todays_meal_plan(ctx):
    await ctx.response.send_message(f"Das Essen wurde heute nicht gekocht")


@tree.command(name="weeklyplan", description="Displays the weekly meal plan", guild=discord.Object(id=config.discord_object_id))
async def displays_weekly_meal_plan(ctx):
    await ctx.response.send_message(f"Das Essen wurde diese Woche nicht gekocht")


async def sync_commands():
    await tree.sync(guild=discord.Object(id=config.discord_object_id))


def run_bot():
    client.run(config.client_token)


run_bot()
