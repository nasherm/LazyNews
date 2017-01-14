#!/usr/bin/env python

# The script is for a program which interacts with the Google custom search API. The program searches key terms
# decided by the user, and uses the information to generate emails which send links to news stories based on these key
# terms.

from apiclient.discovery import build
from collections import defaultdict
import time
import smtplib
from email.mime.text import MIMEText

myApiKey = "your_api_key"
mySearchID = "your_search_Id"

myEmail = "your_email"
host = "your_host_email"
hostPassword = 'your_host_email_password'

# This functions returns the results of a search based on a news feed
def googleSearch(searchTerm, apiKey, searchId):
    service = build("customsearch", "v1", developerKey=apiKey)
    res = service.cse().list(q=searchTerm, cx=searchId, dateRestrict="d1", gl='uk', imgType="news").execute()
    return res['items']


# This holds the search terms and the links to news articles
d = defaultdict(list)


# Returns a list of links to sites related to googleSearch of key Term
def getSearchList(searchTerm, apiKey, searchId):
    res = googleSearch(searchTerm, apiKey, searchId)
    listOfLinks = []
    for link in res:
        listOfLinks.append(link['title'] + ':' + link['link'])
    return listOfLinks


# Add searches to the dictionary of search terms
def appendSearch(searchTerm, dict, apiKey, searchId):
    listOfLinks = getSearchList(searchTerm, apiKey, searchId)
    dict[searchTerm].append(listOfLinks)


def createFile(fileName, dict):
    theFile = open(fileName, 'w')
    for key in dict.keys():
        for item in dict[key]:
            theFile.write("Topic: " + key + "\n")
            for i in range(0, len(item)):
                theFile.write(item[i])
                theFile.write("\n")
            theFile.write("\n")
    theFile.close()



# Create email for sending links
def writeEmail(infoFile, sender, recipient, subject):
    theFile = open(infoFile, 'r')
    msg = MIMEText(theFile.read())
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    theFile.close()
    return msg


# Send message
def sendMessage(message, host, recip, hostPassword):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(host, hostPassword)
    s.send_message(message)
    s.quit()



def main():
    #Array of topics to search for
    topics = ["your", "own", "search", "terms"]
    newsFILE = 'news.txt'
    # This holds the search terms and the links to news articles
    d = defaultdict(list)
    while(True):
        print("Collecting topic news")
        for topic in topics:
            appendSearch(topic, d, myApiKey, mySearchID)
        createFile(newsFILE, d)
        print("Writing email")
        email = writeEmail(newsFILE, host, myEmail, "NEWS OF THE DAY")
        print("Sending email")
        sendMessage(email, host, myEmail, hostPassword)
        break
    time.sleep(86164) #Wait a day
    return main()


if __name__ == "__main__":
    main()
