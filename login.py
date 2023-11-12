import urllib3
import time
import random
import yaml
import schedule
import re
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class HostlocLogin:
    def __init__(self):
        self.username = ''
        self.passwd = ''
        self.question_id = ''
        self.answer = ''
        self.login_time = ''

    def loadConfig(self):
        with open('./config.yml', 'rt', encoding='utf8') as f:
            data = yaml.safe_load(f)
            self.username = data['username']
            self.passwd = data['passwd']
            if 'question_id' in data:
                self.question_id = str(data['question_id'])
                self.answer = data['answer']

            if 'login_time' in data:
                self.login_time = data['login_time']
                # 检查时间格式是否为 HH:MM
                if not re.match(r"\d{2}:\d{2}", self.login_time):
                    raise ValueError("时间格式不正确，应为 HH:MM")
            else:
                random_hour = random.randint(0, 23)
                random_minute = random.randint(0, 59)
                self.login_time = f"{random_hour:02d}:{random_minute:02d}"
                print(f"set random login time: {self.login_time}")

    def login(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run Chrome in headless mode.
        options.add_argument('--disable-gpu')  # Disable GPU acceleration.
        options.add_argument('--no-sandbox')

        driver = webdriver.Chrome(options=options)
        login_url = 'https://hostloc.com/forum.php'
        driver.get(login_url)

        driver.find_element(By.NAME, "username").send_keys(self.username)
        driver.find_element(By.NAME, "password").send_keys(self.passwd)

        button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        button.click()

        if self.question_id != '' and self.question_id != 0:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.NAME, "questionid")))
            select_box= Select(driver.find_element(By.NAME, "questionid"))
            select_box.select_by_value(self.question_id)

            answer_txt = driver.find_element(By.NAME, "answer")
            answer_txt.send_keys(self.answer)

            lgbt = driver.find_element(By.NAME, "loginsubmit")
            lgbt.click()

        time.sleep(10)

        cnt = random.randint(12, 20)
        for _ in range(cnt):
            uid = random.randint(15000, 50000)
            print(f"visit user: {uid}")
            driver.get(f"https://hostloc.com/space-uid-{uid}.html")
            time.sleep(random.randint(5, 20))

        time.sleep(random.randint(10, 20))
        driver.quit()

def run():
    loc = HostlocLogin()
    loc.loadConfig()

    def login_task():
        loc.login()

    # 启动时执行一次
    #login_task()

    schedule.every().day.at(loc.login_time).do(login_task)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    run()
