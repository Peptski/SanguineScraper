from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import smtplib
import time

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('log-level=3')
driver = webdriver.Chrome( options=chrome_options)

def scrape(url, targetValue, targetId='', targetClass=''):
    driver.get(url)
    time.sleep(5)
    if targetId != '':
        if not driver.find_elements(By.ID, targetId): return False
        res = driver.find_elements(By.ID, targetId)[0].text
    else:
        if not driver.find_elements(By.CLASS_NAME, targetClass): return False
        res = driver.find_elements(By.CLASS_NAME, targetClass)[0].text
    print(f'Found: _{res}_, looking for: _{targetValue}_')
    if res != targetValue:
        with open('found.txt', 'a') as f:
            f.write('\n'.join([res, targetValue, ""]))
    return res == targetValue
    
def alert(url, newData, foundData):
    with open('found.txt', 'a') as f:
        f.write('\n'.join([str(datetime.now())] + foundData))

    with open('targets.txt', 'w') as f:
        f.write('\n'.join(newData))

    print(f'DATA CHANGED IN URL: {url}')
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.ehlo()
    s.login('from', 'from_pw')
    mail = """\
From: 
To: 
Subject: Change detected!

Change detected on URL: %s
""" % (url)
    s.sendmail('from', 'to', mail)
    s.close()


while True:
    with open('targets.txt', 'r') as f:
        data = f.read().splitlines()
        for i in range(len(data)//4):
            startIndex = i * 4
            print(f'Scraping {data[startIndex]}...')
            if data[startIndex + 1] == 'id':
                res = scrape(data[startIndex], data[startIndex + 3], targetId=data[startIndex + 2])
            else:
                res = scrape(data[startIndex], data[startIndex + 3], targetClass=data[startIndex + 2])
            if not res:
                newData = data[:startIndex] + data[startIndex + 4:]
                foundData = data[startIndex:startIndex + 4]
                alert(data[startIndex], newData, foundData)
                break
            else:
                print(f'No change detected...')
    time.sleep(60 * 3)
            

