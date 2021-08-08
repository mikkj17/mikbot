import pymongo
import requests
from typing import Dict
from typing import List

from . import API_KEY, API_SECRET, BASE_API_URL
from .mongo import teams


def get_teams_of_country(country_id: int) -> List[Dict]:
    response = requests.get(
        f'{BASE_API_URL}/teams/list.json?key={API_KEY}&secret={API_SECRET}&country_id={country_id}&size=100'
    )
    if not response.ok:
        return []
    ret = []
    data = response.json()
    ret.extend(data['data']['teams'])
    for _ in range(data['data']['pages'] - 1):
        response = requests.get(data['data']['next_page'])
        if not response.ok:
            return []
        data = response.json()
        ret.extend(data['data']['teams'])

    return ret


def rename_id(team: Dict):
    team['_id'] = team.pop('id')
    return team


def fill_database():
    countries = requests.get(f'{BASE_API_URL}/countries/list.json?&key={API_KEY}&secret={API_SECRET}').json()
    for country in countries['data']['country']:
        country_teams = get_teams_of_country(country['id'])
        if len(country_teams) > 1:
            teams.insert_many([rename_id(team) for team in country_teams])
        else:
            print(country)


def create_index() -> None:
    teams.create_index([('name', pymongo.TEXT)])
