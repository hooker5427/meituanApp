import time
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

#  夜深模拟器的配置

cap = {
    "platformName": "Android",
    "platformVersion": "5.1.1",
    "deviceName": "127.0.0.1:62001",
    "appPackage": "com.sankuai.meituan",
    "appActivity": "com.sankuai.meituan.activity.MainActivity",
    "automationName": "UiAutomator1",
    'unicodeKeyboard': True,  # 中文问题
    "resetKeyboard": True,
    "noReset": True
}

print("正在打开app")
driver = webdriver.Remote("http://localhost:4723/wd/hub", cap)
wait = WebDriverWait(driver, 5)

def get_size():
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return (x, y)


l = get_size()
width = l[0]
height = l[1]


def crawk_one_city(city='北京'):
    try:
        default_city = None
        if wait.until(lambda x: x.find_element_by_xpath(
                "//android.widget.Button[@resource-id='com.sankuai.meituan:id/city_button']")):
            default_city = driver.find_element_by_xpath(
                "//android.widget.Button[@resource-id='com.sankuai.meituan:id/city_button']").text.strip()

        print(f"默认选中的城市是{default_city}")

        if default_city != city:
            driver.find_element_by_xpath(
                "//android.widget.Button[@resource-id='com.sankuai.meituan:id/city_button']").click()

            if wait.until(lambda x: x.find_element_by_xpath(
                    "//android.widget.LinearLayout[@resource-id='com.sankuai.meituan:id/city_container']")):

                list1 = driver.find_elements_by_xpath(
                    '//android.widget.LinearLayout[@resource-id=\'com.sankuai.meituan:id/city_container\']//android.widget.TextView')

                if default_city.find(city) != -1:
                    print("切换都全程")

                    if wait.until(lambda x: x.find_elements_by_xpath(
                            "//android.widget.LinearLayout[@resource-id='com.sankuai.meituan:id/area_container']/android.widget.LinearLayout[1]//android.widget.TextView")):
                        textlist = driver.find_elements_by_xpath(
                            "//android.widget.LinearLayout[@resource-id='com.sankuai.meituan:id/area_container']/android.widget.LinearLayout[1]//android.widget.TextView")
                        textlist[0].click()
                else:
                    print("切换城市")
                    list1[-1].click()
                    if wait.until(
                            lambda x: x.find_element_by_xpath(
                                '//android.widget.EditText[@resource-id="com.sankuai.meituan:id/citylist_search"]')
                    ):
                        input_search = driver.find_element_by_xpath(
                            '//android.widget.EditText[@resource-id="com.sankuai.meituan:id/citylist_search"]')
                        input_search.send_keys(str(city))
                        time.sleep(1)
                        if len(driver.find_elements_by_xpath(
                                "//android.widget.ListView[@resource-id='android:id/list']//android.widget.TextView")) > 0:
                            ele = driver.find_elements_by_xpath(
                                "//android.widget.ListView[@resource-id='android:id/list']//android.widget.TextView")[0]
                            ele.click()
                            print(f"正在切换城市{ele.text}")
        else:
            pass
    except  Exception as e:
        print(e)
        pass

    try:
        if wait.until(lambda x: x.find_element_by_xpath(
                "//android.view.View[@resource-id='com.sankuai.meituan:id/category_layout']/android.widget.LinearLayout[1]")):
            print("点击美食")
            driver.find_element_by_xpath(
                "//android.view.View[@resource-id='com.sankuai.meituan:id/category_layout']/android.widget.LinearLayout[1]").click()
    except:
        pass

    try:
        if wait.until(lambda x: x.find_element_by_xpath(
                "//android.widget.Button[@resource-id='com.sankuai.meituan:id/category']")):
            driver.find_element_by_xpath(
                "//android.widget.Button[@resource-id='com.sankuai.meituan:id/category']").click()

        print("点击全部分类")
        if wait.until(lambda x: x.find_element_by_xpath("//android.widget.TextView[@text='全部分类']")):
            driver.find_element_by_xpath("//android.widget.TextView[@text='全部分类']").click()

        print("点击评价最高")
        if wait.until(
                lambda x: x.find_element_by_xpath(
                    "//android.widget.Button[@resource-id='com.sankuai.meituan:id/sort']")):
            driver.find_element_by_xpath("//android.widget.Button[@resource-id='com.sankuai.meituan:id/sort']").click()

        if wait.until(lambda x: x.find_element_by_xpath("//android.widget.TextView[@text='评价最高']")):
            driver.find_element_by_xpath("//android.widget.TextView[@text='评价最高']").click()

    except:
        pass

    print("crawl start ............")
    while True:
        l = get_size()
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.75)
        y2 = int(l[1] * 0.25)
        # 滑动操作
        while True:
            driver.swipe(x1, y1, x1, y2)
            time.sleep(0.5)
            print("正在下拉刷新....")


if __name__ == '__main__':
    # crawk_one_city( city= "上海")
    crawk_one_city(city="杭州")
