import lxml.html
import requests

import time

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import sys

import webbrowser
import pyautogui


##TEAM ABBREVIATIONS
global allTeams
allTeams = {
    'Atlanta Hawks':'ATL',
    'Brooklyn Nets':'BKN',
    'Boston Celtics':'BOS',
    'Charlotte Hornets':'CHO',
    'Chicago Bulls':'CHI',
    'Cleveland Cavaliers':'CLE',
    'Dallas Mavericks':'DAL',
    'Denver Nuggets':'DEN',
    'Detroit Pistons':'DET',
    'Golden State Warriors':'GSW',
    'Houston Rockets':'HOU',
    'Indiana Pacers':'IND',
    'Los Angeles Clippers':'LAC',
    'Los Angeles Lakers':'LAL',
    'Memphis Grizzlies':'MEM',
    'Miami Heat':'MIA',
    'Milwaukee Bucks':'MIL',
    'Minnesota Timberwolves':'MIN',
    'New Orleans Pelicans':'NOP',
    'New York Knicks':'NYK',
    'Oklahoma City Thunder':'OKC',
    'Orlando Magic':'ORL',
    'Philadelphia 76ers':'PHI',
    'Phoenix Suns':'PHX',
    'Portland Trail Blazers':'POR',
    'Sacramento Kings':'SAC',
    'San Antonio Spurs':'SAS',
    'Toronto Raptors':'TOR',
    'Utah Jazz':'UTA',
    'Washington Wizards':'WAS'
}

def emailresults():
    sendee = input("To whom would you like to email: ")
    header = "Game Scores"
    sender = "bigboytommy7@outlook.com"
    password = "butter123"
    body = finalscores
    try:     
        s = smtplib.SMTP(host='smtp.office365.com', port=587)
        s.starttls()
        s.login(sender, password)
        msg = MIMEMultipart()
        msg['From']= sender
        msg['To']= sendee
        msg['Subject']= header
        msg.attach(MIMEText(body, 'plain'))
        s.send_message(msg)
        del msg
        s.quit()
        print("Email has been sent to " + sendee)
    except:
        print("Oops, something went wrong")
        emailresults()   

def makeURL():
    while(True):
        team = input("Enter the name of a pro team or press \"q\" to quit: ")
        if(team=="q" or team=="Q"):
            print("Adios!")
            sys.exit(0)
        ##Starts timer as soon as team name is inputted; used to find scrape execution time
        global start_time
        start_time = time.perf_counter()
        print("Searching...")
        team = team.title()
        #print(team)
        if (team in allTeams):
            global teamOne
            teamOne = team
            abbreviation = allTeams.get(team)
            ##Sample URL - "https://www.basketball-reference.com/teams/GSW/2021.html"
            url = "https://www.basketball-reference.com/teams/" + str(abbreviation) + "/2021.html"
            startScrape(url)            
        else:
            print("Team Not Found!")

def viewRoster():
    print("Searching...")    
    print(teamOne + " roster:")
    ##Scrapes (iterates) through a table full of players in order to print roster
    ##Run-time of scrape to find roster
    starttimeroster = time.perf_counter()
    for player in range(1,11):
        roster = content.xpath('//*[@id="roster"]/tbody/tr[' + str(player) + ']/td[1]/a/text()')
        print("".join(roster))
    ##Reference to source code snippet - //*[@id="roster"]/tbody/tr[2]/td[1]/a
    stoptimeroster = time.perf_counter()
    clock = float(stoptimeroster) - float(starttimeroster)
    clock = round(clock,3)
    print("Results loaded in " + str(clock) + " seconds")

def buyTickets():
    teamOneSplit = teamOne.split()
    teamOneSplit = "-".join(teamOneSplit)
    ##URL changes accordingly (to team chosen)
    ticketURL = "https://seatgeek.com/" + teamOneSplit + "-tickets"
    webbrowser.open(ticketURL) 
    ##Sample URL Reference - https://seatgeek.com/oklahoma-city-thunder-tickets

def randomHighlight():
    ##Site utilized - https://ytroulette.com/
    webbrowser.open("https://ytroulette.com/")
    time.sleep(3)

    ##Mouse automatically goes to those coordiates (location of search box for website) then clicks and types before hitting enter
    pyautogui.click(758,125)
    pyautogui.typewrite(teamOne + " highlights")
    pyautogui.click(1150,125)

def startScrape(url):
    ##Starter code - https://python-docs.readthedocs.io/en/latest/scenarios/scrape.html
    page = requests.get(url)
    ##Page contents available for all functions - allows for more simplistic design & increases functionability
    global content
    content = lxml.html.fromstring(page.content)

    ##This will make the score (outcome) of the game into a list
    scores = content.xpath('//*[@id="meta"]/div[2]/p[2]/a/text()')

    ##//span[@class="review-title"]/following-sibling::text()"
    #print('Buyers: ', buyers)
    scores = "".join(scores)
    ##Removes very odd spacing
    global finalscores
    finalscores = scores.replace("\n","").replace("  "," ").replace("     "," ").replace("   "," ")    
    for key,value in allTeams.items():
        if(value in finalscores):
            finalscores = finalscores.replace(value,key)
    finalscores = teamOne + finalscores
    print(finalscores)
    stop_time = time.perf_counter()
    ##Functions starts after makeURL() is ran; records the end time in order to formulate cumulative time of the webscrape
    clock = float(stop_time) - float(start_time)
    clock = round(clock,3)
    print("Results loaded in " + str(clock) + " seconds")
    ##Total run-time of scrape
    while(True):
        menu = input("Choose an option (or any other button to exit menu)\n"
        "1: Email Results\n"
        "2: View Roster\n"
        "3: Buy Tickets\n"
        "4: Random " + teamOne + " Highlights\n"
        )
        if(menu == str(1)):
            emailresults()
        elif(menu == str(2)):
            viewRoster()
        elif(menu == str(3)):
            buyTickets()
        elif(menu == str(4)):
            randomHighlight()           
        else:
            break                


##Reference URL - "https://www.basketball-reference.com/teams/OKC/2020.html"
##def makeURL(team):
##    today = date.today()
##    date = today.strftime("%Y,%m,%d")
##    print(date)
##    url = "https://www.basketball-reference.com/boxscores/"

##makeURL("Oklahoma City
##today = date.today()
##date = today.strftime("%Y%m%d")
##print(date)

makeURL()
