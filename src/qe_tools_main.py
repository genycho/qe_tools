import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sonarqube_helper import make_report
from scancode_helper import excel_writer

def scancode_json2excel_writer(input_json_path, output_path):
    excel_writer.make_excel_report(input_json_path, output_path)

def sonarqube_result2excel_writer(sonar_url, project_key, output_path):
    response_json = make_report.make_sonarqube_reports(sonar_url, project_key)
    make_report.make_excelreport(output_path, response_json,sonar_url)

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

    