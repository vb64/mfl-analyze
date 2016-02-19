import anomaly, depth

accepted_data_types = ["MFL"]
MINIMAL_PERCENT = 5

class Item(object):

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
    pass

def analyze(data):

    data_type = data.get("dataType", "")
    if data_type not in accepted_data_types:
        raise Exception("dataType: '%s' is not supported" % data_type)

    row_data = data["dataRow"]
    result = []
    d = Defect(row_data)
    #raw_input("matrix size: %dx%d" % (size_x, size_y))

    while d.depth >= MINIMAL_PERCENT:
        result.append([d.x0, d.y0, d.x, d.y, d.depth])
        clear_rectangle(row_data, d.x0, d.y0, d.x, d.y)
        d = Defect(row_data)

    return result

if __name__ == "__main__":
    #import json
    #print analyze(json.loads(open("data01.json", "r").read()))
    import doctest
    doctest.testmod()
