from gautomator.utils.backend import SwaggerUtil
from behave import *


@given('a swagger url')
def step_imp(context):
    context.url = ''


@when('call parser method')
def step_imp(context):
    SwaggerUtil.swagger_parser_factory()
