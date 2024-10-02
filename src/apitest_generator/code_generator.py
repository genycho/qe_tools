#-*- coding: utf-8 -*-
import os, sys, io
from os import path
from common import qe_utils
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
from common.exceptions import QEToolException

def code_generate(template_path, template_filename, output_path, tc_list):
    """
    https://documentation.bloomreach.com/engagement/docs/datastructures
    """
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template(template_filename) 
    output = template.render(tc_list=tc_list)
    # Write the output to a file
    if len(tc_list) <=0:
        raise QEToolException("There is no tc data to generate!!")
    first_tc = tc_list[0]
    output_fullpath = output_path + f"/test_{first_tc.name}.py"
    if path.exists(output_fullpath):
        output_fullpath = output_path + f"/test_{first_tc.name}_{qe_utils.get_curdatetime()}.py"
    with open(output_fullpath, 'wb') as f:
    # with open(output_fullpath, 'w') as f:
        f.write(output.encode("utf-8"))
    return output_fullpath


def code_generate_old(template_path, template_filename, output_path, apispec):
    """
    https://documentation.bloomreach.com/engagement/docs/datastructures
    """
    # Define data to populate the template
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template(template_filename)  #'get_api_template.py'
    # template = Template(template_path)

    # Render the template with the data
    # https://stackoverflow.com/questions/51735093/how-to-pass-an-object-instance-to-a-jinja-html-template 참고해서 클래스 전달하기 
    output = template.render(api_info=apispec)
    # Write the output to a file
    output_fullpath = output_path + f"/test_{apispec.name}.py"
    if path.exists(output_fullpath):
        output_fullpath = output_path + f"/test_{apispec.name}_{qe_utils.get_curdatetime()}.py"
    with open(output_fullpath, 'wb') as f:
    # with open(output_fullpath, 'w') as f:
        f.write(output.encode("utf-8"))
    return output_fullpath


# from jinja2 import Environment, PackageLoader, select_autoescape

# env = Environment(
#     loader=PackageLoader("apitest_generator"),
#     autoescape=select_autoescape()
# )