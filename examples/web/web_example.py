import re
from selenium.webdriver.common.by import By

from gautomator.factory.driver_factory.selenium.locator_modify_util import LocatorModify
from base.web_base import CommonWebBase


class WebSample(CommonWebBase):

    def __init__(self, driver):
        LocatorModify.set_locators(self.locators)
        super().__init__(driver)

    locators = {
        "searchTxtbox": ('NAME', 'q', By.NAME),
        "searchBtn": ('NAME', 'btnK', By.NAME),
        "feelGoodBtn": ('NAME', 'btnI', By.NAME),
        "resultTxt": ('XPATH', '//*[@id="Alh6id"]/div[1]/div', By.XPATH)
    }

    # def open_homepage(self, url):
    #     self.navigate_to_url(url=url)

    def search_text(self, txt: str):
        self.send_value(locator_name='searchTxtbox', text=txt)

    def verify_btn_display(self):
        self.assert_true(self.is_element_displayed(locator_name='feelGoodBtn'))
        self.assert_true(self.is_element_displayed(locator_name='searchBtn'))

    def verify_result(self):
        text = self.get_text_from_element(locator_name='resultTxt')
        self.assert_true(int(re.findall(r'\d+', text)[0]) > 0)
