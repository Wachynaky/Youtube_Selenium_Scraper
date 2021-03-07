from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import re 

def scrape_channel(url):
    data = []
    driver = webdriver.Chrome('chromedrive/chromedriver')
    driver.get(url)
    time.sleep(5)

    height = 0
    tries = 0
    while True:
        old_length = len(data)
        height += 2000
        driver.execute_script(f"window.scrollTo(0, {height});")
        time.sleep(0.25)
        output = driver.page_source
        soup = BeautifulSoup(output, 'html.parser')
        for x in soup.find_all(class_='yt-simple-endpoint style-scope ytd-grid-video-renderer'):
            data.append(x)
        data = list(dict.fromkeys(data))
        if len(data) == old_length:
            tries += 1
        else:
            tries == 0
        if tries >= 10:
            break

    final_output = []
    for element in data:
        title = element.text
        views = int(re.search(r'(\d*.\d*)\W{1}views',str(element)).group(1).replace(',','').replace(' ',''))
        duration = re.search(r'(?<=ago\W)(.*)\W{1}views',str(element)).group(1).replace(',','').replace(str(views),'')
        print(duration)
        try:
            hours = int(re.search(r'(\d*)\W{1}hour', duration).group(1))
        except:
            hours = 0
        try:
            minutes = int(re.search(r'(\d*)\W{1}minute', duration).group(1))
        except:
            minutes = 0
        try:
            seconds = int(re.search(r'(\d*)\W{1}second', duration).group(1))
        except:
            seconds = 0
        duration_in_seconds = hours*3600 + minutes * 60 + seconds
        print(f'total duration: {duration_in_seconds}, hours: {hours}, minutes: {minutes}, seconds: {seconds}.')
        final_output.append(
            {
                'Title':title,
                'views':views,
                'duration':duration_in_seconds,
                'video_number':len(data) - len(final_output)
            }
        )

    output = pd.DataFrame.from_dict(final_output)
    output.to_csv('output.csv',index=True)

if __name__ == "__main__":
    url = 'https://www.youtube.com/c/TechWithTim/videos'
    scrape_channel(url)
