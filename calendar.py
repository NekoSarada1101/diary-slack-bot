import json

import googleapiclient.discovery
import requests
from datetime import datetime, timedelta, timezone
from typing import List

from settings import *

service = googleapiclient.discovery.build('calendar', 'v3', credentials=CREDENTIALS)
today = datetime.now(timezone(timedelta(hours=+9), 'JST'))


def post_calendar():
    calendar_event = []  # type: List[str]
    for calendar_id in CALENDAR_ID_LIST:
        calendar_event.append(fetch_events(calendar_id))
    data = calendar_json(calendar_event)  # type: dict
    print(data)
    json_data = json.dumps(data).encode("utf-8")  # type: json
    response = requests.post(SLACK_WEBHOOK_URL, json_data)  # type: response
    print(response)


def fetch_events(calendar_id: str) -> str:
    time_min = today.replace(hour=0, minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%S%z")  # type: str
    time_max = today.replace(hour=23, minute=59, second=59).strftime("%Y-%m-%dT%H:%M:%S%z")  # type: str

    page_token = None
    while True:
        events = service.events().list(calendarId=calendar_id, pageToken=page_token, timeMin=time_min, timeMax=time_max,
                                       singleEvents=True, orderBy="startTime").execute()  # type: dict
        list_text = ""  # type: str
        for event in events['items']:
            start = event['start'].get('dateTime', event['start'].get('date'))  # type: str

            word_count = 10  # type: int
            if len(start) == word_count:
                start = datetime.strptime(start, "%Y-%m-%d").strftime("%m/%d ")
                list_text += start
            else:
                start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z").strftime("%m/%d  %H:%M-")
                end = event['end'].get('dateTime', event['end'].get('date'))  # type: str
                end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S%z").strftime("%H:%M ")
                list_text += start + end

            list_text += "`" + event['summary'] + "`" + "\n"

        page_token = events.get('nextPageToken')
        if page_token is None:
            break

    return list_text


def calendar_json(calendar_data: List[str]) -> dict:
    summary_list = []  # type: List[str]
    for calendar_id in CALENDAR_ID_LIST:
        calendar = service.calendars().get(calendarId=calendar_id).execute()  # type: dict
        summary_list.append(calendar["summary"])

    attachments = []  # type: List[dict]
    color_list = ["FF0000", "00BFFF", "FFFF00", "FFFFFF"]
    for i in range(len(calendar_data)):
        attachments.append(
            {
                "color": color_list[i],
                "title": summary_list[i],
                "text": calendar_data[i]
            }
        )

    data = {  # type: dict
        "response_type": "ephemeral",
        "text": today.strftime("%m月%d日") + "の予定をお知らせします。",
        "attachments":
            attachments
    }

    return data
