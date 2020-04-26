import urllib

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
import re
import requests


async def send_error(ctx, message):
    await ctx.send(embed=Embed(description=f"{message}", color=Color.gold()))


def send_banner():
    with open("info.json", "r") as f:
        data = json.load(f)
        f.close()
    return random.choice(data["banner"])


def get_url_images_in_text(country):
    '''finds image urls'''
    country.replace(" ", "_")
    resp = requests.get(f"https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_{country}")
    text = resp.text
    urls = []
    results = re.findall(r'(?:http\:|https\:)?\/\/.*\.(?:png|jpg)', text)
    for x in results:
      urls.append(x)
    if len(urls[0]) < 300:
        return urls[0]

    country = "the_"+country
    resp = requests.get(f"https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_{country}")
    text = resp.text
    urls = []
    results = re.findall(r'(?:http\:|https\:)?\/\/.*\.(?:png|jpg)', text)
    for x in results:
        urls.append(x)
    if len(urls[0]) < 300:
        return urls[0]

    return None


async def plot_graph1(ctx, iso3, num, name):
    data = await api_covid.CovidAPI().get_country_timeline1(iso3)
    if data is None:
        await send_error(ctx, "API Error!")
        return
    x_axis = []
    cases = []
    deaths = []
    recovery = []
    for x in data['result']:
        try:
            x_axis.append(datetime.strptime(str(x), '%Y-%m-%d'))
            cases.append(data['result'][x]['confirmed'])
            deaths.append(data['result'][x]['deaths'])
            recovery.append(data['result'][x]['recovered'])
        except Exception:
            pass
    plt.plot(x_axis, cases, color='yellow', linestyle='-', marker='o', markersize=4, markerfacecolor='yellow', label="Total Cases")
    plt.plot(x_axis, recovery, color='green', linestyle='-', marker='o', markersize=4, markerfacecolor='green', label="Total Recoveries")
    plt.plot(x_axis, deaths, color='red', linestyle='-', marker='o', markersize=4, markerfacecolor='red', label="Total Deaths")

    plt.gcf().autofmt_xdate()
    plt.grid()
    plt.legend()
    ax = plt.axes()
    plt.setp(ax.get_xticklabels(), color="white")
    plt.setp(ax.get_yticklabels(), color="white")
    filename = "%s.png" % str(ctx.message.id)
    plt.savefig(filename, transparent=True)
    with open(filename, 'rb') as file:
        discord_file = File(BytesIO(file.read()), filename='plot.png')
    os.remove(filename)
    plt.clf()
    plt.close()
    embed = Embed(title=f"Linear graph for country {name}", color=Color.blue())
    embed.set_image(url="attachment://plot.png")
    embed.set_footer(text=send_banner(), icon_url=ctx.author.avatar_url)
    if num == -1:
        return discord_file
    embed.add_field(name="Bot Invite Link",
                    value="[:envelope: Invite](https://discordapp.com/oauth2/authorize?client_id=694820915669893201&permissions=392257&scope=bot)",
                    inline=True)
    embed.add_field(name="Bot Source code",
                    value="[:tools: GitHub](https://github.com/pseudocoder10/Covid19-Tracker)",
                    inline=True)
    embed.add_field(name="Vote for me",
                    value="[:first_place: top.gg](https://top.gg/bot/694820915669893201/vote)",
                    inline=True)
    await ctx.channel.send(embed=embed, file=discord_file)
    if num == 0:
        return

    plt.plot(x_axis, cases, color='yellow', linestyle='-', marker='o', markersize=4, markerfacecolor='yellow',
             label="Total Cases")
    plt.plot(x_axis, recovery, color='green', linestyle='-', marker='o', markersize=4, markerfacecolor='green',
             label="Total Recoveries")
    plt.plot(x_axis, deaths, color='red', linestyle='-', marker='o', markersize=4, markerfacecolor='red',
             label="Total Deaths")

    plt.gcf().autofmt_xdate()
    plt.grid()
    plt.legend()
    ax = plt.axes()
    ax.set_yscale('log')
    plt.setp(ax.get_xticklabels(), color="white")
    plt.setp(ax.get_yticklabels(), color="white")
    filename = "%s.png" % str(ctx.message.id)
    plt.savefig(filename, transparent=True)
    with open(filename, 'rb') as file:
        discord_file = File(BytesIO(file.read()), filename='plot.png')
    os.remove(filename)
    plt.clf()
    plt.close()
    embed = Embed(title=f"Logarithmic graph for country {name}",
                  color=Color.blue())
    embed.set_image(url="attachment://plot.png")
    embed.add_field(name="Bot Invite Link",
                    value="[:envelope: Invite](https://discordapp.com/oauth2/authorize?client_id=694820915669893201&permissions=392257&scope=bot)",
                    inline=True)
    embed.add_field(name="Bot Source code",
                    value="[:tools: GitHub](https://github.com/pseudocoder10/Covid19-Tracker)",
                    inline=True)
    embed.add_field(name="Vote for me",
                    value="[:first_place: top.gg](https://top.gg/bot/694820915669893201/vote)",
                    inline=True)
    embed.set_footer(text=send_banner(), icon_url=ctx.author.avatar_url)
    await ctx.channel.send(embed=embed, file=discord_file)


