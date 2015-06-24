import mmap

class BinarySearch(object):
    def __init__(self, string=None, filename=None, check=False):
        if string is not None:
            self.string = string
        elif filename is not None:
            with open(filename) as f:
                self.string = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        else:
            raise ValueError('Data source required')
        if check:
            s = self.string
            prv = 0
            cur = s.find('\n') + 1
            while cur+1 < len(s):
                nxt = s.find('\n', cur)
                if s[prv:cur - 1] > s[cur:nxt]:
                    raise ValueError('Input buffer is not (properly) sorted, {} at position {} > {} at position {}'.format(s[prv:cur - 1], prv, s[cur:nxt], cur))
                prv = cur
                cur = nxt + 1

    def __contains__(self, key):
        s = self.string
        beg = 0
        end = len(s)
        while beg < end:
            mid = (beg + end) / 2
            left  = s.rfind('\n', beg, mid) + 1
            if left <= 0:
                left = beg
            right = s. find('\n', mid, end)
            if right < 0:
                right = end
            line = s[left:right]
            if line == key:
                return (left, right)
            if line > key:
                end = left
            else:
                beg = right + 1
        return None

    def close(self):
        if hasattr(self.string, 'close'):
            self.string.close()
        self.string = None

class BinarySearchWithAdd(BinarySearch):
    def __init__(self, logfilename=None, **kwargs):
        super(BinarySearchWithAdd, self).__init__(**kwargs)
        if logfilename is None:
            self.logfile = None
            self.set = set()
        else:
            self.logfile = open(logfilename, 'a+')
            self.set = { line.rstrip() for line in self.logfile }

    def __contains__(self, key):
        match = key in self.set or super(BinarySearchWithAdd, self).__contains__(key)
        if match is not None:
            return match

    def add(self, key):
        self.set.add(key)
        if self.logfile is not None:
            self.logfile.writelines((key,'\n'))

    def test_and_add(self, key):
        match = key in self
        if match is not None:
            return match
        self.add(key)
        return None

    def close(self):
        if self.logfile is not None:
            self.logfile.close()
        super(BinarySearchWithAdd, self).close()
