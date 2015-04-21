'''
Created on 2015年1月14日

@author: shengxia
This module modifies the original tweepy api, so as to verify and fix the infinitely looping problem.
'''
from tweepy.streaming import Stream
from tweepy.streaming import ReadBuffer
from tweepy.error import TweepError

class NewReadBuffer(ReadBuffer):
    def __init__(self, stream, chunk_size):
        super().__init__(stream, chunk_size)
        self.log = open('buffer.log','a')
    def read_len(self, length):
        i = 0 # modified
        while True:
            # modified
            if i == 20:
                self.log.write('in read_len: ')
            if i >= 20:
                self.log.write('%d ' % i)
                self.log.flush()
            if i > 100:
                self.log.write('read too many times without enough data, try to re-connect.\n')
                self.log.close()
                raise TweepError('no data income.')
            # origin
            if len(self._buffer) >= length:
                # modified
                if i > 20:
                    self.log.write('\n')
                    self.log.flush()
                # origin
                return self._pop(length)
            read_len = max(self._chunk_size, length - len(self._buffer))
            self._buffer += self._stream.read(read_len).decode("ascii")
            # modified
            i += 1
    def read_line(self, sep='\n'):
        start = 0
        i = 0 #modified
        while True:
            # modified
            if i == 10:
                self.log.write('in read_len: ')
            if i >= 10:
                self.log.write('%d ' % i)
                self.log.flush()
            if i > 50:
                self.log.write("cannot read size line.\n")
                self.log.close()
                raise TweepError('no size line income.')
            # origin
            loc = self._buffer.find(sep, start)
            if loc >= 0:
                # modified
                if i >= 10:
                    self.log.write('\n')
                    self.log.flush()
                # origin
                return self._pop(loc + len(sep))
            else:
                start = len(self._buffer)
            self._buffer += self._stream.read(self._chunk_size).decode("ascii")
            # modified
            i += 1
            
class NewStream(Stream):
    def __init__(self, auth, listener):
        super().__init__(auth, listener)
        self.log = open('teststream.log','a')
    def _read_loop(self, resp):
        buf = NewReadBuffer(resp.raw, self.chunk_size)

        while self.running:
            length = 0
            i = 0 #modified
            while True:
                line = buf.read_line().strip()
                if not line:
                    i += 1
                    #pass  # keep-alive new lines are expected
                elif line.isdigit():
                    length = int(line)
                    break
                else:
                    raise TweepError('Expecting length, unexpected value found')
                # modified
                if i > 10:
                    self.log.write('Too many keep-alive lines, try to re-connect.\n')
                    self.log.close()
                    raise TweepError('Too many keep-alive lines')

            next_status_obj = buf.read_len(length)
            if self.running:
                self._data(next_status_obj)

            # # Note: keep-alive newlines might be inserted before each length value.
            # # read until we get a digit...
            # c = b'\n'
            # for c in resp.iter_content(decode_unicode=True):
            #     if c == b'\n':
            #         continue
            #     break
            #
            # delimited_string = c
            #
            # # read rest of delimiter length..
            # d = b''
            # for d in resp.iter_content(decode_unicode=True):
            #     if d != b'\n':
            #         delimited_string += d
            #         continue
            #     break
            #
            # # read the next twitter status object
            # if delimited_string.decode('utf-8').strip().isdigit():
            #     status_id = int(delimited_string)
            #     next_status_obj = resp.raw.read(status_id)
            #     if self.running:
            #         self._data(next_status_obj.decode('utf-8'))


        if resp.raw._fp.isclosed():
            self.on_closed(resp)

        