from gautomator.utils.common import TimeUtil
from base import CommonWebBase


class Common(CommonWebBase):
    def __init__(self, driver):
        super().__init__(driver)

    """Action"""

    def clear_cache(self):
        self._driver.execute_cdp_cmd('Storage.clearDataForOrigin', {
            "origin": '*',
            "storageTypes": 'all',
        })
        TimeUtil.short_sleep(2)
        self.refresh_page()
        self.wait_until_page_is_load_complete()

    """Validation"""
