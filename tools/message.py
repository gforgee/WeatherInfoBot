import time

import pywhatkit
import schedule
import time
from datetime import datetime

DEFAULT_MESSAGE = 'Test123ąęłżćś🌡️'


def send_weather_message(msg: str = DEFAULT_MESSAGE, phone_number: str = '', hour: int = 12, minute: int = 0):
    '''
    Sending weather message at specified time
    '''
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Sending message on WhatApp...")
    try:
        pywhatkit.sendwhatmsg(phone_number, msg, hour, minute, wait_time=20, tab_close=True)
        print("✅ Message Sent!")
    except Exception as e:
        print(f"❌ Error occured while sending message: {e}")


def schedule_daily_weather_message(fetch_func, parse_func, phone_number: str):
    """
    Sets daily job for sending message on WhatsApp at specified time
    """

    def job():
        data = fetch_func()
        msg = parse_func(data)
        send_weather_message(msg, phone_number)

    schedule.every().day.at("12:00").do(job)
    print('🕛 Current message send time is set to 12:00.')
    while True:
        schedule.run_pending()
        time.sleep(1)
