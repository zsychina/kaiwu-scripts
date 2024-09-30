import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from helper import (
    kaiwu_login,
    select_bar,
    upload_train_missions_one_page,
    upload_last_train_mission
)

with open('config.json', 'r') as file:
    config = json.load(file)

os.environ['NO_PROXY'] = '*'
service = Service(executable_path=config['driver_path'])
driver = webdriver.Chrome(service=service)


# 1. 登陆kaiwu
driver = kaiwu_login(config, driver)

# 2. 选择集群训练
driver = select_bar(driver, "集群训练")

# 3. 提交当前这一页的所有训练任务的模型
# driver, mission_list = upload_train_missions_one_page(driver)

# 3. 或者仅提交第一个训练任务的模型
driver, mission_list = upload_last_train_mission(driver)




time.sleep(100)
driver.quit()
