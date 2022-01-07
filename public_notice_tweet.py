#!/usr/bin/env python
# coding: utf-8

# ### Patricia Sendao 
# ### Coding for Lawyers 
# ### Final Project

# #### Overview
# This program gathers public hearing notices from the Star-Advertiser's public notices page and tweets the notice on @PublicNoticesHI. The idea for this project came after I took Administrative Law and we were required to find an agency hearing and submit testimony. I found it annoying that to find out about these public hearings, I had to proactively search them out on this website. I hope that this project could at least help next semester's class receive notifications when new notices are posted. 
# 
# The program does the following: 
# - Determines whether a notice has been posted that day on the main page
# - Pulls link from posting and scrapes the page for notice text
# - Tweets small portion of notice text and link to @PublicNoticesHI
# - Takes post text and saves to csv as a record of the hearing notices
# 
# The source page: 
# https://statelegals.staradvertiser.com/category/public-notices/public-hearings/.
# 
# The Twitter page:
# https://twitter.com/PublicNoticesHI
# 

# #### Import Libraries

# In[24]:


# import necessary packages



# #### Scrape Website for Public Notices
# 
# This step is used no matter what and starts on the main Star-Advertiser's public notices website. 

# In[25]:

import requests
import re
from bs4 import BeautifulSoup
import tweepy
import datetime
import csv
from os.path import exists
import docx
import twitter_passwords
import time

import os
# Get the “Legals/Public Notices” page on the Star-Advertiser website.
url = "https://statelegals.staradvertiser.com/category/public-notices/public-hearings/"

# # I tried to create function for scraping, but never got it to work with the first part of the program.
# # But I could get it to work with the latter part to send tweets and save to csv
# def scrape(item):
#     hdr = {'User-Agent': 'Mozilla/5.0'}
#     response = requests.get(item, headers=hdr)
#     # print(response.text)
#     html = response.text

# Disguise request with HTTP headers to stop '403 Forbidden' error
hdr = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=hdr)
html = response.text
soup = BeautifulSoup(html,'html.parser') 

print(url)


# #### How to Run the Code
# 
# The program is set to run to examine the public notice website, determine whether there are any new postings that day, and if so, tweet a small portion of the text and link on Twitter. 
# 
# There are at least two roadblocks that might come up in the course of trying to check this program. 
# 
# 1. If there are no notices that day, then the program does nothing. This may be the case when running this month because less notices have been posted in December than November as the holidays approach. 
# 
# 2. If you try to run the chunk of code that tweets the notice more than once on a given day, the program receives a '403 Forbidden' error because Twitter blocks you from tweeting the same thing twice. I had been convinced in my class presentation that it was jupyter notebook that was giving me grief because the code would stop working unexpectedly, but this was the actual issue. 
# 
# So, to address issue 1, I first have a block of code that is how I would want the program to run on a server. If there is a notice that day, it will send a tweet, but if not then nothing happens. If there's no notice on the particular day you want to run the program, then I've flagged where to change the string of the date so it can pull a notice from a previous day.
# 
# I don't have a really good workaround for issue 2. I flagged one area where I could see that manipulating the length of the tweet could be a potential workaround. Otherwise, I'm happy to share either the login credentials for the twitter profile or delete any posts so that the code can be run again. 

# #### Scrapes Page For All Links That Match Today's Date

# In[26]:


#sets todays date
today = datetime.date.today().strftime("%Y/%m/%d")
#today = '2022/01/04'
print(today)

all = soup.find_all('a', href = re.compile('https://statelegals.staradvertiser.com/\d{4}/\d{2}/\d{2}/\d{10}'))
print(all[0]['href'])

print(len(all))
all = [str(i) for i in all]



# Search all notices for posts that match today's date and pulls "a" tag and span which includes part of text
matching = [s for s in all if today in s]
# # Replace 'today' w/ string of notice that exists if no notice matches today
# # for example
# matching = [s for s in all if "2021/12/12" in s]

print(matching)
# print(len(matching))

# creates list that truncates string to just url
links = []

