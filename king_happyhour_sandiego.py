# The data belongs to https://kingofhappyhour.com/sandiego/
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Lists with the saved data
places = []
ref = []
# All the features coming from the king of happy hour San Diego
url = ["https://kingofhappyhour.com/sandiego/features/kings_picks", "https://kingofhappyhour.com/sandiego/features/just_added", "https://kingofhappyhour.com/sandiego/features/most_viewed", "https://kingofhappyhour.com/sandiego/features/late_night", "https://kingofhappyhour.com/sandiego/features/taco_tuesday"]

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

    
# This function has give us the URL of every restaurant. Now we use
# The URL to scrape the bar or restaurant's information.

name = []
number = []
location = []
sunday = []
monday = []
tuesday = []
wednesday = []
thursday = []
friday = []
saturday = []


for i in range(len(ref)):
    try:
        bussiness_hour = []
        happy_hour = []
        deal_day = []
        output = []
        url = f"https://kingofhappyhour.com{ref[i]}"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        target = soup.find_all("div", class_="visible-sm-block")

        for j in target:
            # This returns the name of the restaurant/bar
            name_value = j.find('h3').text
            name.append(name_value)
        # This returns the location and the number
        loc_phone = soup.find("div", "text-center small-caps")
        c = loc_phone.text
        c = c.replace("            ", "")
        data_list = c.split("\n")
        location_data = data_list[1] + " " + data_list[2]
        cell = data_list[3]
        location.append(location_data)
        number.append(cell)

        daily_specials = soup.find_all('div', {'class': 'daily_special'})
        for daily_special in daily_specials:
            business_hours = daily_special.find('strong')
            if business_hours:
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
                    else:
                        happy_hour.append("Not Happy Hour")

                    p = daily_special.find_all("p")
                    if len(p) >= 2:
                        for i in p:
                            if len(happy_hour) != 7 and p[1] != "\n":
                                if len(p) >= 3:
                                    c = p[1].text + " " + p[2].text
                                    deal_day.append(c)
                                else:
                                    c = p[1].text
                                    deal_day.append(c)
                    else:
                        deal_day.append("Not deal today")
                      
        weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

        for i in range(len(weekdays)):
            if bussiness_hour[i] == "Closed":
                output.append("Closed")
            else:
                y = "Bussines hour: " + bussiness_hour[i] + " Happy hour: " + happy_hour[i] + " Today deal: " + deal_day[i]
                output.append(y)
        
        sunday.append(output[0])
        monday.append(output[1])
        tuesday.append(output[2])
        wednesday.append(output[3])
        thursday.append(output[4])
        friday.append(output[5])
        saturday.append(output[6])

    finally:
        pass




df = pd.DataFrame({"Name":name, "Location":location, "Contact Number":number, 
                   "Sunday":sunday, "Monday":monday, "Tuesday":tuesday, "Wednesday":wednesday, "Thursday":thursday, "Friday":friday, "Saturday":saturday})
df.to_excel("King Happy Hour San Diego.xlsx")
df.to_csv("King Happy Hour San Diego.csv")