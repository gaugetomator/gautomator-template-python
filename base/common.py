from gautomator.factory.driver_factory.selenium import SeleniumActions
from gautomator.factory.driver_factory.appium.appium_actions import AppiumActions
from gautomator.utils.common import AssertUtil, MultiAssertsUtil


class CommonBase(SeleniumActions, AssertUtil, MultiAssertsUtil, AppiumActions):

    def __init__(self, driver, timeout=None):
        super().__init__(driver, timeout=timeout)
        SeleniumActions.__init__(self, driver=driver, timeout=timeout)
        AppiumActions.__init__(self, driver=driver)
        AssertUtil.__init__(self)
        MultiAssertsUtil.__init__(self)

