import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import when_mentioned_or
from discord.utils import get
from discord.ext.commands import bot

client = commands.Bot(command_prefix=when_mentioned_or("cov!"))
client.remove_command("help")


@client.event
async def on_ready():
    print("Ready")
    while True:
        await client.change_presence(activity=discord.Game(f"with statistics in {len(client.guilds)} servers"))
        await asyncio.sleep(600)


async def find_channel(guild):
    for c in guild.text_channels:
        if not c.permissions_for(guild.me).send_messages:
            continue
        return c
    return None


@client.event
async def on_guild_join(guild):
    channel = await find_channel(guild)
    if channel is None:
        return
    embed = discord.Embed(description=
                          "Thanks for inviting me to the server.\nFor detailed information about commands, type `cov!help`"
                          , color=discord.Color.green())
    embed.set_author(name="Covid-19 Tracker",
                     icon_url="https://images-ext-2.discordapp.net/external/OR3Jfbi8p9tH1j9N0Eo7neQ8aZp8ADMptXYCBxBoyHg/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/694820915669893201/cebbb95d2fb4d74981512ffd39c7035e.webp?width=610&height=610")
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
    embed.set_footer(text="Made by bhavya#9855")

    await channel.send(embed=embed)

    channel = client.get_channel(702437218916237313)
    await channel.send(embed=discord.Embed(
        description=f"Joined server **{guild.name}** with **{len(guild.members)}** members | Total guilds {len(client.guilds)}",
        color=discord.Color.green()))


@client.event
async def on_guild_remove(guild):
    channel = client.get_channel(702437218916237313)
    await channel.send(embed=discord.Embed(
        description=f"Left server **{guild.name}** with **{len(guild.members)}** members | Total guilds {len(client.guilds)}",
        color=discord.Color.red()))


@client.command()
async def invite(ctx):
    embed = discord.Embed(color=discord.Color.blue())
    embed.set_author(name="Covid-19 Tracker",
                     icon_url="https://images-ext-2.discordapp.net/external/OR3Jfbi8p9tH1j9N0Eo7neQ8aZp8ADMptXYCBxBoyHg/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/694820915669893201/cebbb95d2fb4d74981512ffd39c7035e.webp?width=610&height=610")
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
    embed.set_footer(text="Made by bhavya#9855")
    await ctx.send(embed=embed)


@client.command()
async def help(ctx):
    desc = ""
    desc += "__General Commands__\n\n"
    desc += "1. `cov!overall`\nGet Overall stats about Covid-19\nEx: **cov!overall**\n"
    desc += "2. `cov!top`\nGet top 10 affected countries\nEx: **cov!top**\n"
    desc += "3. `cov!stats <country_name or ISO2/3 code>`\nGet statistics about a particular country. Find out ISO codes [here](https://en.wikipedia.org/wiki/ISO_3166-1#Current_codes)\nEx: **cov!stats united states of america** or **cov!stats usa** or **cov!stats us**\n"
    desc += "4. `cov!plot <country_name or ISO2/3 code>`\nPlot linear and logarithmic graphs for a particular country\nEx: **cov!plot India** or **cov!plot ind** or **cov!plot in**\n"
    desc += "5. `cov!hist <country_name or ISO2/3 code>`\nGet past 6 days data for a particular country\nEx: **cov!hist India** or **cov!hist ind** or **cov!hist in**\n"
    desc += '6. `cov!compare <country_names or ISO2/3 code>`\nCompare graphs for a countries (use " " if country name has spaces) (5 max)\nEx: **cov!compare India US** or **cov!compare Ind "United States of America"**\n\n'

    desc += "__India specific commands__\n\n"
    desc += "1. `cov!ind stats`\nGet stats about a particular state/union-territory/city of India\nEx: **cov!ind stats**\n"
    desc += "2. `cov!ind today`\nGet stats about new cases/deaths/recoveries in India today\nEx: **cov!ind today**\n\n"
    desc += "__USA specific commands__\n\n"
    desc += "1. `cov!usa stats`\nGet stats about a particular state of USA\nEx: **cov!usa stats**\n"
    desc += "2. `cov!usa today`\nGet stats about new cases/deaths/recoveries in USA today\nEx: **cov!usa today**\n\n"
    desc += "__Miscellaneous Commands__\n\n"
    desc += "1. `cov!invite` Invite the bot to your server\n2. `cov!help` Display help (this message)\n\n"

    embed=discord.Embed(description=desc, color=discord.Color.blue())
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


@client.event
async def on_message(message):
    if message.content == f"<@!694820915669893201>" or message.content == f"<@694820915669893201>":
        embed = discord.Embed(description=
                              "Thanks for inviting me to the server.\nFor detailed information about commands, type `cov!help`"
                              , color=discord.Color.green())
        embed.set_author(name="Covid-19 Tracker",
                         icon_url="https://images-ext-2.discordapp.net/external/OR3Jfbi8p9tH1j9N0Eo7neQ8aZp8ADMptXYCBxBoyHg/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/694820915669893201/cebbb95d2fb4d74981512ffd39c7035e.webp?width=610&height=610")
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
        embed.set_footer(text="Made by bhavya#9855")

        await message.channel.send(embed=embed)
    

    await client.process_commands(message)


if __name__ == "__main__":
    try:
        client.load_extension("bot")
        client.load_extension("india")
        client.load_extension("usa")
    except Exception as e:
        print(f'Failed to load file')
        print(str(e))
    client.run("<bot token>")
