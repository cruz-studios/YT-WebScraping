#Importing Selenium libraries
from re import T
from venv import create
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd 
from df2gspread import df2gspread as d2g

#Importing Gspread libraries
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

#Setting up framework for google sheet
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)

#Create the Webdriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

#Open the Youtube Page
driver.get('https://www.youtube.com/c/LexClips/videos')
time.sleep(5)

#Find the element of the videos and loop through them
# videos = driver.find_elements(By.CLASS_NAME, 'style-scope ytd-grid-renderer')
videos = driver.find_elements(By.CLASS_NAME, 'style-scope ytd-grid-video-renderer')

video_list = []

for video in videos:
    title = video.find_element(By.ID, 'video-title').text
    views = video.find_element(By.ID, 'metadata-line').text.split()[0]
    #print('Video Title: ', title , '\nTotal Views: ', views)
    vid_item = {
        'title' : title,
        'views' : views
    }

    video_list.append(vid_item)

#Creating a datafram
df  = pd.DataFrame(video_list)
print(df)

spreadsheet_key = '1KdVu6iIi_ak96gFWynkzQQhz_V-nhZsnQ2HG6NF3fB8'
wks_name = 'Master'

d2g.upload(df,spreadsheet_key,wks_name, row_names = True, credentials=creds)

