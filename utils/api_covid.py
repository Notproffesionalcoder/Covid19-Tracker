import aiohttp
import base64
import json


class CovidAPI:
    def __init__(self):
        self.url = ""

    async def api_response(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as resp:
                    response = await resp.json()
                    return response
        except Exception:
            return None

    async def get_all_data(self):
        self.url = "https://api.covid19india.org/data.json"
        response = await self.api_response()
        return response

    async def get_district_data(self):
        self.url = "https://api.covid19india.org/state_district_wise.json"
        response = await self.api_response()
        return response

    async def get_daily_data(self):
        self.url = "https://api.covid19india.org/states_daily.json"
        response = await self.api_response()
        return response

    async def get_all_countries_data(self):
        self.url="https://corona.lmao.ninja/countries?sort=country"
        response = await self.api_response()
        return response

    async def get_overall_data(self):
        self.url = "https://corona.lmao.ninja/all"
        response = await self.api_response()
        return response

    async def iso3_to_iso2(self, code:str):
        self.url = f"https://restcountries.eu/rest/v2/alpha?codes={code}"
        response = await self.api_response()
        return response[0]['alpha2Code']

    async def get_countries_list(self):
        self.url = "https://api.covid19api.com/countries"
        response = await self.api_response()
        return response

    async def get_country_data(self, country):
        self.url = f"https://corona.lmao.ninja/countries/{country}"
        response = await self.api_response()
        return response

    async def get_country_timeline(self,country):
        self.url = f"https://api.thevirustracker.com/free-api?countryTimeline={country}"
        response = await self.api_response()
        return response

