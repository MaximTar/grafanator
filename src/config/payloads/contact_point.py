from config import config


def build_contact_point_payload(token: str, chat_id: str) -> dict:
    return {
        "name": config.CONTACT_POINT_NAME,
        "type": "telegram",
        "settings": {
            "bottoken": token,
            "chatid": chat_id,
            "disable_notifications": False,
            "message": config.TG_MESSAGE_TEMPLATE,
        },
    }
