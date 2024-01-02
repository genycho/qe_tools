#-*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import csv
import requests
from common.exceptions import QEToolException
from common import qe_utils
import pandas as pd
import json
from pandas import json_normalize
import openpyxl
from common.exceptions import QEToolException
from common import qe_utils

### Constants ###
APIPATH_ISSUELIST = "/api/issues/search"
TEMP_USERID = "admin"
TEMP_USERPW = "admin1@3$"
SONARQUBE_URL = "http://34.27.250.231:9000"

def make_sonarqube_reports(sonarqube_url, project_component_key):
    """ """
    page_no = 1
    all_issues_list = []
    first_page_response_json = _get_result_each500(sonarqube_url, project_component_key, page_no)
    total_count = first_page_response_json['total']
    all_issues_list.append(first_page_response_json['issues'])
    to_iter_count = total_count % 500

    for page_no in range(to_iter_count):
        first_page_response_json = _get_result_each500(sonarqube_url, project_component_key, page_no)
        all_issues_list.append(first_page_response_json['issues'])
    return all_issues_list



def _convert_json_to_issuelist(issue_json_item, row_no, sonarqube_url):
    to_return_list = []
    # writer.writerow(["No", "Type", "Severity", "Rule", "Message", "File", "Line"])
    to_return_list.append(str(row_no))
    to_return_list.append(issue_json_item['type'])
    to_return_list.append(issue_json_item['severity'])
    to_return_list.append(issue_json_item['rule'])
    to_return_list.append(issue_json_item['message'])
    to_return_list.append(issue_json_item['component'])
    if 'line' not in issue_json_item:
        to_return_list.append('none')
    else:
        to_return_list.append(str(issue_json_item['line']))
    to_return_list.append(issue_json_item['status'])
    to_return_list.append(f"{sonarqube_url}/project/issues?id={issue_json_item['project']}&open={issue_json_item['key']}")

    return to_return_list


def make_excelreport(output_path, result_sonarqube_json, sonarqube_url):
    date_string = qe_utils.get_curdatetime()
    file_name = output_path+"/license_scancode_"+ date_string + ".xlsx"

    writer=pd.ExcelWriter(file_name, engine='openpyxl')

    all_issuelist = []
    row_count = 1
    fixed_count = 0
    bug_all_count = 0
    bug_critmajor_count = 0
    codesmell_all_count = 0
    codesmell_critmajor_count = 0
    project_name = ""
    summary_dict={}
    for a_issue_json in result_sonarqube_json:
        this_type = a_issue_json['type']
        this_severity = a_issue_json['severity']
        this_status = a_issue_json['status']
        project_name = a_issue_json['project']
        if "CLOSED" == this_status:
            fixed_count +=1
            continue
        if "BUG" == this_type:
            bug_all_count += 1
            if this_severity in ["BLOCKER","CRITICAL","MAJOR"]:
                bug_critmajor_count +=1
        elif "CODE_SMELL" == this_type:
            codesmell_all_count += 1
            if this_severity in ["BLOCKER","CRITICAL","MAJOR"]:
                codesmell_critmajor_count +=1
        all_issuelist.append(_convert_json_to_issuelist(a_issue_json,row_count,sonarqube_url))
        row_count += 1
    summary_dict.update({". Project":})
    summary_df = json_normalize(summary_info)
    details_df = json_normalize(result_sonarqube_json)
    date_string = qe_utils.get_curdatetime()
    file_name = output_path+"/license_scancode_"+ date_string + ".xlsx"
    writer=pd.ExcelWriter(file_name, engine='openpyxl')

    summary_df.to_excel(writer, sheet_name='scan_info', index=False)
    details_df.to_excel(writer, sheet_name='result_summary', index=True)
    details_df.to_excel(writer, sheet_name='files_details', index=True)

    worksheet1 = writer.sheets['scan_info']
    _autofit_columnsize(worksheet1, [1,2,3,4,5])
    worksheet2 = writer.sheets['result_summary']
    _autofit_columnsize(worksheet2, [1,2,3,4])
    worksheet3 = writer.sheets['files_details']
    _autofit_columnsize(worksheet3, [1,2,3,4,5,6,7,8,9])
    writer.close()