async def plot_graph2(ctx, iso3, name):
    data = await api_covid.CovidAPI().get_country_timeline1(iso3[0])
    if data is None:
        await send_error(ctx, "API Error!")
        return
    x_axis = []
    cases = []
    for x in data['result']:
        try:
            x_axis.append(datetime.strptime(str(x), '%Y-%m-%d'))
        except Exception:
            pass
    for x in iso3:
        data = await api_covid.CovidAPI().get_country_timeline1(x)
        if data is None:
            await send_error(ctx, "API Error!")
            return
        arr = []
        for y in data['result']:
            try:
                arr.append(data['result'][y]['confirmed'])
            except Exception:
                pass
        cases.append(arr)
    col = ["red", "orange", "green", "blue", "yellow"]
    for i in range(0, len(iso3)):
        plt.plot(x_axis, cases[i], color=col[i], linestyle='-', marker='o', markersize=4, markerfacecolor=col[i],
                 label=name[i])

    plt.gcf().autofmt_xdate()
    plt.grid()
    plt.legend()
    ax = plt.axes()
    plt.setp(ax.get_xticklabels(), color="white")
    plt.setp(ax.get_yticklabels(), color="white")
    filename = "%s.png" % str(ctx.message.id)
    plt.savefig(filename, transparent=True)
    with open(filename, 'rb') as file:
        discord_file = File(BytesIO(file.read()), filename='plot.png')
    os.remove(filename)
    plt.clf()
    plt.close()
    embed = Embed(title=f"Linear graph for country {name}", color=Color.blue())
    embed.set_image(url="attachment://plot.png")
    embed.set_footer(text=send_banner(), icon_url=ctx.author.avatar_url)
    embed.add_field(name="Bot Invite Link",
                    value="[:envelope: Invite](https://discordapp.com/oauth2/authorize?client_id=694820915669893201&permissions=392257&scope=bot)",
                    inline=True)
    embed.add_field(name="Bot Source code",
                    value="[:tools: GitHub](https://github.com/pseudocoder10/Covid19-Tracker)",
                    inline=True)
    embed.add_field(name="Vote for me",
                    value="[:first_place: top.gg](https://top.gg/bot/694820915669893201/vote)",
                    inline=True)
    await ctx.channel.send(embed=embed, file=discord_file)


