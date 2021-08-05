import os
import pymongo
import requests
import time
from dotenv import load_dotenv
from pymongo.cursor import Cursor
from pymongo.results import UpdateResult
from typing import Dict

load_dotenv()
API_KEY = os.getenv('LIVESCORE_API_KEY')
API_SECRET = os.getenv('LIVESCORE_API_SECRET')
BASE_API_URL = 'https://livescore-api.com/api-client'
client = pymongo.MongoClient('localhost')
db = client["mikbot"]
teams = db['teams']
users = db['users']


def get_superliga_results() -> Dict:
    return requests.get(f'{BASE_API_URL}/scores/live.json?key={API_KEY}&secret={API_SECRET}&competition_id=40').json()


def get_events(fixture_id: int) -> Dict:
    return requests.get(f'{BASE_API_URL}/scores/events.json?key={API_KEY}&secret={API_SECRET}&id={fixture_id}').json()


def search_for_team(team_name: str) -> Cursor:
    return teams.find({'$text': {'$search': team_name, '$caseSensitive': False}}) # TODO: this sucks


def subscribe(user_id: str, team: Dict) -> UpdateResult:
    return users.update_one(
        {'_id': user_id},
        {'$addToSet': {'subscriptions': {'team_id': team['_id'], 'team_name': team['name']}}},
        upsert=True
    )


def unsubscribe(user_id: str, team: Dict) -> UpdateResult:
    return users.update_one(
        {'_id': user_id},
        {'$pull': {'subscriptions': {'team_id': team['_id'], 'team_name': team['name']}}},
        upsert=True
    )


def get_updates(fixture_id: int) -> None:
    previous_events = get_events(fixture_id)
    while True:
        events = get_events(fixture_id)
        number_of_new_events = int(events['data']['event'][-1]['sort']) - int(previous_events['data']['event'][-1]['sort'])
        if number_of_new_events != 0:
            for event in events['data']['event'][-number_of_new_events:]:
                yield event
        previous_events = events
        time.sleep(30)

        # TODO: check if game is done


if __name__ == '__main__':
    pass
