import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

def kaiwu_login(config, driver):
    # 登陆界面
    driver.get('https://aiarena.tencent.com/p/competition/')
    mail_input = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="basic_email"]'))
    )
    mail_input.send_keys(config['account']['mail'])
    
    password_input = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="basic_password"]'))
    )
    password_input.send_keys(config['account']['password'])
    
    checkbox_button = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="basic"]/div[4]/label/span[1]/input'))
    )
    checkbox_button.click()
    
    login_button = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="basic"]/div[5]/div/div/div/div/span/button'))
    )
    login_button.click()
    
    # 赛程选择界面
    enter_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/section/div[2]/div/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[2]/div/div/button'))
    )
    enter_button.click()
    time.sleep(2)
    return driver
    

def select_bar(driver, bar_name="集群训练"):
    assert bar_name in ['集群训练', '模型管理', '模型评估', '比赛测评', '我的团队', '比赛成绩'], '请检查栏目名称是否正确'
    left_bar = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/section/div/div/div/div/div[2]/div[1]/ul'))
    )
    left_bar_list = left_bar.find_elements(By.TAG_NAME, 'li')
    for left_bar_item in left_bar_list:
        if str(left_bar_item.find_element(By.XPATH, './span[2]').text).strip() == bar_name:
            left_bar_item.click()
            time.sleep(2)
            return driver


###### uploader
def upload_train_missions_one_page(config, driver):
    missions = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/section/div/div/div/div/div[2]/div[2]/div/div/div[2]/div/div'))
    )
    mission_list = missions.find_elements(By.XPATH, './div')
    for mission in mission_list:
        name = mission.find_element(By.XPATH, './div[1]/div[1]/div[1]/div/div/div/span').text
        
        model_list_button = mission.find_element(By.XPATH, './div[1]/div[2]/div/div/div[2]/button')
        model_list_button.click()
        time.sleep(2)
        
        # model_list_page = driver.find_element(By.CLASS_NAME, 'ant-drawer-wrapper-body')
        model_list_page = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ant-drawer-wrapper-body'))
        )

        # 提交每一个模型
        driver = submit_models(config, driver, model_list_page, name)

        quit_button = model_list_page.find_element(By.XPATH, './div[1]/div/button')
        quit_button.click()
        time.sleep(3)

    return driver


def upload_last_train_mission(config, driver):
    missions = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/section/div/div/div/div/div[2]/div[2]/div/div/div[2]/div/div'))
    )
    mission_list = missions.find_elements(By.XPATH, './div')
    mission = mission_list[0]
    name = mission.find_element(By.XPATH, './div[1]/div[1]/div[1]/div/div/div/span').text
    
    model_list_button = mission.find_element(By.XPATH, './div[1]/div[2]/div/div/div[2]/button')
    model_list_button.click()
    time.sleep(2)
    
    # model_list_page = driver.find_element(By.CLASS_NAME, 'ant-drawer-wrapper-body')
    model_list_page = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'ant-drawer-wrapper-body'))
    )

    # 提交每一个模型
    driver = submit_models(config, driver, model_list_page, name)

    quit_button = model_list_page.find_element(By.XPATH, './div[1]/div/button')
    quit_button.click()
    time.sleep(3)

    return driver



def submit_models(config, driver, model_list_page, name):
    models = model_list_page.find_element(By.CLASS_NAME, 'ant-table-tbody')
    model_list = models.find_elements(By.XPATH, ".//tr[contains(@class, 'ant-table-row')]")
    for model in model_list:
        # 模型训练时间
        model_train_time = model.find_element(By.XPATH, './td[1]/div/span').text
        model_train_time = model_train_time.split('min')[0] + 'm'
        
        # 过滤小于2小时的模型
        if 'h' not in model_train_time or int(model_train_time.split('h')[0]) < int(config['upload_filter']):
            continue
        
        submit_to_model_manager_button = model.find_element(By.XPATH, "./td[4]/div/div/div[2]/button")
        submit_to_model_manager_button.click()
        time.sleep(2)

        pages = driver.find_elements(By.CLASS_NAME, 'ant-drawer-wrapper-body')
        assert len(pages) == 2, '“提交模型管理”出错'
        model_manager_page = pages[-1]
        
        model_name_input = model_manager_page.find_element(By.XPATH, ".//input[@id='name']")
        model_name_input.send_keys(f"{name}-{model_train_time}")

        submit_button = model_manager_page.find_element(By.XPATH, './div[2]/form/div/div[2]/div/div[1]/button')
        submit_button.click()
        time.sleep(1)

        # notice = driver.find_element(By.CLASS_NAME, 'ant-message-notice-content')
        notice = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ant-message-notice-content'))
        )
        
        keep_this_page = notice.find_element(By.XPATH, ".//button")
        keep_this_page.click()
        time.sleep(2)

        # 自动退出，无需手动按关闭
        # quit_button = model_manager_page.find_element(By.XPATH, './div[1]/div/button')
        # quit_button.click()
        # time.sleep(2)
    
    return driver



