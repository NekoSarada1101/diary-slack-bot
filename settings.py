from google.oauth2 import service_account

SLACK_WEBHOOK_URL = "SLACK_WEBHOOK_URL"
GMAIL_LIST = [
    "GMAIL_LIST_1",
    "GMAIL_LIST_2",
    "GMAIL_LIST_3",
    ...
]
OPEN_WEATHER_API_KEY = "OPEN_WEATHER_API_KEY"
LAT_LNG = ["LAT", "LNG"]

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/drive'
]
SERVICE_ACCOUNT_FILE = 'credentials.json'

CREDENTIALS = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
