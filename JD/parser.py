'''
Created on Jul 2, 2013
@author: george.g.zhao
处理html文档，找出评论
'''
import urllib2 as ulib2

import bs4


if __name__ == '__main__':
    url = 'http://club.jd.com/review/882186-1-1-0.html'
    html_doc = ulib2.urlopen(url).read()

    soup = bs4.BeautifulSoup(html_doc)
    soup.encode('gb2312')
    product_infor = soup.body.find('div', id='product-info')
    product_name = product_infor.find('li', attrs={'class': 'p-name'}).find('a').text
    print product_name
    comments_num = soup.body.find('div', id='comments-list').find('div', attrs={'class': 'mt'}).find('li', attrs={
    'class': 'curr', 'scoe': '0'}).find('em').text[1:-1]
    print comments_num
    comments = soup.body.find('div', id='comments-list').find_all('div', attrs={'class': 'item'})
    for comment in comments:
        print \
        comment.find('div', attrs={'class': 'user'}).find('div', attrs={'class': 'u-name'}).find('a')['href'].split(
            '/')[-1].split('-')[0]
        
            
        
        
        
    
    