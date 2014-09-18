# coding=utf-8

'''
Created on Jul 6, 2013

@author: george.g.zhao
'''

import os
import re
p = re.compile('::[0-9]{4}-[0-9]{2}-[0-9]{2}')
def read_file(directory):
    for r,_,f in os.walk(directory):
        for files in f:
            if files.split('.')[0].isdigit():
                yield os.path.join(r,files)

def comments(file_path):
    item = file_path.split('\\')[-1][:-4]
    with open(file_path) as indata:
        while True:
            try:
                line1 = indata.readline()
                if not line1:break
                line2 = indata.readline()
                line1 = line1.split()
                user,rating = line1[0],line1[1]
                while not p.match(line2[-13:-1]):
                    nline=indata.readline()
                    if not nline: break
                    line2+=nline
                times =  line2[:-1].split('::')[-1]
                yield '%s,%s,%s,%s\n'%(user,item,rating,times)
            except:
                print 'error'+file_path
            
if __name__ == '__main__':
#     outdata =  open('jd.ds','w')
    file_list=[]
    file_set=set([])
    for files in read_file('..\\data'):
        file_list.append(files.split('\\')[-1])
        file_set.add(files.split('\\')[-1])
    print len(file_list),len(file_set)
#         for comment in comments(files):
#             outdata.write(comment)
#     outdata.close()
#     for comment in comments('..\\data\\670-671-2694\\764146.txt'):
#         print comment
        