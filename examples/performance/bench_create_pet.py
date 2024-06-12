from .create_pet import ApiExample
from gautomator.utils.common import AssertUtil
from gautomator.const.api.request import RequestConst

from performance import task, HttpUser, between

class BenchCreatePet(HttpUser):
    wait_time = between(1, 5)
     
    @task
    def bench_create_pet(self):
        data = ApiExample.data_prepare()
        r = self.client.post(url='https://petstore.swagger.io/v2/pet', json=data)
        AssertUtil.equal(r.status_code, RequestConst.StatusCode.OK)
        
        