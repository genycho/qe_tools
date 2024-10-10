#-*- coding: utf-8 -*-
import os, sys, io
import pytest
import json, time
# from common import api_test_util as util
from apitest_generator import spec_parser
from apitest_generator import code_generator
import logging

def test_specparser_swagger_v20_basic(get_dirpath,get_projectpath):
    swagger_json_path = get_dirpath+"/testcode_generator/api/test_resource/swagger_petstore_v2_107.json"
    api_infos_list = spec_parser.parse_swagger_json(swagger_json_path)

    template_file_path = get_dirpath+"/testcode_generator/api/test_resource"
    template_file_name = "get_api_template_petstore.py.jinja"
    # output_path = get_dirpath+"/testcode_generator/api/test_result"
    output_path = get_projectpath+"/testcode_generation_result"
    
    first_api = api_infos_list[0]
    result = code_generator.code_generate(template_file_path, template_file_name, output_path, first_api)







    