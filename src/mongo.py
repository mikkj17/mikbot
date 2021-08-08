import pymongo
from pymongo.cursor import Cursor
from pymongo.results import UpdateResult
from typing import Dict

from . import MONGO_CONNECTION_URL

client = pymongo.MongoClient(MONGO_CONNECTION_URL)
db = client["mikbot"]
teams = db['teams']
users = db['users']


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


def main() -> None:
    for team in search_for_team('OB'):
        print(team)