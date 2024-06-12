from gautomator.utils.common import StringUtil


class ApiExample:
        
    @staticmethod
    def data_prepare() -> dict:
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
        return {
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

        