<a href="https://top.gg/bot/694820915669893201" >
  <img src="https://top.gg/api/widget/694820915669893201.svg" alt="Covid-19 Tracker" />
</a>

# Covid19-Tracker

A discord bot coded in python for information and stats about ongoing Novel Coronavirus (Covid-19). Invite the bot to your server using this  [link](https://discordapp.com/oauth2/authorize?client_id=694820915669893201&permissions=392257&scope=bot)

The bot shows detailed statistics about confirmed cases/deaths/recoveries of any country along with various graphs, trends and comparison between countries. The bot additionally provides more information about every state/district of India and USA.

Data about the bot is extracted from various API's provided by [covid19india.org](https://www.covid19india.org/), [NovelCovid API](https://github.com/novelcovid/api) and [TheVirusTracker](https://thevirustracker.com/)

The prefix for the bot is `cov!` or `@mention`. Type `cov!help` for information about commands.

## Features
### General Commands:

* `cov!overall`: Get overall stats about coronavirus.

![](https://raw.githubusercontent.com/pseudocoder10/Covid19-Tracker/master/screenshots/overall.png)
* `cov!top`: Shows list of worst affected countries

![](https://raw.githubusercontent.com/pseudocoder10/Covid19-Tracker/master/screenshots/top.png)
* `cov!stats <country_name or ISO2/3 code>`: Get statistics about a particular country. Find out ISO codes [here](https://en.wikipedia.org/wiki/ISO_3166-1#Current_codes "here")

![](https://raw.githubusercontent.com/pseudocoder10/Covid19-Tracker/master/screenshots/stats.png)

* `cov!plot <country_name or ISO2/3 code>`: Plot linear and logarithmic graphs for a particular country

![](https://raw.githubusercontent.com/pseudocoder10/Covid19-Tracker/master/screenshots/plot.png)
* `cov!compare <list of countries>`: Compare Covid-19 graphs of various countries.

![](https://raw.githubusercontent.com/pseudocoder10/Covid19-Tracker/master/screenshots/compare.png)
* `cov!hist <country_name or ISO2/3 code>`: Show past 6 days statistics for a country.

![](https://raw.githubusercontent.com/pseudocoder10/Covid19-Tracker/master/screenshots/hist.png)
### India specific Commands:
* `cov!ind stats`: Get stats about a particular state/union-territory/city of India

![](https://raw.githubusercontent.com/pseudocoder10/Covid19-Tracker/master/screenshots/ind_stats.png)
Also shows data for districts for any state:

![](https://i.imgur.com/7YQe71k.png)

* `cov!ind today`: Get stats about new cases/deaths/recoveries in India today

![](https://media.discordapp.net/attachments/669978544914432040/704224304719593532/unknown.png)

### USA specific Commands:
* `cov!usa stats`: Get stats about a particular state/union-territory/city of India

![](https://media.discordapp.net/attachments/669978544914432040/704225579775295578/unknown.png)
Also shows data for any state specifically:

![](https://raw.githubusercontent.com/pseudocoder10/Covid19-Tracker/master/screenshots/usa_stats.png)

* `cov!usa today`: Get stats about new cases/deaths/recoveries in India today

![](https://raw.githubusercontent.com/pseudocoder10/Covid19-Tracker/master/screenshots/usa_today.png)

### Miscellaneous Commands 
* `cov!invite` Invite the bot to your server 
* `cov!help` Displays help about commands 

#### To try the bot yourself, invite the bot to your server using this [link](https://discordapp.com/oauth2/authorize?client_id=694820915669893201&permissions=392257&scope=bot)
