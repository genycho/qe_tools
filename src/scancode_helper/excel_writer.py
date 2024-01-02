#-*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
import pandas as pd
import json
from pandas import json_normalize
import openpyxl
from common.exceptions import QEToolException
from common import qe_utils

def _header_parser_v1(raw_json):
    to_return_dict = {}
    if raw_json.get('headers') == None or len(raw_json['headers']) ==0:
        raise QEToolException("There is no headers info!!")
    if len(raw_json['headers']) != 1:
        raise QEToolException("There is no headers info!! header size - " +str(len(raw_json['headers'])))
    # to_return_dict.update({"tool_name":raw_json.get("tool_name")})
    # to_return_dict.update({"tool_version":raw_json.get("tool_version")})
    # to_return_dict.update({"start_timestamp":raw_json.get("start_timestamp")})
    # to_return_dict.update({"end_timestamp":raw_json.get("end_timestamp")})
    # to_return_dict.update({"duration":raw_json.get("duration")})
    to_return_dict.update({"tool_name":raw_json['headers'][0]["tool_name"]})
    to_return_dict.update({"tool_version":raw_json['headers'][0]["tool_version"]})
    to_return_dict.update({"start_timestamp":raw_json['headers'][0]["start_timestamp"]})
    to_return_dict.update({"end_timestamp":raw_json['headers'][0]["end_timestamp"]})
    to_return_dict.update({"duration":raw_json['headers'][0]["duration"]})
    return to_return_dict

def _licenseinfo_parser_v1(raw_json):
    if len(raw_json['license_detections']) ==0:
        print("there is no any license_detections")
        return raw_json['license_detections']
    return sorted(raw_json['license_detections'], key=lambda x: x['detection_count'], reverse=True)

def _detail_file_detection_parser_v1(raw_json):
    return raw_json['files']

def _autofit_columnsize(worksheet, columns=None, margin=2):
    for i, column_cells in enumerate(worksheet.columns):
        is_ok = False
        if columns == None:
            is_ok = True
        elif isinstance(columns, list) and i in columns:
            is_ok = True
        if is_ok:
            length = max(len(str(cell.value)) for cell in column_cells)
            worksheet.column_dimensions[column_cells[0].column_letter].width = length + margin
    return worksheet


def make_excel_report(scancode_json_path, output_path, options=None):
    with open(scancode_json_path, 'r') as f:
        json_data = json.load(f)
    
    summary_info = _header_parser_v1(json_data)
    detected_license_info = _licenseinfo_parser_v1(json_data)
    detail_file_info = _detail_file_detection_parser_v1(json_data)

    scan_summary_df = json_normalize(summary_info)
    result_summary_df = json_normalize(detected_license_info)
    details_df = json_normalize(detail_file_info)
    date_string = qe_utils.get_curdatetime()
    file_name = output_path+"/license_scancode_"+ date_string + ".xlsx"
    writer=pd.ExcelWriter(file_name, engine='openpyxl')

    scan_summary_df.to_excel(writer, sheet_name='scan_info', index=False)
    result_summary_df.to_excel(writer, sheet_name='result_summary', index=True)
    details_df.to_excel(writer, sheet_name='files_details', index=True)

    worksheet1 = writer.sheets['scan_info']
    _autofit_columnsize(worksheet1, [1,2,3,4,5])
    worksheet2 = writer.sheets['result_summary']
    _autofit_columnsize(worksheet2, [1,2,3,4])
    worksheet3 = writer.sheets['files_details']
    _autofit_columnsize(worksheet3, [1,2,3,4,5,6,7,8,9])

    writer.close()

    # # 헤더 정렬
    # df.to_excel("test.xlsx", index=False, engine="openpyxl", 
    #     header=True, startrow=1, freeze_panes=(1, 1))

    # worksheet.set_column("A:A", 20, workbook.add_format({'align': 'center'}))
    # worksheet.set_column("B:B", 20, workbook.add_format({'align': 'right'}))
    # worksheet.set_column("C:C", 20, workbook.add_format({'align': 'left'}))
    # df.style.set_properties(**{'width': '200px'})

    # font = openpyxl.styles.Font(name='Arial', size=14, bold=True)
    # # font = openpyxl.styles.Font(color='red')
    # fill = openpyxl.styles.PatternFill(fill_type='solid', start_color='FFBBBBBB')
    # border = openpyxl.styles.Border(left=openpyxl.styles.Side(style='thin'), 
    #                                 right=openpyxl.styles.Side(style='thin'), 
    #                                 top=openpyxl.styles.Side(style='thin'), 
    #                                 bottom=openpyxl.styles.Side(style='thin'))

    # red_font = Font(color='FF0000')
    # for row in worksheet.iter_rows():
    #     for cell in row:
    #         if cell.value == 'USA':
    #             cell.font = red_font
    # # Save the workbook
    # writer.save()
    # df = pd.DataFrame({'col1': [1, 2, 3],
    #                 'col2': [4, 5, 6],
    #                 'col3': [7, 8, 9]})
    # df.to_excel("test.xlsx", index=False, engine="openpyxl", 
    #             header=True, startrow=1, freeze_panes=(1, 1))
    # df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]})
    # # 데이터프레임을 엑셀 파일로 저장
    # df.to_excel("output.xlsx", index=False)
    # worksheet.autofilter(0, 0, max_row, max_col - 1)
