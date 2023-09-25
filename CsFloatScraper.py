from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from lxml import etree
from ItemInfo import ItemInfo
import time, random



class CsFloatScraper:
    def get_item_info(self, item_info: ItemInfo, driver):
        float_input = driver.find_element(by=By.ID, value="mat-input-1")

        float_input.clear()
        float_input.send_keys(item_info.inspect_url)

        time.sleep(1 + random.random())

        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')
        dom = etree.HTML(str(soup))

        float_value = dom.xpath('/html/body/app-root/div/div[2]/app-checker-home/div/div/app-checker-item/mat-card/item-float-bar/div/div[1]/span/span')[0].text
        pattern_value =  dom.xpath('/html/body/app-root/div/div[2]/app-checker-home/div/div/app-checker-item/mat-card/div/div/div[2]/div[1]/text()')[0]
        item_info.float = float_value
        item_info.pattern = pattern_value.replace(" ", "")


        




