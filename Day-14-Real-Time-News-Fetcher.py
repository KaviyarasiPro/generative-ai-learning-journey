import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote

print("\n╔════════════════════════════════════╗")
print("║       📰 REAL-TIME NEWS FETCHER    ║")
print("╚════════════════════════════════════╝")
print("\nChoose a news category:")
print("1. Technology")
print("2. Business")
print("3. Artificial Intelligence")
print("4. Sports")

choice = input("\n Enter your choice :")

categories = {
    "1" : "Technology",
    "2" : "Bussiness",
    "3" : "Artificial Intelligence",
    "4" : "Sports"
    }

if choice in categories :
    category = categories[choice]
else:
    print("invalid choice")
    exit()

query = quote(category)
url = (
    f"https://news.google.com/rss/search?"
    f"q={query}&hl=en-US&gl=US&ceid=US:en"
)
response = requests.get(url,timeout=10)

if response.status_code ==200 :
    root = ET.fromstring(response.content)
    articles = root.findall(".//item")
    print("\n╔════════════════════════════════════╗")
    print("║          📰 LATEST NEWS            ║")
    print("╚════════════════════════════════════╝")

    print("\nCategory:", category)

    for number , article in enumerate(articles[:5],start=1):
       title = article.find("title").text
       print("\n",number,".",title)
      
    print("\n──────────────────────────────────────")
    print("        News fetched successfully! ✅")
    print("──────────────────────────────────────")

else :
    print("\n Unable to fetch news.please try again.")
