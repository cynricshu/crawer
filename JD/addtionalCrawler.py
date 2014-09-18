'''
Created on Jul 5, 2013

@author: george.g.zhao
'''

import os
import time
import urllib2 as ulib2
from random import shuffle
from collections import defaultdict

import bs4

import settings


logger = settings.logger


def itemAnalyzer(category, itemid):
    if int(itemid) in settings.ITEMS: return True
    record_writer = open(settings.FILEPATH + category + '/' + itemid + '.txt', 'w')
    url = settings.COMMENTS_URL_FORMAT % (itemid, 1)
    try:
        html_doc = ulib2.urlopen(url).read()
        parser = bs4.BeautifulSoup(html_doc)
        parser.encode('gb2312')
        product_name = parser.body.find('div', id='product-info').find('li', attrs={'class': 'p-name'}).find('a').text
        comments_num = parser.body.find('div', id='comments-list').find('div', attrs={'class': 'mt'}).find('li', attrs={
        'class': 'curr', 'scoe': '0'}).find('em').text[1:-1]
        num_page = (int(comments_num) + 29) / 30
        for i in range(num_page):
            if i:  # not page 0
                url = settings.COMMENTS_URL_FORMAT % (itemid, i + 1)
                html_doc = ulib2.urlopen(url).read()
                parser = bs4.BeautifulSoup(html_doc)
                parser.encode('gb2312')
            comments = parser.body.find('div', id='comments-list').find_all('div', attrs={'class': 'item'})
            for comment in comments:
                userid = comment.find('div', attrs={'class': 'user'}).find('div', attrs={'class': 'u-name'}).find('a')[
                    'href'].split('/')[-1].split('-')[0]
                rating = comment.find('div', attrs={'class': 'o-topic'}).find('span')['class'][1][2:]
                comment_content = '::'.join(
                    [i.strip() for i in comment.find('div', attrs={'class': 'comment-content'}).strings if i.strip()])
                record_writer.write('%s\t%s\n' % (userid, rating))
                record_writer.write(comment_content + '\n')
        record_writer.close()
        settings.ITEMS.add(int(itemid))
        settings.ITEMS_OUT.write('%s::%s\n' % (itemid, product_name))
        return True
    except:
        print 'ERROR: %s:%s,%s ' % (time.ctime(), category, itemid)
        return False


if __name__ == '__main__':
    dic = defaultdict()
    for line in open('itemsToBeCrawled.txt'):
        x, y = line[:-1].split(',')
        dic[int(y)] = (x, y, 0)
    items = [(t[0], t[1]) for t in dic.viewvalues() if t[2] < 20]
    while items:
        for item in items:
            print '%s:crawl item %s,%s' % (time.ctime(), item[0], item[1])
            if not itemAnalyzer(item[0], item[1]):
                dic[int(item[1])] = (item[0], item[1], dic[int(item[1])][2] + 1)
        items = [(t[0], t[1]) for t in dic.viewvalues() if t[2] < 20]
        shuffle(items)
    settings.ITEMS_OUT.close()
    items = [(t[0], t[1]) for t in dic.viewvalues() if t[2] < 20]
    od = open('left_items.txt', 'w')
    for item in items:
        od.write('%s,%s\n' % (item[0], item[1]))
    od.close()
                
            