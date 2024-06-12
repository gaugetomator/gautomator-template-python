from gautomator.utils.common import StringUtil
from gautomator.utils.backend import RequestUtil

from gautomator.model import ResponseObjModel
from gautomator.const.api import RequestConst
from gautomator.factory.request_factory import RequestFactory


class ApiExample:

    def __init__(self):
        pass

    def get_pet_by_id(self, id) -> ResponseObjModel:
        data = RequestFactory().create_request(request_type=RequestConst.Method.GET)
        return RequestUtil.request(url=f'https://petstore.swagger.io/v2/pet/{id}', data=data)

    def create_pet(self, **kawags) -> ResponseObjModel:
        """_summary_
        using this obj to create new pet

        {
            "id": 0,
            "category": {
                "id": 0,
                "name": "string"
            },
            "name": "doggie",
            "photoUrls": [
                "string"
            ],
            "tags": [
                {
                "id": 0,
                "name": "string"
                }
            ],
            "status": "available"
        }

        Returns:
            _type_: ResponseObjModel
        """
        
        # preparing the data for body
        requested_data = {
            'id': StringUtil.generate_random_number(length=3),
            "category": {
                "id": StringUtil.generate_random_number(length=2),
                "name": StringUtil.generate_random_string()
            },
            "name": "Sabertooth",
            "tags": [
                {
                    "id": StringUtil.generate_random_number(length=2),
                    "name": StringUtil.generate_random_string()
                }
            ],
            "status": "available"
        }
        # execution
        params = RequestFactory.create_request(
            request_type=RequestConst.Method.POST, body=requested_data)
        return RequestUtil.request(url='https://petstore.swagger.io/v2/pet',
                                   data=params)


    def get_with_soap(self):
        """_summary_
        SOAP will use different content_type as text/xml; charset=utf-8
        the body will be formated as str
        """
        # requested_data = StringUtil.parse_xml_to_string('test.xml')
        # # execution
        # params = RequestFactory.create_request(request_type=RequestConst.Method.POST, 
        #                                        content_type=RequestConst.Header.CONTENT_TYPE_XML,
        #                                        body=requested_data)
        # return RequestUtil.request(url='http://agency.uat-por-api.vetc-dc.local/Inventory/ViewInventoryService.svc',
        #                            data=params)
        pass