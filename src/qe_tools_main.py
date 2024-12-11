import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sonarqube_helper import make_report
from scancode_helper import excel_writer
from apitest_generator import spec_parser
from apitest_generator import code_generator
from common import tc_generator_constants
from common import qe_utils
from common.exceptions import QEToolException
from apitest_generator.tc_extractor_swagger2 import GetTypeTCAnalyzer
from apitest_generator.tc_extractor_swagger2 import PostJsonBodyTypeTCAnalyzer
from apitest_generator.tc_extractor_swagger2 import PostMultipartTypeTCAnalyzer
from apitest_generator.tc_extractor_swagger2 import PutJsonBodyTypeTCAnalyzer
from apitest_generator.tc_extractor_swagger2 import DeleteTypeTCAnalyzer
import datetime
from dotenv import find_dotenv, load_dotenv
import logging
from common.log_config import setup_logging
from packaging.version import Version

logger = logging.getLogger()
setup_logging()
logger = logging.getLogger(__name__)

def scancode_json2excel_writer(input_json_path, output_path):
    excel_writer.make_excel_report(input_json_path, output_path)

def sonarqube_result2excel_writer(sonar_url, project_key, output_path):
    response_json = make_report.make_sonarqube_reports(sonar_url, project_key)
    make_report.make_excelreport(output_path, response_json,sonar_url)

def testcode_gen(swagger_filepath, template_path, output_path):
    ## swagger json parsing ## 
    api_spec_parsing_result = spec_parser.parse_swagger_json(swagger_filepath)
    api_infos_list = api_spec_parsing_result[0]
    get_sepc_schema_version = Version(api_spec_parsing_result[1])
    ## test case extraction ## 
    post_jsonbody_tc_extractor = PostJsonBodyTypeTCAnalyzer()
    post_multipart_tc_extractor = PostMultipartTypeTCAnalyzer()
    get_tc_extractor = GetTypeTCAnalyzer()
    put_jsonbody_tc_extractor = PutJsonBodyTypeTCAnalyzer()
    delete_tc_extractor = DeleteTypeTCAnalyzer()
    swagger_spec_version = 2
    if get_sepc_schema_version >=Version("2.0.0") and get_sepc_schema_version <Version("3.0.0") :
        swagger_spec_version = 2
    elif get_sepc_schema_version >=Version("3.0.0") and get_sepc_schema_version <Version("4.0.0") :
        swagger_spec_version = 3
    else:
        raise QEToolException(f"Swagger Specification version {get_sepc_schema_version} is not supported version!!")
    for a_api in api_infos_list:
        tcinfo_result = None
        req_content_type = qe_utils.get_request_type(a_api, swagger_spec_version)
        if "get" == a_api.method.lower():
            tcinfo_result = get_tc_extractor.get_tclist(a_api)
            template_filename = tc_generator_constants.GET_METHOD_TEMPLATEFILENAME
        elif "post" == a_api.method.lower():
            if 'application/json' == req_content_type:     
                tcinfo_result = post_jsonbody_tc_extractor.get_tclist(a_api)
                template_filename = tc_generator_constants.POST_JSONBODY_TEMPLATEFILENAME
            elif 'application/json' != req_content_type:
                tcinfo_result = post_multipart_tc_extractor.get_tclist(a_api)
                template_filename = tc_generator_constants.POST_MULTIPART_TEMPLATEFILENAME
            else:
                logger.warning("not supported post type-"+str(req_content_type))
                continue
        elif "put" == a_api.method.lower() or "patch" == a_api.method.lower():
            if 'application/json' == req_content_type:     
                tcinfo_result = put_jsonbody_tc_extractor.get_tclist(a_api)
                template_filename = tc_generator_constants.PUT_JSONBODY_TEMPLATEFILENAME
            else:
                logger.warning("not supported post type-"+str(req_content_type))
                continue
        elif "delete" == a_api.method.lower():
        # if "delete" == a_api.method.lower():
            template_filename = tc_generator_constants.DELETE_METHOD_TEMPLATEFILENAME
            tcinfo_result = delete_tc_extractor.get_tclist(a_api)
        else:
            logger.warning(f"not expected(not supported) api method found!!: {a_api.method} in api operation id ={a_api.operation_id}")
        if tcinfo_result != None and len(tcinfo_result)>0:
            code_output_fullpath = code_generator.code_generate(template_path, template_filename, output_path, tcinfo_result)
        else:
            logger.info(f"there is no tc to print!! for api operation id = {a_api.operation_id}")
# API 플랫폼꺼 넣어보니 
# (1)리퀘스트 json, 멀티파트를 requestBody에서 하나하나 꺼내서 세팅할 것
# (2)delete에 쿼리 파람이 무조건 나옴... 
# (3) api path에 {} 가 있고, operation id가 없을 때, 선언부등이 깨지는데. replace 할까.. 딴걸로 할까..
# (4) POST basic 테스트에 메소드 주석이 없다 
# (5) POST에 아무 요청 내용 없으면 빈값으로  headers = { "Content-Type": "" } 출력됨. 
# (6) 정작 파일 업로드 multipart 에서 file 이 안 찍힘.
# 헤더에 추가한 값들이 클리어되지 않고 누적되어 추가 


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

    