#-*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from common.exceptions import QEToolException
from common import qe_utils
from apitest_generator.model.api_info import ApiInfo
from apitest_generator.model.api_info import ApiTCInfo
import logging
from common.log_config import setup_logging

logger = logging.getLogger()
setup_logging()
logger = logging.getLogger(__name__)

class BasicTCAnalyzer():
    query_params_required_str:str
    query_params_all_str:str
    path_params_str:str
    path_params_set_str:str
    path_params_notexist_str:str
    header_str:str
    project_str:str
    request_str:str
    query_reqparam_count:int
    query_optparam_count:int
    assert_str_list:list
    test_declartion_str:str
    testmethod_declaration:str
    req_content_type:str
    formparms_str:str
    multipart_file_str:str

    def __init__(self):
        self.reset()

    def reset(self):
        self.query_params_required_str = ""
        self.query_params_all_str = ""
        self.path_params_str = ""
        self.path_params_set_str = ""
        self.path_params_notexist_str=""
        self.header_str = ""
        self.project_str = ""
        self.request_str = ""
        self.query_reqparam_count = 0
        self.query_optparam_count = 0
        self.assert_str_list = []
        self.test_declartion_str = ""
        self.testmethod_declaration = ""
        self.formparms_str=""
        self.multipart_file_str=""

    def get_tclist(self,api_info:ApiInfo):
        # 0) 공통으로 적용할 항목 
        self.reset()
        self.req_content_type = qe_utils.get_request_type(api_info, 2)
        self.header_str = f'"Content-Type": "{self.req_content_type}"'
        self.project_str = api_info.project_title.lower().replace(" ","")

    def set_commoninfo(self, tc_info:ApiTCInfo):
        tc_info.project_str = self.project_str
        tc_info.test_declartion_str = self.test_declartion_str
        tc_info.testmethod_declaration = self.testmethod_declaration
        tc_info.header_str = self.header_str
        tc_info.path_params_str = self.path_params_str
        tc_info.path_params_set_str = self.path_params_set_str
        tc_info.query_params_str = self.query_params_required_str
        tc_info.request_str=self.request_str
        tc_info.assert_str_list=self.assert_str_list

