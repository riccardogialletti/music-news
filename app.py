# app.py
import requests
from bs4 import BeautifulSoup

def fetch_news():
    url = "https://www.rockit.it/news"  # Esempio
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    news = soup.find_all("h2")
    for n in news[:5]:
        print(n.text.strip())

if __name__ == "__main__":
    fetch_news()
