from appium.webdriver.common.appiumby import AppiumBy

from gautomator.factory.driver_factory import LocatorModify
from gautomator.const.custom_exception import DriverAppError
from base.mobile_base import CommonMobileBase


class CalculatorLocators():
    locators = {
        "num_btn": ("ID", "com.miui.calculator:id/digit_%(num)s", AppiumBy.ID),
        "function_btn": ("ID", "com.miui.calculator:id/op_%(ops)s", AppiumBy.ID),
        "accept_btn": ("ID", "android:id/button1", AppiumBy.ID),
        "display_screen": ("ID", "com.miui.calculator:id/expression", AppiumBy.ID),
        "equal_btn": ("ACCESSIBILITY_ID", "com.miui.calculator:id/btn_equal_s", AppiumBy.ACCESSIBILITY_ID)
    }


class Calculator(CommonMobileBase):
    def __init__(self, driver):
        LocatorModify.set_locators(
            CalculatorLocators.locators, self.IS_DISTINCT)
        # LocatorModify.set_locators(self.locators, self.IS_DISTINCT)
        super().__init__(driver)
        self.mapping = {
            'x': 'mul',
            ':': 'div',
            '+': 'add',
            '-': 'sub'
        }

    """
        Action
    """

    def click_btn(self, btn_name: str):
        if str(btn_name).isnumeric():
            for n in btn_name:
                self.click_element(locator_name="num_btn", value={'num': n})
        elif btn_name in ('x', '-', '+', ':'):
            self.click_element(locator_name="function_btn", value={
                               'ops': self.mapping[btn_name]})
        else:
            raise DriverAppError(
                f'Do not support btn {btn_name} in Calculator app.')

    def acknowledge(self):
        self.click_element(locator_name='accept_btn')

    def get_result(self):
        self.click_element(locator_name='equal_btn')

    """
        Verify
    """

    def verify_result(self, expected_result: str):
        self.assert_equal(self.get_text_from_element(
            locator_name='display_screen'), '= %s' % expected_result)
