# send data to discord

import requests
import typing
import copy

from gps_tracker.settings import Config
from gps_tracker.discord_embed import base

func_map: typing.Dict[str, typing.Callable] = {
    "_id": lambda x: x,
    "accuracy": lambda x: "{0:.2f} m".format(x),
    "activity":  lambda x: x, # idk
    "altitude": lambda x: "{0:.1f} m".format(x),
    "battery": lambda x: "{0}".format(int(x)),
    "collectedAt": lambda x: x if isinstance(x, str) else str(x),
    "device": lambda x: x,
    "latitude": lambda x: "{0:.5f} °".format(x),
    "longitude": lambda x: "{0:.5f} °".format(x),
    "provider": lambda x: x,
    "speed": lambda x: "{0:.2f} m/s".format(x),
    "direction": lambda x: "{0:.1f} °".format(x)
}


name_map: typing.Dict[str, str] = {
    "_id": "🌐 Request ID",
    "accuracy": "🔍 Accuracy",
    "activity": "Activity", # idk what this is
    "altitude": "⛰️ Altitude",
    "battery": "🔋 Battery",
    "collectedAt": "⏱️ Time",
    "device": "📱 Device",
    "latitude": "📡 Latitude",
    "longitude": "📡 Longitude",
    "direction": "🧭 Direction", # might be bearing
    "provider": "🛰️ GPS source",
    "speed": "🏃 Speed"
}


def generate_content(data: typing.Dict) -> typing.List[typing.Dict[str, str]]:
    fields: typing.List[typing.Dict[str, str]] = []
    for field_name, field_value in data.items():
        if field_name not in name_map:
            continue
        if field_value:
            fields.append(
                {
                    "name": name_map[field_name],
                    "value": func_map[field_name](field_value)
                }
            )
    return fields


def format_url(latitude: float, longitude: float) -> str:
    return f"https://maps.google.com/?q={latitude},{longitude}"


def post_to_discord(location_data: typing.Dict) -> bool:
    url: str = format_url(latitude=location_data.get("latitude", ""), longitude=location_data.get("longitude", ""))
    data: typing.Dict = copy.deepcopy(base(url=url))
    data["embeds"].append({
        "title": "Location Info",
        "color": 15172872,
        "fields": generate_content(data=location_data)
    })
    r: requests.models.Response = requests.request(
        method="POST", url=Config.discord_webhook, json=data, headers={"Content-Type": "application/json"}
    )
    print(data)
    return r.ok


{'content': None, 'embeds': [{'title': 'Location', 'description': 'Click here', 'url': 'https://maps.google.com/?q=51.5885015,-0.3390988', 'color': 5814783, 'image': {'url': 'https://images.app.goo.gl/w2giEUuRNdHahSvb6'}, 'thumbnail': {'url': 'https://images.app.goo.gl/w2giEUuRNdHahSvb6'}}, {'title': 'Location Info', 'color': 15172872, 'fields': [{'name': '📡 Latitude', 'value': '51.58850 °'}, {'name': '📡 Longitude', 'value': '-0.33910 °'}, {'name': '📱 Device', 'value': 'a355b5cfccdabe30'}, {'name': '🔍 Accuracy', 'value': '13.61 m'}, {'name': '🔋 Battery', 'value': '18'}, {'name': '🏃 Speed', 'value': '0.00 m/s'}, {'name': '🧭 Direction', 'value': '0.0 °'}, {'name': '⛰️ Altitude', 'value': '108.7 m'}, {'name': '🛰️ GPS source', 'value': 'network'}, {'name': 'Activity', 'value': ''}, {'name': '🌐 Request ID', 'value': '619e8fe473f559755c61e87c'}]}], 'username': 'GPS Tracking Service', 'avatar_url': 'https://media.istockphoto.com/vectors/satellite-icon-black-minimalist-icon-isolated-on-white-background-vector-id867290448'}

