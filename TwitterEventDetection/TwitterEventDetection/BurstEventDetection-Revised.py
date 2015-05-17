
import os
from nltk.corpus import stopwords
from nltk.stem import snowball
import time
import re
import csv
import math
from TwitterStream import TwitterStream

class EventDetector(object):
    '''
    EventDetector accept twitter stream as input, detect bursty events in it.
    '''

    def __init__(self, textprocessor, temporalprocessor, stream = None):
        '''
        stream: a twitter stream, an iterable item with create time and text.
        '''
        self.textprocessor = textprocessor
        self.temporalprocessor = temporalprocessor
        self.stream = stream

    def process_text(self, text):
        '''
        Process a single twitter text.

        Including twitter level and term level operations.
        '''
        terms = self.textprocessor.tokenize(text)
        terms = [self.textprocessor.stem(t.lower)
                 for t in terms if t.lower() not in self.stopwords]
        return terms

    def process_stream(self):
        for tweet in self.stream:
            time_s = tweet[0]
            id_str = tweet[1]
            text = tweet[2]
            rt_str = tweet[3]
            time_t = time.strptime(time_s, '%Y-%m-%d %H:%M:%S')
            terms = self.textprocessor.process(text)
            self.temporalprocessor.process(time_t, id_str, terms, rt_str)

class TextProcessor(object):
    '''
    TextProcessor process twitter text in to stemmed terms.
    '''
    def __init__(self):
        self.patt = re.compile('(?u)\w+://[\w\./#]+|&\w+;|\s+-\s+|\s+:\s+|\s+|[^\w\'-]+')
        self.stopwords = []
        self.stemmer = snowball.EnglishStemmer()
        if 'stopwords.txt' in os.listdir('./'):
            try:
                f = open('./stopwords.txt', encoding = 'utf-8')
                self.stopwords = eval(f.read())
                f.close()
            except:
                self.stopwords = stopwords.words('english')
        else:
            self.stopwords = stopwords.words('english')

    def tokenize(self, text):
        return [t.lower().replace('-','') for t in self.patt.split(text)]

    def stem(self, term):
        # remove more than two same character in sequence.
        dup = 0
        term_nondup = ''
        for i in range(0,len(term)):
            if i == 0:
                term_nondup += term[i]
            elif term[i] == term[i-1]:
                dup += 1
                if dup < 2:
                    term_nondup += term[i]
            else:
                dup = 0
                term_nondup += term[i]
        # then use a common stemmer
        return self.stemmer.stem(term_nondup)

    def remove_stopwords(self, terms):
        return [t.lower() for t in terms if t.lower() not in self.stopwords]

    def process(self, text):
        terms = self.tokenize(text)
        return [self.stem(t) for t in terms if t not in self.stopwords]

