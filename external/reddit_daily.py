import requests
from selenium import webdriver

from datetime import date,timedelta
from dateutil.parser import parse
import numpy as np
from collections import Counter

stocks_list = ['GME', 'AMC', 'SPCE', 'FUBO', 'BBBY', 'LGND', 'FIZZ', 'SPWR', 'SKT', 'GSX', 'TR', 'GOGO', 'AXDX',
                  'BYND', 'OTRK', 'CLVS', 'RKT', 'SRG', 'IRBT', 'PRTS', 'PGEN', 'TSLA']

#   https://chromedriver.chromium.org/downloads

def get_comments(comment_list):
    html = requests.get(f'https://api.pushshift.io/reddit/comment/search?ids{comment_list}&fields=body&size=1000')
    try:
        newcomments = html.json()
    except:
        print(html)

    return newcomments


def get_stock_list(newcomments, stocks_list):
    stock_dict = Counter()
    for a in newcomments['data']:
        for ticker in stocks_list:
            if ticker in a['body']:
                stock_dict[ticker] += 1
    return stock_dict

def grab_stock_count(stock_dict, raw_comment_list):
    orig_list = np.array(raw_comment_list['data'])
    comment_list = ",".join(orig_list[0:1000])
    remove_me = slice(0, 1000)
    cleaned = np.delete(orig_list, remove_me)
    i = 0
    while i < len(cleaned):
        print(len(cleaned))
        cleaned = np.delete(cleaned, remove_me)
        new_comments_list = ",".join(cleaned[0:1000])
        newcomments = get_comments(new_comments_list)
        for a in newcomments['data']:
            for ticker in stocks_list:
                if ticker in a['body']:
                    stock_dict[ticker] += 1
    stock = dict(stock_dict)
    return stock

def reddit_scan():
    url = 'https://www.reddit.com/r/wallstreetbets/search/?q=flair%3A%22Daily%20Discussion%22&restrict_sr=1&sort=new'
#    html = requests.get(url)
#    print(html.text)
    driver = webdriver.Chrome(executable_path=r'chromedriver.exe')
    driver.get(url)

    yesterday = date.today() - timedelta(days=4)
    links = driver.find_elements_by_xpath('//*[@class="_eYtD2XCVieq6emjKBH3m"]')
    link = ''
    for a in links:
        if a.text.startswith('Daily Discussion Thread'):
            dates = "".join(a.text.split(' ')[-3:])
            parsed = parse(dates)
            if parse(str(yesterday)) == parsed:
                link = a.find_element_by_xpath('../..').get_attribute('href')

        if a.text.startswith('Weekend'):
            weekend_date = a.text.split(' ')
            parsed_date = weekend_date[-3] + ' ' + weekend_date[-2].split("-")[1] + weekend_date[-1]
            parsed = parse(parsed_date)
            saturday = weekend_date[-3] + ' ' + str(int(weekend_date[-2].split("-")[1].replace(',','')) - 1) \
                       + ' ' + weekend_date[-1]

            if parse(str(yesterday)) == parsed:
                link = a.find_element_by_xpath('../..').get_attribute('href')

            elif parse(str(yesterday)) == parse(str(saturday)):
                link = a.find_element_by_xpath('../..').get_attribute('href')

    print (link)
    stock_link = link.split('/')[-3]
    html = requests.get(f'https://api.pushshift.io/reddit/submission/comment_ids/{stock_link}')
    raw_comment_list = html.json()
    driver.close()
    orig_list = np.array(raw_comment_list['data'])
    comment_list = ",".join(orig_list[0:1000])

    newcomments = get_comments(comment_list)
    stock_dict = get_stock_list(newcomments, stocks_list)
    stock = grab_stock_count(stock_dict, raw_comment_list)

    print(stock)

if __name__ == '__main__':
    reddit_scan()