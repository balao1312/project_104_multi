import redis
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup


def one_page_scraping(url, timestamp, page):
    specialty_dict = {}  # 字典存技能統計
    edu_req_dict = {'高中以上': 0, '專科以上': 0, '大學以上': 0, '碩士以上': 0, '不拘': 0}  # 字典存學歷需求
    major_req_dict = {}  # 字典存科系要求
    count = 0  # 資料總筆數

    ss = requests.session()
    ss.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/' \
                               '537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    res = ss.post(url, timeout=10)
    soup = BeautifulSoup(res.text, 'lxml')
    job_name_list = soup.select('article', class_="js-job-item")

    result_list = []
    for job in job_name_list:
        try:
            comp_name = job['data-cust-name']
            job_name = job['data-job-name']

            detail_link = 'http:' + job.select_one('a', class_='js-job-link')['href']

            # 取得細項網址
            detail_code = detail_link.split('/')[-1].split('?')[0]
            detail_link_oo = 'https://m.104.com.tw/job/' + detail_code

            # print(detail_link_oo)
            print(comp_name)
            print(job_name)
            print(detail_link)
            print(detail_link_oo)

            res = ss.post(detail_link_oo, timeout=10, allow_redirects=False)
            res = res.text
            # print(res)
            dfs = pd.read_html(res)
            # print(len(dfs))
            # for ii,dd in enumerate(dfs):
            #     print(ii)
            #     print(dd)
            #     print('-'*40)

            # 開始建細項list
            detail_list = [comp_name, job_name]  # 公司名稱、職缺名稱

            detail_list.append(detail_link)  # 徵才網址

            detail_list.append(dfs[1].iat[0, 1][:-5])  # 薪水區間
            detail_list.append(dfs[0].iat[1, 1][-2:])  # 工作性質
            detail_list.append(dfs[0].iat[0, 1])  # 工作地點
            detail_list.append(dfs[2].iat[3, 1])  # 管理責任
            detail_list.append(dfs[2].iat[0, 1])  # 出差外派
            detail_list.append(dfs[2].iat[1, 1])  # 上班時段
            detail_list.append(dfs[2].iat[2, 1])  # 休假制度
            detail_list.append(dfs[3].iat[1, 1])  # 可上班日
            detail_list.append(dfs[0].iat[2, 1])  # 需求人數
            detail_list.append(dfs[3].iat[0, 1])  # 接受身份
            detail_list.append(dfs[3].iat[2, 1])  # 工作經歷
            detail_list.append(dfs[3].iat[3, 1])  # 學歷要求

            # 學歷要求統計
            if '不拘' in dfs[3].iat[3, 1]:
                edu_req_dict['不拘'] += 1
            elif '高中' in dfs[3].iat[3, 1]:
                edu_req_dict['高中以上'] += 1
            elif '專科' in dfs[3].iat[3, 1]:
                edu_req_dict['專科以上'] += 1
            elif '大學' in dfs[3].iat[3, 1]:
                edu_req_dict['大學以上'] += 1
            elif '碩士' in dfs[3].iat[3, 1]:
                edu_req_dict['碩士以上'] += 1

            # 科系要求
            ffilter = (dfs[3][0] == '科系要求：')
            # print(f'科系要求: \n{dfs[3][ff]}')
            if len(dfs[3][ffilter]):
                detail_list.append(dfs[3][ffilter].iat[0, 1])
                # 科系要求統計
                majors = dfs[3][ffilter].iat[0, 1].split('、')
                for major in majors:
                    if not major in major_req_dict:
                        major_req_dict[major] = 1
                    else:
                        major_req_dict[major] += 1
            else:
                detail_list.append('不拘')

            # 語文條件
            ffilter = (dfs[3][0] == '語文條件：')
            # print(f'科系要求: \n{dfs[3][ff]}')
            if len(dfs[3][ffilter]):
                detail_list.append(dfs[3][ffilter].iat[0, 1])
            else:
                detail_list.append('不拘')

            # 擅長工具
            ffilter = (dfs[3][0] == '擅長工具：')
            # print(f'科系要求: \n{dfs[3][ff]}')
            if len(dfs[3][ffilter]):
                detail_list.append(dfs[3][ffilter].iat[0, 1])
                # 擅長工具統計
                specialtys = dfs[3][ffilter].iat[0, 1].split('、')
                for specialty in specialtys:
                    if not specialty in specialty_dict:
                        specialty_dict[specialty] = 1
                    else:
                        specialty_dict[specialty] += 1
            else:
                detail_list.append('不拘')

        except Exception as e:
            print('======================')
            print('目標不符設定 錯誤內容 ： ')
            print(e)
            print('======================')
            continue
        count += 1
        # print(detail_list)
        result_list.append(detail_list)

        time.sleep(0.5)

    print(f'==> Get {count} records')
    # print(result_list)
    # print(specialty_dict)
    # print(edu_req_dict)
    # print(major_req_dict)

    # to reids
    q_key = f'{str(timestamp)}_{page}'
    value = {'count': count, 'result_list': result_list, 'specialty_dict': specialty_dict, 'edu_req_dict': edu_req_dict,
             'major_req_dict': major_req_dict}

    r = redis.Redis(host='172.105.202.99', port=6379)
    try:
        r.set(q_key, str(value))
    except Exception as e:
        print(e)
    print(f'==> result sent to redis, key= {q_key}\n')


if __name__ == '__main__':
    one_page_scraping(
        'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=資料工程&order=15&asc=0&page=1&mode=l&jobsource'
        '=2018indexpoc '
        , time.time()
        , 3)
