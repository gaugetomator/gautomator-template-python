from appium.webdriver.common.appiumby import AppiumBy

from gautomator.factory.driver_factory import LocatorModify
from gautomator.const.custom_exception import DriverAppError
from base.mobile_base import CommonMobileBase


class CalculatorLocators():
    locators = {
        "name_btn": ("XPATH", '//XCUIElementTypeButton[@name="%(name)s"]', AppiumBy.XPATH),
        "display_screen": ("XPATH", '//*[contains(@value,"%(input)s")]//following-sibling::XCUIElementTypeStaticText', AppiumBy.XPATH),
    }


class Calculator(CommonMobileBase):
    def __init__(self, driver):
        LocatorModify.set_locators(
            CalculatorLocators.locators, self.IS_DISTINCT)
        super().__init__(driver)
        self.mapping = {
            'x': 'X',
            ':': '/',
            '+': '+',
            '-': '-'
        }
    """
        Action
    """

    def click_btn(self, btn_name: str):
        if str(btn_name).isnumeric():
            for n in btn_name:
                self.click_element(locator_name="name_btn", value={'name': n})
        elif btn_name in ('x', '-', '+', ':'):
            self.click_element(locator_name="name_btn", value={
                               'name': self.mapping[btn_name]})
        else:
            raise DriverAppError(
                f'Do not support btn {btn_name} in Calculator app.')

    def get_result(self):
        self.click_element(locator_name="name_btn", value={'name': '='})

    """
        Verify
    """

    def verify_result(self, expected_result: str, f_num, s_num, method):
        self.assert_equal(self.get_text_from_element(
            locator_name='display_screen', value={'input': f'{f_num}{method}{s_num}'}), expected_result)
