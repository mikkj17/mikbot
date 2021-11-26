import requests
import time
from typing import Dict

from constants import API_KEY, API_SECRET, BASE_API_URL
from constants import mongo


def get_superliga_results() -> Dict:
    return requests.get(f'{BASE_API_URL}/scores/live.json?key={API_KEY}&secret={API_SECRET}&competition_id=40').json()


def get_events(fixture_id: int) -> Dict:
    return requests.get(f'{BASE_API_URL}/scores/events.json?key={API_KEY}&secret={API_SECRET}&id={fixture_id}').json()


def sub_unsub(user_id: int, team_name: str, sub: bool) -> str:
    possible_teams = mongo.search_for_team(team_name)

    if possible_teams.count() == 0:
        message = 'Team not found!'

    elif possible_teams.count() > 1:
        formatted_teams = '\n'.join(f"{team['name']} - {team['_id']}" for team in possible_teams)
        message = f'Multiple teams found. Please specify one of the following using their ID:\n{formatted_teams}'

    else:
        team = possible_teams[0]

        if sub:
            update = mongo.subscribe(user_id, team)
        else:
            update = mongo.unsubscribe(user_id, team)
        
        if update.upserted_id is None and update.modified_count == 0:
            message = f"You're already subscribed to {team['name']} :soccer:"
        else:
            message = f"You're now subscribed to {team['name']} :soccer:"
    
    return message


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

        # TODO: check if game is finished

