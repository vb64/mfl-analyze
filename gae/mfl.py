import anomaly, depth

accepted_data_types = ["MFL"]
MINIMAL_PERCENT = 10

class Defect(object):
    """
    """
    def __init__(self, data):
        size_y = len(data[0])
        line_index = 0
        max_amplitude = anomaly.Item(line_index, data).amplitude
        # find line with maximum amplitude
        for i in range(1, size_y):
            amplitude = anomaly.Item(i, data).amplitude
            if amplitude > max_amplitude:
                max_amplitude = amplitude
                line_index = i
    
        defect = anomaly.Item(line_index, data)
        self.x0, self.y0, self.x, self.y = defect.rectangle()
        self.depth = depth.calculate(self.x, defect.h0, defect.amplitude, False)

    @property
    def x1(self):
        return self.x0 + self.x

    @property
    def y1(self):
        return self.y0 + self.y

    def isIntercept(self, rect):
        if (self.y0 > rect.y1) or (self.y1 < rect.y0):
            return False
        if (self.x0 > rect.x1) or (self.x1 < rect.x0):
            return False
        return True

    def isNear(self, defects):
        for d in defects:
            if self.isIntercept(d):
                return True
        return False

    def __str__(self):
        return "%d%% x0:%d y0:%d x:%d y:%d" % (self.depth, self.x0, self.y0, self.x, self.y)

    def __eq__(self, other):
        return all((self.x0 == other.x0, self.y0 == other.y0, self.x == other.x, self.y == other.y))

    def __ne__(self, other):
        return not self.__eq__(other)

def clear_rectangle(data, x0, y0, x, y):
    """
    >>> dat = [ \
        [3, 13, 23, 13],   \
        [2, 12, 32, 12],   \
        [3, 23, 23, 23],   \
        [4, 34, 44, 34],   \
        [7, 47, 57, 47],   \
        [3, 33, 43, 33],   \
        [2, 22, 22, 22],   \
        [1, 11, 21, 11]    \
    ]
    >>> clear_rectangle(dat, 2, 1, 3, 2)
    >>> dat_1 = [ \
        [3, 13, 23, 13],   \
        [2, 12, 32, 12],   \
        [3, 13, 23, 23],   \
        [4, 13, 23, 34],   \
        [7, 13, 23, 47],   \
        [3, 33, 43, 33],   \
        [2, 22, 22, 22],   \
        [1, 11, 21, 11]    \
    ]
    >>> dat[0]
    [3, 13, 23, 13]
    >>> dat[1]
    [2, 12, 32, 12]
    >>> dat[2]
    [3, 13, 23, 23]
    >>> dat[3]
    [4, 13, 23, 34]
    >>> dat[4]
    [7, 13, 23, 47]
    >>> dat[5]
    [3, 33, 43, 33]
    >>> dat[6]
    [2, 22, 22, 22]
    >>> dat[7]
    [1, 11, 21, 11]

    """
    for i in range(x0, x0+x):
        for j in range(y0, y0+y):
            data[i][j] = data[0][j]

def analyze(data):
    """
    >>> dat = { \
      "dataType": "MFL",      \
      "magnetID": "EPRO700",  \
      "isInside": 0,          \
      "dataRow": [            \
        [3, 13, 23, 13],   \
        [2, 12, 32, 12],   \
        [3, 23, 23, 23],   \
        [4, 34, 44, 34],   \
        [7, 47, 57, 47],   \
        [3, 33, 43, 33],   \
        [2, 22, 22, 22],   \
        [1, 11, 21, 11]    \
      ],                   \
      "dataFilt": [        \
        [3, 13, 23, 13],   \
        [2, 12, 32, 12],   \
        [3, 23, 23, 23],   \
        [4, 34, 44, 34],   \
        [7, 47, 57, 47],   \
        [3, 33, 43, 33],   \
        [2, 22, 22, 22],   \
        [1, 11, 21, 11]    \
      ],                   \
      "zoomDataFormat": 1  \
    }
    >>> analyze(dat)
    [[1, 0, 6, 3, 85]]

    """
    data_type = data.get("dataType", "")
    if data_type not in accepted_data_types:
        raise Exception("dataType: '%s' is not supported" % data_type)

    row_data = data["dataRow"]
    result = []
    d = Defect(row_data)
    #raw_input("matrix size: %dx%d" % (size_x, size_y))

    while d.depth >= MINIMAL_PERCENT:
        if not d.isNear(result):
            result.append(d)
        clear_rectangle(row_data, d.x0, d.y0, d.x, d.y)
        d1 = Defect(row_data)
        if d == d1:
            break
        d = d1

    return [[d.x0, d.y0, d.x, d.y, d.depth] for d in result]

if __name__ == "__main__":
    #import json
    #print analyze(json.loads(open("data01.json", "r").read()))
    import doctest
    doctest.testmod()
