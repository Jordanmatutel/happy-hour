# The data belongs to https://kingofhappyhour.com/sandiego/
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime


# Obtains the weekday
date = datetime.datetime.now()
today_weekday = date.strftime("%A")

# Lists with the saved data
today_bussiness_hour = []
today_happy_hour = []
places = []
ref = []
deals = []
# All the features coming from the king of happy hour San Diego
url = ["https://kingofhappyhour.com/sandiego/features/kings_picks", "https://kingofhappyhour.com/sandiego/features/just_added", "https://kingofhappyhour.com/sandiego/features/most_viewed", "https://kingofhappyhour.com/sandiego/features/late_night"]

# Use the url and extract every restaurant's URL on the feature.
for i in range(len(url)):
    page = requests.get(url[i])
    soup = BeautifulSoup(page.content, "html.parser")
    target = soup.find_all("a", class_="bar_name")
    # Takes the URL of every bar/restaurant
    for j in target:
        href_value = j['href']
        ref.append(href_value)
    target = soup.find_all("div",class_="happy_hour_info")    
    # Deals and happy hour info
    for j in target:
        c = j.find("p")
        if c != None:
            deals.append(c.text)
        else:
            deals.append("Closed")

    # Happy Hours
    happy_hour_info = soup.find_all('div', {'class': 'happy_hour_info'})
    for i in happy_hour_info:
        strong_element = i.find('strong')
        if strong_element is not None:
            happy_hour_time = strong_element.next_sibling.strip()
            today_happy_hour.append(happy_hour_time)
        else:
            today_happy_hour.append("Close")

    
# This function has give us the URL of every restaurant. Now we use
# The URL to scrape the bar or restaurant's information.

name = []
number = []
location = []

for i in range(len(ref)):
    try:
        url = f"https://kingofhappyhour.com{ref[i]}"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        target = soup.find_all("div", class_="visible-sm-block")

        for j in target:
            # This returns the name of the restaurant/bar
            name_value = j.find('h3').text
            name.append(name_value)
        # This returns the location and the numbre
        loc_phone = soup.find("div", "text-center small-caps")
        c = loc_phone.text
        c = c.replace("            ", "")
        data_list = c.split("\n")
        location_data = data_list[1] + " " + data_list[2]
        cell = data_list[3]
        location.append(location_data)
        number.append(cell)

        target = soup.find_all("div", "daily_special")
        for element in target:
                day = element.find("p","list-head")
                if day and day.text == today_weekday:
                    bussines = element.strong.next_sibling.strip()
                    today_bussiness_hour.append(bussines)


    finally:
        pass


df = pd.DataFrame({"Name":name, "Location":location, "Contact Number":number, "Bussiness Hours":today_bussiness_hour, "Happy Hours": today_happy_hour, "Happy Hours Deals":deals})
df.to_excel("King Happy Hour San Diego.xlsx")