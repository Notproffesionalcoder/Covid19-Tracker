# Covid19-Tracker

A discord bot coded in python for information and stats about ongoing Novel Coronavirus (Covid-19). Invite the bot to your server using this  [link](https://discordapp.com/oauth2/authorize?client_id=694820915669893201&permissions=392257&scope=bot)

The bot shows detailed statistics about confirmed cases/deaths/recoveries of any country along with various graphs. The bot additionally provides more information about every state/district of India.

Data about the bot is extracted from various API's provided by [covid19india.org](https://www.covid19india.org/), [NovelCovid API](https://github.com/novelcovid/api) and [TheVirusTracker](https://thevirustracker.com/)

The prefix for the bot is `-` or `@mention`. Type `-help` for information about commands.

## Features
### General Commands:
* `-overall`: Get overall stats about coronavirus.
![](https://i.imgur.com/3pc6RAa.png)
![](https://i.imgur.com/n15gNKy.png)
* `-stats <country_name or ISO2/3 code>`: Get statistics about a particular country. Find out ISO codes [here](https://en.wikipedia.org/wiki/ISO_3166-1#Current_codes "here")
![](https://i.imgur.com/zDcnLmh.png)
* `-plot <country_name or ISO2/3 code>`: Plot linear and logarithmic graphs for a particular country
![](https://i.imgur.com/g3LaAhy.png)
### India specific Commands:
* `-ind stats`: Get stats about a particular state/union-territory/city of India
![](https://i.imgur.com/lR78Vas.png)
![](https://i.imgur.com/7YQe71k.png)
* `-ind today`: Get stats about new cases/deaths/recoveries in India today
![](https://i.imgur.com/r6523cF.png)
### Miscellaneous Commands 
* `-invite` Invite the bot to your server 
* `-help` Displays help about commands 

#### To try the bot yourself, invite the bot to your server using this [link](https://discordapp.com/oauth2/authorize?client_id=694820915669893201&permissions=392257&scope=bot)
