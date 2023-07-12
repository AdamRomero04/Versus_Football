import requests
from bs4 import BeautifulSoup
import re
import datetime
import time
import json
import myapp
from flask import Flask
from myapp import Names, db, app

class generalInfo():
    name = "None"
    position = "None"
    age = "None"
    foot = "None"
    nation = "None"
    currClub = "None"


class links():
    playerPic = "None"
    nationFlag = "None"
    clubBadge = "None"


class generalStats(object):
    goals = 0
    assists = 0
    xG = 0
    xA = 0
    g_a = 0
    goalsPer90 = 0
    assistsPer90 = 0
    matchesPlayed = 0
    minutesPlayed = 0
    yellowCards = 0
    redCards = 0
    trophiesWon = 0


class forward(generalStats):
    shotsOnTarget = 0
    penalties = 0
    takeOns = 0
    takeOnPerc = 0
    dribbles = 0  # called carries
    finalThirdTouches = 0
    keyPasses = 0
    progPasses = 0
    crosses = 0


class defender(generalStats):
    fouls = 0
    tackles = 0
    blocks = 0
    interceptions = 0
    clearances = 0
    totalPasses = 0
    passAccuracy = 0
    aerialDuelPerc = 0


class goalkeeper(generalStats):
    saves = 0
    savePerc = 0
    cleanSheets = 0
    cleanSheetPerc = 0
    goalsAgainst = 0
    xgAgainst = 0
    penFaced = 0
    penSaved = 0
    totalPasses = 0
    passAccuracy = 0


class midfielder(forward, defender):
    longBallCompPerc = 0
    recoveries = 0


def getHTMLfile(url, htmlName):
    r = requests.get(url)
    if r.status_code == 200:
        print("Request was successful.")
    else:
        print("Request failed with status code:", r.status_code)
    content = r.content
    soup = BeautifulSoup(content, 'html5lib')
    format_content = soup.prettify()
    with open(htmlName, "w", encoding="utf-8") as file:
        file.write(format_content)

    return soup


def getLink(soup, type, keyword, clas):
    target_link = "None"
    for link in soup.find_all(type):
        if keyword in link.get(clas, ''):
            target_link = link[clas]
            break
    return target_link


def getbyTypeKeyword(soup, element_type, keyword):
    target = "None"
    for line in soup.find_all(element_type):
        if keyword in line.get_text():
            target = line.get_text()
            break
    return target


def getTypeKeyword(soup, element_type, keyword):
    target = None
    elements = soup.find_all(
        element_type, text=lambda text: text and keyword in text)
    if elements:
        target = elements[0].get_text()
    return target


def createPlayer(position):
    if (position == "FW"):
        class player(generalInfo, links, forward):
            pass
        return player()

    if (position == "MF"):
        class player(generalInfo, links, midfielder):
            pass
        return player()

    if (position == "DF"):
        class player(generalInfo, links, defender):
            pass
        return player()

    if (position == "GK"):
        class player(generalInfo, links, goalkeeper):
            pass
        return player()


def ageFinder(soup):
    birthdate = soup.find('span', id="necro-birth")
    birthdate = birthdate['data-birth']

    current_date = datetime.date.today()
    birth_date_obj = datetime.datetime.strptime(birthdate, '%Y-%m-%d').date()
    age = current_date.year - birth_date_obj.year
    if (current_date.month, current_date.day) < (birth_date_obj.month, birth_date_obj.day):
        age -= 1

    return age


def generalInfoFill(player, soup, position):
    playerNameScrape = soup.find('h1').text.strip()
    player.name = playerNameScrape

    player.position = position

    player.age = ageFinder(soup)

    word = "Footed:"
    footLine = soup.find('strong', string=lambda text: text and word in text)
    footLine = footLine.next_sibling.strip()
    player.foot = footLine

    nation = soup.find(
        'strong', string=lambda text: text and "National Team:" in text)
    nation = nation.next_sibling
    nation = nation.next_sibling.text.strip()
    player.nation = nation

    club = soup.find(
        'strong', string=lambda text: text and "Club:" in text)
    club = club.next_sibling
    club = club.next_sibling.text.strip()
    player.currClub = club

    print(player.name)


