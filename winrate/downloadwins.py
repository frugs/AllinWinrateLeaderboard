from bs4 import BeautifulSoup
import urllib.request


def download_current_player_wins():
    webpage = urllib.request.urlopen('http://www.rankedftw.com/clan/AIlin/ladder-rank/')
    soup = BeautifulSoup(webpage,'html.parser')

    table = soup.select(".team-size-1")[0]
    rows = table.find_all("tr")[1:]

    player_wins = []

    for row in rows:
        cells = row.find_all("td")
        name = cells[3].select(".name")[0].getText()
        wins = cells[5].getText()
        played = cells[7].getText()

        player_wins.append((name, int(wins), int(played)))

    return player_wins