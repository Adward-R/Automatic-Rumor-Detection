'''
Created on 2015年5月14日

@author: Henry Ching
'''
from locale import atoi
import os
import codecs
import re

class s_data(object):
    """
    get and store serialized data
    """
    def __init__(self):
        """

        :rtype : object
        """
        self.fid = ''
        self.tokens = []
        self.timestamp = ''

    def get_serialized_data(self, line):

        comma_idx = line.find(',')
        self.fid = line[0:comma_idx]
        line = line[comma_idx + 1:]

        comma_idx = line.find(',')
        self.timestamp = line[0:comma_idx]
        line = line[comma_idx + 1:]

        line = re.sub(r'\[|\]|\'|\"|\r|\n', '', line)
        line = line.replace(' ', '')
        self.tokens = line.split(',')

    def print_data(self):
        print(self.fid)
        print(self.timestamp)
        print(self.tokens)

def Get_Burst_ID(Burst_ID_List, datapath):
    with codecs.open(os.path.join(datapath, 'hotspot.txt'), encoding='utf-8') as f:
        for line in f:
            array = line.split(':')
            array[2] = re.sub(r'\r|\n', '', array[2])
            Burst_ID_List.append(array[2])

if __name__ == '__main__':
    datapath = '../../serialized'
    dirlist = os.listdir(datapath)

    Burst_ID_List = []
    serialized_data = s_data()
    Get_Burst_ID(Burst_ID_List, datapath)

    output = codecs.open(os.path.join(datapath, "time_eval.txt"), "w", "utf-8")

    interval = 0
    for id in Burst_ID_List:
        if id != '0':
            flag = 0
            for path in dirlist:
                if not (path.startswith('burst') or path.startswith('hot') or path.startswith('mass')):
                    now_interval = atoi(path[0:4])
                    with codecs.open(os.path.join(datapath, path), encoding='utf-8') as f:
                        for line in f:
                            serialized_data.get_serialized_data(line)
                            if serialized_data.fid == id:
                                output.write(str(interval) + ':' + str(interval - now_interval))
                                flag = 1
                                break
                if flag:
                    break
        else:
            output.write(str(interval) + ':' + 'None')
        print(str(interval) + ' finished')
        interval += 1

    output.close()

