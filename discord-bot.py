import discord
from discord import app_commands
import config

from canteen_plan.canteen_plan import get_daily_menu, get_weekly_menu

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await sync_commands()


@tree.command(name="todaysplan", description="Displays today's meal plan",
              guild=discord.Object(id=config.discord_object_id))
async def displays_todays_meal_plan(ctx, tomorrow: bool = False):
    if tomorrow:
        await ctx.response.send_message(get_daily_menu(1))
    else:
        await ctx.response.send_message(get_daily_menu(0))


@tree.command(name="weeklyplan", description="Displays the weekly meal plan",
              guild=discord.Object(id=config.discord_object_id))
async def displays_weekly_meal_plan(ctx, weekly_offset: int = 0):
    await get_weekly_menu(ctx, weekly_offset)


async def sync_commands():
    await tree.sync(guild=discord.Object(id=config.discord_object_id))


def run_bot():
    client.run(config.client_token)


run_bot()
