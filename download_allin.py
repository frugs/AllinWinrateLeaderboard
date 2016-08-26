from bs4 import BeautifulSoup
import urllib.request

webpage = urllib.request.urlopen('http://www.rankedftw.com/clan/AIlin/ladder-rank/')
soup = BeautifulSoup(webpage,'html.parser')

table = soup.select(".team-size-1")[0]
rows = table.find_all("tr")[1:]

file = open("wins.txt", mode="w")

for row in rows:
    cells = row.find_all("td")
    name = cells[3].select(".name")[0].getText()
    wins = cells[5].getText()
    played = cells[7].getText()

    print(name, wins, played, file=file)