from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient
import hashlib
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pprint
from selenium.webdriver.common.action_chains import ActionChains

client = MongoClient('127.0.0.1', 27017)
db = client['mail_db']
mail_db = db.news

s = Service('./chromedriver')
driver = webdriver.Chrome(service=s)
driver.get('https://account.mail.ru/login?&fail=1&from=navi')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
elem = driver.find_element(By.XPATH, "//input[@name='username']")
elem.send_keys("study.ai_172@mail.ru")
elem.send_keys(Keys.RETURN)
time.sleep(5)
elem = driver.find_element(By.XPATH, "//input[@name='password']")
elem.send_keys("NextPassword172#")
elem.send_keys(Keys.RETURN)
time.sleep(25)
urls = []
top = ''
while True:
    time.sleep(3)
    elem = driver.find_elements(By.XPATH,
                                "//a[@class='llc llc_normal llc_new llc_new-selection js-letter-list-item js-tooltip-direction_letter-bottom']")
    if top == elem[-1].get_attribute('href'):
        break
    for i in elem:
        urls.append(i.get_attribute('href'))
    actions = ActionChains(driver)
    actions.move_to_element(elem[-1]).perform()
    top = f"{elem[-1].get_attribute('href')}"


links = set(urls)
mails = []
for item in links:
    mail_info = {}
    driver.get(item)
    time.sleep(10)
    sender = driver.find_element(By.XPATH, ".//div[@class='letter__author']").text
    letter_subj = driver.find_element(By.XPATH, ".//h2[@class='thread-subject']").text
    letter_date = driver.find_element(By.XPATH, ".//div[@class='letter__date']").text
    letter_text = driver.find_element(By.XPATH, "//*[contains(@id, '_BODY')]").text
    mail_info['sender'] = sender
    mail_info['letter_date'] = letter_date
    mail_info['letter_subj'] = letter_subj
    mail_info['letter_text'] = letter_text
    mail_info['_id'] = hashlib.md5(str(mail_info).encode('utf-8')).hexdigest()
    mails.append(mail_info)
    print(mail_info)#чтобы видеть выполнение кода
    try:
        mail_db.insert_one(mail_info)
    except DuplicateKeyError:
        print(f"Document  {mail_info['letter_subj']} already exist")

result = list(mail_db.find({}))
pprint(result)
