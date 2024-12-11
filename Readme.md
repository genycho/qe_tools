# Welcome to AI Platoform Team QE Tools Project

## This is several helping code to QE work

(1) make a sonarqube overview report(excel format) extracting information from sonarqube

(2) 


## Running this exercise locally
```
	execute the below pytest command in IDE terminal venv

```


## Local Setting Guide

### Prerequisites
install the following libraries:

* python3 -m venv venv # 파이썬 가상환경 만들기

* source ./venv/bin/activate # 가상환경 활성화

* pip install pytest


#어디까지 하다 말았는지 너무 뜨문뜨문해서 기억이 안 나서 여기에 기록하기. 

[1] [2024/11/01] get_dirpath 추가- 파일 업로드에서 파일 설정이 코드 생성 안 됨 
[2] [2024/11/01] 헤더에 키 설정하는 경우, 1회가 아니라 누적해서 추가됨. 어딘가 초기화가 안 되는 듯.... 
[3] [2024/11/01] API Platform 걸로 돌려보니 POST, json 바디 안에 생성이 안 됨. 바로 파라미터 밑에 생기니 이 코드 파싱 부분 추가. 
[4] [2024/11/01] test_post_v1files_notexistid / test_put_apikeyupdate_notexistid,  에서 not exist id가 준비되지 않음 
[5] DELETE 한정 - request_str <- api platform 걸로 돌려보니, operation id가 일괄 없음. 이때 api path를 