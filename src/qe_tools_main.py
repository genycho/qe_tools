import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sonarqube_helper import make_report
from scancode_helper import excel_writer
from apitest_generator import spec_parser
from apitest_generator import code_generator
from common import tc_generator_constants
from apitest_generator.tc_extractor_swagger2 import GetTypeTCAnalyzer
from apitest_generator.tc_extractor_swagger2 import PostJsonBodyTypeTCAnalyzer
import datetime
from dotenv import find_dotenv, load_dotenv
import logging
from common.log_config import setup_logging

logger = logging.getLogger()
setup_logging()
logger = logging.getLogger(__name__)


def scancode_json2excel_writer(input_json_path, output_path):
    excel_writer.make_excel_report(input_json_path, output_path)

def sonarqube_result2excel_writer(sonar_url, project_key, output_path):
    response_json = make_report.make_sonarqube_reports(sonar_url, project_key)
    make_report.make_excelreport(output_path, response_json,sonar_url)

def testcode_gen(swagger_filepath, template_path, output_path):
    api_infos_list = spec_parser.parse_swagger_json(swagger_filepath)
    for a_api in api_infos_list:
        # if "get" == a_api.method.lower():
        #     get_tc_extractor = GetTypeTCAnalyzer()
        #     tcinfo_result = get_tc_extractor.get_tclist(a_api)
        #     template_filename = tc_generator_constants.GET_METHOD_TEMPLATEFILENAME
        #     if tcinfo_result != None:
        #         code_output_fullpath = code_generator.code_generate(template_path, template_filename, output_path, tcinfo_result)
        if "post" == a_api.method.lower():
            post_tc_extractor = PostJsonBodyTypeTCAnalyzer()
            tcinfo_result = post_tc_extractor.get_tclist(a_api)
            template_filename = tc_generator_constants.POST_METHOD_TEMPLATEFILENAME
            if tcinfo_result != None and len(tcinfo_result) >0:
                code_output_fullpath = code_generator.code_generate(template_path, template_filename, output_path, tcinfo_result)
            else:
                logger.info("there is not tc to print!!")

if __name__=="__main__":
    # file_path = sys.argv[1]
    to_command = sys.argv[1]
    if "scancode" == to_command:
        if len(sys.argv) != 2:
            print("Insufficient arguments. -scancode -input_json_path -output_path")
            sys.exit()
        scancode_json2excel_writer(sys.argv[2], sys.argv[3])
    elif "sonarqube" == to_command:
        if len(sys.argv) != 3:
            print("Insufficient arguments. -sonarqube -sonar_url -project_key")
            sys.exit()
        sonarqube_result2excel_writer(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print("Not supported commands!(scancode, sonarqube only): "+ to_command)

    