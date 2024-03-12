import random  # 导入随机模块
import time  # 导入时间模块
from selenium import webdriver  # 导入浏览器驱动模块
from selenium.webdriver.common.by import By  # 导入定位元素方法
from selenium.webdriver.support.ui import WebDriverWait  # 导入等待页面加载模块
from selenium.webdriver.support import expected_conditions as EC  # 导入预期条件模块
from selenium.webdriver.common.action_chains import ActionChains  # 导入动作链模块

options = webdriver.ChromeOptions()  # 创建Chrome浏览器选项对象
options.add_argument('--incognito')  # 添加隐身模式参数

for _ in range(200):  # 外部循环，执行200次
    # 创建浏览器实例
    driver = webdriver.Chrome(options=options)  # 创建Chrome浏览器实例，并传入选项
    driver.maximize_window()  # 最大化浏览器窗口
    driver.get('https://www.wjx.cn/vm/your.aspx')  # 打开指定的网址

    # 单选题
    for i in [1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 15, 16]:  # 遍历单选题的题号
        # 随机选择单选题选项
        random.choice(driver.find_elements(By.XPATH, f'//*[@id="div{i}"]/div[2]/div/span')).click()

    # 多选题
    for i in range(7, 9):  # 遍历多选题的题号范围
        time.sleep(random.random())  # 随机等待一段时间
        checkboxs = driver.find_elements(By.XPATH, f'//*[@id="div{i}"]/div[2]/div/span')  # 定位多选题选项
        change_checkboxs = random.sample(  # 随机选择多选题选项
            checkboxs,
            random.choice(
                list(
                    range(
                        1, len(checkboxs) + 1
                    )
                )
            )
        )
        for check in change_checkboxs:  # 遍历选中的多选题选项
            check.click()  # 点击选项

    # 矩形单选题
    def click_random_element(driver, prefix, count):  # 定义一个函数用于点击矩形单选题的选项
        try:
            drv_dom = WebDriverWait(driver, 10).until(  # 等待元素加载完成
                EC.presence_of_element_located((By.ID, prefix + str(count)))
            )
            drv_array = drv_dom.find_elements(By.XPATH, '//*[@id="{}{}"]/td/a'.format(prefix, count))  # 定位选项
            if drv_array:  # 如果找到选项
                random_index = random.randint(0, len(drv_array) - 1)  # 随机选择一个选项
                action = ActionChains(driver)  # 创建动作链对象
                action.move_to_element(drv_array[random_index]).click().perform()  # 移动到选项并点击
                return True
            else:  # 如果未找到选项
                return False
        except Exception as e:  # 处理异常情况
            print("Exception:", e)  # 打印异常信息
            return False

    def process_elements(driver, prefix, max_count):  # 定义一个函数用于处理矩形单选题
        count = 1
        while count <= max_count and click_random_element(driver, prefix, count):  # 循环处理选项
            count += 1

    # 处理矩形单选题
    process_elements(driver, 'drv13_', 27)  # 处理drv13题目，最多27题
    process_elements(driver, 'drv14_', 27)  # 处理drv14题目，最多27题

    # 提交按钮
    random.choice(driver.find_elements(By.XPATH, f'//*[@id="ctlNext"]')).click()  # 随机点击提交按钮

    # 智检
    try:
        driver.find_element(By.XPATH, f'//*[@id="SM_BTN_1"]').click()  # 点击智检按钮
    except:
        pass

    time.sleep(3)  # 等待3秒

    driver.quit()  # 关闭浏览器
