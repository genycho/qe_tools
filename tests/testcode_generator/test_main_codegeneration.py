#-*- coding: utf-8 -*-
import os, sys, io
import pytest
import json, time
# from common import api_test_util as util
import qe_tools_main as main

def test_main_basic(get_dirpath,get_projectpath):
    swagger_json_path = get_dirpath+"/testcode_generator/api/test_resource/swagger_petstore_v2_107.json"
    template_file_path = get_dirpath+"/testcode_generator/api/test_resource"
    template_file_name = "get_api_template_v2.py.jinja"
    output_path = get_projectpath+"/testcode_generation_result"
    main.testcode_gen(swagger_json_path,template_file_path, template_file_name, output_path)
    print("")



    