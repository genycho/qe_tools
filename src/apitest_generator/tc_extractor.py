#-*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from common.exceptions import QEToolException
from apitest_generator.model.api_info import ApiInfo
from apitest_generator.model.api_info import ApiTCInfo

class GetTypeTCAnalyzer():
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
        # 0) 공통으로 적용할 항목 
        self.header_str = f'"Content-Type": "{api_info.produces[0]}"' if api_info.produces != None and len(api_info.produces)>0 else ""
        self.project_str = api_info.project_title.lower().replace(" ","")
        
        for a_param in api_info.parameters:
            param_type = a_param['in']
            name = a_param['name']
            p_type = a_param['type']
            required = a_param['required']
            # 쿼리 파라미터 체크
            if 'query' == param_type:
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
                self.path_params_set_str+=(f'test_{name} = {self.project_str}_util.get{name}()')
                # self.path_params_str += f'.format({name}="{p_type}")'
                self.path_params_str += f'.format({name}=test_{name})'
                if p_type == "integer":
                    self.path_params_notexist_str+=(f'test_{name} = 999999')
                else:
                    self.path_params_notexist_str+=(f'test_{name} = "not_exist_id"')
            # TODO formData
        # 1번)기본 호출 - 필수/선택 파라미터 있으면, 1번은 필수만
        tc_list.append(self.get_first_basic_tc(api_info))
        if self.query_optparam_count > 0:
            # 2번)기본호출 - 필수/선택 모든 파라미터 
            tc_list.append(self.get_second_basic_tc(api_info))
        # 3번) path parameter가 있는 경우 not_exist_id TC 
        if "" != self.path_params_str:
            tc_list.append(self.get_third_pathparamnotexist_tc(api_info))
        return tc_list

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
        tc_info_3.query_params_str = self.query_params_required_str
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
        """"""
        tc_info_1 = ApiTCInfo()
        tc_info_1.set_apiinfo(api_info)
        if api_info.security != None and len(api_info.security) >0:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_basic(get_{self.project_str}_baseurl, get_loggedin_session)"
        else:
            self.test_declartion_str = f"{api_info.operation_id.lower()}_basic(get_{self.project_str}_baseurl)"
        tc_info_1.testfile_declaration = f"API Test for {api_info.operation_id}, {api_info.summary}, \ndescription:{api_info.description}"
        tc_info_1.testmethod_declaration = "테스트 목적 : basic(required params only)"
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
            self.test_declartion_str = f"{api_info.operation_id.lower()}_basic(get_{self.project_str}_baseurl)"  
        self.set_commoninfo(tc_info_1)
        this_assert_str_list = []
        this_assert_str_list.append("assert 200 == response.status_code, response.text\n")
        this_assert_str_list.append("response_json = response.json()\n")
        this_assert_str_list.append("assert '' in response_json")
        tc_info_1.query_params_str = self.query_params_required_str
        tc_info_1.assert_str_list = this_assert_str_list
        return tc_info_1
    
    def get_basic_tc_object(self, api_info):
        tc_info = ApiTCInfo()
        tc_info.set_apiinfo(api_info)
        self.set_commoninfo(tc_info)
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