async def plot_graph(ctx, iso2, num):
    data = await api_covid.CovidAPI().get_country_timeline(iso2)
    if data is None:
        await send_error(ctx, "API Error!")
        return
    x_axis = []
    cases = []
    deaths = []
    recovery = []
    for x in data['timelineitems'][0]:
        try:
            x_axis.append(datetime.strptime(str(x), '%m/%d/%y'))
            cases.append(data['timelineitems'][0][x]['total_cases'])
            deaths.append(data['timelineitems'][0][x]['total_deaths'])
            recovery.append(data['timelineitems'][0][x]['total_recoveries'])
        except Exception:
            pass
    plt.plot(x_axis, cases, color='yellow', linestyle='-', marker='o', markersize=4, markerfacecolor='yellow', label="Total Cases")
    plt.plot(x_axis, recovery, color='green', linestyle='-', marker='o', markersize=4, markerfacecolor='green', label="Total Recoveries")
    plt.plot(x_axis, deaths, color='red', linestyle='-', marker='o', markersize=4, markerfacecolor='red', label="Total Deaths")

    plt.gcf().autofmt_xdate()
    plt.grid()
    plt.legend()
    ax = plt.axes()
    plt.setp(ax.get_xticklabels(), color="white")
    plt.setp(ax.get_yticklabels(), color="white")
    filename = "%s.png" % str(ctx.message.id)
    plt.savefig(filename, transparent=True)
    with open(filename, 'rb') as file:
        discord_file = File(BytesIO(file.read()), filename='plot.png')
    os.remove(filename)
    plt.clf()
    plt.close()
    embed = Embed(title=f"Linear graph for country {data['countrytimelinedata'][0]['info']['title']}", color=Color.blue())
    embed.set_image(url="attachment://plot.png")
    embed.set_footer(text=send_banner(), icon_url=ctx.author.avatar_url)
    await ctx.channel.send(embed=embed, file=discord_file)
    if num == 0:
        return

    plt.plot(x_axis, cases, color='yellow', linestyle='-', marker='o', markersize=4, markerfacecolor='yellow',
             label="Total Cases")
    plt.plot(x_axis, recovery, color='green', linestyle='-', marker='o', markersize=4, markerfacecolor='green',
             label="Total Recoveries")
    plt.plot(x_axis, deaths, color='red', linestyle='-', marker='o', markersize=4, markerfacecolor='red',
             label="Total Deaths")

    plt.gcf().autofmt_xdate()
    plt.grid()
    plt.legend()
    ax = plt.axes()
    ax.set_yscale('log')
    plt.setp(ax.get_xticklabels(), color="white")
    plt.setp(ax.get_yticklabels(), color="white")
    filename = "%s.png" % str(ctx.message.id)
    plt.savefig(filename, transparent=True)
    with open(filename, 'rb') as file:
        discord_file = File(BytesIO(file.read()), filename='plot.png')
    os.remove(filename)
    plt.clf()
    plt.close()
    embed = Embed(title=f"Logarithmic graph for country {data['countrytimelinedata'][0]['info']['title']}",
                  color=Color.blue())
    embed.set_image(url="attachment://plot.png")
    embed.set_footer(text=send_banner(), icon_url=ctx.author.avatar_url)
    await ctx.channel.send(embed=embed, file=discord_file)


