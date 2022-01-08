from threading import Thread

import requests


BOT_TOKEN = ''
GRP_CHAT_ID = ''

SEND_MSG_URL = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text='.format(BOT_TOKEN, GRP_CHAT_ID)
DEL_MSG_URL = 'https://api.telegram.org/bot{}/deleteMessage?chat_id={}&message_id='.format(BOT_TOKEN, GRP_CHAT_ID)
SEND_PHOTO_URL = 'https://api.telegram.org/bot{}/sendPhoto?chat_id={}&caption='.format(BOT_TOKEN, GRP_CHAT_ID)


def initialize(bot_token: str, group_chat_id: str):
    global BOT_TOKEN
    global GRP_CHAT_ID
    global SEND_MSG_URL
    global DEL_MSG_URL
    global SEND_PHOTO_URL

    BOT_TOKEN = bot_token
    GRP_CHAT_ID = group_chat_id

    SEND_MSG_URL = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text='.format(BOT_TOKEN, GRP_CHAT_ID)
    DEL_MSG_URL = 'https://api.telegram.org/bot{}/deleteMessage?chat_id={}&message_id='.format(BOT_TOKEN, GRP_CHAT_ID)
    SEND_PHOTO_URL = 'https://api.telegram.org/bot{}/sendPhoto?chat_id={}&caption='.format(BOT_TOKEN, GRP_CHAT_ID)


def async_handler(func, *args):
    t = Thread(target=func, args=args)
    t.start()


def send_msg(text: str):
    url = SEND_MSG_URL + text.replace(" ", "%20")
    try:
        res = requests.post(url)
        if res.ok:
            return res.json()['result']['message_id']
    except Exception as e:
        print("Telegram Exception: ", e)
        return None


def send_msg_async(text: str):
    async_handler(send_msg, text)


def del_msg(msg_id: str):
    url = DEL_MSG_URL + str(msg_id).replace(" ", "%20")
    try:
        res = requests.post(url)
        if res.ok:
            return res.json()
    except Exception as e:
        print("Telegram Exception: ", e)
        return None


def del_msg_async(msg_id: str):
    async_handler(del_msg, msg_id)


def send_photo(caption: str, photo):
    mime = "image/jpeg"

    if isinstance(photo, str):
        if photo.endswith("png"):
            mime = "image/png"
        photo = open(photo, 'rb')

    url = SEND_PHOTO_URL + f"&caption={caption}"
    try:
        res = requests.post(url, files={"photo": (caption, photo, mime)})
        if res.ok:
            return res.json()
    except Exception as e:
        print("Telegram Exception: ", e)
        return None


def send_photo_async(caption: str, photo):
    async_handler(send_photo, caption, photo)


if __name__ == "__main__":
    result = send_photo_async("maggie", "/Users/vikash/Downloads/maggie.jpeg")

    send_msg_async("wubba lubba dub dub")
    message_id = send_msg("wubba lubba dub dub")
    #
    import time
    time.sleep(5)
    print(f"Deleting message {message_id}")
    del_msg_async(message_id)
