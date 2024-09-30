import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from helper import (
    kaiwu_login,
    select_bar,
    eval_models_one_page,
)


with open('config.json', 'r') as file:
    config = json.load(file)

os.environ['NO_PROXY'] = '*'
service = Service(executable_path=config['driver_path'])
driver = webdriver.Chrome(service=service)


# 1. 登陆kaiwu
driver = kaiwu_login(config, driver)

# 2. 选择模型评估
driver = select_bar(driver, "模型管理")

# 3. 当前这一页所有模型提交评估
driver = eval_models_one_page(config, driver)

time.sleep(100)
driver.quit()


