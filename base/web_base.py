import math

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from gautomator.const.common import EnvConst, EmojiCodeConst, TimeConst
from gautomator.factory.driver_factory.selenium import LocatorModify
from gautomator.utils.common import logger, GetUtil, StringUtil, TimeUtil, find_tuple
from .common import CommonBase


class CommonWebBase(CommonBase):
    TIMEOUT = TimeConst.Timeout.TIMEOUT_10
    def __init__(self, driver, timeout=None):
        super().__init__(driver, timeout=self.TIMEOUT if not timeout else timeout)
        LocatorModify.set_locators(self._common_locators)

    _common_locators = {
        'textLabel': ('XPATH', '//*[text()="%(text)s"]', By.XPATH),
        'promptAlert': ('LINK_TEXT', '"%(alert_text)s"', By.LINK_TEXT),
        'loadingIcon': ('XPATH', '//div[@class="loading-rocket "]', By.XPATH)
    }

    """ Action functions"""

    def scroll_up_by_press_key(self):
        logger.info("Action: Press key: Page Up")
        self.press_key(Keys.PAGE_UP)

    def clear_all_browser_cookies(self):
        logger.info("Action: Clear browser cookies")
        self.clear_browser_cookies()

    def navigate_back_browser(self):
        self.navigate_back()

    def go_to_base_url(self):
        self.go_to_url(url=GetUtil.suite_get(
            keyword=EnvConst.Environment.ENV_OBJ).base_url)

    def go_to_url(self, url: str = None):
        self.navigate_to_url(url)

    @staticmethod
    def get_element_main_color(element: WebElement):
        background_color = element.value_of_css_property("background-color")
        try:
            color_hex = eval(background_color.split('rgba')[1])
            return find_tuple(color_hex[0:3])
        except:
            color_hex = eval(background_color.split('rgb')[1])
            return find_tuple(color_hex)

    @staticmethod
    def convert_icon_in_string(value: str):
        if ':' in value:
            text_icon = f":{value[value.find((start := ':')):].split(':')[1]}:"
            try:
                icon = EmojiCodeConst.key[text_icon]
                return value.replace(text_icon, icon)
            except Exception as err:
                logger.debug(f"No have icon with text: {value}\n{err}")
                return value
        else:
            return value

    def switch_window_by_id(self, window_id=1):
        logger.info('Action: Switch to new tab')
        self.switch_window(window_id=window_id)

    def switch_to_latest_window(self):
        logger.info('Action: Switch to latest tab')
        window_id = len(self.get_window_handles()) - 1
        self.switch_window_by_id(window_id=window_id)

    def switch_to_tab(self, window_id: int = 0):
        logger.info('Action: Switch to default tab')
        self.switch_window(window_id=window_id)

    def close_latest_tab(self):
        self.switch_to_latest_window()
        self.close_drive()
        self.switch_to_tab()

    def close_other_tab(self):
        while len(self.get_window_handles()) > 1:
            self.close_latest_tab()

    def wait_page_load_complete(self, timeout: int = TimeConst.Timeout.TIMEOUT_10):
        self.is_element_gone(locator_name='loadingIcon', timeout=timeout)

    def get_header_index(self, header_locator_nm, timeout: int = TimeConst.Timeout.TIMEOUT_10):
        headers = {}
        table_list_header: list[WebElement] = self.find_elements(
            locator_name=header_locator_nm, timeout=timeout)
        for header in table_list_header:
            value = StringUtil.remove_all_except_text(
                header.text.split("\n")[0])
            if not value:
                continue
            headers[value] = [header, table_list_header.index(header) + 1]
        return headers

    def get_total_pages(self, total_records_locator_nm, selected_paging_locator_nm):
        return math.ceil(int(self.get_text_from_element(locator_name=total_records_locator_nm)) / int(self.get_text_from_element(locator_name=selected_paging_locator_nm)))

    def get_row_detail(self, header_locator_nm, table_rows_locator_nm, table_col_by_number_locator_nm, total_pages: int = 1, next_locator_nm: str = None, timeout: int = TimeConst.Timeout.TIMEOUT_10):
        headers = self.get_header_index(
            header_locator_nm=header_locator_nm, timeout=timeout)
        details = {}
        row_index = 0
        for page in range(total_pages):
            rows = self.find_elements(
                locator_name=table_rows_locator_nm, timeout=timeout)
            if rows:
                for row in rows:
                    tmp = {}
                    for header, index in headers.items():
                        header_element = index[0]
                        col_number = index[1]
                        self.scroll_to_view_element(element=header_element)
                        tmp[header] = self.find_element_inside_element(
                            element=row, locator_name=table_col_by_number_locator_nm, value={'col_number': col_number}).text
                    details[row_index] = tmp
                    row_index += 1
                if total_pages > 1 and page < total_pages:
                    self.click_element(locator_name=next_locator_nm)
                    TimeUtil.short_sleep(sleep_tm=TimeConst.Timeout.TIMEOUT_2)
            else:
                logger.info("No record found.")

        return details

    """ Verify functions"""

    def verify_dropdown_list_is_displayed(self, expected_value_nm: str, dropdown_locator_nm: str):
        actual_elements: list[WebElement] = self.find_elements(
            locator_name=dropdown_locator_nm)
        values = []
        for ele in actual_elements:
            values.append(ele.text)
        self.assert_equal(expected_value=expected_value_nm,
                          actual_value=values)
