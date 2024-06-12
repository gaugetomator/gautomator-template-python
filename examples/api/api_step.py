from .api_action import ApiExample
from gautomator.utils.common import AssertUtil
from gautomator.const.api import RequestConst

from getgauge.python import step


@step('[API][Find Pet by ID] Find id = <id>')
def step_imp(id):
    r = ApiExample().get_pet_by_id(id)
    verify = AssertUtil
    verify.equal(RequestConst.StatusCode.OK, r.status_code)
    verify.equal(r.response_data['id'], id, message='Return id as {r.response_data.id} instead of {id}')


@step('[API][Create new pet] Create new pet')
def step_imp():
    r = ApiExample().create_pet()
    verify = AssertUtil
    verify.equal(RequestConst.StatusCode.OK, r.status_code)
    verify.equal(r.response_data['name'], 'Sabertooth', 'Return name as {r.response_data.name} instead of Sabertooth')


@step('[API] Request with SOAP')
def step_imp():
    from gautomator.utils.common import logger
    r = ApiExample().get_with_soap()
    logger.info(r)