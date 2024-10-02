#-*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import random
import string
from dataclasses import dataclass

@dataclass
class api_info:
    api_name:str
    api_method:str
    api_description:str
    api_path:str
    service:str
    exec_infos:list
    # [ Requests ]
    query_params:dict
    json_body_params:dict = {}
    formdata_body_params:dict
    auth_needed:bool
    # [ Responses ]
    response_codes:list
    response_json_body_params:dict
    

@dataclass
class api_test_info(api_info):
    test_cases:list
    