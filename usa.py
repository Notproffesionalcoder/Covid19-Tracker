import discord
from discord.ext import commands
from discord import Embed, Color, File
from random import randint
from utils import paginator, api_covid
from operator import itemgetter
import matplotlib.pyplot as plt
from io import BytesIO
import os
from datetime import datetime
import json
import random
import time


async def send_error(ctx, message):
    await ctx.send(embed=Embed(description=f"{message}", color=Color.gold()))


async def send_help(ctx):
    desc = "__USA specific commands__\n\n"
    desc += "1. `cov!usa stats`\nGet stats about a particular state of USA\nEx: **cov!usa stats**\n"
    desc += "2. `cov!usa today`\nGet stats about new cases/deaths/recoveries in USA today\nEx: **cov!usa today**\n\n"

    embed = discord.Embed(description=desc, color=discord.Color.blue())
    embed.set_author(name="Information About Commands")
    embed.set_footer(text="Made by bhavya#9855")
    embed.add_field(name="Prefix", value="`cov!` or `@mention`", inline=False)
    embed.add_field(name="Bot Invite Link",
                    value="[:envelope: Invite](https://discordapp.com/oauth2/authorize?client_id=694820915669893201&permissions=392257&scope=bot)",
                    inline=True)
    embed.add_field(name="Bot Source code",
                    value="[:tools: GitHub](https://github.com/pseudocoder10/Covid19-Tracker)",
                    inline=True)
    embed.add_field(name="Vote for me",
                    value="[:first_place: top.gg](https://top.gg/bot/694820915669893201/vote)",
                    inline=True)
    await ctx.send(embed=embed)


def send_banner():
    with open("info.json", "r") as f:
        data = json.load(f)
        f.close()
    return random.choice(data["banner"])


class Usa(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.covid = api_covid.CovidAPI()

    def embed(self, text, color=None):
        color = Color(color) if color else Color(randint(0, 0xFFFFFF))
        return Embed(description=text, color=color)

    @commands.group(brief="Stats about states of USA", invoke_without_command=True)
    async def usa(self, ctx):
        await send_help(ctx)

    @usa.command(brief='Get coronavirus stats for a state')
    async def stats(self, ctx, choice: int = None):
        count = 1
        states_data = await self.covid.get_usa_states()
        if states_data is None:
            await send_error(ctx, "API Error!")
            return

        states = []
        for x in states_data:
            states.append(x['state'])
        states = sorted(states)

        data = []
        data.append(["0", "Overall USA stats"])

        for x in states:
            data.append([str(count), x])
            count += 1

        if choice is None:
            header = ["ID", "Region"]
            message = f"To get stats for a region, type `cov!usa stats <ID of region from table>`. React to change pages"
            await paginator.Paginator(data, header, "Select the region [React to change pages]", 16, message).paginate(ctx, self.client)
            return

        if choice not in range(0, len(data)):
            await send_error(ctx, f"Please enter a valid integer between 0 and {len(data) - 1}")
            return

        if choice != 0:
            choice -= 1
            data = {}
            for x in states_data:
                if x['state'] == states[choice]:
                    data = x
            embed = discord.Embed(color=Color(randint(0, 0xFFFFFF)))
            embed.set_author(name=f"Data for the state {data['state']}", icon_url="https://corona.lmao.ninja/assets/img/flags/us.png")
            embed.set_thumbnail(url="https://corona.lmao.ninja/assets/img/flags/us.png")
            embed.add_field(name="Total Cases", value=f"{data['cases']} (+{data['todayCases']})", inline=False)
            embed.add_field(name="Total Deaths", value=f"{data['deaths']} (+{data['todayDeaths']})", inline=False)
            embed.add_field(name="Active", value=str(data['active']), inline=True)
            embed.add_field(name="Tests Conducted", value=str(data['tests']), inline=True)
            embed.add_field(name="Tests per million", value=str(data['testsPerOneMillion']), inline=True)

            embed.add_field(name="Bot Invite Link",
                            value="[:envelope: Invite](https://discordapp.com/oauth2/authorize?client_id=694820915669893201&permissions=392257&scope=bot)",
                            inline=True)
            embed.add_field(name="Bot Source code",
                            value="[:tools: GitHub](https://github.com/pseudocoder10/Covid19-Tracker)",
                            inline=True)
            embed.add_field(name="Vote for me",
                            value="[:first_place: top.gg](https://top.gg/bot/694820915669893201/vote)",
                            inline=True)
            await ctx.send(embed=embed)
            return

        else:

            cases = 0
            newcases = 0
            deaths = 0
            newdeaths = 0
            active = 0
            for x in states_data:
                cases += x['cases']
                newcases += x['todayCases']
                deaths += x['deaths']
                newdeaths += x['todayDeaths']
                active += x['active']
            data = []
            data.append([str(cases), str(active), str(deaths), str(newcases), str(newdeaths)])
            header = ["Total", "Active Cases", "Deaths", "New Cases", "New Deaths"]
            await paginator.Paginator(data, header, f"Data for USA", 10).paginate(ctx, self.client)

            all_states_data = []
            for x in states_data:
                # name total new_case death new_death
                all_states_data.append([x["state"], x["cases"], x["todayCases"], x["deaths"], x["todayDeaths"]])
            all_states_data.append(["USA", cases, newcases, deaths, newdeaths])
            all_states_data = sorted(all_states_data, key=itemgetter(1), reverse=True)
            data = [[x[0], str(x[1]), str(x[2]), str(x[3]), str(x[4])] for x in all_states_data]
            header = ["Region", "Total Cases", "New Cases", "Deaths", "New Deaths"]
            await paginator.Paginator(data, header, f"Data for India", 16).paginate(ctx, self.client)

    @usa.command(brief='Stats about daily new cases')
    async def today(self, ctx):
        states_data = await self.covid.get_usa_states()
        if states_data is None:
            await send_error(ctx, "API Error!")
            return
        cases = 0
        newcases = 0
        deaths = 0
        newdeaths = 0
        active = 0
        for x in states_data:
            cases += x['cases']
            newcases += x['todayCases']
            deaths += x['deaths']
            newdeaths += x['todayDeaths']
            active += x['active']

        all_states_data = []
        all_states_data.append(["USA", newcases, newdeaths])
        for x in states_data:
            # name new_case new_death new_recoveries
            all_states_data.append([x["state"], x["todayCases"], x["todayDeaths"]])
        all_states_data = sorted(all_states_data, key=itemgetter(1), reverse=True)

        data = [[x[0], str(x[1]), str(x[2])] for x in all_states_data]
        header = ["Region", "New Cases", "New Deaths"]
        await paginator.Paginator(data, header, f"Data for India", 16).paginate(ctx, self.client)


def setup(client):
    client.add_cog(Usa(client))