
import os 
import csv

class TwitterStream(object):
    '''
    An iterable tweet stream. Generate from file.
    '''


    def __init__(self):
        '''
        Generate an iterable tweet stream.
        Use TwitterStream().generator()
        '''
        self.files = []
        self.fileset = set()
        self.sorted = True
        
    def generator(self):
        '''
        Return tweets one by one from the files.
        '''
        no_former_tweet = True
        former_tweet = ('NAN', 'NAN', 'NAN', 'NAN')
        for fn in self.files:
            with open(fn, newline = '', encoding = 'utf-8') as f:
                csv_reader = csv.reader(f)
                # the default field index
                idx_id = 0
                idx_time = 1
                idx_rt = 12
                idx_txt = 14
                first_row = True
                while True:
                    try:
                        row = next(csv_reader)
                        # ignore the first row, read only the field name
                        if first_row:
                            idx_id = row.index('id')
                            idx_time = row.index('created_at')
                            idx_rt = row.index('retweeted_status_id')
                            idx_txt = row.index('text')
                            first_row = False
                            continue
                        if former_tweet[1] != row[idx_rt]:
                            if not no_former_tweet:
                                yield former_tweet
                            else:
                                no_former_tweet = False
                        former_tweet = (row[idx_time], row[idx_id], row[idx_txt],row[idx_rt])
                    except StopIteration:
                        break
                    except:
                        pass
        
    def source(self, path):
        '''
        Set file source of tweets.
        '''
        if os.path.isdir(path):
            file_lst = os.listdir(path)
            for fn in file_lst:
                if fn.endswith('_status.csv'):
                    self.fileset.add(os.path.join(path,fn))
        elif os.path.exists(path):
            self.fileset.add(path)
        self.sorted = False
    
    def sort(self):
        if not self.sorted:
            self.files = [x for x in self.fileset]
            self.files.sort()
            self.sorted = True