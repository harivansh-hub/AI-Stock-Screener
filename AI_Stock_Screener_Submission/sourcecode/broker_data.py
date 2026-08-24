import os
import pyotp

from dotenv import load_dotenv
from SmartApi import SmartConnect
from SmartApi.smartWebSocketV2 import SmartWebSocketV2


load_dotenv("credentials.env")


API_KEY = os.getenv("ANGEL_API_KEY")
CLIENT_CODE = os.getenv("ANGEL_CLIENT_CODE")
PASSWORD = os.getenv("ANGEL_PASSWORD")
TOTP_SECRET = os.getenv("ANGEL_TOTP_SECRET")


if not all([
    API_KEY,
    CLIENT_CODE,
    PASSWORD,
    TOTP_SECRET
]):
    raise ValueError(
        "Missing Angel One credentials in .env"
    )


# -------------------------
# LOGIN
# -------------------------

smart_api = SmartConnect(
    api_key=API_KEY
)


totp = pyotp.TOTP(
    TOTP_SECRET
).now()


session = smart_api.generateSession(
    CLIENT_CODE,
    PASSWORD,
    totp
)


if not session.get("status"):

    print("LOGIN FAILED")
    print(session)

    raise SystemExit


auth_token = session["data"]["jwtToken"]

feed_token = smart_api.getfeedToken()


print("LOGIN SUCCESSFUL")
print("Feed token received")


# -------------------------
# WEBSOCKET
# -------------------------

sws = SmartWebSocketV2(
    auth_token,
    API_KEY,
    CLIENT_CODE,
    feed_token
)


def on_data(wsapp, message):

    print("\nLIVE TICK:")
    print(message)


def on_open(wsapp):

    print("\nWEBSOCKET CONNECTED")

    token_list = [

        {
            "exchangeType": 1,
            "tokens": [
                "2885"
            ]
        }

    ]

    sws.subscribe(
        "stock_screener",
        1,
        token_list
    )


def on_error(wsapp, error):

    print("WEBSOCKET ERROR:")
    print(error)


def on_close(wsapp):

    print("WEBSOCKET CLOSED")


sws.on_data = on_data
sws.on_open = on_open
sws.on_error = on_error
sws.on_close = on_close


print("\nConnecting to Angel One...")

sws.connect()