
import os
import time
from datetime import date, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

dirname = os.path.dirname(__file__)

load_dotenv()

def holland():
    # set url
    userid=os.getenv("lta_userid")
    pw=os.getenv("lta_pw")
    url = 'https://clubspark.lta.org.uk/hollandpark2'

    # call open browser function
    driver = webdriver.Chrome(os.path.join(dirname, 'chromedriver'))
    driver.get(url)
    # login to website
    driver.find_element(By.XPATH, '//*[@id="account-options"]/ul/li[1]/span[1]/a').click()
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="sign-in-view"]/section/div/div/div[2]/div/div/div[2]/form/div/ul/li[1]/button').click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div/div/div/div[1]/div/span/div/input").send_keys(userid)
    driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div/div/div/div[2]/div/div/span/lightning-input/div/input').send_keys(pw)
    driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div/div/div/div[3]/button").click()
    time.sleep(6)
    driver.find_element(By.XPATH, "//*[@id=\"content\"]/div[1]/div/div/div/ul/li[2]/a").click()
    
    current_date = date.today()
    end_date = date.today() + timedelta(days=8)

    d = {}
    while current_date < end_date:
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        free_tags = soup.find_all('span', class_="available-booking-slot")
        free_times = []
        for tag in free_tags:
            split_tag = tag.text.split(":")
            start_time = split_tag[0][-2:]
            free_times.append(int(start_time))

        date_formatted = current_date.strftime('%d/%m/%Y')
        d[date_formatted] = set(free_times)
        current_date += timedelta(days=1)
        driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div/form/div/div/div[1]/div/div[1]/a[3]').click()

    return d