class TemporalProcessor(object):
    '''
    TemporalProcessor process tweets (as sequence of term list).

    Do the following things:
    Save the tweets aggregating for each time interval.
    Count terms for each time interval.
    Compare the term frequencies between intervals, extract burst keywords.
    '''
    def __init__(self, interval_lenth, alpha, beta, s, update_freq = 1, start_time = None, result_dir = './data'):
        '''
        Parameters:
        interval_lenth: lenth of an interval.
        start_time: start time of the stream, if not given, will be detected.
        update_freq: update the stats once how many intervals
        alpha: learning rate.
        beta: background noise rate.
        s: if n > ewma + sqrt(ewmvar) * s, then the term is bursty.
        '''
        # set interval parameters
        self.interval_lenth = interval_lenth
        self.update_freq = update_freq
        self.alpha = alpha
        self.beta = beta
        self.s = s
        if start_time is None:
            self.start_time = 0
            self.interval_start = 0
        else:
            self.start_time = start_time
            self.interval_start = start_time
        self.interval_end = self.interval_start + self.interval_lenth
        # directory to store results
        if not os.path.exists(result_dir):
            os.mkdir(result_dir)
        self.result_dir = result_dir
        if not os.path.exists(result_dir):
            os.mkdir(result_dir)
        # dictionary store the stats of each word
        # {term : (ewma, ewmvar)}
        self.stats = {}
        # term count for current interval
        self.curr_term_count = {}
        # tweets count for current interval
        self.curr_tweets_count = 0
        # unsaved tweets for next update of stats
        self.unsaved_stats = {}
        # interval count
        self.ii = 0
        self.curr_file = None
        self.curr_writer = None

    def process(self, time_tuple, id_str, terms, rt_str):
        #print('in temporal process:1')
        time_digit = time.mktime(time_tuple)
        time_str = time.strftime('%Y%m%d %H:%M:%S', time_tuple)
        # only happen once and only happen when no start_time given.
        if self.start_time == 0:
            #print('in temporal process:2')
            self.start_time = time_digit
            self.interval_start = time_digit
            self.interval_end = time_digit + self.interval_lenth
        # the coming tweets is not in the current interval
        # which means we should go to the next interval.
        while time_digit >= self.interval_end:
            #print('in temporal process:3')
            # TBD: find emerging terms!
            if self.ii > self.update_freq:
                self.find_emerging_terms() # TBD:
            # only perform when the total volumn is not 0.
            # save stats of last interval

            #self.save_curr_interval()

            # close current file, set current file to None
            self.curr_file.close()
            self.curr_file = None
            self.curr_writer = None
            # merge current interval to unsaved stats
            for term, count in self.curr_term_count.items():
                if term in self.unsaved_stats:
                    self.unsaved_stats[term] += count / self.curr_tweets_count
                else:
                    self.unsaved_stats[term] = count / self.curr_tweets_count
            # turn to next interval
            self.ii += 1
            self.interval_start = self.interval_end
            self.interval_end = self.interval_start + self.interval_lenth
            # update stats every 'undate_freq' intervals
            if self.ii % self.update_freq == 0:
                self.update_stats()
                self.unsaved_stats.clear()
            self.curr_term_count.clear()
            self.curr_tweets_count = 0

        # when first tweet coming in a new interval
        if self.curr_file is None:
            #print('in temporal process:4')
            self.curr_file = open(os.path.join(self.result_dir,
                '%.4d_%s_tweets.txt' % (self.ii, time.strftime('%Y%m%d_%H%M',
                    time.localtime(self.interval_start)))),
                        'w', newline = '', encoding = 'utf-8')
            self.curr_writer = csv.writer(self.curr_file)
        #print('in temporal process:5')
        # save the processed tweet
        if rt_str=='':
            self.curr_writer.writerow([id_str, time_str, terms.__str__()])
        else:
            self.curr_writer.writerow([rt_str, time_str, terms.__str__()])
        # proceed the incoming tweet
        self.curr_tweets_count += 1
        for term in set(terms):
            if term in self.curr_term_count:
                self.curr_term_count[term] += 1
            else:
                self.curr_term_count[term] = 1

    def save_curr_interval(self):
        with open(os.path.join(self.result_dir, '%.4d_%s_counts.csv'
            % (self.ii, time.strftime('%Y%m%d_%H%M',
                time.localtime(self.interval_start)))),
                  'w', newline = '', encoding = 'utf-8') as f:
            csvw = csv.writer(f)
            for term, count in self.curr_term_count.items():
                csvw.writerow([term, count, count / self.curr_tweets_count])

    def update_stats(self):
        a = self.alpha
        for term in self.unsaved_stats.keys() | self.stats.keys():
            delta = (self.unsaved_stats.get(term, 0) / self.update_freq) \
                    - self.stats.get(term, (0, 0))[0]
            self.stats[term] = (self.stats.get(term, (0, 0))[0] + a * delta,
                    (1 - a) * (self.stats.get(term, (0, 0))[1] + a * delta ** 2))

    def find_emerging_terms(self):
        with open(os.path.join(self.result_dir,'burst_terms'), 'a', encoding = 'utf-8') as f:
            f.write('Interval %d:\n' % self.ii)
            for term, count in self.curr_term_count.items():
                stats = self.stats.get(term,(0,0))
                ewma = stats[0]
                ewmvar = stats[1]
                ewma = max(ewma, self.beta)
                ratio = (count / self.curr_tweets_count - ewma) / (math.sqrt(ewmvar) + self.beta) #THE FORMULA
                if ratio > self.s:
                    f.write('%s %f\r\n' % (term, ratio)) #\r\n under windows
            f.write('\n')
            f.flush()

if __name__ == '__main__':
    ts = TwitterStream()
    #datapath = '/Users/Adward/Github/Automatic-Rumor-Detection/TwitterEventDetection/TestData/original'
    datapath = '/Volumes/Adward_Backup/SRTP/data'
    dirlist = os.listdir(datapath)
    for path in dirlist:
        if path.startswith('201') and os.path.isdir(os.path.join(datapath,path)):
            ts.source(os.path.join(datapath,path))
    ts.sort()
    temp = TemporalProcessor(3600,0.3,0.0002,8,
            #result_dir='/Users/Adward/Github/Automatic-Rumor-Detection/TwitterEventDetection/TestData/serialized')
            result_dir = '/Volumes/Adward_Backup/SRTP/serialized_test')
    ed = EventDetector(TextProcessor(),temp,ts.generator())
    ed.process_stream()
