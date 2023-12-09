# app/bot.py

import app.config as config
import discord
from discord.ext import commands
from app.util.markdown import to_markdown
import asyncio
from app.model.models import Ability, Archetype, ArchetypeBenefit, Spell, Skill, RangedWeapon, MeleeWeapon, Equipment
from app.repository.search import find_ik_entity

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


async def send_single_result(ctx, entry):
    description = to_markdown(entry.details)
    embed = discord.Embed(title=entry.name, description=description)
    if hasattr(entry, "prerequisites"):
        embed.add_field(name="Prerequisites", value=entry.prerequisites, inline=True)
    if hasattr(entry, "archetype"):
        embed.add_field(name="Archetype", value=entry.archetype, inline=True)
    if hasattr(entry, "stats"):
        embed.add_field(name="Stats", value=entry.stats, inline=True)
    if hasattr(entry, "spell_cost"):
        embed.add_field(name="COST", value=entry.spell_cost, inline=True)
    if hasattr(entry, "range"):
        embed.add_field(name="RNG", value=entry.range, inline=True)
    if hasattr(entry, "aoe"):
        embed.add_field(name="AOE", value=entry.aoe, inline=True)
    if hasattr(entry, "pow"):
        embed.add_field(name="POW", value=entry.pow, inline=True)
    if hasattr(entry, "upkeep"):
        embed.add_field(name="UP", value=entry.upkeep, inline=True)
    if hasattr(entry, "offense"):
        embed.add_field(name="OFF", value=entry.offense, inline=True)
    if hasattr(entry, "cost"):
        embed.add_field(name="Cost", value=entry.cost + " gc", inline=True)
    if hasattr(entry, "ammo"):
        embed.add_field(name="Ammo", value=entry.ammo, inline=True)
    if hasattr(entry, "range_effective"):
        embed.add_field(name="Effective Range", value=entry.range_effective, inline=True)
    if hasattr(entry, "range_extreme"):
        embed.add_field(name="Extreme Range", value=entry.range_extreme, inline=True)
    if hasattr(entry, "skill"):
        embed.add_field(name="Skill", value=entry.skill, inline=True)
    if hasattr(entry, "category"):
        embed.add_field(name="Category", value=entry.category, inline=True)
    await ctx.send(embed=embed)


async def send_multiple_results(ctx, result):
    description = "Do you mean?"
    for idx, entry in enumerate(result):
        description += "\n`{0}. {1}`".format(idx+1, entry.name)
    embed = discord.Embed(title="Multiple Found", description=description)
    embed.set_footer(text="Type 1-10 to choose, or c to cancel.")
    option_message = await ctx.send(embed=embed)

    def followup(message):
        return (
                message.content.isnumeric() or message.content == "c"
        ) and message.author == ctx.message.author

    try:
        followup_message = await bot.wait_for(
            "message", timeout=60.0, check=followup
        )
    except asyncio.TimeoutError:
        await option_message.edit(content="Time Out", embed=None)
    else:
        if followup_message.content == "c":
            await option_message.delete()
            await followup_message.delete()
            return
        chosen_index = int(followup_message.content) - 1
        entry = result[chosen_index]
        await option_message.delete()
        await followup_message.delete()
        await send_single_result(ctx, entry)
        return


@bot.command(name="ability")
async def ability(ctx, *, keyword):
    result = find_ik_entity(Ability, keyword)
    if len(result) <= 0:
        await ctx.send("No results found.")
    elif len(result) == 1:
        await send_single_result(ctx, result[0])
    else:
        await send_multiple_results(ctx, result)


@bot.command(name="archetype")
async def archetype(ctx, *, keyword):
    result = find_ik_entity(Archetype, keyword)
    if len(result) <= 0:
        await ctx.send("No results found.")
    elif len(result) == 1:
        await send_single_result(ctx, result[0])
    else:
        await send_multiple_results(ctx, result)


@bot.command(name="archetype_benefit", aliases=["benefit"])
async def archetype(ctx, *, keyword):
    result = find_ik_entity(ArchetypeBenefit, keyword)
    if len(result) <= 0:
        await ctx.send("No results found.")
    elif len(result) == 1:
        await send_single_result(ctx, result[0])
    else:
        await send_multiple_results(ctx, result)


@bot.command(name="spell")
async def spell(ctx, *, keyword):
    result = find_ik_entity(Spell, keyword)
    if len(result) <= 0:
        await ctx.send("No results found.")
    elif len(result) == 1:
        await send_single_result(ctx, result[0])
    else:
        await send_multiple_results(ctx, result)


@bot.command(name="ranged_weapon", aliases=["rweapon"])
async def ranged_weapon(ctx, *, keyword):
    result = find_ik_entity(RangedWeapon, keyword)
    if len(result) <= 0:
        await ctx.send("No results found.")
    elif len(result) == 1:
        await send_single_result(ctx, result[0])
    else:
        await send_multiple_results(ctx, result)


@bot.command(name="melee_weapon", aliases=["mweapon"])
async def melee_weapon(ctx, *, keyword):
    result = find_ik_entity(MeleeWeapon, keyword)
    if len(result) <= 0:
        await ctx.send("No results found.")
    elif len(result) == 1:
        await send_single_result(ctx, result[0])
    else:
        await send_multiple_results(ctx, result)


@bot.command(name="skill")
async def skill(ctx, *, keyword):
    result = find_ik_entity(Skill, keyword)
    if len(result) <= 0:
        await ctx.send("No results found.")
    elif len(result) == 1:
        await send_single_result(ctx, result[0])
    else:
        await send_multiple_results(ctx, result)


@bot.command(name="equipment")
async def equipment(ctx, *, keyword):
    result = find_ik_entity(Equipment, keyword)
    if len(result) <= 0:
        await ctx.send("No results found.")
    elif len(result) == 1:
        await send_single_result(ctx, result[0])
    else:
        await send_multiple_results(ctx, result)


def run_bot():
    bot.run(config.DISCORD_TOKEN)
