from bs4 import BeautifulSoup
import requests
import pandas as pd

url="https://www.worldometers.info/coronavirus/"
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, "lxml")
covid_table = soup.find("table", attrs={"id": "main_table_countries_today"})
head = covid_table.thead.find_all("tr")

headings = []
for th in head[0].find_all("th"):
    headings.append(th.text.replace("\n","").strip())

body = covid_table.tbody.find_all("tr") 
# print(body[0])
data = []
for r in range(1,len(body)):
    row = []
    for tr in body[r].find_all("td"):
        row.append(tr.text.replace("\n","").strip())
    data.append(row)
df = pd.DataFrame(data,columns=headings)
df = df.iloc[7:]
df = df.reset_index(drop=True)
print(df.head(5))
df.to_csv("covid-19.csv")
