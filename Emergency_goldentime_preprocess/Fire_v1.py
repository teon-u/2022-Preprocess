"""  0. 데이터 호출 및 입력  """
print("\n[0. 데이터 호출 및 입력]")
import time
start = time.time() #실행시간 측정
import pandas as pd
import numpy as np
from datetime import timedelta
import os
dir = os.path.dirname(os.path.abspath(__file__)) # 경로설정
print("    현재경로 :",dir)
df = pd.read_excel(dir+'/Data/'+'2021_출동현황_화재_펌프차_중복제거_시간제거_최종.xlsx')
dfm = pd.read_excel(dir+'/Data/'+'mapping_table.xlsx')


"""  1. 시구분  """
print("\n[1. 시구분 컬럼 생성]")
temp_list = []
nan_count = 0
for i in df['loc']: # loc 컬럼 한바퀴 돌리기
    try:
        temp = i.split() # 단어단위로 분할
        temp_list.append(temp[1]) # 각 주소의 두번째 단어인 시 추출, 리스트 추가
    except:
        temp_list.append(np.nan) # 결측치 처리
        nan_count += 1 # 결측치 세기
print("    원본 컬럼의 결측치 :",nan_count)
print("    Base Row :",len(df['loc']))
print("    Made Row :",len(temp_list))
df['시구분'] = temp_list


"""  2. 도농구분  """
print("\n[2. 도농구분 컬럼 생성]")
# 도시 리스트
city_list = ['성남','분당','안양','광명','수원','수원남부','하남','부천','군포','구리','오산','의정부','안산','의왕','시흥','과천','동두천','일산','고양']
# 도농복합 리스트
dnbh_list = ['평택','송탄','포천','연천','양주','김포','남양주','파주','가평','용인','이천','안성','양평','여주','화성','광주']

temp_list = []
nan_count = 0
not_count = 0
for i in df['시구분']:
    try:
        if i[:-1] in city_list: # 도시 리스트 안에 있으면 도시, "성남시" 로 표현되어있어 "시" 제외
            temp_list.append("도시")
        elif i[:-1] in dnbh_list: # 도농복합 리스트 안에 있으면 도농복합
            temp_list.append("도농복합")
        else:
            temp_list.append("분류불가")
            not_count += 1
            #print(i) #디버그용
    except: # 위에서 에러나면 결측값 처리 (Float 자료형 등등)
        temp_list.append(np.nan)
        nan_count += 1
print("    원본 컬럼의 결측치 :",nan_count)
print("    분류 불가 :",not_count)
print("    Base Row :",len(df['시구분']))
print("    Made Row :",len(temp_list))
df['도농구분'] = temp_list

# 이상한 값
# row:14976 / column:loc / 1109(두산위브더스 101동 지하1층 방재실)
# row:24230 / column:loc / 0(강산타워 6층 604호)


""" 3. 1번  """
print("\n[3. 1번(구조 프로세스) 컬럼 생성]")
temp_list = []
nan_count = 0
for i in range(len(df)): # 데이터프레임 길이로 반복문 돌리기
    try:
        temp = df['move_order'][i] - df['start_date'][i] # move order 에서 start date 빼기
    except:
        temp = np.nan # 앞의 계산이 안되면 결측치 처리
        nan_count += 1
        
    temp_list.append(temp)

print("    원본 컬럼의 결측치 :",nan_count)
print("    Base Row :",len(df))
print("    Made Row :",len(temp_list))
df['1번'] = temp_list


"""  4. 2번  """
print("\n[4. 2번(구조 프로세스) 컬럼 생성]")
temp_list = []
nan_count = 0
for i in range(len(df)): # 데이터프레임 길이로 반복문 돌리기
    try:
        temp = df['move_date'][i] - df['move_order'][i] # move date 에서 move order 빼기
    except:
        temp = np.nan # 앞의 계산이 안되면 결측치 처리
        nan_count += 1
        
    temp_list.append(temp)

print("    원본 컬럼의 결측치 :",nan_count)
print("    Base Row :",len(df))
print("    Made Row :",len(temp_list))
df['2번'] = temp_list


"""  5. 3번  """
print("\n[5. 3번(구조 프로세스) 컬럼 생성]")
temp_list = []
nan_count = 0
for i in range(len(df)): # 데이터프레임 길이로 반복문 돌리기
    try:
        temp = df['field_arrive'][i] - df['move_date'][i] #  field arrive 에서 move date 빼기
    except:
        temp = np.nan # 앞의 계산이 안되면 결측치 처리
        nan_count += 1
        
    temp_list.append(temp)

print("    원본 컬럼의 결측치 :",nan_count)
print("    Base Row :",len(df))
print("    Made Row :",len(temp_list))
df['3번'] = temp_list


"""  6. 1+2+3  """
print("\n[6. 1+2+3(구조 프로세스 총 소요시간) 컬럼 생성]")
temp_list = []
nan_count = 0
for i in range(len(df)):
    try:
        temp = df['1번'][i] + df['2번'][i] + df['3번'][i] # 1+2+3번
    except:
        temp = np.nan # 앞의 계산이 안되면 결측치 처리
        nan_count += 1
    
    temp_list.append(temp)

print("    원본 컬럼의 결측치 :",nan_count)
print("    Base Row :",len(df))
print("    Made Row :",len(temp_list))
df['1+2+3'] = temp_list


