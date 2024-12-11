#-*- coding: utf-8 -*-
""" 

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
# this_apipath = (GET)/auth/istokenvalid

def test_get_is_token_valid_auth_istokenvalid_get_basic(get_fastapi_baseurl):
    """  """
    test_f_id = fastapi_util.getf_id()
    headers = {  }
    params = {
        "tempToken":"None",
        "question_id":"integer",
        "question_id":"integer",
        "streaming":"boolean",
        "start":"string",
        "end":"string",
        "size":"integer"
    }
    response = requests.get(get_fastapi_baseurl + constants.GET_IS_TOKEN_VALID_AUTH_ISTOKENVALID_GET_APIPATH.format(f_id=test_f_id), params=params, headers=headers)
    assert 200 == response.status_code, response.text
    response_json = response.json()
    assert '' in response_json


def test_get_is_token_valid_auth_istokenvalid_get_allparams(get_fastapi_baseurl):
    """ 테스트 목적 : basic(all params) """
    test_f_id = fastapi_util.getf_id()
    headers = {  }
    params = {
        "tempToken":"None",
        "question_id":"integer",
        "question_id":"integer",
        "streaming":"boolean",
        "start":"string",
        "end":"string",
        "size":"integer"
    }
    response = requests.get(get_fastapi_baseurl + constants.GET_IS_TOKEN_VALID_AUTH_ISTOKENVALID_GET_APIPATH.format(f_id=test_f_id), params=params, headers=headers)
    assert 200 == response.status_code, response.text
    response_json = response.json()
    assert '' in response_json


def test_get_is_token_valid_auth_istokenvalid_get_notexistid(get_fastapi_baseurl):
    """ 테스트 목적 : path parameter does not exist, expected 404  """
    test_f_id = 999999
    headers = {  }
    params = {
        "tempToken":"None",
        "question_id":"integer",
        "question_id":"integer",
        "streaming":"boolean",
        "days":"integer",
        "start":"string",
        "end":"string",
        "page":"None",
        "size":"None",
        "start_q_id":"None",
        "size":"integer",
        "upsert":"None"
    }
    response = requests.get(get_fastapi_baseurl + constants.GET_IS_TOKEN_VALID_AUTH_ISTOKENVALID_GET_APIPATH.format(f_id=test_f_id), params=params, headers=headers)
    assert 404 == response.status_code, response.text
    assert '' in response.json()


def test_get_is_token_valid_auth_istokenvalid_get_422(get_fastapi_baseurl):
    """ 테스트 목적 : Tests for the 422: {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}  """
    test_f_id = fastapi_util.getf_id()
    headers = {  }
    params = {
        "tempToken":"None",
        "question_id":"integer",
        "question_id":"integer",
        "streaming":"boolean",
        "days":"integer",
        "start":"string",
        "end":"string",
        "page":"None",
        "size":"None",
        "start_q_id":"None",
        "size":"integer",
        "upsert":"None"
    }
    response = requests.get(get_fastapi_baseurl + constants.GET_IS_TOKEN_VALID_AUTH_ISTOKENVALID_GET_APIPATH.format(f_id=test_f_id), params=params, headers=headers)
    assert 422 == response.status_code, response.text
    response_json = response.json()
    assert '' in response_json

