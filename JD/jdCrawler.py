'''
Created on Jul 2, 2013

@author: george.g.zhao
'''
import os
import time
import bs4
import StringIO
import urllib2 as ulib2

import settings


logger = settings.logger
log = settings.logging



def l1Analyzer(l1id):
    if not os.path.exists(settings.FILEPATH+l1id):
        os.makedirs(settings.FILEPATH+l1id)
    current_path = settings.FILEPATH+l1id+'/'
    brand_code = open(current_path+'brand_code.txt','w')
    url = settings.LEVEL1_URL_FORMAT%l1id
    level2=[]
    try:
        html_doc = ulib2.urlopen(url).read()
        parser = bs4.BeautifulSoup(html_doc)
        brands= parser.body.find('dl',id='select-brand').find('div',attrs={'class':'content'}).find_all('a')
        for a in brands:
            a_url_s = a['href'].split('-')
            if not int(a_url_s[3])+int(a_url_s[4]):
                continue
            else:
                b_code='-'.join(a_url_s[:5])
                brand_code.write("'%s':'%s',\n"%(b_code,a.text))        
                level2.append(b_code)      
    except Exception, e:
        log.exception(e)
        log.info(url)
        logger.error(url)
    finally:
        brand_code.close()
    return level2


def l2Analyzer(l2id):
    url = settings.LEVEL2_URL_FORMAT%(l2id,1)
    items = []
    try:
        html_doc = ulib2.urlopen(url).read()
        parser = bs4.BeautifulSoup(html_doc)
        parser.encode('utf-8')
        num_of_pages = parser.body.find('div',attrs={'class':'fore1'}).find('span',attrs={'class':'text'}).contents[1].replace('/','')
        num_of_pages = int(num_of_pages)
        for i in range(num_of_pages):
            if i>0: #if page 0 no need to open url again
                url = settings.LEVEL2_URL_FORMAT%(l2id,i+1)
                html_doc = ulib2.urlopen(url).read()
                parser = bs4.BeautifulSoup(html_doc)
                parser.encode('utf-8')
            lis=parser.body.find('div',id='plist').find_all('li')
            for li in lis:
                num_comments = int(li.find('span',attrs={'class':'evaluate'}).find('a').text[4:-6])
                if num_comments<10:
                    continue
                items.append(li['sku'])             
    except Exception, e:
        log.exception(e)
        logger.error(url)   
    return items
    
def itemAnalyzer(category,itemid):
    if int(itemid) in settings.ITEMS:return
    record_writer = open(settings.FILEPATH+category+'/'+itemid+'.txt','w')    
    url = settings.COMMENTS_URL_FORMAT%(itemid,1)
    try:
        html_doc = ulib2.urlopen(url).read()
        parser = bs4.BeautifulSoup(html_doc)
        parser.encode('gb2312')
        product_name = parser.body.find('div',id='product-info').find('li',attrs={'class':'p-name'}).find('a').text
        comments_num = parser.body.find('div',id='comments-list').find('div',attrs={'class':'mt'}).find('li',attrs={'class':'curr','scoe':'0'}).find('em').text[1:-1]
        num_page = (int(comments_num)+29)/30        
        for i in range(num_page):
            if i>0:#not page 0
                url = settings.COMMENTS_URL_FORMAT%(itemid,i+1)
                html_doc = ulib2.urlopen(url).read()
                parser = bs4.BeautifulSoup(html_doc)
            comments = parser.body.find('div',id='comments-list').find_all('div',attrs={'class':'item'})
            for comment in comments:
                userid = comment.find('div',attrs={'class':'user'}).find('div',attrs={'class':'u-name'}).find('a')['href'].split('/')[-1].split('-')[0]
                rating = comment.find('div',attrs={'class':'o-topic'}).find('span')['class'][1][2:]
                comment_content = '::'.join([i.strip().replace('\n','') for i in comment.find('div',attrs={'class':'comment-content'}).strings if i.strip()])
                record_writer.write('%s\t%s\n'%(userid,rating))
                record_writer.write(comment_content+'\n')
        record_writer.close()
        settings.ITEMS.add(int(itemid))
        settings.ITEMS_OUT.write('%s::%s\n'%(itemid,product_name))
    except Exception, e:
        log.exception(e)
        logger.error('%s,%s'%(category,itemid))
    
if __name__ == '__main__':
    outdata = open('itemsToBeCrawled.txt','w')
    for idx,category in enumerate(settings.CATEGORIES.iterkeys()):
        print '%s:Start to Crawl the data for category %s'%(time.ctime(),category)
        brands = l1Analyzer(category)
        for brand in brands:
            items=l2Analyzer(brand)
            for item in items:
#                 itemAnalyzer(category,item)
                outdata.write('%s,%s\n'%(category,item))
        print '%s:Finish Crawling the data for category %s,%d:%d finished.'%(time.ctime(),settings.CATEGORIES[category],idx,len(settings.CATEGORIES))
    settings.ITEMS_OUT.close()
    outdata.close()