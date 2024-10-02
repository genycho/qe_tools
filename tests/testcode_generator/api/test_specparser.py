#-*- coding: utf-8 -*-
import os, sys, io
import pytest
import json, time
# from common import api_test_util as util
from apitest_generator import spec_parser

def test_specparser_swagger_v20_basic(get_dirpath):
    # swagger_json_path = get_dirpath+"/testcode_generator/api/test_resource/petstore_v3_openapi.json"
    swagger_json_path = get_dirpath+"/testcode_generator/api/test_resource/swagger_petstore_v2_107.json"
    returned_dict = spec_parser.parse_swagger_json(swagger_json_path)
    print("")
    # parameters [{'name': 'status', 'in': 'query', 'description': 'Status values that need to be considered for filter', 
    # 'required': True, 'type': 'array', 'items': {...}, 
    # 'collectionFormat': 'multi'}]

def test_specparser_swagger_v30_basic(get_dirpath):
    # swagger_json_path = get_dirpath+"/testcode_generator/api/test_resource/petstore_v3_openapi.json"
    swagger_json_path = get_dirpath+"/testcode_generator/api/test_resource/swagger_petstore_v3_1019.json"
    returned_dict = spec_parser.parse_swagger_json(swagger_json_path)



    