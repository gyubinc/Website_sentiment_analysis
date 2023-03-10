import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

import re
import time

from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    text = p.sub(' ', str(data))
    text = text.replace('[', '')
    text = text.replace(']', '')
    text = text.replace('125610', '')
    text = ILLEGAL_CHARACTERS_RE.sub(r'', text)
    return text.strip()


def get_crawl(URL):
    response = driver.get(URL)
    html = driver.page_source
    soup7 = BeautifulSoup(html, 'html.parser')
    ex_id_divs_title = soup7.select('body > div > div:nth-child(7) > div > table.pic_bg > tbody > tr > td > span')
    ex_id_divs = soup7.select('#bonmoon > tbody > tr:nth-child(1) > td > div')
    ex_date = soup7.select('body > div > div:nth-child(7) > div > table:nth-child(13) > tbody > tr > td:nth-child(2) > span:nth-child(4)')

    ex_see = soup7.select('body > div > div:nth-child(7) > div > table:nth-child(13) > tbody > tr > td:nth-child(2) > span:nth-child(7) > span')
    ex_like = soup7.select_one('#div_chu_bbs > div').text
    ex_comment = soup7.select('body > div > div:nth-child(7) > div > table:nth-child(25) > tbody > tr > td.sm > div > b')

    crawl_data_title = remove_html_tags(ex_id_divs_title)

    crawl_data = remove_html_tags(ex_id_divs)
    crawl_data = crawl_data[:-40]

    crawl_date = remove_html_tags(ex_date)
    crawl_date = crawl_date[6:25]

    crawl_see = remove_html_tags(ex_see)
    crawl_like = remove_html_tags(ex_like)
    crawl_like = crawl_like[2:]

    crawl_comment = remove_html_tags(ex_comment)

    result = pd.DataFrame({'title': [crawl_data_title], 'text': [crawl_data], 'date': [crawl_date], 'see': [crawl_see], 'like': [crawl_like], 'comment': [crawl_comment]})
    return result


if __name__ == "__main__":
    driver.implicitly_wait(3)
    driver.get("https://www.koreapas.com/")
    print(driver.page_source)

    time.sleep(1)

    # 로그인 버튼 XPath
    login_x_path = '/html/body/div/div[5]/div[2]/div/table[2]/tbody/tr/td[2]/form/div/div/input'
    # ID 칸 css selector
    driver.find_element(By.CSS_SELECTOR, 'body > div > div:nth-child(7) > div:nth-child(2) > div > table:nth-child(2) > tbody > tr > td:nth-child(2) > form > table > tbody > tr:nth-child(1) > td:nth-child(1) > input').send_keys("id")
    time.sleep(1)
    # PW 칸 css selector
    driver.find_element(By.CSS_SELECTOR, 'body > div > div:nth-child(7) > div:nth-child(2) > div > table:nth-child(2) > tbody > tr > td:nth-child(2) > form > table > tbody > tr:nth-child(2) > td > input').send_keys("pass")
    time.sleep(1)
    driver.find_element(By.XPATH, login_x_path).click()
    time.sleep(3)

    # row 생략 없이 출력
    pd.set_option('display.max_rows', None)
    # col 생략 없이 출력
    pd.set_option('display.max_columns', None)

    print('\n' + '-' * 40 + '\n')
    df = pd.DataFrame({'title': [], 'text': [], 'date': [], 'see': [], 'like': [], 'comment': []})
    for i in range(1684000, 1683000, -1):

        try:
            main_url = "https://www.koreapas.com/bbs/view.php?id=mento&page=1&sn1=&divpage=322&sn=off&ss=on&sc=on&no=" + str(i)
            data = get_crawl(main_url)
            df = pd.concat([df, data])
            time.sleep(2)

        except:
            time.sleep(1)
            continue

    print(df)
    print(df.describe())
    df.describe()
    print(df.info())

    df.to_excel('이천개.xlsx', index=False)