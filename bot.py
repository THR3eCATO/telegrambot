import os
import time
import threading
import requests
from bs4 import BeautifulSoup
import telegram
from flask import Flask

app = Flask(__name__)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID   = os.environ.get("TELEGRAM_CHAT_ID")

checked_titles = set()
bot = telegram.Bot(token=BOT_TOKEN)

def send_message(text: str):
    bot.send_message(chat_id=CHAT_ID, text=text)

def check_site():
    while True:
        try:
            url = "https://personeltemin.msb.gov.tr/Anasayfa/Duyurular"
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, "html.parser")
            items = soup.select("ul.duyuru-listesi li a")

            for item in items:
                title = item.get_text(strip=True)
                link  = "https://personeltemin.msb.gov.tr" + item["href"]
                if title not in checked_titles:
                    checked_titles.add(title)
                    send_message(f"📢 Yeni Duyuru:\n\n{title}\n🔗 {link}")
        except Exception as e:
            send_message(f"⚠️ Hata: {e}")
        time.sleep(600)

@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    # Botu ayrı bir thread'de çalıştırıyoruz
    thread = threading.Thread(target=check_site)
    thread.daemon = True
    thread.start()

    # Flask uygulamasını çalıştır (portu Render'ın istediği gibi ayarla)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