def linkFill(player, soup):
    player.playerPic = getLink(soup, 'img', "headshots", 'src')

    regBadge = (player.currClub).replace(' ', '-')
    query = regBadge + 'club-icon-archive'
    clubLink = "https://www.google.com/search?q={" + query + "}&tbm=isch"
    newsoup = getHTMLfile(clubLink, "clubLink.html")
    time.sleep(1)
    with open("clubLink.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    onesoup = BeautifulSoup(html_content, 'html5lib')
    almostClubBadge = onesoup.find('img', class_='yWs4tf')
    almostClubBadge = str(almostClubBadge)
    almostClubBadge = almostClubBadge.split('"')
    player.clubBadge = almostClubBadge[5]
    print(player.clubBadge)

    regNation = (player.nation).replace(' ', '-')
    query = "nation-flag-of-" + regNation + '-wikipedia'
    flagLink = "https://www.google.com/search?q={" + query + "}&tbm=isch"
    newersoup = getHTMLfile(flagLink, "flagLink.html")
    time.sleep(1)
    with open("flagLink.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    twosoup = BeautifulSoup(html_content, 'html5lib')
    almostNationFlag = twosoup.find('img', class_='yWs4tf')
    almostNationFlag = str(almostNationFlag)
    almostNationFlag = almostNationFlag.split('"')
    player.nationFlag = almostNationFlag[5]
    print(player.nationFlag)

def genStatFill(player, soup):
    start = soup.find(id="stats_standard_dom_lg")
    target = "None"
    for line in start.find_all(attrs={'data-stat': 'year_id'}):
        if "2022-2023" in line.get_text():
            target = line  # 200 - 209 finds first term in graph
            break

    for i in range(10):
        target = target.next_sibling
    pos = target.text.strip()
    if (pos == "1st"):
        player.trophiesWon = 1

    for i in range(2):
        target = target.next_sibling
    player.matchesPlayed = target.text.strip()
    player.matchesPlayed = int(player.matchesPlayed)

    for i in range(4):
        target = target.next_sibling
    player.minutesPlayed = target.text.strip()
    player.minutesPlayed = player.minutesPlayed.replace(',', '')
    player.minutesPlayed = int(player.minutesPlayed)

    for i in range(4):
        target = target.next_sibling
    player.goals = target.text.strip()
    player.goals = int(player.goals)

    for i in range(2):
        target = target.next_sibling
    player.assists = target.text.strip()
    player.assists = int(player.assists)

    for i in range(2):
        target = target.next_sibling
    player.g_a = target.text.strip()
    player.g_a = int(player.g_a)

    for i in range(8):
        target = target.next_sibling
    player.yellowCards = target.text.strip()
    player.yellowCards = int(player.yellowCards)

    for i in range(2):
        target = target.next_sibling
    player.redCards = target.text.strip()
    player.redCards = int(player.redCards)

    for i in range(2):
        target = target.next_sibling
    player.xG = target.text.strip()
    player.xG = float(player.xG)

    for i in range(4):
        target = target.next_sibling
    player.xA = target.text.strip()
    player.xA = float(player.xA)

    for i in range(10):
        target = target.next_sibling
    player.goalsPer90 = target.text.strip()
    player.goalsPer90 = float(player.goalsPer90)

    for i in range(2):
        target = target.next_sibling
    player.assistsPer90 = target.text.strip()
    player.assistsPer90 = float(player.assistsPer90)


def gkFill(player, soup):
    start = soup.find(id="stats_keeper_dom_lg")
    target = "None"
    for line in start.find_all(attrs={'data-stat': 'year_id'}):
        if "2022-2023" in line.get_text():
            target = line
            break

    for i in range(20):
        target = target.next_sibling
    player.goalsAgainst = target.text.strip()
    player.goalsAgainst = int(player.goalsAgainst)

    for i in range(6):
        target = target.next_sibling
    player.saves = target.text.strip()
    player.saves = int(player.saves)

    for i in range(2):
        target = target.next_sibling
    player.savePerc = target.text.strip()
    player.savePerc = float(player.savePerc)

    for i in range(8):
        target = target.next_sibling
    player.cleanSheets = target.text.strip()
    player.cleanSheets = int(player.cleanSheets)

    for i in range(2):
        target = target.next_sibling
    player.cleanSheetPerc = target.text.strip()
    player.cleanSheetPerc = float(player.cleanSheetPerc)

    for i in range(2):
        target = target.next_sibling
    player.penFaced = target.text.strip()
    player.penFaced = int(player.penFaced)

    for i in range(2):
        target = target.next_sibling
    penaltyAllowed = target.text.strip()
    player.penSaved = str(int(player.penFaced) - int(penaltyAllowed))
    player.penSaved = int(player.penSaved)

    start = soup.find(id="stats_keeper_adv_dom_lg")
    target = "None"
    for line in start.find_all(attrs={'data-stat': 'year_id'}):
        if "2022-2023" in line.get_text():
            target = line
            break
    for i in range(24):
        target = target.next_sibling
    player.xgAgainst = target.text.strip()
    player.xgAgainst = float(player.xgAgainst)

    start = soup.find(id="stats_passing_dom_lg")
    target = "None"
    for line in start.find_all(attrs={'data-stat': 'year_id'}):
        if "2022-2023" in line.get_text():
            target = line
            break
    for i in range(14):
        target = target.next_sibling
    player.totalPasses = target.text.strip()
    player.totalPasses = int(player.totalPasses)

    for i in range(4):
        target = target.next_sibling
    player.passAccuracy = target.text.strip()
    player.passAccuracy = float(player.passAccuracy)

def fwFill(player, soup):
    start = soup.find(id="stats_shooting_dom_lg")
    target = "None"
    for line in start.find_all(attrs={'data-stat': 'year_id'}):
        if "2022-2023" in line.get_text():
            target = line
            break
    for i in range(18):
        target = target.next_sibling
    player.shotsOnTarget = target.text.strip()
    player.shotsOnTarget = int(player.shotsOnTarget)

    for i in range(16):
        target = target.next_sibling
    player.penalties = target.text.strip()
    player.penalties = int(player.penalties)

    start = soup.find(id="stats_passing_types_dom_lg")
    target = "None"
    for line in start.find_all(attrs={'data-stat': 'year_id'}):
        if "2022-2023" in line.get_text():
            target = line
            break
    for i in range(26):
        target = target.next_sibling
    player.crosses = target.text.strip()
    player.crosses = int(player.crosses)

    start = soup.find(id="stats_passing_dom_lg")
    target = "None"
    for line in start.find_all(attrs={'data-stat': 'year_id'}):
        if "2022-2023" in line.get_text():
            target = line
            break
    for i in range(50):
        target = target.next_sibling
    player.keyPasses = target.text.strip()
    player.keyPasses = int(player.keyPasses)

    for i in range(8):
        target = target.next_sibling
    player.progPasses = target.text.strip()
    player.progPasses = int(player.progPasses)

    start = soup.find(id="stats_possession_dom_lg")
    target = "None"
    for line in start.find_all(attrs={'data-stat': 'year_id'}):
        if "2022-2023" in line.get_text():
            target = line
            break

    for i in range(22):
        target = target.next_sibling
    player.finalThirdTouches = target.text.strip()
    player.finalThirdTouches = int(player.finalThirdTouches)

    for i in range(8):
        target = target.next_sibling
    player.takeOns = target.text.strip()
    player.takeOns = int(player.takeOns)

    for i in range(2):
        target = target.next_sibling
    player.takeOnPerc = target.text.strip()
    player.takeOnPerc = float(player.takeOnPerc)

    for i in range(6):
        target = target.next_sibling
    player.dribbles = target.text.strip()
    player.dribbles = int(player.dribbles)

def dfFill(player, soup):
    start = soup.find(id="stats_passing_dom_lg")
    target = "None"
    for line in start.find_all(attrs={'data-stat': 'year_id'}):
        if "2022-2023" in line.get_text():
            target = line
            break
    for i in range(14):
        target = target.next_sibling
    player.totalPasses = target.text.strip()
    player.totalPasses = int(player.totalPasses)

    for i in range(4):
        target = target.next_sibling
    player.passAccuracy = target.text.strip()
    player.passAccuracy = float(player.passAccuracy)

    start = soup.find(id="stats_defense_dom_lg")
    target = "None"
    for line in start.find_all(attrs={'data-stat': 'year_id'}):
        if "2022-2023" in line.get_text():
            target = line
            break
    for i in range(14):
        target = target.next_sibling
    player.tackles = target.text.strip()
    player.tackles = int(player.tackles)

    for i in range(18):
        target = target.next_sibling
    player.blocks = target.text.strip()
    player.blocks = int(player.blocks)

    for i in range(6):
        target = target.next_sibling
    player.interceptions = target.text.strip()
    player.interceptions = int(player.interceptions)

    for i in range(4):
        target = target.next_sibling
    player.clearances = target.text.strip()
    player.clearances = int(player.clearances)

    start = soup.find(id="stats_misc_dom_lg")
    target = "None"
    for line in start.find_all(attrs={'data-stat': 'year_id'}):
        if "2022-2023" in line.get_text():
            target = line
            break
    for i in range(20):
        target = target.next_sibling
    player.fouls = target.text.strip()
    player.fouls = int(player.fouls)

    for i in range(24):
        target = target.next_sibling
    player.aerialDuelPerc = target.text.strip()
    player.aerialDuelPerc = float(player.aerialDuelPerc)

def mfFill(player, soup):
    start = soup.find(id="stats_passing_dom_lg")
    target = "None"
    for line in start.find_all(attrs={'data-stat': 'year_id'}):
        if "2022-2023" in line.get_text():
            target = line
            break
    for i in range(40):
        target = target.next_sibling
    player.longBallCompPerc = target.text.strip()
    player.longBallCompPerc = float(player.longBallCompPerc)

    start = soup.find(id="stats_misc_dom_lg")
    target = "None"
    for line in start.find_all(attrs={'data-stat': 'year_id'}):
        if "2022-2023" in line.get_text():
            target = line
            break
    for i in range(38):
        target = target.next_sibling    
    player.recoveries = target.text.strip()
    player.recoveries = int(player.recoveries)

def to_json(baller):
        if(baller.position == "FW"):
            return{
                'name': baller.name,
                'position': baller.position,
                'age': baller.age,
                'foot': baller.foot,
                'nation': baller.nation,
                'currClub': baller.currClub,
                'playerPic': baller.playerPic,
                'nationFlag': baller.nationFlag,
                'clubBadge': baller.clubBadge,
                'goals': baller.goals,
                'assists': baller.assists,
                'xG': baller.xG,
                'xA': baller.xA,
                'g_a': baller.g_a,
                'goalsPer90': baller.goalsPer90,
                'assistsPer90': baller.assistsPer90 ,
                'matchesPlayed': baller.matchesPlayed ,
                'minutesPlayed': baller.minutesPlayed ,
                'yellowCards': baller.yellowCards ,
                'redCards': baller.redCards ,
                'trophiesWon': baller.trophiesWon,
                'shotsOnTarget': baller.shotsOnTarget,
                'penalties': baller.penalties,
                'takeOns': baller.takeOns,
                'takeOnPerc': baller.takeOnPerc,
                'dribbles': baller.dribbles,
                'finalThirdTouches': baller.finalThirdTouches,
                'keyPasses': baller.keyPasses,
                'progPasses': baller.progPasses,
                'crosses': baller.crosses
            }
        if(baller.position == "MF"):
            return{
                'name': baller.name,
                'position': baller.position,
                'age': baller.age,
                'foot': baller.foot,
                'nation': baller.nation,
                'currClub': baller.currClub,
                'playerPic': baller.playerPic,
                'nationFlag': baller.nationFlag,
                'clubBadge': baller.clubBadge,
                'goals': baller.goals,
                'assists': baller.assists,
                'xG': baller.xG,
                'xA': baller.xA,
                'g_a': baller.g_a,
                'goalsPer90': baller.goalsPer90,
                'assistsPer90': baller.assistsPer90 ,
                'matchesPlayed': baller.matchesPlayed ,
                'minutesPlayed': baller.minutesPlayed ,
                'yellowCards': baller.yellowCards ,
                'redCards': baller.redCards ,
                'trophiesWon': baller.trophiesWon,
                'shotsOnTarget': baller.shotsOnTarget,
                'penalties': baller.penalties,
                'takeOns': baller.takeOns,
                'takeOnPerc': baller.takeOnPerc,
                'dribbles': baller.dribbles,
                'finalThirdTouches': baller.finalThirdTouches,
                'keyPasses': baller.keyPasses,
                'progPasses': baller.progPasses,
                'crosses': baller.crosses,
                'fouls': baller.fouls,
                'tackles': baller.tackles,
                'blocks': baller.blocks,
                'interceptions': baller.interceptions,
                'clearances': baller.clearances,
                'totalPasses': baller.totalPasses,
                'passAccuracy': baller.passAccuracy,
                'aerialDuelPerc': baller.aerialDuelPerc,    
                'recoveries': baller.recoveries,
                'longBallCompPerc': baller.longBallCompPerc                        
            }
        if(baller.position == "DF"):
            return{
                'name': baller.name,
                'position': baller.position,
                'age': baller.age,
                'foot': baller.foot,
                'nation': baller.nation,
                'currClub': baller.currClub,
                'playerPic': baller.playerPic,
                'nationFlag': baller.nationFlag,
                'clubBadge': baller.clubBadge,
                'goals': baller.goals,
                'assists': baller.assists,
                'xG': baller.xG,
                'xA': baller.xA,
                'g_a': baller.g_a,
                'goalsPer90': baller.goalsPer90,
                'assistsPer90': baller.assistsPer90 ,
                'matchesPlayed': baller.matchesPlayed ,
                'minutesPlayed': baller.minutesPlayed ,
                'yellowCards': baller.yellowCards ,
                'redCards': baller.redCards ,
                'trophiesWon': baller.trophiesWon,
                'fouls': baller.fouls,
                'tackles': baller.tackles,
                'blocks': baller.blocks,
                'interceptions': baller.interceptions,
                'clearances': baller.clearances,
                'totalPasses': baller.totalPasses,
                'passAccuracy': baller.passAccuracy,
                'aerialDuelPerc': baller.aerialDuelPerc
            }
        if(baller.position == "GK"):
            return{
                'name': baller.name,
                'position': baller.position,
                'age': baller.age,
                'foot': baller.foot,
                'nation': baller.nation,
                'currClub': baller.currClub,
                'playerPic': baller.playerPic,
                'nationFlag': baller.nationFlag,
                'clubBadge': baller.clubBadge,
                'goals': baller.goals,
                'assists': baller.assists,
                'xG': baller.xG,
                'xA': baller.xA,
                'g_a': baller.g_a,
                'goalsPer90': baller.goalsPer90,
                'assistsPer90': baller.assistsPer90 ,
                'matchesPlayed': baller.matchesPlayed ,
                'minutesPlayed': baller.minutesPlayed ,
                'yellowCards': baller.yellowCards ,
                'redCards': baller.redCards ,
                'trophiesWon': baller.trophiesWon,
                'saves': baller.saves,
                'savePerc': baller.savePerc,
                'cleanSheets': baller.cleanSheets,
                'cleanSheetPerc': baller.cleanSheetPerc,
                'goalsAgainst': baller.goalsAgainst,
                'xgAgainst': baller.xgAgainst,
                'penFaced': baller.penFaced,
                'penSaved': baller.penSaved,
                'totalPasses': baller.totalPasses,
                'passAccuracy': baller.passAccuracy
            }
playerNameArray = []
playerArray = []
with app.app_context():
    name = Names.query.first()
    playerNameArray.append(name.firstname)
    playerNameArray.append(name.secondname)

print(playerNameArray)

for i in range(2):
    gen_url = "https://fbref.com/en/players/"
    playerNameLow = playerNameArray[i].lower()
    nameshort = playerNameLow.split(' ')
    nameshortUpper = playerNameArray[i].split(' ')
    urlNameShort = (nameshort[1])[0:2]
    trailurl = gen_url + urlNameShort + "/"

    soup = getHTMLfile(trailurl, "followLink.html")
    time.sleep(3)

    target_link = getLink(
        soup, 'a', nameshortUpper[0] + '-' + nameshortUpper[1], 'href')

    print(target_link)
    playerlink = "https://fbref.com/" + target_link
    newsoup = getHTMLfile(playerlink, "playerLink.html")
    time.sleep(3)

    with open("playerLink.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    newsoup = BeautifulSoup(html_content, 'html5lib')

    with open("playerLink.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    newsoup = BeautifulSoup(html_content, 'html5lib')

    strong_tags = newsoup.find_all('strong')

    playerPosRef = None
    for strong_tag in strong_tags:
        if 'Position:' in strong_tag.text:
            playerPosRef = strong_tag

    almostPos = playerPosRef.next_sibling.strip()
    actualPos = almostPos.split(' ')[0]
    if(len(actualPos) >= 5 and actualPos[3] == 'M'):
        actualPos = "MF"
    else:
        actualPos = actualPos[:2]
    
    playerVal = createPlayer(actualPos)
    playerArray.append(playerVal)
    generalInfoFill(playerArray[i], newsoup, actualPos)
    linkFill(playerArray[i], newsoup)
    genStatFill(playerArray[i], newsoup)

    if (actualPos == "GK"):
        gkFill(playerArray[i], newsoup)
        
    if (actualPos == "FW"):
        fwFill(playerArray[i], newsoup)

    if (actualPos == "DF"):
        dfFill(playerArray[i], newsoup)

    if (actualPos == "MF"):
        fwFill(playerArray[i], newsoup)
        dfFill(playerArray[i], newsoup)
        mfFill(playerArray[i], newsoup)

player0 = to_json(playerArray[0])
player1 = to_json(playerArray[1])
serialized_players = json.dumps([player0, player1])
print(serialized_players)

url = 'http://localhost:5000/players'
response = requests.post(url, json=serialized_players)

if response.status_code == 200:
    print('POST request successful')

else:
    print('POST request failed')


with app.app_context():
    db.session.query(Names).delete()
    db.session.commit()