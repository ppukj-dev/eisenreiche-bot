# app/bot.py

import app.config as config
import discord
from discord.ext import commands
from app.util.markdown import to_markdown
import asyncio

from app.repository.ability import AbilityRepository
from app.repository.archetype import ArchetypeRepository
from app.repository.skill import SkillRepository
from app.repository.spell import SpellRepository
from app.database import SessionLocal

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

ability_repo = AbilityRepository(SessionLocal())
archetype_repo = ArchetypeRepository(SessionLocal())
skill_repo = SkillRepository(SessionLocal())
spell_repo = SpellRepository(SessionLocal())


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
    result = ability_repo.find_ik_ability(keyword)
    if len(result) <= 0:
        await ctx.send("No results found.")
    elif len(result) == 1:
        await send_single_result(ctx, result[0])
    else:
        await send_multiple_results(ctx, result)


@bot.command(name="archetype")
async def archetype(ctx, *, keyword):
    result = archetype_repo.find_ik_archetype(keyword)
    if len(result) <= 0:
        await ctx.send("No results found.")
    elif len(result) == 1:
        await send_single_result(ctx, result[0])
    else:
        await send_multiple_results(ctx, result)


@bot.command(name="archetype_benefit", aliases=["benefit"])
async def archetype(ctx, *, keyword):
    result = archetype_repo.find_ik_archetype_benefit(keyword)
    if len(result) <= 0:
        await ctx.send("No results found.")
    elif len(result) == 1:
        await send_single_result(ctx, result[0])
    else:
        await send_multiple_results(ctx, result)


@bot.command(name="spell")
async def spell(ctx, *, keyword):
    result = spell_repo.find_ik_spell(keyword)
    if len(result) <= 0:
        await ctx.send("No results found.")
    elif len(result) == 1:
        await send_single_result(ctx, result[0])
    else:
        await send_multiple_results(ctx, result)


# @bot.command(name="skill")
# async def skill(ctx, *, keyword):
#     result = skill_repo.find_ik_skill(keyword)
#     if len(result) <= 0:
#         await ctx.send("No results found.")
#     elif len(result) == 1:
#         await send_single_result(ctx, result[0])
#     else:
#         await send_multiple_results(ctx, result)


def run_bot():
    bot.run(config.DISCORD_TOKEN)
