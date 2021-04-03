# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import praw
from praw.models import MoreComments
import pandas as pd
import csv

def reddit_scan():
    tickerlist = ['GME', 'AMC', 'SPCE', 'FUBO', 'BBBY', 'LGND', 'FIZZ', 'SPWR', 'SKT', 'GSX', 'TR', 'GOGO', 'AXDX',
                  'BYND', 'OTRK', 'CLVS', 'RKT', 'SRG', 'IRBT', 'PRTS', 'PGEN', 'TSLA']

    nameList = []

    postfix_2_remove = ['Inc.', 'Ltd.', 'Common Stock', 'Corporation', 'Incorporated', 'Companies', 'Ordinary Shares', 'Shares']

    with open('nasdaq_symbols_over_10B_cap.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            comp_name = row[1]

            if comp_name == 'Name':
                continue

            # remove from postfixes
            for postfix in postfix_2_remove:
                fn_res = comp_name.find(postfix)
                if fn_res != -1:
                    comp_name = comp_name[:fn_res]

            nameList.append(comp_name)

            print(comp_name)

    reddit = praw.Reddit(client_id='4hOsAKLbbGom3A',
                         client_secret ='VeLHJtXR3odB3F4zR_nbwFqtFDJVag',
                         username ='maxspplash',
                         password = '159852psf',
                         user_agent ='spplashscrap')
    subreddit = reddit.subreddit('wallstreetbets')

    hot = subreddit.new(limit=100)
    sum = [0] * len(nameList)  # our output array
    counttotal = 0  # total number of comment read
    submissions_counter = 0

    for submissions in hot:
        if not submissions.stickied:
            submissions_counter += 1
            if submissions_counter > 5:
                comments = submissions.comments
                for comment in comments:
                    if isinstance(comment, MoreComments):
                        continue
                    counttotal += 1
                    for i, ticker in enumerate(nameList):
                        if ticker in comment.body:
                            sum[i] = sum[i] + 1


    output = pd.DataFrame(data={'Tick': tickerlist, 'Counts': sum})
    print('Total comments read: ', counttotal)
    print(output[output['Counts'] > 0])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    reddit_scan()