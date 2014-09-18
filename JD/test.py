# coding=utf-8
'''
Created on Jul 12, 2013

@author: george.g.zhao
'''
import bs4
import urllib2 as ulib2


if __name__ == '__main__':
    url='http://list.jd.com/670-671-672-1311-0-0-0-0-0-0-1-1-2-1.html'
    html_doc = ulib2.urlopen(url).read()
    outdata=open('670-671-672-1311-0-0-0-0-0-0-1-1-2-1.html','w')
    outdata.write(html_doc)