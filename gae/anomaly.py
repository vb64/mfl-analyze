class Item(object):
    """
    Extracting an array of measurements of sensor with line_index from whole array data.
    Calculate maximum amplitude, h0 and geometry size (rectangle) for anomaly.

    >>> dat = [ \
        [1, 11, 21, 11],   \
        [2, 12, 22, 12],   \
        [3, 13, 23, 13],   \
        [4, 14, 24, 14],   \
        [5, 15, 25, 15],   \
        [3, 13, 23, 13],   \
        [2, 12, 22, 12],   \
        [1, 11, 21, 11]    \
    ]
    >>> defect = Item(0, dat)
    >>> defect.sensor_data
    [1, 2, 3, 4, 5, 3, 2, 1]
    >>> defect.h0
    1
    >>> defect.amplitude
    4
    >>> defect.rectangle()
    (0, 0, 8, 4)

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

    def rectangle(self, width_signal_fading=10):
        ampl_position = self.deltas.index(self.ampl_value)
        return 0, 0, len(self.source_data), len(self.source_data[0])

if __name__ == "__main__":
    import doctest
    doctest.testmod()
