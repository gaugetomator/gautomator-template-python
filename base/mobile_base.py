from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webelement import WebElement

from gautomator.const.common import StringConst, common_const, EnvConst
from gautomator.const.mobile import CapabilitiesConst
from .common import CommonBase
from gautomator.utils.common import logger, PathUtil, StringUtil, StoreUtil, TimeUtil, GetUtil, JsonConverterUtil
from gautomator.factory.driver_factory import LocatorModify, AppHelper
from android.const import UserConst


class FunctionKeys:
    PASTE = "Dán"
    COPY = "Sao chép"
    CUT = "Cắt"


class CommonMobileBase(CommonBase):
    IS_DISTINCT = False

    def __init__(self, driver):
        LocatorModify.set_locators(locators_dict=self._locators, is_distinct_locator=self.IS_DISTINCT)
        super().__init__(driver)

    _locators = {
        # find ele by accessibility id
        "locatorByAccId": ("ACCESSIBILITY_ID", "%(value)s", AppiumBy.ACCESSIBILITY_ID),

        # find ele by xpath
        "locatorByContentDesc": ("XPATH", '//*[contains(@content-desc,"%(value)s")]', AppiumBy.XPATH),
        "locatorByHint": ("XPATH", '//*[contains(@hint,"%(value)s")]', AppiumBy.XPATH),
        "locatorByText": ("XPATH", '//*[contains(@text,"%(value)s")]', AppiumBy.XPATH),

        # common button
        "continueButton": ("ACCESSIBILITY_ID", "Tiếp tục", AppiumBy.ACCESSIBILITY_ID),
        "closeButton": ("ACCESSIBILITY_ID", 'Đóng', AppiumBy.ACCESSIBILITY_ID),
        "loginButton": ("ACCESSIBILITY_ID", "Đăng nhập", AppiumBy.ACCESSIBILITY_ID),
        "tryAgainButton": ("ACCESSIBILITY_ID", "Thử lại", AppiumBy.ACCESSIBILITY_ID),
        "backAgainButton": ("ACCESSIBILITY_ID", "Quay lại", AppiumBy.ACCESSIBILITY_ID),
        "reSendButton": ("ACCESSIBILITY_ID", "Gửi lại", AppiumBy.ACCESSIBILITY_ID),
        "acceptButton": ("ACCESSIBILITY_ID", "Đồng ý", AppiumBy.ACCESSIBILITY_ID),
        "newTransactionButton": ("ACCESSIBILITY_ID", "Giao dịch mới", AppiumBy.ACCESSIBILITY_ID),
        "cancelButton": ("ACCESSIBILITY_ID", "Hủy giao dịch", AppiumBy.ACCESSIBILITY_ID),
        "backHomeButton": ("ACCESSIBILITY_ID", "Về trang chủ", AppiumBy.ACCESSIBILITY_ID),
    }

    """
    Actions
    """
    @staticmethod
    def active_app():
        app_package = GetUtil.suite_get(EnvConst.Environment.CONFIG_APP_OBJ).get(CapabilitiesConst.APP_PACKAGE)
        AppHelper(GetUtil.suite_get(EnvConst.Driver.MOBILE_DRIVER)).activate_app(app_id=app_package)

    @staticmethod
    def set_permission():
        app_package = GetUtil.suite_get(EnvConst.Environment.CONFIG_APP_OBJ).get(CapabilitiesConst.APP_PACKAGE)
        AppHelper(GetUtil.suite_get(EnvConst.Driver.MOBILE_DRIVER)).set_permission(permissions="all", app_id=app_package)
        
    @staticmethod
    def terminate_app():
        app_package = GetUtil.suite_get(EnvConst.Environment.CONFIG_APP_OBJ).get(CapabilitiesConst.APP_PACKAGE)
        AppHelper(GetUtil.suite_get(EnvConst.Driver.MOBILE_DRIVER)).terminate_app(app_id=app_package)

    @staticmethod
    def clear_app():
        app_package = GetUtil.suite_get(EnvConst.Environment.CONFIG_APP_OBJ).get(CapabilitiesConst.APP_PACKAGE)
        AppHelper(GetUtil.suite_get(EnvConst.Driver.MOBILE_DRIVER)).clear_app(app_id=app_package)

    def screenshot_ele(self, file_name: str, **kwargs):
        """
        Screenshot an element and save image to file
        :param file_name:
        :return:
        """
        ele: WebElement = kwargs.get("element") if kwargs.get("element") \
            else self.find_element(locator_name=kwargs.get("locator_name"))
        logger.info("Action: Screen shot element ")
        ele.screenshot(filename=PathUtil.join_prj_root_path(f'screenshot_{file_name}'))

    def paste_text_into_ele(self, locator_name: str, text: str, **kwargs):
        self.driver.set_clipboard_text(text=text)
        self.long_click_gesture(locator_name=locator_name, value=kwargs.get("value"))
        self.click_gesture(locator_name="locatorByAccId", value={"value": FunctionKeys.PASTE})

    def paste_password_into_ele(self, locator_name: str, encoded_password: str, **kwargs):
        self.driver.set_clipboard_text(text=StringUtil.base64_decode_text(encoded_data=encoded_password))
        self.long_click_gesture(locator_name=locator_name, value=kwargs.get("value"))
        self.click_gesture(locator_name="locatorByAccId", value={"value": FunctionKeys.PASTE})

    def type_text_into_ele(self, locator_name: str, text: str, **kwargs):
        self.click_gesture(locator_name=locator_name, value=kwargs.get("value"))
        self.send_value(locator_name=locator_name, text=text, value=kwargs.get("value"))

    def type_password_into_ele(self, locator_name: str, password: str, is_raw_pass: bool = False, **kwargs):
        self.click_gesture(locator_name=locator_name, value=kwargs.get("value"))
        if is_raw_pass:
            self.send_value(locator_name=locator_name, text=password, value=kwargs.get("value"))
        else:
            self.send_value(locator_name=locator_name, text=StringUtil.base64_decode_text(encoded_data=password),
                            value=kwargs.get("value"))

    def get_content_decs(self, locator_name: str, **kwargs):
        return self.get_attribute(locator_name=locator_name, attr_mn="content-desc", value=kwargs.get("value"))

    def hide_keyboard(self):
        self.driver.hide_keyboard()

    def is_checked(self, locator_name: str):
        return True if self.get_attribute(locator_name=locator_name, attr_mn="checked") == common_const.CommonTypeUsageConst.TRUE else False

    @staticmethod
    def generate_password(length: int):
        pwd = StringUtil.generate_random_pwd(length=length)
        logger.info(f"Password: {pwd}")
        StoreUtil.scenario_store(keyword=UserConst.PASSWORD, data=pwd)
        return pwd

    @staticmethod
    def wait_time(time: int):
        TimeUtil.sleep(time)

    """
    Validations
    """

    def verify_ele_is_empty_str(self, locator_name: str, **kwargs):
        self.equal(expected_value=StringConst.EMPTY_STRING,
                   actual_value=self.get_text_from_element(locator_name=locator_name, value=kwargs.get("value")))

    def verify_password_is_encrypted(self, locator_name: str, encoded_password: str, **kwargs):
        decode_password = StringUtil.base64_decode_text(encoded_data=encoded_password)
        self.equal(expected_value="•" * len(decode_password),
                   actual_value=self.get_text_from_element(locator_name=locator_name,
                                                           value=kwargs.get("value")))

    def verify_password_is_decrypted(self, locator_name: str, encoded_password: str, **kwargs):
        self.equal(expected_value=StringUtil.base64_decode_text(encoded_data=encoded_password),
                   actual_value=self.get_text_from_element(locator_name=locator_name,
                                                           value=kwargs.get("value")))

    def verify_text_of_ele(self, locator_name: str, expected_rs: str, **kwargs):
        self.equal(expected_value=expected_rs,
                   actual_value=self.get_text_from_element(locator_name=locator_name,
                                                           value=kwargs.get("value")))

    def verify_length_of_texbox(self, locator_name: str, expected_length: int, **kwargs):
        self.equal(expected_value=expected_length,
                   actual_value=len(self.get_text_from_element(locator_name=locator_name,
                                                               value=kwargs.get("value"))))

    def verify_list_acc_ids_are_displayed(self, acc_ids: any):
        for acc_id in acc_ids:
            print(f"acc_id: {acc_id}")
            self.true(self.is_element_displayed(locator_name="locatorByAccId", value={"value": acc_id}))