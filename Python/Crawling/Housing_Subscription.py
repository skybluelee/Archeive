from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium import webdriver
import time

# 년, 월 선택하기
def select_month(driver, year, month_select):
    time.sleep(1)
    content = driver.find_element(By.ID, "content")
    sub_content_box = content.find_element(By.CLASS_NAME, "sub_content_box")

    # 년 선택
    year = sub_content_box.find_element(By.CLASS_NAME, "cal_top")
    year_button = Select(year.find_element(By.ID, "sel_year"))
    try:
        year_button.select_by_value(str(year))
        time.sleep(1)
    except Exception as e:                             
        print("해당 년도 존재하지 않음", e) 
    
    # 월 선택
    month = sub_content_box.find_element(By.CLASS_NAME, "cal_bottom")
    month_button = month.find_elements(By.CSS_SELECTOR, "ul > li")
    month_button[month_select - 1].click()
    time.sleep(1)

def data_collect(driver):
    # 각 모집공고에 해당하는 데이터를 딕셔너리에 저장하고 초기화 진행       
    info_dict = {}         # 건물 정보
    appointment_dict = {}  # 청약 정보
    supply_dict = {}       # 공급 대상 정보
    etc_dict = {}          # 기타 정보

    h5_list = [] # 템플릿 저장 
    move_schedule = None # 입주 예정월 초기화 

    content_detail = driver.find_element(By.CLASS_NAME, "ui-dialog.ui-corner-all.ui-widget.ui-widget-content.ui-front.ui-draggable.pop_w_900")
    down_bar = content_detail.find_element(By.CLASS_NAME, "ui-dialog-content.ui-widget-content")        
    driver.switch_to.frame("iframeDialog") # iframe으로 들어가기        
    printArea = driver.find_element(By.ID, "printArea")

    # 입주예정월
    inde_txt = printArea.find_elements(By.CLASS_NAME, "inde_txt")
    for sent in inde_txt:
        if sent.text[:7] == '* 입주예정월':
            move_schedule = sent.text[10:17]

    # 입주자 모집 공고
    table_info = printArea.find_element(By.CLASS_NAME, "tbl_st.tbl_normal.tbl_center")
    tbody_info = table_info.find_element(By.TAG_NAME, 'tbody')
    for tr_info in tbody_info.find_elements(By.TAG_NAME, 'tr'):
        info_dict[tr_info.find_element(By.TAG_NAME, 'td').text] = tr_info.find_element(By.CLASS_NAME, 'txt_l').text

    thead_info = table_info.find_element(By.TAG_NAME, 'thead')

    # 건물 이름
    building_name = thead_info.text 
    info_dict['건물이름'] = building_name      

    # 입주자 모집 이외의 데이터 목록과 데이터
    # 각 템플릿이 존재하므로 탬플릿 별로 데이터 처리
    h5 = printArea.find_elements(By.CSS_SELECTOR, "h5")
    for data in h5:
        h5_list.append(data.text)
    h5_list = h5_list[1:]
    table_total = printArea.find_elements(By.CLASS_NAME, "tbl_st.tbl_row.tbl_col.tbl_center")

    for idx, value in enumerate(h5_list):
        # 청약 일정의 경우
        if value == '청약일정':
            # 청약일정은 템플릿의 index를 확인하는 thead값이 없음
            appoint_list = ['모집공고일', '청약접수', '당첨자 발표일', '계약일'] # 확인용 리스트
            appoint_data = [] # 청약 일정 관련 데이터
            for tbody in table_total[idx].find_elements(By.TAG_NAME, 'tbody'):
                for tr in tbody.find_elements(By.TAG_NAME, 'tr'):
                    appoint_data.append(tr.text) # 청약 일정 데이터 수집

            # 청약 접수 이외는 단순 데이터
            appointment_dict['모집공고일'] = appoint_data[0][6:16]
            appointment_dict['당첨자 발표일'] = appoint_data[-2][8:]
            appointment_dict['계약일'] = appoint_data[-1][4:]

            # 청약 접수 데이터
            # 구분이 없다면(바로 날짜가 온다면) 날짜 이외의 정보는 없음
            if appoint_data[1][6].isnumeric(): 
                appointment_dict['구분'] = ['구분없음']
                appointment_dict['전체지역'] = appoint_data[1][5:]
            # 날짜가 아닌 구분, 해당지역 등의 데이터가 있는 경우
            else: 
                type_list = appoint_data[1][5:].split()
                for app_num in range(2, len(appoint_data)-2):    
                    app_data = appoint_data[app_num].split()
                    for i in range(len(app_data)):
                        tmp = appointment_dict.get(type_list[i], [])
                        tmp.append(app_data[i])
                        appointment_dict[type_list[i]] = tmp
                # 구분을 PK로 사용하므로 없다면 추가
                if not appointment_dict['구분']:
                    appointment_dict['구분'] = ['구분없음']

        # 공급대상의 경우
        # 공급대상 이하의 모든 지표에서 계(합)은 SQL로 간단하게 구현 가능하고 계가 존재한다면 필터링해야 하므로 제외함
        # 또한 Not Null인 PK를 주택형을 만들었기에 타입의 경우 주택형으로 변경
        elif value == '공급대상':
            supply_target_data = [] # 전체 데이터
            supply_target_list = [] # 인덱스 확인

            # 공급 대상 데이터 수집
            for tbody in table_total[idx].find_elements(By.TAG_NAME, 'tbody'):
                for tr in tbody.find_elements(By.TAG_NAME, 'tr'):
                    supply_target_data.append(tr.text) 
            # 인덱스 수집
            for tbody in table_total[idx].find_elements(By.TAG_NAME, 'thead'):
                for tr in tbody.find_elements(By.TAG_NAME, 'tr'):
                    supply_target_list.append(tr.text)

            # 공급대상에 주택구분이 존재하는 경우 주택구분을 따로 저장하고 슬라이싱하여 데이터에서 제외
            if not supply_target_data[0][0].isnumeric(): 
                for num_idx, num_value in enumerate(supply_target_data[0]):
                    if num_value == ' ':
                        break
                supply_dict['주택구분'] = supply_target_data[0][:num_idx]
                supply_target_data[0] = supply_target_data[0][num_idx + 1:]

            # 예외처리 1               
            if supply_target_list == ['주택구분 군 타입 전용면적 공급세대수 주택관리번호(모델번호)']: # 오피스텔의 경우
                supply_target_list = ['군', '주택형', '주택공급면적', '공급세대_일반', '주택관리번호']
                for supply_target_num in range(len(supply_target_data)):
                    sup_target_data = supply_target_data[supply_target_num].split()
                    for i in range(5): 
                        tmp = supply_dict.get(supply_target_list[i], [])
                        tmp.append(sup_target_data[i])
                        supply_dict[supply_target_list[i]] = tmp

            # 예외처리 2
            elif supply_target_list[0] == '주택구분 군 타입 전용면적 공급세대수 주택관리번호(모델번호)':
                # 공급세대를 특별 공급 유형 + 일반으로 변형
                supply_target_list2 = supply_target_list[2].split()
                supply_target_list = ['군', '주택형', '전용면적']                  
                supply_target_list += supply_target_list2
                supply_target_list += ['공급세대_일반', '주택관리번호']
                for supply_target_num in range(len(supply_target_data)):
                    sup_target_data = supply_target_data[supply_target_num].split()
                    del sup_target_data[7] # 계를 제외
                    for i in range(len(supply_target_list)): 
                        tmp = supply_dict.get(supply_target_list[i], [])
                        tmp.append(sup_target_data[i])
                        supply_dict[supply_target_list[i]] = tmp
            # 대표 템플릿
            else: # supply_target_list[0] == '주택구분 주택형 주택공급면적 공급세대수 주택관리번호(모델번호)'
                supply_target_list = ['주택형', '주택공급면적', '공급세대_일반', '공급세대_특별', '주택관리번호']
                supply_target_data.pop() # 공급대상의 마지막 데이터는 공급세대수의 합이므로 제외
                for supply_target_num in range(len(supply_target_data)):
                    sup_target_data = supply_target_data[supply_target_num].split()
                    del sup_target_data[4] # 계를 제외
                    for i in range(5): 
                        tmp = supply_dict.get(supply_target_list[i], [])
                        tmp.append(sup_target_data[i])
                        supply_dict[supply_target_list[i]] = tmp

        # 특별공급 공급대상의 경우
        # 템플릿이 한 종류만 존재
        elif value == '특별공급 공급대상':
            supply_special_data = []
            for tbody in table_total[idx].find_elements(By.TAG_NAME, 'tbody'):
                for tr in tbody.find_elements(By.TAG_NAME, 'tr'):
                    supply_special_data.append(tr.text) # 특별공급 공급대상 데이터 수집
            
            supply_special_list = ['다자녀가구', '신혼부부', '생애최초', '청년', '노부모부양', '기관추천', '이전기관', '기타']

            for supply_special_num in range(len(supply_special_data)):
                sup_special_data = supply_special_data[supply_special_num].split()
                del sup_special_data[0] # 주택형은 중복이니 제외
                del sup_special_data[8] # 계 제외
                for i in range(8): 
                    tmp = supply_dict.get(supply_special_list[i], [])
                    tmp.append(sup_special_data[i])
                    supply_dict[supply_special_list[i]] = tmp       
            
        # 공급금액, 2순위 청약금 및 입주예정월의 경우
        # 템플릿은 한가지만 존재
        # 2순위의 경우 존재하는 경우를 대비하여 내부에 str값이 있다면 Null이 되도록 설정
        elif value == '공급금액, 2순위 청약금 및 입주예정월':
            supply_cost_data = []
            for tbody in table_total[idx].find_elements(By.TAG_NAME, 'tbody'):
                for tr in tbody.find_elements(By.TAG_NAME, 'tr'):
                    supply_cost_data.append(tr.text) # 공급금액, 2순위 청약금 및 입주예정월 데이터 수집
            
            supply_cost_list = ['공급금액', '2순위청약금']

            for supply_cost_num in range(len(supply_cost_data)):
                sup_cost_data = supply_cost_data[supply_cost_num].split()
                del sup_cost_data[0] # 주택형은 중복이니 제외
                for i in range(2):
                    try: 
                        # 2순위 청약금의 경우 청약금이 존재하지 않는 경우 str값이 저장됨
                        # 청약금의 경우 type이 int이므로 2순위 청약금이 존재하지 않는 경우 Null값이 되도록 설계
                        tmp = supply_dict.get(supply_cost_list[i], [])
                        tmp.append(sup_cost_data[i])
                        supply_dict[supply_cost_list[i]] = tmp  
                    except:
                        pass       
            
            # 2순위 청약금이 '청약통장으로 청약(청약금 없음)' 인 경우
            if not supply_dict['2순위청약금'][0][0].isnumeric():
                # table에 Null이 나오도록 설계
                supply_dict['2순위청약금'] = ['Null'] * len(supply_cost_data)

        # 공급내역 및 입주예정월의 경우
        # 비고는 중요하지 중요하지 않다고 판단하여 생략
        elif value == '공급내역 및 입주예정월':
            supply_content_data = []
            supply_content_list = []
            for tbody in table_total[idx].find_elements(By.TAG_NAME, 'tbody'):
                for tr in tbody.find_elements(By.TAG_NAME, 'tr'):
                    supply_content_data.append(tr.text) # 공급내역 및 입주예정월 데이터 수집
            for thead in table_total[idx].find_elements(By.TAG_NAME, 'thead'):
                for tr in thead.find_elements(By.TAG_NAME, 'tr'):
                    supply_content_list.append(tr.text) # 공급금액 및 입주예정월 인덱스 수집
                                
            if supply_content_list == ['주택형 공급세대수 비고']:  
                # 주택형(PK)이 없는 경우
                if supply_dict.get('주택형', None) == None:                   
                    for supply_content_num in range(len(supply_content_data)):
                        sup_content_data = supply_content_data[supply_content_num].split()
                        # 비고는 생략
                        if len(sup_content_data) >= 3:
                            sup_content_data = sup_content_data[:2]
                        
                        supply_content_list = ['주택형', '공급세대_일반']
                        for i in range(2):
                            tmp = supply_dict.get(supply_content_list[i], [])
                            tmp.append(sup_content_data[i])
                            supply_dict[supply_content_list[i]] = tmp  
                # 주택형(PK)이 있는 경우
                else:       
                    for supply_content_num in range(len(supply_content_data)):
                        sup_content_data = supply_content_data[supply_content_num].split()
                        # 비고는 생략
                        if len(sup_content_data) >= 3:
                            sup_content_data = sup_content_data[:2]    

                        del sup_content_data[0] # 주택형은 중복이니 제외
                        supply_content_list = ['공급세대_일반']
                        for i in range(1): # 비고는 생략
                            tmp = supply_dict.get(supply_content_list[i], [])
                            tmp.append(sup_content_data[i])
                            supply_dict[supply_content_list[i]] = tmp  

            elif supply_content_list == ['주택형 공급금액(최고가 기준) 입주예정월']:
                # 입주예정월
                move_schedule = supply_content_data[0][-7:]
                supply_content_data[0] = supply_content_data[0][:-7]  

                # 주택형(PK)이 없는 경우
                if supply_dict.get('주택형', None) == None: 
                    supply_content_list = ['주택형', '공급금액']
                    for i in range(2):
                        tmp = supply_dict.get(supply_content_list[i], [])
                        tmp.append(sup_content_data[i])
                        supply_dict[supply_content_list[i]] = tmp 
                # 주택형이 있는 경우
                else:   
                    supply_content_list = ['공급금액']                
                    for supply_content_num in range(len(supply_content_data)):  
                        sup_content_data = supply_content_data[supply_content_num].split()
                        del sup_content_data[0] # 주택형은 중복이니 제외
                        for i in range(1): 
                            tmp = supply_dict.get('공급금액', [])
                            tmp.append(sup_content_data[i])
                            supply_dict[supply_content_list[i]] = tmp    

        # 공급금액 및 입주예정월의 경우
        elif value == '공급금액 및 입주예정월':
            supply_cost2_data = []
            supply_cost2_list = []
            for tbody in table_total[idx].find_elements(By.TAG_NAME, 'tbody'):
                for tr in tbody.find_elements(By.TAG_NAME, 'tr'):
                    supply_cost2_data.append(tr.text) # 공급금액 및 입주예정월 데이터 수집      
            for tbody in table_total[idx].find_elements(By.TAG_NAME, 'thead'):
                for tr in tbody.find_elements(By.TAG_NAME, 'tr'):
                    supply_cost2_list.append(tr.text) # 공급금액 및 입주예정월 인덱스 수집              

            if supply_cost2_list == ['군 타입 공급금액 청약신청금']:
                supply_cost2_list = ['공급금액', '청약신청금']
                for supply_cost2_num in range(len(supply_cost2_data)):
                    sup_cost2_data = supply_cost2_data[supply_cost2_num].split()
                    del sup_cost2_data[0] # 군은 중복이니 제외
                    del sup_cost2_data[0] # 타입 또한 중복이니 제외
                    for i in range(2): 
                        tmp = supply_dict.get(supply_cost2_list[i], [])
                        tmp.append(sup_cost2_data[i])
                        supply_dict[supply_cost2_list[i]] = tmp  
                                                    
        # 기타사항의 경우
        elif value == '기타사항':
            etc_data = []
            etc_list = []
            for tbody in table_total[idx].find_elements(By.TAG_NAME, 'tbody'):
                for tr in tbody.find_elements(By.TAG_NAME, 'tr'):
                    for td in tbody.find_elements(By.TAG_NAME, 'td'):
                        etc_data.append(td.text) # 기타사항 데이터 수집
            for thead in table_total[idx].find_elements(By.TAG_NAME, 'thead'):
                for tr in thead.find_elements(By.TAG_NAME, 'th'):
                    etc_list.append(tr.text)

            for i in range(len(etc_list)):
                etc_dict[etc_list[i]] = etc_data[i]

    driver.switch_to.default_content()

    return info_dict, appointment_dict, supply_dict, etc_dict, move_schedule

