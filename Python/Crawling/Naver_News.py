from selenium.webdriver.common.by import By
import time

# 출판사, 제목, 기자, 본문, 댓글창
def main(driver, num):
    time.sleep(10)
    total = driver.find_element(By.CLASS_NAME, "end_container")
    title_area = total.find_element(By.CLASS_NAME, "newsct_wrapper._GRID_TEMPLATE_COLUMN._STICKY_CONTENT")
    title_info = title_area.find_element(By.CLASS_NAME, "media_end_head_title")
    title = title_info.text
    pub_info = title_area.find_element(By.CLASS_NAME, "media_end_head_top")
    pub = pub_info.find_element(By.CSS_SELECTOR, "img").get_attribute("title")
    rep_info = title_area.find_element(By.CLASS_NAME, "media_end_head_journalist")
    reporter = rep_info.text
    article_info = title_area.find_element(By.ID, "dic_area")
    article = article_info.text
    input_area = title_area.find_element(By.CLASS_NAME, "media_end_head_info_datestamp")
    input_area2 = input_area.find_element(By.CLASS_NAME, "media_end_head_info_datestamp_bunch")
    input_time = input_area2.find_element(By.CSS_SELECTOR, "span").get_attribute("data-date-time")
    try: # 호감순 댓글 확인 가능
        more_comments = title_area.find_element(By.CLASS_NAME, "u_cbox_btn_view_comment")
        comment_exposed = 'yes'
    except: # 댓글 확인 불가
        more_comments = title_area.find_element(By.CLASS_NAME, "simplecmt_link.is_navercomment")
        comment_exposed = 'no'
    time.sleep(1)
    more_comments.click()


# 더보기 클릭
def more_comments(driver):
    comment_area = driver.find_element(By.CLASS_NAME, "newsct_wrapper._GRID_TEMPLATE_COLUMN._STICKY_CONTENT")
    total_comment = comment_area.find_element(By.ID, "cbox_module")
    time.sleep(0.5)
    see_more = total_comment.find_element(By.CLASS_NAME, "u_cbox_paginate")
    see_more.click()

# 댓글 통계
def comments_analysis(driver, title, sql_num):
    comment_area = driver.find_element(By.CLASS_NAME, "newsct_wrapper._GRID_TEMPLATE_COLUMN._STICKY_CONTENT")
    total_comment = comment_area.find_element(By.ID, "cbox_module")
    time.sleep(0.5)
    try:
        comments_num = total_comment.find_element(By.CLASS_NAME, "u_cbox_wrap.u_cbox_ko.u_cbox_type_sort_new")
    except:
        comments_num = total_comment.find_element(By.CLASS_NAME, "u_cbox_wrap.u_cbox_ko.u_cbox_type_sort_favorite")
    comments_cnt = comments_num.find_element(By.CLASS_NAME, "u_cbox_comment_count_wrap")
    comments = comments_cnt.find_elements(By.CSS_SELECTOR, "ul > li")
    total = comments[0].find_elements(By.CSS_SELECTOR, "span")[0].text
    self_removed = comments[1].find_elements(By.CSS_SELECTOR, "span")[0].text
    auto_removed = comments[2].find_elements(By.CSS_SELECTOR, "span")[0].text

    male, female, age_10, age_20, age_30, age_40, age_50, age_60 = -1, -1, -1, -1, -1, -1, -1, -1
    try:
        comments_two = comments_num.find_element(By.CLASS_NAME, "u_cbox_chart_wrap.u_cbox_chart_open")
        comments_sex_age = comments_two.find_element(By.CLASS_NAME, "u_cbox_chart_cont_inner")
        comments_sex = comments_sex_age.find_element(By.CLASS_NAME, "u_cbox_chart_sex")
        comments_male = comments_sex.find_element(By.CLASS_NAME, "u_cbox_chart_progress.u_cbox_chart_male")
        male = comments_male.find_elements(By.CSS_SELECTOR, "span")[0].text[:-1]
        comments_female = comments_sex.find_element(By.CLASS_NAME, "u_cbox_chart_progress.u_cbox_chart_female")
        female = comments_female.find_elements(By.CSS_SELECTOR, "span")[0].text[:-1]

        comments_age = comments_sex_age.find_element(By.CLASS_NAME, "u_cbox_chart_age")
        comments_age_total = comments_age.find_elements(By.CLASS_NAME, "u_cbox_chart_progress")
        age_list = []
        for i in comments_age_total:
            age_list.append(i.text[:-5])
        age_10, age_20, age_30, age_40, age_50, age_60 = age_list[0], age_list[1], age_list[2], age_list[3], age_list[4], age_list[5][:-1]
    except:
        pass


# 전체 댓글 수집
def comments(driver, title, timestamp, sql_num, input_time):
    comment_area = driver.find_element(By.CLASS_NAME, "newsct_wrapper._GRID_TEMPLATE_COLUMN._STICKY_CONTENT")
    total_comments = comment_area.find_element(By.ID, "cbox_module")
    total_comment = total_comments.find_element(By.ID, "cbox_module_wai_u_cbox_content_wrap_tabpanel")
    comments = total_comment.find_elements(By.CSS_SELECTOR, "li")
    for i in comments:
        comment = i.find_element(By.CLASS_NAME, "u_cbox_text_wrap").text
        if comment != '클린봇이 부적절한 표현을 감지한 댓글입니다.' and comment != '작성자에 의해 삭제된 댓글입니다.' and comment != '운영규정 미준수로 인해 삭제된 댓글입니다.' :
            comment = comment
            good_bad = i.find_element(By.CLASS_NAME, "u_cbox_recomm_set")
            good_bads = good_bad.find_elements(By.CSS_SELECTOR, "a > em")
