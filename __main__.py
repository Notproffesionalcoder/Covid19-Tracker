import discord
from discord.ext import commands
from discord.ext.commands import when_mentioned_or
from discord.utils import get
from discord.ext.commands import bot

client = commands.Bot(command_prefix=when_mentioned_or("-"))
client.remove_command("help")


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("with statistics"))
    print("Ready")


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
                          "Thanks for inviting me to the server.\nFor detailed information about commands, type `-help`"
                          , color=discord.Color.green())
    embed.set_author(name="Covid-19 Tracker",
                     icon_url="https://images-ext-2.discordapp.net/external/OR3Jfbi8p9tH1j9N0Eo7neQ8aZp8ADMptXYCBxBoyHg/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/694820915669893201/cebbb95d2fb4d74981512ffd39c7035e.webp?width=610&height=610")
    embed.add_field(name="Prefix", value="`-` or `@mention`", inline=False)
    embed.add_field(name="Bot Invite Link", value="[:envelope: Invite](https://discordapp.com/oauth2/authorize?client_id=694820915669893201&permissions=392257&scope=bot)", inline=False)
    embed.add_field(name="Bot Source code", value="[:tools: GitHub](https://github.com/pseudocoder10/Covid19-Tracker)", inline=False)
    embed.set_footer(text="Made by bhavya#9855")

    await channel.send(embed=embed)


@client.command()
async def invite(ctx):
    embed = discord.Embed(color=discord.Color.blue())
    embed.set_author(name="Covid-19 Tracker",
                     icon_url="https://images-ext-2.discordapp.net/external/OR3Jfbi8p9tH1j9N0Eo7neQ8aZp8ADMptXYCBxBoyHg/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/694820915669893201/cebbb95d2fb4d74981512ffd39c7035e.webp?width=610&height=610")
    embed.add_field(name="Prefix", value="`-` or `@mention`", inline=True)
    embed.add_field(name="Bot Invite Link",
                    value="[:envelope: Invite](https://discordapp.com/oauth2/authorize?client_id=694820915669893201&permissions=392257&scope=bot)",
                    inline=True)
    embed.add_field(name="Bot Source code", value="[:tools: GitHub](https://github.com/pseudocoder10/Covid19-Tracker)",
                    inline=True)
    embed.set_footer(text="Made by bhavya#9855")
    await ctx.send(embed=embed)


@client.command()
async def help(ctx):
    desc = ""
    desc += "__General Commands__\n\n"
    desc += "1. `-overall`\nGet Overall stats about Covid-19\nEx: **-overall**\n"
    desc += "2. `-stats <country_name or ISO2/3 code>`\nGet statistics about a particular country. Find out ISO codes [here](https://en.wikipedia.org/wiki/ISO_3166-1#Current_codes)\nEx: **-stats united states of america** or **-stats usa** or **-stats us**\n"
    desc += "3. `-plot <country_name or ISO2/3 code>`\nPlot linear and logarithmic graphs for a particular country\nEx: **-plot India** or **-plot ind** or **-plot in**\n\n"
    desc += "__India specific commands__\n\n"
    desc += "1. `-ind stats`\nGet stats about a particular state/union-territory/city of India\nEx: **-ind stats**\n"
    desc += "2. `-ind today`\nGet stats about new cases/deaths/recoveries in India today\nEx: **-ind today**\n\n"
    desc += "__Miscellaneous Commands__\n\n"
    desc += "1. `-invite` Invite the bot to your server\n2. `-help` Display help (this message)\n\n"

    embed=discord.Embed(description=desc, color=discord.Color.blue())
    embed.set_author(name="Information About Commands")
    embed.set_footer(text="Made by bhavya#9855")
    embed.add_field(name="Prefix", value="`-` or `@mention`", inline=True)
    embed.add_field(name="Bot Invite Link",
                    value="[:envelope: Invite](https://discordapp.com/oauth2/authorize?client_id=694820915669893201&permissions=392257&scope=bot)",
                    inline=True)
    embed.add_field(name="Bot Source code", value="[:tools: GitHub](https://github.com/pseudocoder10/Covid19-Tracker)",
                    inline=True)
    await ctx.send(embed=embed)


if __name__ == "__main__":
    try:
        client.load_extension("bot")
        client.load_extension("india")
    except Exception as e:
        print(f'Failed to load file')
        print(str(e))
    client.run("<enter discord token here>")
