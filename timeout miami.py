# Data from https://www.timeout.com/miami/bars/best-happy-hour-miami

import pandas as pd
import requests
from bs4 import BeautifulSoup

href = []
names = []
hour = []
address = []
cellphone = []
opening = []

url = "https://www.timeout.com/miami/bars/best-happy-hour-miami"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
# Name
name1 = soup.find_all("h3","_h3_cuogz_1")
for i in name1:
    c = i.text
    names.append(c)

names.pop(0)
for i in range(len(names)):
    names[i] = names[i].split(".")[1]

counting = 0
# Happy hour
hours = soup.find_all("div", "_summary_kc5qn_21")
for i in hours:
    strong = i.find("strong").text
    hour.append(strong)

# Href
ref = soup.find_all("div","_title_kc5qn_9")
for i in ref:
    a = i.find('a')['href']
    href.append(a)

for i in range(len(href)):
    if href[i][0] == "h":
        href[i] = "Link"


# Link extractor
for i in range(len(href)):
    if href[i] != "Link":
        url = "https://www.timeout.com" + href[i]
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
    # Address
        n = soup.find("dl" , class_="_list_k1wdy_5")
        dd_list = n.find("dd", class_="_description_k1wdy_9")
        for dd in dd_list:
            address.append(dd.text)
    # Number
        c = soup.find_all("a", class_= "_a_k1wdy_35")
        if c:
            for s in c:
                if s.text[0] == "V":
                    pass
                else:
                    cellphone.append(s.text)
                    print(counting, s.text)
                    counting = counting + 1
        elif not c:
            cellphone.append("None") 
    # Opening Hours
        c = soup.find_all("div", {"data-section": "openinghours"})
        if not c:
            opening.append("None")
        else:
            for element in c:
                t = element.find("dd", class_="_description_k1wdy_9")
                opening.append(t.text)
        

    if href[i] == "Link":
        address.append("Link")
        cellphone.append("Link")
        opening.append("Link")

print(len(names))
print(len(hour))
print(len(address))
print(len(opening))

c = pd.DataFrame({"Name":names, "Happy Hour":hour, "Address":address, "Opening Hours":opening})
c.to_csv("Miami.csv")
