from .web_example import WebSample
from getgauge.python import step

from gautomator.const.common import EnvConst

from gautomator.utils.common import GetUtil


@step('[Web][Google] Verify button display')
def step_imp():
    p = WebSample(GetUtil.suite_get(EnvConst.Driver.WEB_DRIVER).get('google'))
    p.verify_btn_display()
