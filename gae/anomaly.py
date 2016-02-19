DFLT_FADING_PERCENT = 10

class Item(object):
    """
    Extracting an array of measurements of sensor with line_index from whole array data.
    Calculate maximum amplitude, h0 and geometry size (rectangle) for anomaly.

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
    >>> defect = Item(0, dat)
    >>> defect.sensor_data
    [3, 2, 3, 4, 7, 3, 2, 1]
    >>> defect.deltas
    [0, -1, 0, 1, 4, 0, -1, -2]
    >>> defect.h0
    3
    >>> defect.amplitude
    4
    >>> defect.rectangle()
    (2, 0, 3, 1)

    >>> defect = Item(2, dat)
    >>> defect.sensor_data
    [23, 32, 23, 44, 57, 43, 22, 21]
    >>> defect.deltas
    [0, 9, 0, 21, 34, 20, -1, -2]
    >>> defect.h0
    23
    >>> defect.amplitude
    34
    >>> defect.rectangle()
    (2, 0, 3, 1)

    """

    def __init__(self, line_index, data):
        self.line_index = line_index
        self.source_data = data
        self.sensor_data = [data[x][line_index] for x in range(len(data))]
        self.deltas = map(lambda x: x - self.h0, self.sensor_data)
        self.ampl_value = max(self.deltas)

    @property
    def amplitude(self):
        """Maximum amplitude for the line of sensor data"""
        return self.ampl_value

    @property
    def h0(self):
        """Middle level of sensor signal"""
        return self.sensor_data[0]

    def amplitude_on_interval(self, pos_left, pos_right):
        return max(self.deltas[pos_left:pos_right])

    def rectangle(self, width_signal_fading=DFLT_FADING_PERCENT):
        ampl_position = self.deltas.index(self.ampl_value)

        pos_left = ampl_position - 1 - index_le(reversed(self.deltas[:ampl_position]), 0)
        pos_right = len(self.deltas) - 1

        # if no h0 level into sensor data after maximum
        try:
            pos_right = ampl_position + 1 + index_le(self.deltas[ampl_position+1:], 0)
        except:
            pass

        # find top border of defect in source array
        border = 0
        line = self.line_index
        while line > border:
            amplitude = Item(line, self.source_data).amplitude_on_interval(pos_left, pos_right)
            if (amplitude > self.amplitude) or (amplitude <= (self.amplitude * width_signal_fading / 100)):
                break
            line -= 1
        pos_top = line

        # find bottom border of defect in source array
        border = len(self.source_data[0]) - 1
        line = self.line_index
        while line < border:
            amplitude = Item(line, self.source_data).amplitude_on_interval(pos_left, pos_right)
            if (amplitude > self.amplitude) or (amplitude <= (self.amplitude * width_signal_fading / 100)):
                break
            line += 1
        pos_bottom = line

        return (pos_left, pos_top, pos_right - pos_left, pos_bottom - pos_top)

def index_le(sequence, value):
    """
    Find first element in numeric sequence, then less or equal value.
    Return index in sequence for this element.
    If element not found, raise exception.
    """
    i = 0
    for item in sequence:
        if item <= value:
            return i
        i += 1
    raise Exception

if __name__ == "__main__":
    import doctest
    doctest.testmod()