def make_csvreport(output_path, result_sonarqube_json, sonarqube_url):
    """
    """
    # if 'total' not in result_sonarqube_json:
    #     raise QEToolException("There is no required information: total")
    # if 'issues' not in result_sonarqube_json:
    #     raise QEToolException("There is no required information: issues")
    # if result_sonarqube_json['total'] <=0:
    #     #IF? 
    #     pass

    result_file_path_name = f"{output_path}/sonarqube_{qe_utils.get_curdatetime()}.csv"
    f = open(result_file_path_name, "w",newline='')

    all_issuelist = []
    row_count = 1
    fixed_count = 0
    bug_all_count = 0
    bug_critmajor_count = 0
    codesmell_all_count = 0
    codesmell_critmajor_count = 0
    project_name = ""
    for a_issue_json in result_sonarqube_json['issues']:
        this_type = a_issue_json['type']
        this_severity = a_issue_json['severity']
        this_status = a_issue_json['status']
        project_name = a_issue_json['project']
        if "CLOSED" == this_status:
            fixed_count +=1
            continue
        if "BUG" == this_type:
            bug_all_count += 1
            if this_severity in ["BLOCKER","CRITICAL","MAJOR"]:
                bug_critmajor_count +=1
        elif "CODE_SMELL" == this_type:
            codesmell_all_count += 1
            if this_severity in ["BLOCKER","CRITICAL","MAJOR"]:
                codesmell_critmajor_count +=1
        all_issuelist.append(_convert_json_to_issuelist(a_issue_json,row_count,sonarqube_url))
        row_count += 1
    writer = csv.writer(f)
    writer.writerow(["[ SonarQube Result(Overview) ]"])
    writer.writerow([". Project",project_name])
    writer.writerow([". Report date", str(qe_utils.get_curdate())])
    writer.writerow(["[ Summary ]"])
    writer.writerow([". (Bug)(All)", str(bug_all_count)])
    writer.writerow([". (BUG)(CRITICAL&MAJOR)", str(bug_critmajor_count)])
    writer.writerow([". (CODESMELL)(ALL)", str(codesmell_all_count)])
    writer.writerow([". (CODESMELL)(CRITICAL&MAJOR)", str(codesmell_critmajor_count)])
    writer.writerow([". (FIXED)", str(fixed_count)])
    writer.writerow(["[ Details ]"])
    
    writer.writerow(["No", "Type", "Severity", "Rule", "Message", "File", "Line", "Status", "sonarqube link(url+value)"])
    writer.writerows(all_issuelist)
    f.close()


def _get_result_each500(sonarqube_url, project_component_key, page:int):
    params = {
        "additionalFields" : "rules,ruleDescriptionContextKey", 
        "componentKeys" : project_component_key, 
        "ps" : "500", 
        "p" : page
    }
    request_session=requests.Session()
    request_session.auth = (TEMP_USERID,TEMP_USERPW)
    response = request_session.get(sonarqube_url+APIPATH_ISSUELIST, params = params, headers={})
    if 200 != response.status_code:
        raise QEToolException("Failed to get info from sonarqube - "+sonarqube_url)
    return response.json()
# {
#     "total": 663,
#     "p": 1,
#     "ps": 100,
#     "paging": {
#         "pageIndex": 1,
#         "pageSize": 100,
#         "total": 663
#     },
#     "effortTotal": 3669,
#     "issues": [
#         {
#             "key": "AYVXnVoR72C7TrsBOvIc",
#             "rule": "typescript:S1128",
#             "severity": "MINOR",
#             "component": "exaone_universe_fe:src/components/comment/BoardSingleComent.tsx",
#             "project": "exaone_universe_fe",
#             "line": 13,
#             "hash": "0da92399b2ab9ad64b50438f81a6839e",
#             "textRange": {
#                 "startLine": 13,
#                 "endLine": 13,
#                 "startOffset": 9,
#                 "endOffset": 15
#             },
#             "flows": [],
#             "status": "OPEN",
#             "message": "Remove this unused import of 'result'.",
#             "effort": "2min",
#             "debt": "2min",
#             "author": "82758086+mmnn323@users.noreply.github.com",
#             "tags": [
#                 "es2015",
#                 "unused"
#             ],
#             "creationDate": "2022-12-16T13:42:40+0900",
#             "updateDate": "2022-12-28T16:22:11+0900",
#             "type": "CODE_SMELL",
#             "scope": "MAIN",
#             "quickFixAvailable": true,
#             "messageFormattings": []
#         },