import collections 
from dataclasses import dataclass

# @dataclass
# class ApiParameter:
#     name=""   #
#     path=""   #path, formData
#     description=""
#     required= False
#     type=""
#     format=""

#     def get_parameter_v2(self, parameter_json):
#         self.name = parameter_json.get("name")
#         self.path = parameter_json.get("path")
#         self.description = parameter_json.get("description")
#         self.required = parameter_json.get("required")
#         self.type = parameter_json.get("type")
#         self.format = parameter_json.get("format")


# @dataclass 
class ApiInfo:
    project_title = ""
    base_url = ""
    name = ""
    operation_id = ""
    description = ""
    summary = ""
    path = ""
    method = ""
    tag = []
    consumes = ""
    produces = ""
    parameters = []
    responses = []
    security = ""
    security_definitions = ""   #커스텀? None(인증 헤더 필요없음) / auth_header (Bearer 토큰) / 그 외에.. 

    def get_apiinfo_v2(self, project_title, base_url, api_path, api_mehotd, apiinfo_json):
        self.project_title = project_title
        self.base_url = base_url
        self.path = api_path
        self.method = api_mehotd
        self.name = apiinfo_json.get("operationId") if apiinfo_json.get("operationId") else apiinfo_json.get("summary")
        self.operation_id = apiinfo_json.get("operationId")
        self.description = apiinfo_json.get("description")
        self.summary = apiinfo_json.get("summary")
        self.tag = apiinfo_json.get("tags")[0] if apiinfo_json.get("tags") and len(apiinfo_json.get("tags"))>0 else None
        self.consumes = apiinfo_json.get("consumes")
        self.produces = apiinfo_json.get("produces")
        self.parameters = apiinfo_json.get("parameters")
        # "parameters": [
        #             {
        #                 "in": "body",
        #                 "name": "body",
        #                 "description": "Pet object that needs to be added to the store",
        #                 "required": true,
        #                 "schema": {
        #                     "$ref": "#/definitions/Pet"
        #                 }
        #             }
        #         ],


        self.responses = apiinfo_json.get("responses")
        self.security = apiinfo_json.get("security")


    def get_apiinfo_v3(self, project_title, base_url, api_path, api_mehotd, apiinfo_json):
        self.project_title = project_title
        self.base_url = base_url
        self.path = api_path
        self.method = api_mehotd
        self.name = apiinfo_json.get("operationId") if apiinfo_json.get("operationId") else apiinfo_json.get("summary")
        self.operation_id = apiinfo_json.get("operationId")
        self.description = apiinfo_json.get("description")
        self.summary = apiinfo_json.get("summary")
        self.tag = apiinfo_json.get("tags")[0] if apiinfo_json.get("tags") and len(apiinfo_json.get("tags"))>0 else None

        self.consumes = apiinfo_json.get("consumes")
        self.produces = apiinfo_json.get("produces")
        
        self.parameters = apiinfo_json.get("parameters")
        # 1) 쿼리
        # "parameters": [
        #             {
        #                 "name": "status",
        #                 "in": "query",
        #                 "description": "Status values that need to be considered for filter",
        #                 "required": false,
        #                 "explode": true,
        #                 "schema": {
        #                     "type": "string",
        #                     "default": "available",
        #                     "enum": [
        #                         "available",
        #                         "pending",
        #                         "sold"
        #                     ]
        #                 }
        #             }
        #         ],
        apiinfo_json.get("requestBody")  #TODO 
        self.responses = apiinfo_json.get("responses")
        self.security = apiinfo_json.get("security")

    # def __init__(self):
        # self.name=""

# @dataclass
class ApiTCInfo(ApiInfo):
    project_str:str #관련 라이브러리 import에서 쓰이는 문자열입니다
    testfile_declaration:str    #테스트 파일 상단 주석 설명에 사용됩니다
    test_pytestmarker_str:str #각 테스트함수 위에 pytest.mark ~ 문장을 생성합니다
    test_declartion_str:str #각 테스트함수 이름을 정의하는 문장입니다
    testmethod_declaration:str  #각 테스트 함수(케이스) 주석 설명에 사용됩니다
    header_str:str  #테스트 상단 헤더 content-type 등 설정에 사용되는 라인입니다
    path_params_set_str:str #상단 path parameter를 세팅하는 라인입니다
    path_params_str:str #상단 path parameter를 세팅하는 라인입니다
    query_params_str:str    #상단 params={}을 채우는데 사용되는 문자열입니다
    request_str:str #테스트 실행 문구를 구성합니다
    jsonbody_str:str    #post,put 등에서 json 요청 바디를 표시하는 문자열입니다
    assert_str_list:str #테스트 assertion 을 출력하는데 사용되는 리스트입니다

    def set_apiinfo(self, api_info:ApiInfo):
        self.name = api_info.method+"_"+api_info.name
        self.base_url = api_info.base_url
        self.consumes = api_info.consumes
        self.description = api_info.description
        self.method = api_info.method
        self.operation_id = api_info.operation_id
        self.parameters = api_info.operation_id
        self.path = api_info.path
        self.produces = api_info.produces
        self.tag = api_info.tag
        self.project_title = api_info.project_title
        self.responses = api_info.responses
        self.summary = api_info.summary
        self.security_definitions = api_info.security_definitions

