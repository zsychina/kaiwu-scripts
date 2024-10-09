import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from helper import (
    kaiwu_login,
    select_bar,
    eval_models_range
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

# 3. 根据区间评估模型
driver = eval_models_range(config, driver, name='qq', maxh=83, minh=76, page=50)



time.sleep(100)
driver.quit()
