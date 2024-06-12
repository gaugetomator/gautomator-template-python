from gautomator.model.request import RequestObjModel

from behave import *


@given('a request Model')
def step_imp(context):
    context.request = RequestObjModel()


@then('verify {key} {value} created')
def step_imp(context, key, value):
    setattr(context.request, key, value)


@when('init {key} {value} to object')
def step_imp(context, key, value):
    assert getattr(context.request, key) == value
