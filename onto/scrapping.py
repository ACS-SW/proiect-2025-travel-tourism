import requests
from bs4 import BeautifulSoup
import csv

def get_attractions(city):
    city_url = city.lower().replace(" ", "-")
    url = f"https://www.atlasobscura.com/things-to-do/{city_url}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Eroare la {city}: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 🔍 Selector actualizat
    attraction_tags = soup.select("a div.CardTitle__Text-sc-1gyrgim-0")
    
    attractions = []
    for tag in attraction_tags:
        text = tag.get_text(strip=True)
        if text and text not in attractions:
            attractions.append(text)

    return attractions


cities = ["Dublin", "Taipei", "Kathmandu", "Baku", "Amman"]


with open("attractions_atlas.csv", "w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["City", "Attraction"])

    for city in cities:
        results = get_attractions(city)
        print(f"{city}: {len(results)} atractions found.")
        for name in results:
            writer.writerow([city, name])
