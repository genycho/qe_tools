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
    project_str:str
    testfile_declaration:str
    testmethod_declaration:str
    query_params_str:str
    path_params_str:str
    path_params_set_str:str
    header_str:str
    test_declartion_str:str
    assert_str_list:str
    request_str:str

    def set_apiinfo(self, api_info:ApiInfo):
        self.name = api_info.name
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