class DeleteTypeTCAnalyzer(BasicTCAnalyzer):
    """
    DELETE Method, 
    """
    def get_tclist(self,api_info:ApiInfo):
        """
        """
        tc_list = []
        self.jsonbody_str = ""
        super().get_tclist(api_info)
        self.reset()
        for a_param in api_info.parameters:
            param_type = a_param['in']
            p_name = a_param['name']
            # 쿼리 파라미터 체크
            if 'query' == param_type:   # TO_EXTRACT
                required = a_param['required']
                p_type = a_param['type']
                if True == required:
                    if self.query_reqparam_count > 0:
                        self.query_params_required_str+=',\n        '
                        self.query_params_all_str+=',\n        '
                    self.query_params_required_str+=f'"{p_name}":"{p_type}"'
                    self.query_params_all_str+=f'"{p_name}":"{p_type}"'
                    self.query_reqparam_count+=1
                else:
                    if self.query_reqparam_count+self.query_optparam_count > 0:
                        self.query_params_all_str+=',\n        '
                    self.query_params_all_str+=f'"{p_name}":"{p_type}"'
                    self.query_optparam_count +=1
            # path 파라미터 체크
            elif 'path' == param_type:   # TO_EXTRACT
                p_type = a_param['type']
                self.path_params_set_str=(f'test_{p_name} = {self.project_str}_util.get{p_name}()')
                self.path_params_str = f'.format({p_name}=test_{p_name})'
                if p_type == "integer":
                    self.path_params_notexist_str=(f'test_{p_name} = 999999')
                else:
                    self.path_params_notexist_str=(f'test_{p_name} = "not_exist_id"')
            elif 'body' == param_type:
                for a_body_param_name, values in a_param['schema']['properties'].items():
                    self.jsonbody_str += f',\n"{a_body_param_name}":"{values['type']}"'
            elif 'header' == param_type:
                self.header_str+=f',\n"{p_name}":"{a_param['type']}"'
            else:
                logger.info("not supported parameter type - "+param_type)
        # 1번)기본 호출 - 기본
        tc_list.append(self.get_delete_basic_tc(api_info))
        # 2번)path 파라미터 있으면, not exist TC 
        if "" != self.path_params_str:
            tc_list.append(self.get_delete_pathparamnotexist_tc(api_info))
        # 4번) 에러 응답 상태 코드 
        if api_info.responses != None or len(api_info.responses)>0:
            for a_response_key in api_info.responses.keys():
                try:
                    if 400<=int(a_response_key) and 500 > int(a_response_key):
                        tc_list.append(self.get_delete_errorreresponse_tc(api_info, a_response_key))
                except Exception as ignore:
                    logger.warning(f"responses status code was not int type, but was {a_response_key}")
        # 5번),6번) 인증정보 없이, 잘못된 인증 정보로 요청 TC 
        if api_info.security != None and len(api_info.security) >0:
            tc_list.append(self.get_delete_noauth_tc(api_info))
        return tc_list
    
    def get_delete_basic_tc(self, api_info):
        """
        """
        self.testfile_declaration = f"API Test for {api_info.operation_id}, {api_info.summary}, \ndescription:{api_info.description}"
        self.testmethod_declaration = "테스트 목적 : basic"
        if api_info.security != None and len(api_info.security) >0:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_basic(get_{self.project_str}_baseurl, get_loggedin_session)"
            if self.path_params_str == "" : 
                self.request_str = f"get_loggedin_session.{api_info.method.lower()}(get_{self.project_str}_baseurl + constants.{api_info.method.upper()}_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"get_loggedin_session.{api_info.method.lower()}(get_{self.project_str}_baseurl + constants.{api_info.method.upper()}_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        else:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_basic(get_{self.project_str}_baseurl)"
            if self.path_params_str == "" : 
                self.request_str = f"requests.{api_info.method.lower()}(get_{self.project_str}_baseurl + constants.{api_info.method.upper()}_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"requests.{api_info.method.lower()}(get_{self.project_str}_baseurl + constants.{api_info.method.upper()}_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
            self.test_declartion_str = f"{api_info.operation_id.lower()}_basic(get_{self.project_str}_baseurl)"  
        tc_info = ApiTCInfo()
        tc_info.set_apiinfo(api_info)
        self.set_commoninfo(tc_info)
        this_assert_str_list = []
        if '204' in api_info.responses.keys():
            this_assert_str_list.append("assert 204 == response.status_code, response.text\n")
        else:            
            this_assert_str_list.append("assert 200 == response.status_code, response.text\n")
            this_assert_str_list.append("response_json = response.json()\n")
            this_assert_str_list.append("assert '' in response_json")
        tc_info.query_params_str = self.query_params_all_str
        tc_info.assert_str_list = this_assert_str_list
        return tc_info

    def get_delete_pathparamnotexist_tc(self, api_info):
        """
        """
        self.testfile_declaration = f"This tests to summary:{api_info.summary}, description:{api_info.description}"
        self.testmethod_declaration = "테스트 목적 : path parameter does not exist, expected 404 "
        if api_info.security != None and len(api_info.security) >0:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_notexistid(get_{self.project_str}_baseurl, get_loggedin_session)"
            if self.path_params_str == "" : 
                self.request_str = f"get_loggedin_session.{api_info.method.lower()}(get_{self.project_str}_baseurl + constants.{api_info.method.upper()}_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"get_loggedin_session.{api_info.method.lower()}(get_{self.project_str}_baseurl + constants.{api_info.method.upper()}_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        else:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_notexistid(get_{self.project_str}_baseurl)"
            if self.path_params_str == "" : 
                self.request_str = f"requests.{api_info.method.lower()}(get_{self.project_str}_baseurl + constants.{api_info.method.upper()}_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"requests.{api_info.method.lower()}(get_{self.project_str}_baseurl + constants.{api_info.method.upper()}_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        tc_info = ApiTCInfo()
        tc_info.set_apiinfo(api_info)
        self.set_commoninfo(tc_info)
        tc_info.path_params_set_str = self.path_params_notexist_str
        tc_info.query_params_str = self.query_params_all_str
        this_assert_str_list = []
        this_assert_str_list.append("assert 404 == response.status_code, response.text\n")
        this_assert_str_list.append("assert '' in response.json()")
        tc_info.assert_str_list = this_assert_str_list
        return tc_info

    def get_delete_errorreresponse_tc(self, api_info, response_code):
        self.testfile_declaration = f"This tests to summary:{api_info.summary}, description:{api_info.description}"
        if api_info.security != None and len(api_info.security) >0:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_{response_code}(get_{self.project_str}_baseurl, get_loggedin_session)"
        else:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_{response_code}(get_{self.project_str}_baseurl)"
        tc_info = ApiTCInfo()
        tc_info.set_apiinfo(api_info)
        self.set_commoninfo(tc_info)
        tc_info.testmethod_declaration = f"테스트 목적 : Tests for the case of response code= {response_code}, description= {api_info.responses.get(response_code)} "
        tc_info.query_params_str = self.query_params_required_str
        this_assert_str_list = []
        this_assert_str_list.append(f"assert {response_code} == response.status_code, response.text\n")
        this_assert_str_list.append("response_json = response.json()\n")
        this_assert_str_list.append("assert '' in response_json")
        tc_info.assert_str_list = this_assert_str_list
        return tc_info

    def get_delete_noauth_tc(self, api_info):
        """
        """
        self.test_declartion_str = f"{api_info.operation_id.lower()}_noauth(get_{self.project_str}_baseurl)"
        self.testmethod_declaration = "테스트 목적 : noauth "
        if self.path_params_str == "" : 
            self.request_str = f"requests.{api_info.method.lower()}(get_{self.project_str}_baseurl + constants.{api_info.method.upper()}_{api_info.operation_id.upper()}_APIPATH"
        else:
            self.request_str = f"requests.{api_info.method.lower()}(get_{self.project_str}_baseurl + constants.{api_info.method.upper()}_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        tc_info = ApiTCInfo()
        tc_info.set_apiinfo(api_info)
        self.set_commoninfo(tc_info)
        tc_info.testmethod_declaration = "테스트 목적 : noauth "
        tc_info.query_params_str = self.query_params_all_str
        this_assert_str_list = []
        this_assert_str_list.append("assert 401 == response.status_code, response.text\n")
        tc_info.assert_str_list = this_assert_str_list
        return tc_info


class PutJsonBodyTypeTCAnalyzer(BasicTCAnalyzer):
    """
    PUT/PATCH Method, json body, multipart 
    """
    jsonbody_str:str
    
    def get_tclist(self,api_info:ApiInfo):
        """
        """
        tc_list = []
        self.jsonbody_str = ""
        self.reset()
        super().get_tclist(api_info)
        for a_param in api_info.parameters:
            param_type = a_param['in']
            p_name = a_param['name']
            # 쿼리 파라미터 체크
            if 'query' == param_type:   # TO_EXTRACT
                required = a_param['required']
                p_type = a_param['type']
                if True == required:
                    if self.query_reqparam_count > 0:
                        self.query_params_required_str+=',\n        '
                        self.query_params_all_str+=',\n        '
                    self.query_params_required_str+=f'"{p_name}":"{p_type}"'
                    self.query_params_all_str+=f'"{p_name}":"{p_type}"'
                    self.query_reqparam_count+=1
                else:
                    if self.query_reqparam_count+self.query_optparam_count > 0:
                        self.query_params_all_str+=',\n        '
                    self.query_params_all_str+=f'"{p_name}":"{p_type}"'
                    self.query_optparam_count +=1
            # path 파라미터 체크
            elif 'path' == a_param['in']:   # TO_EXTRACT
                p_type = a_param['type']
                self.path_params_set_str=(f'test_{p_name} = {self.project_str}_util.get{p_name}()')
                self.path_params_str = f'.format({p_name}=test_{p_name})'
                if p_type == "integer":
                    self.path_params_notexist_str=(f'test_{p_name} = 999999')
                else:
                    self.path_params_notexist_str=(f'test_{p_name} = "not_exist_id"')
            # json 바디 파라미터 체크
            elif 'body' == a_param['in']:   # TO_EXTRACT
                self.jsonbody_str = f'#{a_param["schema"]}'
            elif 'header' == a_param['in']:   # TO_EXTRACT
                self.header_str +=f'"{a_param["name"]}":"{a_param["type"]}"'  #TODO 
        # 1번)기본 호출 - 기본
        tc_list.append(self.get_putjson_basic_tc(api_info))
        # 2번)path 파라미터 있으면, not exist TC 
        if "" != self.path_params_str:
            tc_list.append(self.get_putjson_pathparamnotexist_tc(api_info))
        # 3번)json 바디 있으면 parameterized test 추가
        if "" != self.jsonbody_str:
            tc_list.append(self.get_putjson_parameterzied_tc(api_info))
        # 4번) 에러 응답 상태 코드 
        if api_info.responses != None or len(api_info.responses)>0:
            for a_response_key in api_info.responses.keys():
                try:
                    if 400<=int(a_response_key) and 500 > int(a_response_key):
                        tc_list.append(self.get_putjson_errorreresponse_tc(api_info, a_response_key))
                except Exception as ignore:
                    logger.warning(f"responses status code was not int type, but was {a_response_key}")
        # 5번),6번) 인증정보 없이, 잘못된 인증 정보로 요청 TC 
        if api_info.security != None and len(api_info.security) >0:
            tc_list.append(self.get_putjson_noauth_tc(api_info))
        return tc_list
    
    def get_putjson_noauth_tc(self, api_info,):
        self.test_declartion_str = f"{api_info.operation_id.lower()}_noauth(get_{self.project_str}_baseurl)"
        if self.path_params_str == "" : 
            self.request_str = f"requests.{api_info.operation_id.lower()}(get_{self.project_str}_baseurl + constants.{api_info.method.upper()}_{api_info.operation_id.upper()}_APIPATH"
        else:
            self.request_str = f"requests.{api_info.operation_id.lower()}(get_{self.project_str}_baseurl + constants.{api_info.method.upper()}_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        tc_info = ApiTCInfo()
        tc_info.set_apiinfo(api_info)
        self.set_commoninfo(tc_info)
        tc_info.testmethod_declaration = "테스트 목적 : noauth "
        tc_info.jsonbody_str = self.jsonbody_str
        tc_info.query_params_str = self.query_params_required_str
        this_assert_str_list = []
        this_assert_str_list.append("assert 401 == response.status_code, response.text\n")
        tc_info.assert_str_list = this_assert_str_list
        return tc_info

    def get_putjson_errorreresponse_tc(self, api_info, response_code):
        """ 4xx responses """
        if api_info.security != None and len(api_info.security) >0:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_{response_code}(get_{self.project_str}_baseurl, get_loggedin_session)"
        else:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_{response_code}(get_{self.project_str}_baseurl)"
        tc_info = ApiTCInfo()
        tc_info.set_apiinfo(api_info)
        self.set_commoninfo(tc_info)
        tc_info.testmethod_declaration = f"테스트 목적 : Tests for the case of response code= {response_code}, description= {api_info.responses.get(response_code)} "
        tc_info.jsonbody_str = self.jsonbody_str
        tc_info.query_params_str = self.query_params_required_str
        this_assert_str_list = []
        this_assert_str_list.append(f"assert {response_code} == response.status_code, response.text\n")
        this_assert_str_list.append("response_json = response.json()\n")
        this_assert_str_list.append("assert '' in response_json")
        tc_info.assert_str_list = this_assert_str_list
        return tc_info

    def get_putjson_parameterzied_tc(self, api_info):
        if api_info.security != None and len(api_info.security) >0:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_parameterized(get_{self.project_str}_baseurl, get_loggedin_session, input, expected)"
            if self.path_params_str == "" : 
                self.request_str = f"get_loggedin_session.{api_info.method}(get_{self.project_str}_baseurl + constants.{api_info.method.upper()}_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"get_loggedin_session.{api_info.method}(get_{self.project_str}_baseurl + constants.{api_info.method.upper()}_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        else:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_parameterized(get_{self.project_str}_baseurl, input, expected)"
            if self.path_params_str == "" : 
                self.request_str = f"requests.{api_info.method}(get_{self.project_str}_baseurl + constants.{api_info.method.upper()}_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"requests.{api_info.method}(get_{self.project_str}_baseurl + constants.{api_info.method.upper()}_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        tc_info = ApiTCInfo()
        tc_info.set_apiinfo(api_info)
        self.set_commoninfo(tc_info)
        tc_info.test_pytestmarker_str = '@pytest.mark.skip(reason="상황에 따라 수행")\n@pytest.mark.parametrize("input, expected", {("first_input","first_expected")})'
        tc_info.testfile_declaration = f"This tests to summary:{api_info.summary}, description:{api_info.description}"
        tc_info.testmethod_declaration = "테스트 목적 : pytest parameterized test sample for json request body"
        tc_info.jsonbody_str = self.jsonbody_str
        tc_info.query_params_str = self.query_params_required_str
        self.this_assert_str_list = []
        self.this_assert_str_list.append("assert expected == response.status_code, response.text")
        tc_info.assert_str_list = self.this_assert_str_list
        return tc_info

    def get_putjson_pathparamnotexist_tc(self, api_info):
        if api_info.security != None and len(api_info.security) >0:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_notexistid(get_{self.project_str}_baseurl, get_loggedin_session)"
            if self.path_params_str == "" : 
                self.request_str = f"get_loggedin_session.{api_info.method}(get_{self.project_str}_baseurl + constants.{api_info.method.upper()}_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"get_loggedin_session.{api_info.method}(get_{self.project_str}_baseurl + constants.{api_info.method.upper()}_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        else:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_notexistid(get_{self.project_str}_baseurl)"
            if self.path_params_str == "" : 
                self.request_str = f"requests.{api_info.method}(get_{self.project_str}_baseurl + constants.{api_info.method.upper()}_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"requests.{api_info.method}(get_{self.project_str}_baseurl + constants.{api_info.method.upper()}_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        tc_info = ApiTCInfo()
        tc_info.set_apiinfo(api_info)
        self.set_commoninfo(tc_info)
        # tc_info = self.get_postjsonbody_basic_tc_object(api_info)
        tc_info.testmethod_declaration = "테스트 목적 : path parameter does not exist, expected 404 "
        tc_info.jsonbody_str = self.jsonbody_str
        tc_info.path_params_str = self.path_params_notexist_str
        tc_info.query_params_str = self.query_params_all_str
        this_assert_str_list = []
        this_assert_str_list.append("assert 404 == response.status_code, response.text\n")
        this_assert_str_list.append("assert '' in response.json()")
        tc_info.assert_str_list = this_assert_str_list
        return tc_info

    def get_putjson_basic_tc(self, api_info):
        if api_info.security != None and len(api_info.security) >0:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_basic(get_{self.project_str}_baseurl, get_loggedin_session)"
            if self.path_params_str == "" : 
                self.request_str = f"get_loggedin_session.{api_info.method}(get_{self.project_str}_baseurl + constants.{api_info.method.upper()}_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"get_loggedin_session.{api_info.method}(get_{self.project_str}_baseurl + constants.{api_info.method.upper()}_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        else:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_basic(get_{self.project_str}_baseurl)"
            if self.path_params_str == "" : 
                self.request_str = f"requests.{api_info.method}(get_{self.project_str}_baseurl + constants.POST_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"requests.{api_info.method}(get_{self.project_str}_baseurl + constants.POST_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        tc_info = ApiTCInfo()
        tc_info.set_apiinfo(api_info)
        self.set_commoninfo(tc_info)
        tc_info.testfile_declaration = f"API Test for {api_info.operation_id}, {api_info.summary}, \ndescription:{api_info.description}"
        tc_info.testmethod_declaration = "테스트 목적 : basic"
        tc_info.jsonbody_str = self.jsonbody_str
        this_assert_str_list = []
        this_assert_str_list.append("assert 200 == response.status_code, response.text\n")
        this_assert_str_list.append("response_json = response.json()\n")
        this_assert_str_list.append("assert '' in response_json\n")
        tc_info.query_params_str = self.query_params_all_str
        tc_info.assert_str_list = this_assert_str_list
        return tc_info


class PostMultipartTypeTCAnalyzer(BasicTCAnalyzer):
    def get_tclist(self,api_info:ApiInfo):
        # 0) (A)json 바디 타입 vs (B)multipart-formdata 분기
        # B-1) basic 수행, 파일 첨부. form-param 이 있는지 없는지. 
        # B-2) basic 수행, 파일 첨부. form-param 별 존재하지 않을 때. 
        # B-3) file이 없을 때  
        tc_list = []
        self.reset()
        super().get_tclist(api_info)
        # 1번)기본 호출
        self.formparms_str = "{"
        for a_param in api_info.parameters:
            name = a_param['name']
            # path 파라미터 체크
            if 'path' == a_param['in']:   # TO_EXTRACT
                p_type = a_param['type']
                self.path_params_set_str=(f'test_{name} = {self.project_str}_util.get{name}()')
                self.path_params_str = f'.format({name}=test_{name})'
                if p_type == "integer":
                    self.path_params_notexist_str=(f'test_{name} = 999999')
                else:
                    self.path_params_notexist_str=(f'test_{name} = "not_exist_id"')
            elif 'formData' == a_param['in']:   # TO_EXTRACT
                #form params
                if "file" != a_param['type']:
                    if self.formparms_str !="{":
                        self.formparms_str +=f'        ,"{a_param['name']}":"{a_param['type']}" #required:{a_param['required']}\n'
                    else:
                        self.formparms_str +=f'\n        "{a_param['name']}":"{a_param['type']}" #required:{a_param['required']}\n'
                elif "file" == a_param['type']:
                    self.multipart_file_str =f'test_file_path = get_dirpath + "/{api_info.project_title}/test_resource/sample_file.jpg"\n    files= {{\n        "{a_param['name']}": ("sample_file.jpg", open(test_file_path, "rb"),"image/jpeg")\n    }}'
        self.formparms_str += "    }"
        # 1번)기본 호출 - 기본
        tc_list.append(self.get_postmultipart_basic_tc_object(api_info))
        # 2번)path 파라미터 있으면, not exist TC 
        if "" != self.path_params_str:
            tc_list.append(self.get_postmultipart_pathparamnotexist_tc(api_info))
        # 4번) 에러 응답 상태 코드 
        if api_info.responses != None or len(api_info.responses)>0:
            for a_response_key in api_info.responses.keys():
                try:
                    if 400<=int(a_response_key) and 500 > int(a_response_key):
                        tc_list.append(self.get_postmultipart_errorreresponse_tc(api_info, a_response_key))
                except Exception as ignore:
                    logger.warning(f"responses status code was not int type, but was {a_response_key}")
        # 5번),6번) 인증정보 없이, 잘못된 인증 정보로 요청 TC 
        if api_info.security != None and len(api_info.security) >0:
            tc_list.append(self.get_postmultipart_noauth_tc(api_info))
        return tc_list
    
    def get_postmultipart_noauth_tc(self, api_info,):
        self.test_declartion_str = f"{api_info.operation_id.lower()}_noauth(get_{self.project_str}_baseurl, get_dirpath)"
        tc_info.testmethod_declaration = "테스트 목적 : noauth "
        if self.path_params_str == "" : 
            self.request_str = f"requests.post(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH"
        else:
            self.request_str = f"requests.post(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        tc_info = ApiTCInfo()
        tc_info.set_apiinfo(api_info)
        self.set_commoninfo(tc_info)
        this_assert_str_list = []
        this_assert_str_list.append("assert 401 == response.status_code, response.text\n")
        tc_info.assert_str_list = this_assert_str_list
        return tc_info

    def get_postmultipart_errorreresponse_tc(self, api_info, response_code):
        """ 4xx responses """
        tc_info = self.get_postmultipart_basic_tc_object(api_info)
        if api_info.security != None and len(api_info.security) >0:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_{response_code}(get_{self.project_str}_baseurl, get_loggedin_session, get_dirpath)"
        else:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_{response_code}(get_{self.project_str}_baseurl, get_dirpath)"
        tc_info = ApiTCInfo()
        tc_info.set_apiinfo(api_info)
        self.set_commoninfo(tc_info)
        tc_info.testmethod_declaration = f"테스트 목적 : Tests for the case of response code= {response_code}, description= {api_info.responses.get(response_code)} "
        this_assert_str_list = []
        this_assert_str_list.append(f"assert {response_code} == response.status_code, response.text\n")
        this_assert_str_list.append("response_json = response.json()\n")
        this_assert_str_list.append("assert '' in response_json")
        tc_info.assert_str_list = this_assert_str_list
        return tc_info

    def get_postmultipart_pathparamnotexist_tc(self, api_info):
        if api_info.security != None and len(api_info.security) >0:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_notexistid(get_{self.project_str}_baseurl, get_loggedin_session, get_dirpath)"
            if self.path_params_str == "" : 
                self.request_str = f"get_loggedin_session.post(get_{self.project_str}_baseurl + constants.POST_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"get_loggedin_session.post(get_{self.project_str}_baseurl + constants.POST_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        else:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_notexistid(get_{self.project_str}_baseurl, get_dirpath)"
            if self.path_params_str == "" : 
                self.request_str = f"requests.post(get_{self.project_str}_baseurl + constants.POST_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"requests.post(get_{self.project_str}_baseurl + constants.POST_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        tc_info = ApiTCInfo()
        tc_info.set_apiinfo(api_info)
        self.set_commoninfo(tc_info)
        tc_info.testmethod_declaration = "테스트 목적 : path parameter does not exist, expected 404 "
        tc_info.pathparam = self.path_params_notexist_str
        this_assert_str_list = []
        this_assert_str_list.append("assert 404 == response.status_code, response.text\n")
        this_assert_str_list.append("assert '' in response.json()")
        tc_info.assert_str_list = this_assert_str_list
        return tc_info

    def get_postmultipart_basic_tc_object(self, api_info):
        if api_info.security != None and len(api_info.security) >0:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_basic(get_{self.project_str}_baseurl, get_loggedin_session, get_dirpath)"
            if self.path_params_str == "" : 
                self.request_str = f"get_loggedin_session.post(get_{self.project_str}_baseurl + constants.POST_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"get_loggedin_session.post(get_{self.project_str}_baseurl + constants.POST_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        else:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_basic(get_{self.project_str}_baseurl, get_dirpath)"
            if self.path_params_str == "" : 
                self.request_str = f"requests.post(get_{self.project_str}_baseurl + constants.POST_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"requests.post(get_{self.project_str}_baseurl + constants.POST_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        tc_info = ApiTCInfo()
        tc_info.set_apiinfo(api_info)
        self.set_commoninfo(tc_info)
        tc_info.testfile_declaration = f"API Test for {api_info.operation_id}, {api_info.summary}, \ndescription:{api_info.description}"
        tc_info.testmethod_declaration = "테스트 목적 : basic(multipart/form-data)"
        tc_info.formparms_str = self.formparms_str
        tc_info.multipart_file_str = self.multipart_file_str
        this_assert_str_list = []
        if '201' in api_info.responses.keys():
            this_assert_str_list.append("assert 201 == response.status_code, response.text\n")
        else:            
            this_assert_str_list.append("assert 200 == response.status_code, response.text\n")
        this_assert_str_list.append("response_json = response.json()\n")
        this_assert_str_list.append("assert '' in response_json")
        tc_info.assert_str_list = this_assert_str_list
        return tc_info

class PostJsonBodyTypeTCAnalyzer(BasicTCAnalyzer):
    jsonbody_str:str
    def get_tclist(self,api_info:ApiInfo):
        # 0) (A)json 바디 타입 vs (B)multipart-formdata 분기
        # <- 응답 상태 코드 체크해서 200인지 201인지 체크 
        # A-1) basic 수행, 쿼리 파람이 있을수도 있나? json 바디. 만약가능하다면 json 바디에서 필수값만
        # A-2) basic 수행, 만약가능하다면 json 바디에서 필수값만
        # A-3) 만약가능하다면 json 바디 파람에서 validation 테스트 <- 여기에 parameterized test를 넣자. 
        # A-5) 필수필드 없는 경우 테스트  
        # A-5) path param 있는 경우 not exist 테스트 
        # A-6) 만약 response가 200 외에 또 있다면. 
        # B-1) basic 수행, 파일 첨부. form-param 이 있는지 없는지. 
        # B-2) basic 수행, 파일 첨부. form-param 별 존재하지 않을 때. 
        # B-3) file이 없을 때  
        # B-3) file이 없을 때 
        ##############
        tc_list = []
        self.reset()
        super().get_tclist(api_info)
        for a_param in api_info.parameters:
            param_type = a_param['in']
            name = a_param['name']
            # 쿼리 파라미터 체크
            if 'query' == param_type:   # TO_EXTRACT
                p_type = a_param['type']
                required = a_param['required']
                if True == required:
                    if self.query_reqparam_count >0:
                        self.query_params_required_str+=',\n        '
                        self.query_params_all_str+=',\n        '
                    self.query_params_required_str+=f'"{name}":"{p_type}"'
                    self.query_params_all_str+=f'"{name}":"{p_type}"'
                    self.query_reqparam_count+=1
                else:
                    if self.query_reqparam_count+self.query_optparam_count > 0:
                        self.query_params_all_str+=',\n        '
                    self.query_params_all_str+=f'"{name}":"{p_type}"'
                    self.query_optparam_count +=1
            # path 파라미터 체크
            elif 'path' == a_param['in']:   # TO_EXTRACT
                p_type = a_param['type']
                self.path_params_set_str=(f'test_{name} = {self.project_str}_util.get{name}()')
                # self.path_params_str += f'.format({name}="{p_type}")'
                self.path_params_str = f'.format({name}=test_{name})'
                if p_type == "integer":
                    self.path_params_notexist_str=(f'test_{name} = 999999')
                else:
                    self.path_params_notexist_str=(f'test_{name} = "not_exist_id"')
            elif 'body' == a_param['in']:   # TO_EXTRACT
                # p_type = a_param['type']
                # required = a_param['required']
                self.jsonbody_str = f'#{a_param["schema"]}'
        # 1번)기본 호출 - 기본
        tc_list.append(self.get_postjsonbody_basic_tc_object(api_info))
        # 2번)path 파라미터 있으면, not exist TC 
        if "" != self.path_params_str:
            tc_list.append(self.get_postjsonbody_pathparamnotexist_tc(api_info))
        # 3번)json 바디 있으면 parameterized test 추가
        if "" != self.jsonbody_str:
            tc_list.append(self.get_postjsonbody_parameterzied_tc(api_info))
        # 4번) 에러 응답 상태 코드 
        if api_info.responses != None or len(api_info.responses)>0:
            for a_response_key in api_info.responses.keys():
                try:
                    if 400<=int(a_response_key) and 500 > int(a_response_key):
                        tc_list.append(self.get_errorreresponse_tc(api_info, a_response_key))
                except Exception as ignore:
                    logger.warning(f"responses status code was not int type, but was {a_response_key}")
        # 5번),6번) 인증정보 없이, 잘못된 인증 정보로 요청 TC 
        if api_info.security != None and len(api_info.security) >0:
            tc_list.append(self.get_noauth_tc(api_info))
        return tc_list
    
    def get_noauth_tc(self, api_info,):
        tc_info = self.get_postjsonbody_basic_tc_object(api_info)
        self.test_declartion_str = f"{api_info.operation_id.lower()}_noauth(get_{self.project_str}_baseurl)"
        tc_info.testmethod_declaration = "테스트 목적 : noauth "
        if self.path_params_str == "" : 
            self.request_str = f"requests.post(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH"
        else:
            self.request_str = f"requests.post(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        self.set_commoninfo(tc_info)
        tc_info.jsonbody_str = self.jsonbody_str
        tc_info.query_params_str = self.query_params_required_str
        this_assert_str_list = []
        this_assert_str_list.append("assert 401 == response.status_code, response.text\n")
        tc_info.assert_str_list = this_assert_str_list
        return tc_info

    def get_errorreresponse_tc(self, api_info, response_code):
        """ 4xx responses """
        tc_info = self.get_postjsonbody_basic_tc_object(api_info)
        if api_info.security != None and len(api_info.security) >0:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_{response_code}(get_{self.project_str}_baseurl, get_loggedin_session)"
        else:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_{response_code}(get_{self.project_str}_baseurl)"
        tc_info.testmethod_declaration = f"테스트 목적 : Tests for the case of response code= {response_code}, description= {api_info.responses.get(response_code)} "
        self.set_commoninfo(tc_info)
        tc_info.jsonbody_str = self.jsonbody_str
        tc_info.query_params_str = self.query_params_required_str
        this_assert_str_list = []
        this_assert_str_list.append(f"assert {response_code} == response.status_code, response.text\n")
        this_assert_str_list.append("response_json = response.json()\n")
        this_assert_str_list.append("assert '' in response_json")
        tc_info.assert_str_list = this_assert_str_list
        return tc_info

    def get_postjsonbody_parameterzied_tc(self, api_info):
        
        if api_info.security != None and len(api_info.security) >0:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_parameterized(get_{self.project_str}_baseurl, get_loggedin_session, input, expected)"
            if self.path_params_str == "" : 
                self.request_str = f"get_loggedin_session.post(get_{self.project_str}_baseurl + constants.POST_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"get_loggedin_session.post(get_{self.project_str}_baseurl + constants.POST_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        else:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_parameterized(get_{self.project_str}_baseurl, input, expected)"
            if self.path_params_str == "" : 
                self.request_str = f"requests.post(get_{self.project_str}_baseurl + constants.POST_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"requests.post(get_{self.project_str}_baseurl + constants.POST_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        tc_info = ApiTCInfo()
        tc_info.set_apiinfo(api_info)
        self.set_commoninfo(tc_info)
        tc_info.test_pytestmarker_str = '@pytest.mark.skip(reason="상황에 따라 수행")\n@pytest.mark.parametrize("input, expected", {("first_input","first_expected")})'
        tc_info.testfile_declaration = f"This tests to summary:{api_info.summary}, description:{api_info.description}"
        tc_info.testmethod_declaration = "테스트 목적 : pytest parameterized test sample for json request body"
        tc_info.jsonbody_str = self.jsonbody_str
        tc_info.query_params_str = self.query_params_required_str
        this_assert_str_list = []
        this_assert_str_list.append("assert expected == response.status_code, response.text\n")
        tc_info.assert_str_list = this_assert_str_list
        return tc_info

    def get_postjsonbody_pathparamnotexist_tc(self, api_info):
        if api_info.security != None and len(api_info.security) >0:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_notexistid(get_{self.project_str}_baseurl, get_loggedin_session)"
            if self.path_params_str == "" : 
                self.request_str = f"get_loggedin_session.post(get_{self.project_str}_baseurl + constants.POST_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"get_loggedin_session.post(get_{self.project_str}_baseurl + constants.POST_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        else:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_notexistid(get_{self.project_str}_baseurl)"
            if self.path_params_str == "" : 
                self.request_str = f"requests.post(get_{self.project_str}_baseurl + constants.POST_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"requests.post(get_{self.project_str}_baseurl + constants.POST_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        tc_info = ApiTCInfo()
        tc_info.set_apiinfo(api_info)
        # self.set_commoninfo(tc_info)
        self.set_commoninfo(tc_info)
        tc_info.testmethod_declaration = "테스트 목적 : path parameter does not exist, expected 404 "
        tc_info.jsonbody_str = self.jsonbody_str
        tc_info.pathparam = self.path_params_notexist_str
        tc_info.query_params_str = self.query_params_required_str
        this_assert_str_list = []
        this_assert_str_list.append("assert 404 == response.status_code, response.text\n")
        this_assert_str_list.append("assert '' in response.json()")
        tc_info.assert_str_list = this_assert_str_list
        return tc_info

    def get_postjsonbody_basic_tc_object(self, api_info):
        if api_info.security != None and len(api_info.security) >0:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_basic(get_{self.project_str}_baseurl, get_loggedin_session)"
            if self.path_params_str == "" : 
                self.request_str = f"get_loggedin_session.post(get_{self.project_str}_baseurl + constants.POST_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"get_loggedin_session.post(get_{self.project_str}_baseurl + constants.POST_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        else:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_basic(get_{self.project_str}_baseurl)"
            if self.path_params_str == "" : 
                self.request_str = f"requests.post(get_{self.project_str}_baseurl + constants.POST_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"requests.post(get_{self.project_str}_baseurl + constants.POST_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        tc_info = ApiTCInfo()
        tc_info.set_apiinfo(api_info)
        self.set_commoninfo(tc_info)
        tc_info.testfile_declaration = f"API Test for {api_info.operation_id}, {api_info.summary}, \ndescription:{api_info.description}"
        tc_info.testmethod_declaration = "테스트 목적 : basic"
        tc_info.jsonbody_str = self.jsonbody_str
        this_assert_str_list = []
        if '201' in api_info.responses.keys():
            this_assert_str_list.append("assert 201 == response.status_code, response.text\n")
        else:            
            this_assert_str_list.append("assert 200 == response.status_code, response.text\n")
        this_assert_str_list.append("response_json = response.json()\n")
        this_assert_str_list.append("assert '' in response_json")
        tc_info.query_params_str = self.query_params_required_str
        tc_info.assert_str_list = this_assert_str_list
        return tc_info
    

class GetTypeTCAnalyzer(BasicTCAnalyzer):
    query_params_required_str:str
    query_params_all_str:str
    path_params_str:str
    path_params_set_str:str
    path_params_notexist_str:str
    header_str:str
    project_str:str
    request_str:str
    query_reqparam_count:int
    query_optparam_count:int
    assert_str_list:list
    test_declartion_str:str

    def __init__(self):
        self.query_params_required_str = ""
        self.query_params_all_str = ""
        self.path_params_str = ""
        self.path_params_set_str = ""
        self.path_params_notexist_str=""
        self.header_str = ""
        self.project_str = ""
        self.request_str = ""
        self.query_reqparam_count = 0
        self.query_optparam_count = 0
        self.assert_str_list = []
        self.test_declartion_str = ""

    def get_tclist(self,api_info:ApiInfo):
        # 11) basic 수행, 쿼리 파람 값 필수값만 넣고 
        #     12) basic 수행, 쿼리 파람 값을 다 채워서 
        #     12) path param이 있는 경우 not exist로 
        #     13) 권한 없이 호출 시도 
        #     13) 이건 주석으로 - 공통 / 다른 Method 등 
        #     14) 만약 response가 200 외에 또 있다면. 
        ##############
        # GET에서 
        # 3번)path에 path parameter가 있으면 path_parameter에 not_exist_id =999999999 넣는 TC.
        # 보류)path parameter가 2개 이상인 경우에는 그냥 첫번째 것만 하고, 보류. 너무 많이 생겨도 구찮으니까? 
        # 4번) 응답 response가 200 외에 또 있으면 그건 그거대로 갯수만큰 추가하자 
        ###############
        tc_list = []
        self.reset()
        super().get_tclist(api_info)
        # 0) 공통으로 적용할 항목 
        self.header_str = f'"Content-Type": "{api_info.consumes[0]}"' if api_info.consumes != None and len(api_info.consumes)>0 else ""
        self.project_str = api_info.project_title.lower().replace(" ","")
        for a_param in api_info.parameters:
            param_type = a_param['in']
            name = a_param['name']
            # 쿼리 파라미터 체크
            if 'query' == param_type:
                p_type = a_param['type']
                required = a_param['required']
                if True == required:
                    if self.query_reqparam_count >0:
                        self.query_params_required_str+=',\n        '
                        self.query_params_all_str+=',\n        '
                    self.query_params_required_str+=f'"{name}":"{p_type}"'
                    self.query_params_all_str+=f'"{name}":"{p_type}"'
                    self.query_reqparam_count+=1
                else:
                    if self.query_reqparam_count+self.query_optparam_count > 0:
                        self.query_params_all_str+=',\n        '
                    self.query_params_all_str+=f'"{name}":"{p_type}"'
                    self.query_optparam_count +=1
            # path 파라미터 체크
            elif 'path' == a_param['in']:
                p_type = a_param['type']
                required = a_param['required']
                self.path_params_set_str=(f'test_{name} = {self.project_str}_util.get{name}()')
                # self.path_params_str += f'.format({name}="{p_type}")'
                self.path_params_str = f'.format({name}=test_{name})'
                if p_type == "integer":
                    self.path_params_notexist_str=(f'test_{name} = 999999')
                else:
                    self.path_params_notexist_str=(f'test_{name} = "not_exist_id"')
            # TODO formData
        # 1번)기본 호출 - 필수/선택 파라미터 있으면, 1번은 필수만
        tc_list.append(self.get_first_basic_tc(api_info))
        if self.query_optparam_count > 0:
        # 2번)기본호출 - 필수/선택 모든 파라미터 
            tc_list.append(self.get_second_basic_tc(api_info))
        # 3번) path parameter가 있는 경우 not_exist_id TC 
        if "" != self.path_params_str:
            tc_list.append(self.get_third_pathparamnotexist_tc(api_info))
        # 4번) 에러 응답 상태 코드 
        if api_info.responses != None or len(api_info.responses)>0:
            for a_response_key in api_info.responses.keys():
                try:
                    if 400<=int(a_response_key) and 500 > int(a_response_key):
                        tc_list.append(self.get_errorreresponse_tc(api_info, a_response_key))
                except Exception as ignore:
                    logger.warning(f"responses status code was not int type, but was {a_response_key}")
        # 5번),6번) 인증정보 없이, 잘못된 인증 정보로 요청 TC 
        if api_info.security != None and len(api_info.security) >0:
            tc_list.append(self.get_noauth_tc(api_info))
        return tc_list
    
    def get_noauth_tc(self, api_info,):
        tc_info = self.get_basic_tc_object(api_info)
        self.test_declartion_str = f"{api_info.operation_id.lower()}_noauth(get_{self.project_str}_baseurl)"
        tc_info.testmethod_declaration = "테스트 목적 : noauth "
        if self.path_params_str == "" : 
            self.request_str = f"requests.get(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH"
        else:
            self.request_str = f"requests.get(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        self.set_commoninfo(tc_info)
        tc_info.query_params_str = self.query_params_all_str
        this_assert_str_list = []
        this_assert_str_list.append("assert 401 == response.status_code, response.text\n")
        tc_info.assert_str_list = this_assert_str_list
        return tc_info

    def get_errorreresponse_tc(self, api_info, response_code):
        """ 4xx responses """
        tc_info = self.get_basic_tc_object(api_info)
        if api_info.security != None and len(api_info.security) >0:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_{response_code}(get_{self.project_str}_baseurl, get_loggedin_session)"
        else:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_{response_code}(get_{self.project_str}_baseurl)"
        tc_info.testmethod_declaration = f"테스트 목적 : Tests for the {response_code}: {api_info.responses.get(response_code)} "
        self.set_commoninfo(tc_info)
        # if api_info.security != None and len(api_info.security) >0:
        #     if self.path_params_str == "" : 
        #         self.request_str = f"get_loggedin_session.get(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH"
        #     else:
        #         self.request_str = f"get_loggedin_session.get(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        # else:
        #     if self.path_params_str == "" : 
        #         self.request_str = f"requests.get(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH"
        #     else:
        #         self.request_str = f"requests.get(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        # self.set_commoninfo(tc_info)
        this_assert_str_list = []
        this_assert_str_list.append(f"assert {response_code} == response.status_code, response.text\n")
        this_assert_str_list.append("response_json = response.json()\n")
        this_assert_str_list.append("assert '' in response_json")
        tc_info.assert_str_list = this_assert_str_list
        return tc_info
    
    def get_third_pathparamnotexist_tc(self, api_info):
        """ not exist path id for 404 returns """
        tc_info_3 = self.get_basic_tc_object(api_info)
        if api_info.security != None and len(api_info.security) >0:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_notexistid(get_{self.project_str}_baseurl, get_loggedin_session)"
        else:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_notexistid(get_{self.project_str}_baseurl)"
        tc_info_3.testfile_declaration = f"This tests to summary:{api_info.summary}, description:{api_info.description}"
        tc_info_3.testmethod_declaration = "테스트 목적 : path parameter does not exist, expected 404 "
        if api_info.security != None and len(api_info.security) >0:
            if self.path_params_str == "" : 
                self.request_str = f"get_loggedin_session.get(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"get_loggedin_session.get(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        else:
            if self.path_params_str == "" : 
                self.request_str = f"requests.get(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"requests.get(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        self.set_commoninfo(tc_info_3)
        tc_info_3.path_params_set_str = self.path_params_notexist_str
        tc_info_3.query_params_str = self.query_params_all_str
        this_assert_str_list = []
        this_assert_str_list.append("assert 404 == response.status_code, response.text\n")
        this_assert_str_list.append("assert '' in response.json()")
        tc_info_3.assert_str_list = this_assert_str_list
        return tc_info_3

    def get_second_basic_tc(self, api_info):
        """ 파라미터 부분만 다른 2번째 basic TC 정의 - 별도 함수로 공용화. GET 등 메소드별 차이가 있을까? """
        tc_info_2 = ApiTCInfo()
        tc_info_2.set_apiinfo(api_info)
        if api_info.security != None and len(api_info.security) >0:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_allparams(get_{self.project_str}_baseurl, get_loggedin_session)"
        else:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_allparams(get_{self.project_str}_baseurl)"
        tc_info_2.testfile_declaration = f"This tests to summary:{api_info.summary}, description:{api_info.description}"
        tc_info_2.testmethod_declaration = "테스트 목적 : basic(all params)"
        if api_info.security != None and len(api_info.security) >0:
            if self.path_params_str == "" : 
                self.request_str = f"get_loggedin_session.get(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"get_loggedin_session.get(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        else:
            if self.path_params_str == "" : 
                self.request_str = f"requests.get(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"requests.get(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        self.set_commoninfo(tc_info_2)
        tc_info_2.query_params_str = self.query_params_all_str
        this_assert_str_list = []
        this_assert_str_list.append("assert 200 == response.status_code, response.text\n")
        this_assert_str_list.append("response_json = response.json()\n")
        this_assert_str_list.append("assert '' in response_json")
        tc_info_2.query_params_str = self.query_params_required_str
        tc_info_2.assert_str_list = this_assert_str_list
        return tc_info_2

    def get_first_basic_tc(self, api_info):
        """ """
        self.testfile_declaration = f"API Test for {api_info.operation_id}, {api_info.summary}, \ndescription:{api_info.description}"
        self.testmethod_declaration = "테스트 목적 : basic(required params only)"
        if api_info.security != None and len(api_info.security) >0:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_basic(get_{self.project_str}_baseurl, get_loggedin_session)"
            if self.path_params_str == "" : 
                self.request_str = f"get_loggedin_session.get(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"get_loggedin_session.get(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        else:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_basic(get_{self.project_str}_baseurl)"
            if self.path_params_str == "" : 
                self.request_str = f"requests.get(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"requests.get(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
            self.test_declartion_str = f"{api_info.operation_id.lower()}_basic(get_{self.project_str}_baseurl)"  
        tc_info = ApiTCInfo()
        tc_info.set_apiinfo(api_info)
        self.set_commoninfo(tc_info)
        this_assert_str_list = []
        this_assert_str_list.append("assert 200 == response.status_code, response.text\n")
        this_assert_str_list.append("response_json = response.json()\n")
        this_assert_str_list.append("assert '' in response_json")
        tc_info.query_params_str = self.query_params_required_str
        tc_info.assert_str_list = this_assert_str_list
        return tc_info
    
    def get_basic_tc_object(self, api_info):
        tc_info = ApiTCInfo()
        tc_info.set_apiinfo(api_info)
        self.set_commoninfo(tc_info)
        if api_info.security != None and len(api_info.security) >0:
            if self.path_params_str == "" : 
                self.request_str = f"get_loggedin_session.get(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"get_loggedin_session.get(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        else:
            if self.path_params_str == "" : 
                self.request_str = f"requests.get(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH"
            else:
                self.request_str = f"requests.get(get_{self.project_str}_baseurl + constants.GET_{api_info.operation_id.upper()}_APIPATH{self.path_params_str}"
        tc_info.query_params_str = self.query_params_required_str
        return tc_info
    
    def set_commoninfo(self,tc_info):
        tc_info.project_str = self.project_str
        tc_info.header_str = self.header_str
        tc_info.path_params_str = self.path_params_str
        tc_info.query_params_str = self.query_params_all_str
        tc_info.test_declartion_str = self.test_declartion_str
        tc_info.request_str=self.request_str
        tc_info.assert_str_list=self.assert_str_list
        tc_info.path_params_set_str = self.path_params_set_str
