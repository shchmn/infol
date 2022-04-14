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
db = client['mail']
maildb = db.maildb

s = Service('./chromedriver')
driver = webdriver.Chrome(service=s)
wait = WebDriverWait(driver, 15)

driver.get('https://account.mail.ru/login?')
time.sleep(10)
elem = driver.find_element(By.XPATH, "//input[@name='username']")
elem.send_keys("study.ai_172@mail.ru")
elem.send_keys(Keys.ENTER)
time.sleep(5)
elem = driver.find_element(By.XPATH, "//input[@name='password']")
elem.send_keys("NextPassword172#")
elem.send_keys(Keys.ENTER)
time.sleep(10)

urls = []
top = ''
xpath = "//a[contains(@href,'/inbox/0:')]"
_ = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

last_letter = None
while True:
    letters = driver.find_elements(By.XPATH, xpath)
    l = letters[-1].get_attribute('href')
    if last_letter == l:
        break
    for i in letters:
        urls.append(i.get_attribute('href').split('?')[0])

    last_letter = l
    actions = ActionChains(driver)
    actions.move_to_element(letters[-1]).perform()
    time.sleep(4)

urls = list(set(urls))
data = []
for url in urls:
    driver.get(url)
    _ = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[@class='thread-subject']")))
    time.sleep(5)

    h2 = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[@class='thread-subject']"))).get_attribute("innerText")

    frm = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='letter-contact']"))).get_attribute("title")

    date = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='letter__date']"))).get_attribute("innerText")

    text = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='letter__body']"))).get_attribute("innerText")

    el = {}
    el['from'] = frm
    el['date'] = date
    el['topic'] = h2
    el['text'] = text.replace('\n', ' ').replace('\t', ' ')

    data.append(el)


for el in data:
    try:
        maildb.insert_one(el)
    except DuplicateKeyError:
        print(f"Document  {el['topic']} already exist")

    result = list(maildb.find({}))
    pprint(result)