for item in matching: 
    link = re.findall('https://statelegals.staradvertiser.com/\d{4}/\d{2}/\d{2}/\d{10}', item)
    links.append(link)
links = [''.join(ele) for ele in links]
print(links)


# #### Twitter Bot
# 
# This is what I agreed to when I created @PublicNoticesHI and applied for Twitter API key: 
# 
# *Spam, bots, and automation*
# 
# The use of the Twitter API and developer products to create spam, or engage in any form of platform manipulation, is prohibited. You should review the Twitter Rules on platform manipulation and spam, and ensure that your service does not, and does not enable people to, violate our policies.
# 
# Services that perform write actions, including posting Tweets, following accounts, or sending Direct Messages, must follow the Automation Rules. In particular, you should: 
# 
# Always get explicit consent before sending people automated replies or Direct Messages
# 
# Immediately respect requests to opt-out of being contacted by you
# 
# Never perform bulk, aggressive, or spammy actions, including bulk following
# 
# Never post identical or substantially similar content across multiple accounts
# 
# If you’re operating an API-based bot account you must clearly indicate what the account is and who is responsible for it. You should never mislead or confuse people about whether your account is or is not a bot. A good way to do this is by including a statement that the account is a bot in the profile bio.

# In[20]:


# create for loop that takes [links] and scrapes, and saves 

# I was only able to get this to work in this part of the program and the write to csv portion
def scrape(item):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(item, headers=hdr)
    # print(response.text)
    html = response.text
    soup = BeautifulSoup(html,'html.parser')
    return soup

for item in links:
    print(item)
    time.sleep(1)
    soup = scrape(item)
    notice = []
    # posts are written in two different formats
    # the first for loop catches the least common, 
    # if both are found then resulting string of both is cropped anyways so there shouldn't be duplicate text
    for font in soup.find_all('font', attrs={"size":"2", "color":"#000000"}):
        font = font.text
        notice.append(font.replace("\n", "")) 
    print("Notice",notice)
    # this works for some posts
    for p in soup.find_all('div', attrs={'class':'entry-content'}):
        p = p.text
        notice.append(p.replace("\n", ""))
    #print(notice)
    # converts list elems to string, string too long to tweet
    strList = [str(item) for item in notice]
    myString = " ".join(strList)
    # limit string to 212 characters (280-64 to append url-space-...)
    shortString = myString[0:212]+ "..." + " " + (item)
    print("Short String",shortString)
    # Use Twitter API to tweet
    
    client = tweepy.Client(twitter_passwords.bearer_token,
                           twitter_passwords.consumer_key,
                           twitter_passwords.consumer_secret,
                           twitter_passwords.access_token,
                           twitter_passwords.access_token_secret)
    client.create_tweet(text = shortString)


# #### Automation
# 
# Eventually, once this program was cleaned up, I would have it set up on a server to run once a day.

# #### Saving to a CSV 
# 
# Notices are pulled from the website after awhile. I thought creating a list in a csv of the notices would be helpful later down the line to record the text in case I need to troubleshoot any issues with the posting or to use later on to examine agency notices in state. 

# In[21]:


# # creates list for csv with today's date and notice text
# notices = []
# for item in links:
#     scrape(item)
#     for p in soup.find_all('div', attrs={'class':'entry-content'}):
#         p = p.text
#         p =(p.replace("\n", ""))
#         p = [today, p]
#         notices.append(p)
#
# print(notices)

# Creates new csv if needed
# def createCSV(fieldnames):
#     if(exists('notices.csv') == False):
#         with open('notices.csv', 'w', newline='') as f:
#             writer = csv.DictWriter(f, fieldnames=fieldnames)
#             writer.writeheader()
#
# # Adds list of new notices
# def addNotice(post):
#     with open('notices.csv','a') as f:
#         writer = csv.writer(f)
#         writer.writerows(post)
            
# Add new notices to file
#client_csv_headers = ['date','notice_text']
#createCSV(client_csv_headers)
#addNotice(notices)





