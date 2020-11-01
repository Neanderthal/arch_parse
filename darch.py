# This is a sample Python script.
import argparse
from os import path

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests


LOGIN_PAGE = "https://spbarchives.ru/home?p_p_id=com_liferay_login_web_portlet_LoginPortlet&p_p_lifecycle=1&p_p_state=maximized&p_p_mode=view&refererPlid=20809&_com_liferay_login_web_portlet_LoginPortlet_javax.portlet.action=%2Flogin-esia-request&_com_liferay_login_web_portlet_LoginPortlet_mvcRenderCommandName=%2Flogin%2Flogin&saveLastPath=false&p_auth=jDtfIaa5"
DELAY = 10
PATH = "."


def use(login_page, login, password, archive_url, dir_path):
    # Use a breakpoint in the code line below to debug your script.
    driver = webdriver.Firefox()
    driver.get(login_page)

    enter_button = driver.find_element_by_link_text("Вход через ЕСИА")
    res = enter_button.click()
    login_input = driver.find_element_by_id("mobileOrEmail")

    login_input.send_keys(login)

    password_input = driver.find_element_by_id("password")
    password_input.send_keys(password)

    login_button = driver.find_element_by_id("loginByPwdButton")

    login_button.click()
    WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.site-title')))
    driver.get(archive_url)

    WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.previewPage>img')))
    images = driver.find_elements_by_css_selector("div.previewPage>img")

    urls = [image.get_attribute("src") for image in images]
    modified_urls = [url.replace("VIEW", "IMAGE") for url in urls]
    cookies = {item["name"]: item["value"] for item in driver.get_cookies()}

    for number, url in enumerate(modified_urls):
        response = requests.get(url, cookies=cookies)
        file_path = path.join(dir_path, f'img_{number}.jpeg')
        with open(file_path, 'wb') as f:
            f.write(response.content)
            print(f"File saved - {file_path}")
            
    driver.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ARCHIVE_URL = "https://spbarchives.ru/infres?p_p_id=archiveStorePortlet&p_p_lifecycle=0&p_p_state=exclusive&p_p_mode=view&_archiveStorePortlet_mvcRenderCommandName=%2Fimagenavigator&_archiveStorePortlet_entityKind=Unit&_archiveStorePortlet_archiveAbbr=cgali&_archiveStorePortlet_entityId=112517"

    cli = argparse.ArgumentParser(description='''Download images from spbarchives.ru
     Installed firefox required
     Download and install geckodriver from this page https://github.com/mozilla/geckodriver/releases/tag/v0.27.0 for you OS first''')
    cli.add_argument('--login', '-l', required=True, type=str, help='LOGIN')
    cli.add_argument('--password', '-p', required=True, type=str, help='password')
    cli.add_argument('--url', '-u', type=str, required=True, help='URL to download')
    cli.add_argument('--dir', '-d', type=str, required=True, help='path to save files')
    cli.add_argument('--login_page', '-i', type=str, required=False, help='URL to login page')
    args = cli.parse_args()
    login_page = args.login_page if args.login_page else LOGIN_PAGE
    use(login_page, args.login, args.password, args.url, args.dir)
