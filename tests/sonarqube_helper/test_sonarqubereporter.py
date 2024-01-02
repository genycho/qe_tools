#-*- coding: utf-8 -*-
import os, sys, io
import pytest
import json, time
from sonarqube_helper import make_report

def test_excelwriter_basic(get_dirpath):
    """ 테스트 목적 : 기본확인 """
    sonar_url = "http://34.27.250.231:9000"
    project_key = "vimore"
    result_list = make_report.make_sonarqube_reports(sonar_url, project_key)
    make_report.make_excelreport()

    output_path = get_dirpath+"/sonarqube_helper/test_result"
    make_report.make_excel_report(result_list, output_path, sonar_url)

# def test_excelwriter_simple(get_dirpath):
    # """ 테스트 목적 : 기본확인 """
    # json_result_path = get_dirpath+"/scancode_helper/test_resource/ddu_dla.json"
    # excel_writer.simple_pandas()
