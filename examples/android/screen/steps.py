from getgauge.python import step

from gautomator.const.common import EnvConst
from gautomator.utils.common import GetUtil
from examples.android.screen.actions import Calculator


@step('[Android][Calculator] Verify result from the <method> <f_num> <s_num>')
def step_imp(method, f_num, s_num):
    s_calculator = Calculator(GetUtil.suite_get(
        EnvConst.Driver.MOBILE_DRIVER))
    s_calculator.click_btn(f_num)
    s_calculator.click_btn(method)
    s_calculator.click_btn(s_num)


@step('Compare result <expected_result>')
def step_imp(expected_result):
    s_calculator = Calculator(GetUtil.suite_get(
        EnvConst.Driver.MOBILE_DRIVER))
    s_calculator.verify_result(expected_result)


@step('Get result')
def step_imp():
    s_calculator = Calculator(GetUtil.suite_get(
        EnvConst.Driver.MOBILE_DRIVER))
    s_calculator.get_result()


@step('[Android][Calculator] Set pwd')
def step_imp():
    s_calculator = Calculator(GetUtil.suite_get(
        EnvConst.Driver.MOBILE_DRIVER))
    s_calculator.acknowledge()
