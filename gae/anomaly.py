class Item(object):
    """
    Extracting an array of measurements of sensor for line_index from whole array data.
    Calculate maximum amplitude, x and y sizes for this sensor.

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
    >>> defect.ampl_position
    4
    >>> defect.rectangle()
    (0, 0, 8, 4)

    """

    def __init__(self, line_index, data):
        self.line_index = line_index
        self.source_data = data

        size_x = len(data)
        self.sensor_data = [data[x][line_index] for x in range(size_x)]
        self.h0 = self.sensor_data[0]
        self.deltas = map(lambda x: x - self.h0, self.sensor_data)
        self.ampl_value = max(self.deltas)
        self.ampl_position = self.deltas.index(self.ampl_value)

    @property
    def amplitude(self):
        """Maximum amplitude for the line of sensor data"""
        return self.ampl_value

    def rectangle(self, width_signal_fading=10):
        return 0, 0, len(self.source_data), len(self.source_data[0])

if __name__ == "__main__":
    import doctest
    doctest.testmod()
