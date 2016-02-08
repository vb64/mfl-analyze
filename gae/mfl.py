min_size = 4 # minimum size (any dimension) of input matrix

def analyze(data):

    row_data = data["dataRow"]

    size_x = len(row_data)
    size_y = len(row_data[0])
    #raw_input("matrix size: %dx%d" % (size_x, size_y))

    # check for minimum matrix size
    if size_y < min_size or size_x < min_size:
        raise Exception("wrong source matrix size: %dx%d minimum size is %d" % (size_x, size_y, min_size))

    y = size_y / 4
    x = size_x / 4

    return [
        [0,          0,          x, y, 80],
        [size_x - x, 0,          x, y, 70],
        [0,          size_y - y, x, y, 60],
        [size_x - x, size_y - y, x, y, 50],
    ]