class Tracker(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.covid = api_covid.CovidAPI()

    def embed(self, text, color=None):
        color = Color(color) if color else Color(randint(0, 0xFFFFFF))
        return Embed(description=text, color=color)

    @commands.command(brief='Plot various graphs about a country')
    async def plot(self, ctx, *, country:str = None):
        """Usage: `cov!plot <country 2/3 digit code>` or `cov!plot <country_name>`"""
        
        if country is None:
            await ctx.send(f"Usage: `cov!plot <country 2/3 digit code>` or `cov!plot <country_name>`")
            return
        iso2 = ""
        name = ""
        slug = ""

        if len(country) == 3:
            try:
                country = await self.covid.iso3_to_iso2(country.lower())
            except Exception:
                pass

        data = await self.covid.get_countries_list()
        if data is None:
            await send_error(ctx, "API Error!")
            return

        if country.upper() == "IRAN":
            country = "ir"
        if country.upper() == "RUSSIA":
            country = "ru"

        for x in data:
            try:
                if x['Country'].upper() == country.upper() or x['ISO2'] == country.upper():
                    iso2 = x['ISO2']
                    name = x['Country']
                    slug = x['Slug']
                    break
            except Exception:
                pass

        if len(iso2) == 0:
            await send_error(ctx, "Please enter a valid Country Name or ISO2 or ISO3 code")
            return
        if iso2.lower() == "ir":
            name = "Iran"
        if iso2.lower() == "ru":
            name = "Russia"
        iso3 = await self.covid.iso2_to_iso3(iso2)

     #  await plot_graph(ctx, iso2, 1)
        await plot_graph1(ctx,iso3,1, name)

    @commands.command(brief="Get stats about any country")
    async def stats(self, ctx, *, country:str = None):
        """Usage: `cov!stats <country 2/3 digit code>` or `cov!stats <country_name>`"""

        if country is None:
            await ctx.send(f"Usage: `cov!stats <country 2/3 digit code>` or `cov!stats <country_name>`")
            return

        iso2 = ""
        name = ""
        slug = ""

        if len(country) == 3:
            country = await self.covid.iso3_to_iso2(country.lower())

        data = await self.covid.get_countries_list()
        if data is None:
            await send_error(ctx, "API Error!")
            return

        if country.upper() == "IRAN":
            country = "ir"
        if country.upper() == "RUSSIA":
            country = "ru"

        for x in data:
            try:
                if x['Country'].upper() == country.upper() or x['ISO2'] == country.upper():
                    iso2 = x['ISO2']
                    name = x['Country']
                    slug = x['Slug']
                    break
            except Exception:
                pass

        if len(iso2) == 0:
            await send_error(ctx, "Please enter a valid Country Name or ISO2 or ISO3 code")
            return

        if iso2.lower() == "ir":
            name = "Iran"
        if iso2.lower() == "ru":
            name = "Russia"

        data = await self.covid.get_country_data(iso2)
        tme = round(time.time())
        tme -= data['updated']
        hrs = int(tme / 3600)
        tme = tme % 3600
        min = int(tme / 60)
        tme = tme % 60
        hrs = max(hrs, 0)
        min = max(min, 0)
        update = f"Updated {hrs} hours {min} minutes and {tme} seconds ago"
        embed = discord.Embed(color=Color(randint(0, 0xFFFFFF)))
        embed.set_author(name=f"Data for the country {name}", icon_url=data['countryInfo']['flag'])
        embed.set_thumbnail(url=data['countryInfo']['flag'])
        embed.add_field(name="Total Cases", value=f"{data['cases']} (+{data['todayCases']})", inline=False)
        embed.add_field(name="Total Deaths", value=f"{data['deaths']} (+{data['todayDeaths']})", inline=False)
        embed.add_field(name="Total Recoveries", value=f"{data['recovered']}", inline=False)
        embed.add_field(name="Active", value=str(data['active']), inline=True)
        embed.add_field(name="Critical", value=str(data['critical']), inline=True)
        embed.add_field(name="Tests Conducted", value=str(data['tests']), inline=True)
        embed.set_footer(text=update)

        embed.add_field(name="Bot Invite Link",
                        value="[:envelope: Invite](https://discordapp.com/oauth2/authorize?client_id=694820915669893201&permissions=392257&scope=bot)",
                        inline=True)
        embed.add_field(name="Bot Source code",
                        value="[:tools: GitHub](https://github.com/pseudocoder10/Covid19-Tracker)",
                        inline=True)
        embed.add_field(name="Vote for me",
                        value="[:first_place: top.gg](https://top.gg/bot/694820915669893201/vote)",
                        inline=True)

        iso3 = await self.covid.iso2_to_iso3(iso2)

        with open("wiki.json", "r") as f:
            data = json.load(f)
            f.close()
        pic = get_url_images_in_text(data[iso2.upper()])
        if pic is not None:
            embed.set_image(url=pic)
        else:
            url = await plot_graph1(ctx, iso3, -1, name)
            embed.set_image(url="attachment://plot.png")
            await ctx.send(embed=embed, file=url)
            return
        await ctx.send(embed=embed)


      #  await plot_graph(ctx, iso2, 0)
      #  await plot_graph1(ctx, iso3, 0,name)

    @commands.command(brief="Overall Stats about Covid-19")
    async def overall(self, ctx, *, country: str = None):

        data = await self.covid.get_overall_data()
        if data is None:
            await send_error(ctx, "API Error!")
            return

        tme = round(time.time())
        tme -= data['updated']
        hrs = int(tme / 3600)
        tme = tme % 3600
        min = int(tme / 60)
        tme = tme % 60
        hrs = max(hrs, 0)
        min = max(min, 0)
        update = f"Updated {hrs} hours {min} minutes and {tme} seconds ago"

        embed = Embed(colour=Color(randint(0, 0xFFFFFF)))
        embed.set_author(name="Overall Stats about Covid-19", icon_url="https://images-ext-2.discordapp.net/external/OR3Jfbi8p9tH1j9N0Eo7neQ8aZp8ADMptXYCBxBoyHg/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/694820915669893201/cebbb95d2fb4d74981512ffd39c7035e.webp?width=610&height=610")
        embed.add_field(name="Total Cases", value=str(data["cases"])+f" (+{data['todayCases']})", inline=False)
        embed.add_field(name="Total Deaths", value=str(data["deaths"])+f" (+{data['todayDeaths']})", inline=False)
        embed.add_field(name="Total Recoveries", value=str(data["recovered"]), inline=False)
        embed.add_field(name="Active Cases", value=str(data["active"]), inline=False)
        embed.add_field(name="Critical Cases", value=str(data["critical"]), inline=False)
        embed.add_field(name="Affected Countries", value=str(data["affectedCountries"]), inline=False)

        embed.set_image(url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/COVID-19_Outbreak_World_Map_per_Capita.svg/640px-COVID-19_Outbreak_World_Map_per_Capita.svg.png")
        embed.set_footer(text=update)
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

    @commands.command(bried="Worst affected countries")
    async def top(self,ctx):
        data = await self.covid.get_all_countries_data()
        if data is None:
            await send_error(ctx, "API Error!")
            return
        data = sorted(data, key=lambda i: i['cases'], reverse=True)

        data1 = []
        i = 0
        name, cases, death = "", "", ""
        for x in data:
            if i == 10:
                break
            name += f"\n:flag_{x['countryInfo']['iso2'].lower()}: {x['country']}"
            cases += f"\n{x['cases']} (+{x['todayCases']})"
            death += f"\n{x['deaths']} (+{x['todayDeaths']})"
            data1.append([name, cases, death])
            i += 1
        embed = Embed(colour=Color(randint(0, 0xFFFFFF)))
        embed.set_author(name="Worst affected countries",
                         icon_url="https://images-ext-2.discordapp.net/external/OR3Jfbi8p9tH1j9N0Eo7neQ8aZp8ADMptXYCBxBoyHg/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/694820915669893201/cebbb95d2fb4d74981512ffd39c7035e.webp?width=610&height=610")

        embed.add_field(name="Country", value=name, inline=True)
        embed.add_field(name="Total Cases", value=cases, inline=True)
        embed.add_field(name="Total Deaths", value=death, inline=True)
        embed.set_footer(text="Bot made by @bhavya#9855")

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

    @commands.command(brief="Compare countries")
    async def compare(self, ctx, *args:str):
        countries = args
        if len(countries) == 0:
            await send_error(ctx, "Usage `cov!compare <list of countries>`")
            return
        if len(countries) > 5:
            await send_error(ctx, "Please enter atmost 5 countries")
            return

        iso2 = []
        name = []
        slug = []
        country = []

        for i in countries:
            if len(i) == 3:
                try:
                    country.append(await self.covid.iso3_to_iso2(i.lower()))
                except Exception:
                    pass
            else:
                country.append(i)

        data = await self.covid.get_countries_list()
        if data is None:
            await send_error(ctx, "API Error!")
            return

        for x in data:
            for i in country:
                try:
                    if x['Country'].upper() == i.upper() or x['ISO2'] == i.upper():
                        iso2.append(x['ISO2'])
                        name.append(x['Country'])
                        slug.append(x['Slug'])
                        break
                except Exception:
                    pass
        if len(iso2) == 0:
            await send_error(ctx, "Please enter a valid Country Name or ISO2 or ISO3 code")
            return
        iso3 = []
        for x in iso2:
            iso3.append(await self.covid.iso2_to_iso3(x))
        await plot_graph2(ctx,iso3,name)

    @commands.command(brief='Plot stats about last 6 days')
    async def hist(self, ctx, *, country: str = None):
        """Usage: `cov!hist <country 2/3 digit code>` or `cov!hist <country_name>`"""

        if country is None:
            await ctx.send(f"Usage: `cov!hist <country 2/3 digit code>` or `cov!hist <country_name>`")
            return
        iso2 = ""
        name = ""
        slug = ""

        if len(country) == 3:
            try:
                country = await self.covid.iso3_to_iso2(country.lower())
            except Exception:
                pass

        data = await self.covid.get_countries_list()
        if data is None:
            await send_error(ctx, "API Error!")
            return

        if country.upper() == "IRAN":
            country = "ir"
        if country.upper() == "RUSSIA":
            country = "ru"

        for x in data:
            try:
                if x['Country'].upper() == country.upper() or x['ISO2'] == country.upper():
                    iso2 = x['ISO2']
                    name = x['Country']
                    slug = x['Slug']
                    break
            except Exception:
                pass

        if len(iso2) == 0:
            await send_error(ctx, "Please enter a valid Country Name or ISO2 or ISO3 code")
            return
        if iso2.lower() == "ir":
            name = "Iran"
        if iso2.lower() == "ru":
            name = "Russia"
        iso3 = await self.covid.iso2_to_iso3(iso2)
        data = await self.covid.get_country_timeline1(iso3)
        if data is None:
            await send_error(ctx, "API Error!")
            return

        data = data['result']
        dates = []
        val = []
        for x in data:
            dates.append(x)
            val.append([data[x]['confirmed'], data[x]['deaths'], data[x]['recovered']])

        dates.reverse()
        val.reverse()
        val = [val[i] for i in range(0, 7)]
        dates = [dates[i] for i in range(0, 7)]
        dates = [datetime.strptime(x, '%Y-%m-%d').strftime('%d %b') for x in dates]

        embed = discord.Embed(color=Color(randint(0, 0xFFFFFF)))
        embed.set_author(name=f"Last 6 days Data for the country {name}", icon_url=f"https://corona.lmao.ninja/assets/img/flags/{iso2.lower()}.png")
        embed.set_thumbnail(url=f"https://corona.lmao.ninja/assets/img/flags/{iso2.lower()}.png")
        for i in range(0, 6):
            embed.add_field(name=f":calendar_spiral: {dates[i]}", value=f"Tot: {val[i][0]} \n`(+{val[i][0]-val[i+1][0]})`\nDead: {val[i][1]} \n`(+{val[i][1]-val[i+1][1]})`\nRec: {val[i][2]} \n`(+{val[i][2]-val[i+1][2]})`\n")

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


def setup(client):
    client.add_cog(Tracker(client))