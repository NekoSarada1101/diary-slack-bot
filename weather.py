import json
import requests
from datetime import datetime
from settings import *


def post_weather():
    url = ("https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&exclude=current,minutely,hourly,"
           "alerts&units=metric&lang=ja" % (LAT_LNG[0], LAT_LNG[1], OPEN_WEATHER_API_KEY))  # type: str
    weather_response = json.loads(requests.get(url).text)  # type: dict

    date = datetime.fromtimestamp(weather_response["daily"][0]["dt"]).strftime("%m/%d")  # type: str
    weather = weather_response["daily"][0]["weather"][0]["description"]  # type: str
    image = weather_response["daily"][0]["weather"][0]["icon"]  # type: str
    max_temp = str(round(weather_response["daily"][0]["temp"]["max"], 1)) + "°C"  # type: str
    min_temp = str(round(weather_response["daily"][0]["temp"]["min"], 1)) + "°C"  # type: str
    wind_speed = str(weather_response["daily"][0]["wind_speed"]) + "m/h"  # type: str
    pop = str(weather_response["daily"][0]["pop"] * 100) + "m/h"  # type: str

    data = {  # type: dict
        "response_type": "ephemeral",
        "text": date + "の天気をお知らせします。",
        "attachments": [
            {
                "text": "*" + date + "の天気* ： `" + weather + "`",
                "color": "33ff66",
                "image_url": "http://openweathermap.org/img/wn/" + image + "@2x.png"
            },
            {
                "color": "FF0000",
                "text": " *最高気温* ： `" + max_temp + "`"
            },
            {
                "color": "00BFFF",
                "text": " *最低気温* ： `" + min_temp + "`"
            },
            {
                "color": "FFFFFF",
                "text": " *風速* 　　： `" + wind_speed + "`"
            },
            {
                "color": "5579EC",
                "text": " *降水確率* ： `" + pop + "`"
            }
        ]
    }

    print(data)
    json_data = json.dumps(data).encode("utf-8")  # type: json
    response = requests.post(SLACK_WEBHOOK_URL, json_data)
    print(response)
