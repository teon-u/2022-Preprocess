"""  User Variable  """
location_list = ["군포", "파주", "화성"]

"""  0. 데이터 호출 및 입력  """
print("\n[0. 데이터 호출 및 입력]")
import time
start = time.time() #실행시간 측정
import pandas as pd
import numpy as np
from datetime import timedelta
from datetime import datetime
import os
dir = os.path.dirname(os.path.abspath(__file__)) # 경로설정
print("    현재경로 :",dir)

for location in location_list:
    print("\n\n    <<<"+location+">>>")
    df = pd.read_excel(dir +'/Data/signal_guide/'+ location +'_구급_우선신호_버퍼_교차.xlsx')


    """  1. Time  """
    print("\n   [1. Time 컬럼 생성]")
    # move_date 에서 시간만 추출
    temp_list = []
    for i in range(len(df)):
        temp = df['move_date'][i]
        temp_list.append(str(temp)[11:])

    #print("Base Row :",len(df))
    #print("Made Row :",len(temp_list))
    df['time'] = temp_list


    """  2. 시간구분  """
    print("\n   [2. 시간구분 컬럼 생성]")
    # time 값에 따라 분류
    temp_list = []
    for i in range(len(df)):
        temp = df['time'][i]
        temp = timedelta(hours=int(temp[:2]), minutes=int(temp[3:5]), seconds=int(temp[6:]))
        if (temp>=timedelta(hours=11)) & (temp<timedelta(hours=14)):
            temp_list.append("점심")
        elif (temp>=timedelta(hours=17)) & (temp<timedelta(hours=20)):
            temp_list.append("퇴근")
        elif ((temp>=timedelta(hours=20)) & (temp<timedelta(hours=24)) or temp<timedelta(hours=7)):
            temp_list.append("일몰")
        elif (temp>=timedelta(hours=7)) & (temp<timedelta(hours=10)):
            temp_list.append("출근")
        else:
            temp_list.append("낮")
        
    #print("Base Row :",len(df))
    #print("Made Row :",len(temp_list))
    df['시간구분'] = temp_list


    """  3. Total_time  """
    print("\n   [3. Total_time 컬럼 생성]")
    temp_list = []
    for i in range(len(df)):
        temp = pd.Timestamp(df['field_arrive'][i])
        temp_list.append(temp - df['move_date'][i])

    #print("Base Row :",len(df))
    #print("Made Row :",len(temp_list))
    df['total_time2'] = temp_list


    """  4. time2  """
    print("\n   [4. time2 컬럼 생성]")
    # date 에서 시간 추출 + date 형태 변환
    import datetime
    temp_list = []
    temb_list = []
    for i in range(len(df)):
        temp = (datetime.datetime.strptime('1899-12-30', '%Y-%m-%d') + datetime.timedelta(df['date'][i])).strftime('%Y-%m-%d %H:%M:%S')
        temp_list.append(temp)
        temb_list.append(str(temp)[11:])
        
    #print("Base Row :",len(df))
    #print("Made Row_1 :",len(temp_list))
    #print("Made Row_2 :",len(temb_list))
    df['date'] = temp_list
    df['time2'] = temb_list


    """ 5. 시간구분2  """
    print("\n   [5. 시간구분2 컬럼 생성]")
    # time2 값에 따라 분류
    temp_list = []
    for i in range(len(df)):
        temp = df['time2'][i]
        temp = timedelta(hours=int(temp[:2]), minutes=int(temp[3:5]), seconds=int(temp[6:]))
        if (temp>=timedelta(hours=11)) & (temp<timedelta(hours=14)):
            temp_list.append("점심")
        elif (temp>=timedelta(hours=17)) & (temp<timedelta(hours=20)):
            temp_list.append("퇴근")
        elif ((temp>=timedelta(hours=20)) & (temp<timedelta(hours=24)) or temp<timedelta(hours=7)):
            temp_list.append("일몰")
        elif (temp>=timedelta(hours=7)) & (temp<timedelta(hours=10)):
            temp_list.append("출근")
        else:
            temp_list.append("낮")
        
    #print("Base Row :",len(df))
    #print("Made Row :",len(temp_list))
    df['시간구분2'] = temp_list


    """  6. 소요시간  """
    print("\n   [6. 소요시간 컬럼 생성]")
    # total_time2 - total_time
    temp_list = []
    for i in range(len(df)):
        temp = datetime.timedelta(df['total_time'][i])
        temp_list.append(df['total_time2'][i] - temp)

    #print("Base Row :",len(df))
    #print("Made Row :",len(temp_list))
    df['소요시간'] = temp_list


    """  7. 동일시간  """
    print("\n   [7. 동일시간 컬럼 생성]")
    # 시간구분 == 시간구분2
    temp_list = []
    for i in range(len(df)):
        if df['시간구분'][i] == df['시간구분2'][i]:
            temp_list.append("TRUE")
        else:
            temp_list.append("FALSE")
    #print("Base Row :",len(df))
    #print("Made Row :",len(temp_list))
    df['동일시간'] = temp_list


    """  8. 지역  """
    print("\n   [8. 지역 컬럼 생성]")
    temp_list = []
    for i in range(len(df)):
        temp_list.append(df['center'][i][:2])

    #print("Base Row :",len(df))
    #print("Made Row :",len(temp_list))
    df['지역'] = temp_list


    """  9. 지역2  """
    print("\n   [9. 지역2 컬럼 생성]")
    temp_list = []
    for i in range(len(df)):
        try: # 군포, 파주 테이블 처리 (Center_2 있음)
            temp = df['center_2'][i][:2]
        except: # 화성 테이블 처리 (Center_2 없음)
            temp = df['car_2'][i][:2]

        temp_list.append(temp)

    #print("Base Row :",len(df))
    #print("Made Row :",len(temp_list))
    df['지역2'] = temp_list


    """  10. 동일지역  """
    print("\n   [10. 동일지역 컬럼 생성]")
    temp_list = []
    for i in range(len(df)):
        if df['지역'][i] == df['지역2'][i]:
            temp_list.append("TRUE")
        else:
            temp_list.append("FALSE")

    #print("Base Row :",len(df))
    #print("Made Row :",len(temp_list))
    df['동일지역'] = temp_list


    """  11. 결과출력  """
    print("\n   [11. 데이터 저장]")
    print("    저장경로 :",dir+'/Data/signal_guide/' + location + '_구급_우선신호_버퍼_교차_시간차.xlsx')
    df = df.set_index('no')
    with pd.ExcelWriter(dir +'/Data/signal_guide/' + location + '_구급_우선신호_버퍼_교차_시간차.xlsx') as writer:
        df.to_excel(writer, sheet_name = location +'_구급_우선신호_버퍼_교차')
        df[df['동일시간']=="TRUE"].to_excel(writer, sheet_name = '동일시간')
        df[df['동일지역']=="TRUE"].to_excel(writer, sheet_name = '동일지역')


"""  12. 총 작업시간 출력  """
print("\n[12. 작업시간 출력]")
print("    작업시간 :",time.time()-start)