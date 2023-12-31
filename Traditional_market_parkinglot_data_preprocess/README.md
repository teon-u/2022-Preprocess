# 전통시장 주차장 분석 프로젝트
| 데이터 정제, 전처리, 시각화
## Description
경기도의 수시 데이터 분석 과제로, ㅇㅇ시 전통시장 주차장에 대한 분석을 의뢰받았다.

분석결과는 해당 주차장의 증축과 요금체계 검토, 전통시장 이용률 확인에 활용되었다.

분석 결과물 : https://teon-u.notion.site/0cb220588ac24852bcbb894a1bf192fb?pvs=4

## Process
1. 인터뷰 및 요구사항 정의
    - 분석목적을 인터뷰하고 그에 따른 요구사항을 제안, 협의해 정의
2. 데이터 확인 및 분석방법 기획
    - 각 차량별 입차, 출차, 과금유형 등 데이터로 구성
    - 주차장 혼잡도 분석을 위해 시계열 데이터로 변형해 활용하는 방안
3. 데이터 정제 및 병합
    - 오류데이터 검증 및 이상치 처리, data 폴더의 데이터 병합
4. 특성공학
    - 원 데이터에 전통시장 방문여부에 대한 정보는 없으나, 주차시간 대비 요금정보를 토대로 방문할인 적용 여부 검증 가능
    - 전통시장 주차장 담당자 및 ㅇㅇ시 주무관과 검토하여 방문여부 분류 기준 수립
5. 시계열 데이터 생성
    - 매 시간, 분 당 입차중인 차량, 주차중인 차량, 출차중인 차량 등을 나타낸 별도 데이터 생성
6. 데이터 추출
    - 1_original.csv : 원본 전처리 데이터
    - 2_time_hour.csv : 시단위 생성 데이터
    - 3_time_minute.csv : 분단위 생성 데이터
7. 시각화
    - Looker Studio 활용한 시각화
    - (https://lookerstudio.google.com/reporting/b03a6cba-460f-47bf-8d80-871d69065cb4)

## Usage

```bash
pip install -r requirements.txt
python market-parking_preprocess.py
```
