#!/usr/bin/python
# -*- coding: utf-8 -*-

import csvfilter
import pathlib
import time
import visualize as v
from flask import Flask, request, render_template
from web_scraping import web_scraping, web_scraping_demo

app = Flask(__name__, static_url_path='/static', static_folder='./static')
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1  # 設置瀏覽器不緩存

occupied = False


@app.route('/', methods=['GET', 'POST'])
def start_here():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        global occupied
        if occupied:
            return render_template('hold.html')
        occupied = True
        start_time = time.time()  # 計時的開始時間

        demo = request.form.get('sample')

        if demo == 'on':
            keyword = '資料工程'
            pages = 20
            returned_dict = web_scraping_demo()
        else:
            keyword = request.form.get('keyword').replace(' ', '_')  # 從表格中取得使用者輸入
            pages = int(request.form.get('pages'))
            returned_dict = web_scraping(keyword, pages)  # 從爬蟲函式取得排名名單 呼叫畫圖函式

        try:
            v.visualize_pie(returned_dict['specialty_dict_sorted'], keyword, returned_dict['count'], pages)
            v.visualize_barh(returned_dict['major_req_dict_sorted'], keyword, returned_dict['count'], pages)
            v.visualize_bar(returned_dict['edu_req_dict_sorted'], keyword, returned_dict['count'], pages)
            count = returned_dict['count']
        except:
            return render_template('error.html')

        # 把表格中的每個欄位checkbox取得後存在 show_column 的 list 變數 (有勾的值會是 'on'，沒勾是 None)
        # 再呼叫 csv_filter 函式去生成一個新的使用者客製的表格

        select_all = request.form.get('selectAll')

        if select_all == 'on':
            show_column = ['on' for x in range(18)]
        else:
            job_name = request.form.get('job_name')
            detail_link = request.form.get('detail_link')
            salary = request.form.get('salary')
            jobType = request.form.get('jobType')

            workloc = request.form.get('workloc')
            manageResp = request.form.get('manageResp')
            businessTrip = request.form.get('businessTrip')
            workPeriod = request.form.get('workPeriod')
            vacationPolicy = request.form.get('vacationPolicy')

            startWorkingDay = request.form.get('startWorkingDay')
            needEmp = request.form.get('needEmp')
            role = request.form.get('role')
            workExp = request.form.get('workExp')
            edu = request.form.get('edu')

            major = request.form.get('major')
            language = request.form.get('language')
            specialty = request.form.get('specialty')
            # skill = request.form.get('skill')  # 失效

            # 原始表格有18欄，公司名設定成永遠顯示，所以設'on'
            show_column = ['on', job_name, detail_link, salary, jobType,
                           workloc, manageResp, businessTrip, workPeriod, vacationPolicy,
                           startWorkingDay, needEmp, role, workExp, edu,
                           major, language, specialty]

        if demo == 'on':
            filter_csv = csvfilter.sample()
        else:
            filter_csv = csvfilter.csv_filter(show_column, keyword, pages)

        end_time = time.time()  # 計時的結束時間
        total_time = end_time - start_time
        print(f'total time spent : {total_time:.4f} seconds')
        occupied = False
        return render_template('result.html', total_time=total_time, keyword=keyword, filter_csv=filter_csv, count=count, pages=pages)
        # 導向結果網頁，把需要的變數一併傳出


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
