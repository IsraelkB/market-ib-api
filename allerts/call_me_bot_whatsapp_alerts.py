import requests
from config import israel_whatsapp_settings, jac_whatsapp_settings

israel_detail = {"phone_number": israel_whatsapp_settings.phone_number_israel,
                 "bot_key": israel_whatsapp_settings.bot_key_israel,
                 "base_url_bot": israel_whatsapp_settings.base_url_bot}
jac_detail = {"phone_number": jac_whatsapp_settings.phone_number_jac,
              "bot_key": jac_whatsapp_settings.bot_key_jac,
              "base_url_bot": jac_whatsapp_settings.base_url_bot}


def send_whatsapp_alert_israel(message):
    url = f"{israel_detail["base_url_bot"]}{israel_detail["phone_number"]}&text={message}&apikey={israel_detail["bot_key"]}"
    requests.get(url)

def send_whatsapp_alert_jac(message):
    url = f"{jac_detail["base_url_bot"]}{jac_detail["phone_number"]}&text={message}&apikey={jac_detail["bot_key"]}"
    requests.get(url)