"""  7. 골든타임여부  """
print("\n[7. 골든타임(7분이하)여부 컬럼 생성]")
golden_time = timedelta(days=0, hours=0, minutes=7)
temp_list = []
nan_count = 0
not_count = 0
for i in range(len(df)):
    try:
        if df['1+2+3'][i] <= golden_time:
            temp_list.append('유')
        elif df['1+2+3'][i] > golden_time:
            temp_list.append('무')
        else:
            temp_list.append('분류불가')
            not_count += 1
    except:
        temp_list.append(np.nan)
        nan_count += 1

print("    원본 컬럼의 결측치 :",nan_count)
print("    분류 불가 :",not_count)
print("    Base Row :",len(df['1+2+3']))
print("    Made Row :",len(temp_list))
df['골든타임여부'] = temp_list


"""  8. 3번에 감소율적용  """
print("\n[8. 감소율(도시 or 도농복합에 따른 출동시간 감소)적용 컬럼 생성]")
temp_list = []
nan_count = 0
not_count = 0
add1 = 22 # 도시
add2 = 33 # 도농복합
for i in range(len(df)):
    temp = df['3번'][i] # '3번' 값
    try:
        if df['도농구분'][i] == '도시':
            temp_list.append(temp - (temp * add1 / 100)) # 감소율 계산
        elif df['도농구분'][i] == '도농복합':
            temp_list.append(temp - (temp * add2 / 100)) # 감소율 계산
        else:
            temp_list.append("분류불가")
            #print("[시구분]:",df['시구분'][i],"/ [도농구분]:",df['도농구분'][i],"/ [3번값]",temp) #분류불가 워떤건지 Check
            not_count += 1
    except:
        temp_list.append(np.nan)
        nan_count += 1

print("    원본 컬럼의 결측치 :",nan_count) # '3번' 컬럼이 결측치인 경우
print("    분류 불가 :",not_count) # 도시나 도농복합이 아닌경우
print("    Base Row :",len(df))
print("    Made Row :",len(temp_list))
df['3번에 감소율적용'] = temp_list


"""  9. 1+2+3감소율  """
print("\n[9. 1+2+3감소율(감소율 적용된 총 출동시간) 컬럼 생성]")
temp_list = []
nan_count = 0
for i in range(len(df)):
    try:
        temp = df['1번'][i] + df['2번'][i] + df['3번에 감소율적용'][i] # 1+2+3번에 감소율적용
    except:
        temp = np.nan # 앞의 계산이 안되면 결측치 처리
        nan_count += 1
    
    temp_list.append(temp)

print("    원본 컬럼의 결측치 :",nan_count)
print("    Base Row :",len(df))
print("    Made Row :",len(temp_list))
df['1+2+3감소율'] = temp_list


"""  10. 골든타임여부2  """
print("\n[10. 골든타임여부2 컬럼 생성]")
golden_time = timedelta(days=0, hours=0, minutes=7)
temp_list = []
nan_count = 0
not_count = 0
for i in range(len(df)):
    try:
        if df['1+2+3감소율'][i] <= golden_time:
            temp_list.append('유')
        elif df['1+2+3감소율'][i] > golden_time:
            temp_list.append('무')
        else:
            temp_list.append('분류불가')
            not_count += 1
    except:
        temp_list.append(np.nan)
        nan_count += 1

print("    원본 컬럼의 결측치 :",nan_count)
print("    분류 불가 :",not_count)
print("    Base Row :",len(df['1+2+3감소율']))
print("    Made Row :",len(temp_list))
df['골든타임여부2'] = temp_list


"""  11. 가중치적용  """
print("\n[11. 가중치적용(각 시·군 별 출동시간 차이) 컬럼 생성]")
temp_list = []
nan_count = 0
mapping_dict = dfm.set_index('구분').T.to_dict('records')[0] # dfm(매핑테이블)을 딕셔너리 구조로 변경 {'이천시' : 0.0427}
for i in range(len(df)):
    try:
        weight = mapping_dict[df['시구분'][i][:3]] # 시별 가중치 추출
        temp = df['1+2+3감소율'][i] * weight + df['1+2+3감소율'][i] # 가중치 적용값 계산
        temp_list.append(temp)
    except:
        temp_list.append(np.nan)
        nan_count += 1
print("    원본 컬럼의 결측치 :",nan_count)
print("    Base Row :",len(df['1+2+3감소율']))
print("    Made Row :",len(temp_list))
df['가중치적용'] = temp_list


"""  12. 골든타임여부3  """
print("\n[12. 골든타임여부3 컬럼 생성]")
golden_time = timedelta(days=0, hours=0, minutes=7)
temp_list = []
nan_count = 0
not_count = 0
for i in range(len(df)):
    try:
        if df['가중치적용'][i] <= golden_time:
            temp_list.append('유')
        elif df['가중치적용'][i] > golden_time:
            temp_list.append('무')
        else:
            temp_list.append('분류불가')
            not_count += 1
    except:
        temp_list.append(np.nan)
        nan_count += 1

print("    원본 컬럼의 결측치 :",nan_count)
print("    분류 불가 :",not_count)
print("    Base Row :",len(df['가중치적용']))
print("    Made Row :",len(temp_list))
df['골든타임여부3'] = temp_list


"""  13. 데이터 출력  """
print("\n[13. 데이터 출력]")
df.to_excel(dir+'/Data/'+'output.xlsx')
print("    출력경로 :",dir+'/Data')


"""  14. 작업시간 출력  """
print("    작업시간 :",time.time()-start)