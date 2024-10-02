#-*- coding: utf-8 -*-
import os, sys, io
import pytest
import json, time
# from common import api_test_util as util
from apitest_generator import code_generator

def test_codegenerate_basic(get_dirpath):
    template_file_path = get_dirpath+"/testcode_generator/api/test_resource"
    template_file_name = "get_api_template.txt"
    output_path = get_dirpath+"/testcode_generator/api/test_result"
    api_spec_data = {
        "api_name":"TestAPI",
        "api_desc":"test api description",
        "api_path":"/api/users",
        "api_method":"GET",
        "response_status":[200,400,500],
        "response_body_json":"{}",
        "query_params":[
            {"name":"user_name"}
        ],
        "etc":[]
    }
    result = code_generator.code_generate(template_file_path, template_file_name, output_path, api_spec_data)


    