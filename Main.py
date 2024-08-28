from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from autocorrect import Speller
from PIL import Image
import pytesseract
from nltk.corpus import wordnet
from datetime import datetime
from time import sleep

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
spell=Speller()

tiktok = "https://www.tiktok.com/"

Example_List = ["hearts", "views", "shares", "favorites"]

Tiktok_List = ["favorites", "views", "hearts"]

Classes_List = {"hearts": "btn.btn-primary.rounded-0.t-hearts-button", "views": "btn.btn-primary.rounded-0.t-views-button", "shares": "btn.btn-primary.rounded-0.t-shares-button", "favorites": "btn.btn-primary.rounded-0.t-favorites-button"}

Values_List = {"hearts": "body > div.col-sm-5.col-xs-12.p-1.container.t-hearts-menu > div > form > div > input", "views": "body > div.col-sm-5.col-xs-12.p-1.container.t-views-menu > div > form > div > input", "shares": "body > div.col-sm-5.col-xs-12.p-1.container.t-shares-menu > div > form > div > input", "favorites": "body > div.col-sm-5.col-xs-12.p-1.container.t-favorites-menu > div > form > div > input"}

Search_List = {"hearts": "body > div.col-sm-5.col-xs-12.p-1.container.t-hearts-menu > div > form > div > div > button", "views": "body > div.col-sm-5.col-xs-12.p-1.container.t-views-menu > div > form > div > div > button", "shares": "body > div.col-sm-5.col-xs-12.p-1.container.t-shares-menu.nonec > div > form > div > div > button", "favorites": "body > div.col-sm-5.col-xs-12.p-1.container.t-favorites-menu > div > form > div > div > button"}

Submit_List = {"hearts": "#c2VuZE9nb2xsb3dlcnNfdGlrdG9r > div.row.text-light.d-flex.justify-content-center > div > form > button", "views": "#c2VuZC9mb2xeb3dlcnNfdGlrdG9V > div.row.text-light.d-flex.justify-content-center > div > form > button", "shares": "", "favorites": "#c2VuZF9mb2xsb3dlcnNfdGlrdG9L > div.row.text-light.d-flex.justify-content-center > div > form > button"}


chrome_options = Options()
chrome_options.add_extension('adblocker.crx')

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://example.com")

while True:
    sleep(1)
    opentabs = driver.window_handles
    if len(opentabs)==2:
        driver.switch_to.window(driver.window_handles[1])
        sleep(2)
        driver.close()
        break

while True:
    driver.switch_to.window(driver.window_handles[0])
    sleep(1.5)
    driver.get("https://zefoy.com")
    screenshot_file = 'screenshot.png'
    while True:
        sleep(3)
        driver.get_screenshot_as_file(screenshot_file)

        print(f"Screenshot saved as {screenshot_file}")

        with Image.open('screenshot.png') as img:
            crop_rectangle = (465, 80, 835, 250)
            cropped_img = img.crop(crop_rectangle)
            cropped_img.save('cropped_screenshot.png')


        answer = str(pytesseract.image_to_string(Image.open("cropped_screenshot.png")).strip()).splitlines()[0].replace("'","").replace(" ","")
        print(answer)
        if wordnet.synsets(answer):
            break
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn.refresh-capthca-btn.fa.fa-refresh"))).click()
        
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME, "form-control.form-control-lg.text-center.rounded-0.remove-spaces"))).send_keys(answer)
    sleep(.5)
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn.btn-primary.btn-lg.btn-block.rounded-0.submit-captcha"))).click()

    sleep(3)

    for i in Tiktok_List:
        print(i)
        WebDriverWait(driver,1000).until(EC.element_to_be_clickable((By.CLASS_NAME, Classes_List[i]))).click()
        driver.execute_script("window.open('https://zefoy.com', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])
        sleep(2)
    times = datetime.now().strftime("%M")
    while True:
        for i, e in enumerate(Tiktok_List):
            print(i,e)
            driver.switch_to.window(driver.window_handles[i])
            result = driver.execute_script(f"""
                var selector = '{Values_List[e]}';
                var input = document.querySelector(selector);
                if (input) {{
                    input.value = '{tiktok}';
                    return 'Success';
                }} else {{
                    console.log('Input field not found.');
                    return 'Input field not found.';
                }}
            """)
            print(result)
            sleep(1)
            result = driver.execute_script(f"""
            var selector = '{Search_List[e]}';
            var element = document.querySelector(selector);
            if (element) {{
                element.click();
                return 'Clicked';
            }} else {{
                console.log('Element not found.');
                return 'Search not found.';
            }}""")
            print(result)
            sleep(1.5)
            result = driver.execute_script(f"""
            var selector = '{Submit_List[e]}';
            var element = document.querySelector(selector);
            if (element) {{
                element.click();
                return 'Clicked';
            }} else {{
                console.log('Element not found.');
                return 'No Sumbit Found';
            }}""")
            print(result)
        try:
            WebDriverWait(driver,.5).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn.refresh-capthca-btn.fa.fa-refresh")))
            for i, e in enumerate(Tiktok_List):
                for i, e in enumerate(Tiktok_List):
                    print(i,e)
                    driver.switch_to.window(driver.window_handles[i])
                    driver.close()
            break
        except:
            pass
