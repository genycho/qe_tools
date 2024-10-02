import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sonarqube_helper import make_report
from scancode_helper import excel_writer
from apitest_generator import spec_parser
from apitest_generator import tc_extractor
from apitest_generator import code_generator
from apitest_generator.tc_extractor import GetTypeTCAnalyzer

def scancode_json2excel_writer(input_json_path, output_path):
    excel_writer.make_excel_report(input_json_path, output_path)

def sonarqube_result2excel_writer(sonar_url, project_key, output_path):
    response_json = make_report.make_sonarqube_reports(sonar_url, project_key)
    make_report.make_excelreport(output_path, response_json,sonar_url)

def testcode_gen(swagger_filepath, template_path, template_filename, output_path):
    api_infos_list = spec_parser.parse_swagger_json(swagger_filepath)
    for a_api in api_infos_list:
        if "get" == a_api.method.lower():
            get_tc_extractor = GetTypeTCAnalyzer()
            tcinfo_result = get_tc_extractor.get_tclist(a_api)
            if tcinfo_result != None:
                code_output = code_generator.code_generate(template_path, template_filename, output_path, tcinfo_result)

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

    