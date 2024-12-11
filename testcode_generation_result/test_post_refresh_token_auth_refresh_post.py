#-*- coding: utf-8 -*-
""" 
API Test for refresh_token_auth_refresh_post, Refresh Token, 
description:None
"""
import os, sys, io
import requests
from requests import Request, Session
import pytest
import json, time
from common import api_test_util as util
from common.exceptions import APITestException
from fastapi import fastapi_constants as constants
from fastapi import fastapi_util
# this_apipath = (POST)/auth/refresh

def test_post_refresh_token_auth_refresh_post_basic(get_fastapi_baseurl, get_loggedin_session):
    """ 테스트 목적 : basic """
    test_f_id = fastapi_util.getf_id()
    headers = { "Content-Type": "application/json" }
    payload = {}#{'allOf': [{'$ref': '#/components/schemas/RqReport'}], 'title': 'Rq Report'}
    response = get_loggedin_session.post(get_fastapi_baseurl + constants.POST_REFRESH_TOKEN_AUTH_REFRESH_POST_APIPATH.format(f_id=test_f_id), data=json.dumps(payload,indent=4), headers=headers)
    assert 200 == response.status_code, response.text
    response_json = response.json()
    assert '' in response_json


def test_post_refresh_token_auth_refresh_post_notexistid(get_fastapi_baseurl, get_loggedin_session):
    """ 테스트 목적 : path parameter does not exist, expected 404  """
    test_f_id = fastapi_util.getf_id()
    headers = { "Content-Type": "application/json" }
    payload = {}#{'allOf': [{'$ref': '#/components/schemas/RqReport'}], 'title': 'Rq Report'}
    response = get_loggedin_session.post(get_fastapi_baseurl + constants.POST_REFRESH_TOKEN_AUTH_REFRESH_POST_APIPATH.format(f_id=test_f_id), data=json.dumps(payload,indent=4), headers=headers)
    assert 404 == response.status_code, response.text
    assert '' in response.json()

@pytest.mark.skip(reason="상황에 따라 수행")
@pytest.mark.parametrize("input, expected", {("first_input","first_expected")})
def test_post_refresh_token_auth_refresh_post_parameterized(get_fastapi_baseurl, get_loggedin_session, input, expected):
    """ 테스트 목적 : pytest parameterized test sample for json request body """
    test_f_id = fastapi_util.getf_id()
    headers = { "Content-Type": "application/json" }
    payload = {}#{'allOf': [{'$ref': '#/components/schemas/RqReport'}], 'title': 'Rq Report'}
    response = get_loggedin_session.post(get_fastapi_baseurl + constants.POST_REFRESH_TOKEN_AUTH_REFRESH_POST_APIPATH.format(f_id=test_f_id), data=json.dumps(payload,indent=4), headers=headers)
    assert expected == response.status_code, response.text



def test_post_refresh_token_auth_refresh_post_422(get_fastapi_baseurl, get_loggedin_session):
    """  """
    test_f_id = fastapi_util.getf_id()
    headers = { "Content-Type": "application/json" }
    payload = {}#{'allOf': [{'$ref': '#/components/schemas/RqReport'}], 'title': 'Rq Report'}
    response = get_loggedin_session.post(get_fastapi_baseurl + constants.POST_REFRESH_TOKEN_AUTH_REFRESH_POST_APIPATH.format(f_id=test_f_id), data=json.dumps(payload,indent=4), headers=headers)
    assert 422 == response.status_code, response.text
    response_json = response.json()
    assert '' in response_json


def test_post_refresh_token_auth_refresh_post_noauth(get_fastapi_baseurl):
    """  """
    test_f_id = fastapi_util.getf_id()
    headers = { "Content-Type": "application/json" }
    payload = {}#{'allOf': [{'$ref': '#/components/schemas/RqReport'}], 'title': 'Rq Report'}
    response = requests.post(get_fastapi_baseurl + constants.GET_REFRESH_TOKEN_AUTH_REFRESH_POST_APIPATH.format(f_id=test_f_id), data=json.dumps(payload,indent=4), headers=headers)
    assert 401 == response.status_code, response.text


