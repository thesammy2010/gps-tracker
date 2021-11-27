import copy
import typing

import requests

from gps_tracker.discord_embed import base
from gps_tracker.settings import CONFIG

func_map: typing.Dict[str, typing.Callable] = {
    "_id": lambda x: x,
    "accuracy": lambda x: "{0:.2f} m".format(x),
    "activity": lambda x: x,  # idk
    "altitude": lambda x: "{0:.1f} m".format(x),
    "battery": lambda x: "{0}".format(int(x)),
    "collectedAt": lambda x: x if isinstance(x, str) else str(x),
    "device": lambda x: x,
    "latitude": lambda x: "{0:.5f} °".format(x),
    "longitude": lambda x: "{0:.5f} °".format(x),
    "provider": lambda x: x,
    "speed": lambda x: "{0:.2f} m/s".format(x),
    "direction": lambda x: "{0:.1f} °".format(x),
}


name_map: typing.Dict[str, str] = {
    "_id": "🌐 Request ID",
    "accuracy": "🔍 Accuracy",
    "activity": "Activity",  # idk what this is
    "altitude": "⛰️ Altitude",
    "battery": "🔋 Battery",
    "collectedAt": "⏱️ Time",
    "device": "📱 Device",
    "latitude": "📡 Latitude",
    "longitude": "📡 Longitude",
    "direction": "🧭 Direction",  # might be bearing
    "provider": "🛰️ GPS source",
    "speed": "🏃 Speed",
}


def generate_content(data: typing.Dict) -> typing.List[typing.Dict[str, str]]:
    fields: typing.List[typing.Dict[str, str]] = []
    for field_name, field_value in data.items():
        if field_name not in name_map:
            continue
        if field_value:
            fields.append({"name": name_map[field_name], "value": func_map[field_name](field_value)})
    return fields


def format_url(latitude: float, longitude: float) -> str:
    return f"https://google.com/maps?q={latitude},{longitude}"


def post_to_discord(location_data: typing.Dict) -> bool:
    url: str = format_url(latitude=location_data.get("latitude", ""), longitude=location_data.get("longitude", ""))
    data: typing.Dict = copy.deepcopy(base(url=url))
    data["embeds"].append({"title": "Location Info", "color": 15172872, "fields": generate_content(data=location_data)})
    r: requests.models.Response = requests.request(
        method="POST", url=CONFIG.discord_webhook, json=data, headers={"Content-Type": "application/json"}
    )
    return r.ok
