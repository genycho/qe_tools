#-*- coding: utf-8 -*-
import os, sys, io
import pytest
import json, time
# from common import api_test_util as util
from scancode_helper import excel_writer

def test_excelwriter_basic(get_dirpath):
    """ 테스트 목적 : 기본확인 """
    json_result_path = get_dirpath+"/scancode_helper/test_resource/ddu_dla.json"
    output_path = get_dirpath+"/scancode_helper/test_result"
    excel_writer.make_excel_report(json_result_path, output_path, None)

# def test_excelwriter_simple(get_dirpath):
    # """ 테스트 목적 : 기본확인 """
    # json_result_path = get_dirpath+"/scancode_helper/test_resource/ddu_dla.json"
    # excel_writer.simple_pandas()
