import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

t = 1
timeout = 10
makelist = False
debug = False

headless = True
images = False
max = False

incognito = True

if makelist:
    links = open("oddsportal-links.txt", "a")


def get(driver, url, count):
    print(url)
    driver.get(url)
    time.sleep(1)
    if makelist:
        arr = []
        try:
            getElement(driver, '//td[@class="name table-participant"]/a')
            for a in driver.find_elements_by_xpath('//td[@class="name table-participant"]/a'):
                arr.append(a.get_attribute('href') + "\n")
            print(arr)
            links.writelines(arr)
            time.sleep(1)
        except:
            get(driver, url, count + 1)
    elif count < 2:
        try:
            data = [getElement(driver, '//div[@id="col-content"]/h1').text,
                    driver.find_element_by_xpath('//div[@id="col-content"]/p').text.split(",")[1].strip(),
                    driver.find_element_by_xpath('//div[@id="event-status"]/p/strong').text]
            td = driver.find_element_by_xpath('//a[contains(text(),"Pinnacle")]').find_element_by_xpath(
                '../../..').find_elements_by_tag_name('td')
            data.append(td[1].text)
            data.append(td[3].text)
            data.append(url)
            print(data)
            write(data)
            time.sleep(1)
        except:
            get(driver, url, count + 1)


def write(rows):
    with open('oddsportal-pinnacle.csv', mode='a', newline="") as outfile:
        employee_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow(rows)


def main():
    # logo()
    driver = getChromeDriver()
    with open('oddsportal-links.txt') as urls:
        for line in urls.readlines():
            get(driver, line.strip(), 0)


def click(driver, xpath):
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()


def getElement(driver, xpath):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))


def sendkeys(driver, xpath, keys):
    getElement(driver, xpath).send_keys(keys)


def getChromeDriver(proxy=None):
    options = webdriver.ChromeOptions()
    if debug:
        # print("Connecting existing Chrome for debugging...")
        options.debugger_address = "127.0.0.1:9222"
    if not images:
        # print("Turning off images to save bandwidth")
        options.add_argument("--blink-settings=imagesEnabled=false")
    if headless:
        # print("Going headless")
        options.add_argument("--headless")
        options.add_argument("--window-size=1920x1080")
    if max:
        # print("Maximizing Chrome ")
        options.add_argument("--start-maximized")
    if proxy:
        # print(f"Adding proxy: {proxy}")
        options.add_argument(f"--proxy-server={proxy}")
    if incognito:
        # print("Going incognito")
        options.add_argument("--incognito")
    return webdriver.Chrome(options=options)


def getFirefoxDriver():
    options = webdriver.FirefoxOptions()
    if not images:
        # print("Turning off images to save bandwidth")
        options.set_preference("permissions.default.image", 2)
    if incognito:
        # print("Enabling incognito mode")
        options.set_preference("browser.privatebrowsing.autostart", True)
    if headless:
        # print("Hiding Firefox")
        options.add_argument("--headless")
        options.add_argument("--window-size=1920x1080")
    return webdriver.Firefox(options)


def logo():
    print("""
       ____      __    __        ____             __        __
      / __ \____/ /___/ /____   / __ \____  _____/ /_____ _/ /
     / / / / __  / __  / ___/  / /_/ / __ \/ ___/ __/ __ `/ / 
    / /_/ / /_/ / /_/ (__  )  / ____/ /_/ / /  / /_/ /_/ / /  
    \____/\__,_/\__,_/____/  /_/    \____/_/   \__/\__,_/_/   

================================================================
      Developed by: https://www.fiverr.com/muhammadhassan7/
================================================================
    """)


if __name__ == "__main__":
    main()