driver = webdriver.Chrome()
driver.get("https://www.applyhome.co.kr/ai/aib/selectSubscrptCalenderView.do")

select_month(driver, 2023, 7)

content = driver.find_element(By.ID, "content")
sub_content_box = content.find_element(By.CLASS_NAME, "sub_content_box")
cal_wrap = sub_content_box.find_element(By.CLASS_NAME, "cal_wrap")
calTable = cal_wrap.find_element(By.ID, "calTable")
tbody = calTable.find_element(By.TAG_NAME, 'tbody')
for tr in tbody.find_elements(By.TAG_NAME, 'tr'):
    # 각 포스트별로 초기화
    a = tr.find_elements(By.TAG_NAME, 'a')
    for build in a:
        build.click() # 공고 내용 확인
        time.sleep(1)

        content_detail = driver.find_element(By.CLASS_NAME, "ui-dialog.ui-corner-all.ui-widget.ui-widget-content.ui-front.ui-draggable.pop_w_900")
        info_dict, appointment_dict, supply_dict, etc_dict, move_schedule = data_collect(driver)

        upper_bar = content_detail.find_element(By.CLASS_NAME, "ui-dialog-titlebar.ui-corner-all.ui-widget-header.ui-helper-clearfix.ui-draggable-handle")
        exit_button = upper_bar.find_element(By.CLASS_NAME, "ui-button.ui-corner-all.ui-widget.ui-button-icon-only.ui-dialog-titlebar-close")
        exit_button.click()              
