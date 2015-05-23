__author__ = 'Adward'
import os
import codecs

def indexCreation():
    '''
    Inverted-Index's format: term,id1,id2,...
    :param dbname:
    :return:
    '''
    files = []
    path = '/Volumes/Adward_Backup/SRTP/serialized_test/'
    index_path = '/Volumes/Adward_Backup/SRTP/inverted_index/'
    file_lst = os.listdir(path)
    for fn in file_lst:
        if '.DS_Store'==fn:
            continue
        files.append(os.path.join(path, fn))
    for fn in files:
        with codecs.open(fn, encoding='utf-8', errors='ignore') as f:
            try:
                for line in f:
                    li_ne = line.replace('\n','').replace('\r','').replace('"','').replace(']','').replace('[','')
                    li_ne = li_ne.replace("'",'').replace(' ','').split(',')
                    id = li_ne[0]
                    for token in li_ne[2:]:
                        if token=='':
                            continue
                        with codecs.open(os.path.join(index_path,token), 'a', encoding='utf-8', errors='ignore') as index_f:
                            index_f.write(str(id)+',')
            except:
                print(li_ne)
        print('processed '+fn)

if __name__=='__main__':

    #uncomment the following functions when it is needed; insertion may take quite a while.
    indexCreation()