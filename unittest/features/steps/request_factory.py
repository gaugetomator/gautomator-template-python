from behave import *

from gautomator.factory.request_factory import RequestFactory

from gautomator.utils.common import AssertUtil


@Given('a request factory')
def step_imp(context):
    context.factory = RequestFactory


@When('sending a {request} to factory')
def step_imp(context, request):
    context.request = context.factory.create_request(request)


@then('new object will be generated')
def step_imp(context):
    AssertUtil.true(context.request)
