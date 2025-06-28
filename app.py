import requests
from bs4 import BeautifulSoup
from datetime import datetime

WIX_ENDPOINT = "https://tuosito.wixsite.com/_functions/news"  # <-- Cambia con il tuo URL

NEWS_SOURCES = [
    "https://www.umbriaon.it/cronaca/",
    "https://www.perugiatoday.it/cronaca/"
]

def fetch_news():
    for source in NEWS_SOURCES:
        try:
            resp = requests.get(source, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            articles = soup.select("article")[:3]  # Primi 3 articoli

            for article in articles:
                title_tag = article.select_one("h2")
                title = title_tag.get_text(strip=True) if title_tag else "Titolo non trovato"

                link_tag = article.select_one("a")
                link = link_tag["href"] if link_tag and link_tag.has_attr("href") else source

                excerpt_tag = article.select_one("p")
                excerpt = excerpt_tag.get_text(strip=True) if excerpt_tag else ""

                image_tag = article.select_one("img")
                image_url = image_tag["src"] if image_tag and image_tag.has_attr("src") else ""

                post_data = {
                    "title": title,
                    "excerpt": excerpt,
                    "url": link,
                    "image": image_url,
                    "date": datetime.utcnow().isoformat()
                }

                send_to_wix(post_data)
        except Exception as e:
            print("Errore nel parsing della sorgente", source, ":", e)

def send_to_wix(data):
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(WIX_ENDPOINT, json=data, headers=headers)
        print("Risposta Wix:", response.status_code, response.text)
    except Exception as e:
        print("Errore invio a Wix:", e)

if __name__ == "__main__":
    fetch_news()
