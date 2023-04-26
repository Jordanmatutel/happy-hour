# https://kingofhappyhour.com/sandiego/bars/garage_kitchen_bar
from bs4 import BeautifulSoup
import pandas as pd
import requests
from lxml import html


name = []
bussiness_hour = []
output = []
happy_hour = []
deal_day = []

url = "https://kingofhappyhour.com/sandiego/bars/garage_kitchen_bar"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
daily_specials = soup.find_all('div', {'class': 'daily_special'})

# Itera sobre cada div con clase "daily_special" y extrae el horario de negocios
for daily_special in daily_specials:
    business_hours = daily_special.find('strong').next_sibling.strip()
    bussiness_hour.append(business_hours)
    if business_hours == "Closed":
        happy_hour.append("Closed")
        deal_day.append("Closed")
    else:
        hh = daily_special.find('strong', class_="heading")
        if hh:
            hhr = hh.next_sibling.strip()
            happy_hour.append(hhr)

        p = daily_special.find_all("p")
        for i in p:
            if len(happy_hour) != 7:
                c = p[1].text + " " + p[2].text
                deal_day.append(c)

target = soup.find_all("div", class_="visible-sm-block")

for j in target:
    # This returns the name of the restaurant/bar
    name_value = j.find('h3').text
    name.append(name_value)

loc_phone = soup.find("div", "text-center small-caps")
c = loc_phone.text
c = c.replace("            ", "")
data_list = c.split("\n")
location_data = data_list[1] + " " + data_list[2]
cell = data_list[3]

weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

for i in range(len(weekdays)):
    if bussiness_hour[i] == "Closed":
        output.append("Closed")
    else:
        y = "Bussines hour: " + bussiness_hour[i] + " Happy hour: " + happy_hour[i] + " Today deal: " + deal_day[i]
        output.append(y)

data = pd.DataFrame({"Name":name, "Location":location_data, "Contact Number":cell, 'Sunday':output[0], 'Monday':output[1], 'Tuesday':output[2], 'Wednesday':output[3], 'Thursday':output[4], 'Friday':output[5], 'Saturday':output[6]})
data.to_csv("Example.csv")