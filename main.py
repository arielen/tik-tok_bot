import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from config import vk_phone, vk_password


def tiktok_auth(url):
    options = webdriver.FirefoxOptions()
    options.set_preference(
        'general.useragent.override',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'
    )
    options.set_preference('dom.webdriver.enabled', False)
    driver = webdriver.Firefox(
        executable_path='firefoxdriver/geckodriver.exe',
        options=options
    )

    # check xpath
    def xpath_exists(xpath):
        try:
            driver.find_element_by_xpath(xpath)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    try:
        driver.get(url=url)
        time.sleep(5)

        driver.find_element_by_class_name('login-button').click()
        time.sleep(5)
        # switch to iframe
        iframe = driver.find_element_by_xpath('//iframe[@class="jsx-2873455137"]')
        driver.switch_to.frame(iframe)
        time.sleep(5)

        if xpath_exists('//div[contains(text(), "VK")]'):
            driver.find_element_by_xpath('//div[contains(text(), "VK")]').click()
            time.sleep(5)
        elif xpath_exists('//div[contains(text(), "ВК")]'):
            driver.find_element_by_xpath('//div[contains(text(), "ВК")]').click()
            time.sleep(5)

        driver.switch_to.window(driver.window_handles[1])  # переключаемся на новое окно с вводом пароля
        time.sleep(5)

        email_input = driver.find_element_by_name('email')
        email_input.clear()
        email_input.send_keys(vk_phone)
        time.sleep(5)

        password_input = driver.find_element_by_name('pass')
        password_input.clear()
        password_input.send_keys(vk_password, Keys.ENTER)
        time.sleep(15)

        driver.switch_to.window(driver.window_handles[0])  # переключаемся к основному окну

        following_button = driver.find_element_by_xpath(
            '//*[@id="main"]/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/a[2]'
        ).click()
        time.sleep(5)


    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def main():
    tiktok_auth('https://www.tiktok.com/')


if __name__ == '__main__':
    main()
