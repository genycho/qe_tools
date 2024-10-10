#-*- coding: utf-8 -*-
import os, sys, io
import pytest
import json, time
# from common import api_test_util as util
from apitest_generator.tc_extractor_swagger2 import PostJsonBodyTypeTCAnalyzer
from apitest_generator.model.api_info import ApiInfo

def test_tcextractor_swagger_v20_basic():
    a_api_info = ApiInfo()
    a_api_info.base_url = ""
    a_api_info.consumes = ['']
    a_api_info.description = ""
    a_api_info.method = "post"
    a_api_info.name = "uploadFile"
    a_api_info.operation_id = "uploadFile"
    a_api_info.parameters = [
        {'name':'petId','in':'path','description':'ID of pet to update','required':True,'type':'integer','format':'int64'}
    ]
    a_api_info.path = "'/pet/{petId}/uploadImage'"
    a_api_info.produces = ['application/json']
    a_api_info.project_title = "Swagger Petstore"
    a_api_info.responses = {
        '200':{
            'description': 'successful operation', 
            'schema': {'$ref': '#/definitions/ApiResponse'}
            }
        }
    a_api_info.security = [{'petstore_auth': ['write:pets', 'read:pets']}]
    a_api_info.security_definitions = ""
    a_api_info.summary = "uploads an image"
    a_api_info.tag = "pet"
    post_tc_extractor = PostJsonBodyTypeTCAnalyzer()
    tcinfo_result = post_tc_extractor.get_tclist(a_api_info)