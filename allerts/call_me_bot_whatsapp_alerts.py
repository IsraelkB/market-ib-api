import requests
from config import whatsapp_settings, WhatsappSettings

settings = WhatsappSettings()

def send_whatsapp_alert(message):
    url = f"{settings.bot_url}{message}"
    requests.get(url)

if __name__ == "__main__":
    send_whatsapp_alert("זוהי הודעת בוט שנשלחה אלייך על ידי בעלך שאוהב רק אותך שתדעי שאת כל חייו אסתר המלכה")