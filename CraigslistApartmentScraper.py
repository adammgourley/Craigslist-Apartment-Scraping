from bs4 import BeautifulSoup
import requests
import time, csv, random


def getPrice(listing_num):
    try:
        price = all_listings[listing_num].select("span.result-price")[0].text
        return price
    except:
        return "N/A"


def getLink(listing_num):
    try:
        link = all_listings[listing_num].select("a")[0]["href"]
        return link
    except:
        return "N/A"


def getBeds(listing_num):
    try:
        beds = all_listings[listing_num].select(".housing")[0].text.strip()
        try:
            if beds.split()[0][-1] != "2":
                return beds.split()[0]
            else:
                return "N/A"
        except:
            return "N/A"
    except:
        return "N/A"


def getSQFT(listing_num):
    try:
        sqft = all_listings[listing_num].select(".housing")[0].text.strip()
        try:
            return sqft.split()[2]
        except:
            if sqft.split()[0][-3] == "ft2":
                return sqft.split()
            else:
                return "Not Available"
    except:
        return "N/A"


def getDatePosted(listing_num):
    try:
        date = all_listings[listing_num].select(".result-date")[0].text
        return date
    except:
        return "N/A"


def getTitle(listing_num):
    try:
        title = all_listings[listing_num].select("a.result-title")[0].text
        return title
    except:
        return "N/A"


def getAllData(listing_num):
    title = getTitle(listing_num)
    price = getPrice(listing_num)
    link = getLink(listing_num)
    beds = getBeds(listing_num)
    sqft = getSQFT(listing_num)
    date = getDatePosted(listing_num)

    lst = [title, price, beds, sqft, date, link]
    return lst


with open("ATL_Apartments.csv", "a", newline="") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerow(["Title", "Price", "Beds", "SQFT", "Date Listed", "Link"])

page_intervals = 0
while page_intervals < 2880:
    url = f"https://atlanta.craigslist.org/search/atl/apa?s={page_intervals}"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    all_listings = soup.select("li.result-row")

    for i in range(len(all_listings)):
        data = getAllData(i)
        with open("ATL_Apartments.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow(data)

    user_faking = random.randint(3, 6)
    time.sleep(user_faking)

    page_intervals += 120
    print(f"{str(page_intervals)} listings scraped...")

print("Done.")

