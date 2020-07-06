import time
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import re
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

re_num = re.compile("\d+")
#  夜深模拟器的配置
cap = {
    "platformName": "Android",
    "platformVersion": "5.1.1",
    "deviceName": "192.168.43.210:62001",
    "appPackage": "com.sankuai.meituan",
    "appActivity": "com.sankuai.meituan.activity.MainActivity",
    "automationName": "UiAutomator1",
    'unicodeKeyboard': True,  # 中文问题
    "resetKeyboard": True,
    "noReset": True
}

print("正在打开app")
driver = webdriver.Remote("http://localhost:4723/wd/hub", cap)
wait = WebDriverWait(driver, 10)


def get_size():
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return (x, y)


l = get_size()
width = l[0]
height = l[1]

if wait.until(
        lambda x: x.find_element_by_xpath("//android.widget.TextView[@resource-id='com.sankuai.meituan:id/nearby']")
):
    driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.sankuai.meituan:id/nearby']").click()

    try:
        if wait.until(
                lambda x: x.find_element_by_xpath("//android.widget.ListView[@resource-id='android:id/list']")
        ):
            print(len(driver.find_elements_by_xpath(
                "//android.widget.ListView[@resource-id='android:id/list']/android.widget.FrameLayout")))

            frist = True
            while True:

                list1 = driver.find_elements_by_xpath(
                    "//android.widget.ListView[@resource-id='android:id/list']/android.widget.FrameLayout")
                if frist:
                    list1 = list1[1:]
                    frist = False

                for item in list1:
                    shop_name = item.find_element_by_xpath(
                        "//android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.TextView").text.strip()
                    commemts_people = item.find_element_by_xpath(
                        "//android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.TextView[1]").text.strip()
                    cost_average = item.find_element_by_xpath(
                        "//android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.TextView[2]").text.strip()
                    tags_text = item.find_element_by_xpath(
                        "//android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[2]/android.widget.TextView[1]").text.strip()
                    tags = tags_text.split("/")
                    print(shop_name, commemts_people, cost_average, tags)
                    item.click()

                    if wait.until(
                            lambda x: x.find_element_by_xpath(
                                "//android.widget.TextView[@resource-id='com.sankuai.meituan:id/score_text']")
                    ):
                        stars_text = driver.find_element_by_xpath(
                            "//android.widget.TextView[@resource-id='com.sankuai.meituan:id/score_text']").text
                        stars = re_num.search(stars_text).group()
                        print(f" strts {stars}")

                        addr = driver.find_element_by_xpath(
                            "//android.widget.TextView[@resource-id='com.sankuai.meituan:id/addr']").text.strip()

                        services = driver.find_element_by_xpath(
                            "//android.widget.TextView[@resource-id='com.sankuai.meituan:id/service_content']").text.strip().split()

                        print(addr)
                        print(services)

                        if driver.find_element_by_xpath(
                                "//android.widget.ImageView[@resource-id='com.sankuai.meituan:id/phone']"):
                            phone_image = driver.find_element_by_xpath(
                                "//android.widget.ImageView[@resource-id='com.sankuai.meituan:id/phone']")
                            phone_image.click()

                            # //android.widget.TextView[@resource-id='android:id/text1' and @text='010-64959559']


                            if  wait.until(
                                 lambda  x :x.find_element_by_xpath("//android.widget.TextView")
                            ):
                                list2 = driver.find_elements_by_xpath("//android.widget.TextView")
                                p_list = []
                                if len( list2 ) ==1 :
                                    phone_text = driver.find_element_by_xpath(
                                        "//android.widget.TextView[@resource-id='android:id/message']").text.strip()
                                    p_list.append( phone_text )
                                    cancel_bt = driver.find_element_by_xpath(
                                        "//android.widget.Button[@resource-id='android:id/button2']")
                                    cancel_bt.click()
                                else :
                                    temp =None
                                    for  item  in list2 :
                                        phone = item.text
                                        p_list.append( phone )
                                        temp =  item
                                    temp.click()
                                    cancel_bt = driver.find_element_by_xpath(
                                        "//android.widget.Button[@resource-id='android:id/button2']")
                                    cancel_bt.click()
                                print ( p_list )
                            else:
                                print("没有找到联系电话")
                        else:
                            pass

                    driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='android:id/up']").click()

                x1 = int(l[0] * 0.5)
                y1 = int(l[1] * 0.75)
                y2 = int(l[1] * 0.25)

                driver.swipe(x1, y1, x1, y2)
                time.sleep(0.5)
                print("正在下拉刷新....")

    except TimeoutException:
        print("网速太卡")
    except NoSuchElementException as e:
        print(e, "没找到元素")
    except Exception as e:
        print(e)
        pass