##### evaler
def eval_models_one_page(config, driver, filter_re=None):
    models = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/section/div/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/table/tbody'))
    )
    model_list = models.find_elements(By.XPATH, "./tr[contains(@class, 'ant-table-row')]")
    for model in model_list:
        # 只有检测成功才继续
        succ_status = model.find_element(By.XPATH, './td[1]/div/div[2]/div/span/span').text
        if succ_status.strip() != "检测成功":
            continue
        
        model_name = model.find_element(By.XPATH, './td[1]/div/div[1]').text
        # model_name = f"{model_name.split('-')[0]}{model_name.split('-')[1]}"
        
        if filter_re is not None:
            if not re.match(filter_re, model_name):
                continue
        
        add_eval_button = model.find_element(By.XPATH, './td[12]/div/div/div[1]/button')
        add_eval_button.click()
        time.sleep(1)
        
        add_eval_page = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ant-drawer-wrapper-body'))
        )
        eval_mission_name_input = add_eval_page.find_element(By.XPATH, '//*[@id="name"]')
        eval_mission_name_input.send_keys(f"{model_name}-{config['opponent_model']}")
        
        # 阵营A英雄选择
        camp_A_lineup_input = add_eval_page.find_element(By.XPATH, "./div[2]/form/div/div[1]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div/div[4]/div/div[2]/div/div/span/div")
        camp_A_lineup_input.click()
        time.sleep(1)
        camp_A_lineup_selector_page = camp_A_lineup_input.find_element(By.XPATH, './div/div[2]/div/div/div/div[2]/div/div/div')
        driver = hero_selector(driver, camp_A_lineup_selector_page)
        camp_A_lineup_input.click()
        time.sleep(1)
        
        
        # 阵营B模型选择
        camp_B_model_input = add_eval_page.find_element(By.XPATH, './div[2]/form/div/div[1]/div[3]/div/div[2]/div/div/div/div[1]/div/div/div/div/div/div[1]/div/span/div')
        camp_B_model_input.click()
        time.sleep(1)
        model_B_model_selector_page = add_eval_page.find_element(By.XPATH, "./div[2]/form/div/div[1]/div[3]/div/div[2]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div[contains(@class, 'ant-select-dropdown')]")
        driver = model_selector(driver, model_B_model_selector_page, config['opponent_model'])
        
      
        # 阵营B英雄选择
        camp_B_lineup_input = add_eval_page.find_element(By.XPATH, './div[2]/form/div/div[1]/div[3]/div/div[2]/div/div/div/div[2]/div/div/div/div/div[4]/div/div[2]/div/div/span/div')
        camp_B_lineup_input.click()
        time.sleep(1)
        camp_B_lineup_selector_page = camp_B_lineup_input.find_element(By.XPATH, './div/div[2]/div/div/div/div[2]/div/div/div')
        driver = hero_selector(driver, camp_B_lineup_selector_page)
        camp_B_lineup_input.click()
        time.sleep(1)
        
        # 对局数量
        eval_turn_input = add_eval_page.find_element(By.XPATH, './div[2]/form/div/div[1]/div[5]/div/div[2]/div/div/div/div/div/div/div/p/div/div[2]/input')
        eval_turn_input.send_keys(config['eval_turn'])
        
        # 提交
        submit_button = add_eval_page.find_element(By.XPATH, './div[2]/form/div/div[2]/div/div[1]/button')
        submit_button.click()
        time.sleep(1)
        
        notice = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ant-message-notice-content'))
        )
        
        keep_this_page = notice.find_element(By.XPATH, ".//button")
        keep_this_page.click()
        time.sleep(2)
        
        # 无需手动退出        
        # /html/body/div[4]/div/div[3]/div/div/div[1]/div/button
        # quit_button = add_eval_page.find_element(By.XPATH, './div[1]/div/button')
        # quit_button.click()
        # time.sleep(2)
        
    return driver


def eval_models_range(config, driver, name: str, maxh: int, minh: int, page=5):
    # 查询一个模型在训练时间minh~maxh之间的所有存档点，提交评估
    # name是‘-’之前的字符串
    assert minh < maxh, '调整minh、maxh'

    name_re = f'{name}'
    range_re = "|".join([f'{i}' for i in range(minh, maxh + 1)])
    filter_re = f"{name_re}-({range_re})h\d+"
    
    for current_page_no in range(1, page+1):
        driver = eval_models_one_page(config, driver, filter_re=filter_re)
        
        # 翻页
        next_page = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//li[contains(@title,"下一页")]'))
        )
        next_page.click()
        time.sleep(1)
 
        
    return driver    


def hero_selector(driver, selector_page):
    hero_list = selector_page.find_elements(By.XPATH, "./div[contains(@class, 'ant-select-item')]")
    for hero in hero_list:
        check_button = hero.find_element(By.XPATH, './span/label/span/input')
        check_button.click()
        time.sleep(0.5)
    return driver    


def model_selector(driver, search_element, model_name):
    search_bar_input = search_element.find_element(By.XPATH, './div/div/div[1]/span/input')
    search_bar_input.send_keys(model_name)
    time.sleep(1)
    
    models_available = search_element.find_element(By.XPATH, './div/div/div[2]/div[3]/div/div/div')
    model_available_list = models_available.find_elements(By.XPATH, "./div[contains(@class, 'ant-select-item')]")

    model_wanted = model_available_list[0]
    model_wanted.click()
    time.sleep(1)
    
    return driver


