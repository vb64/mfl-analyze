import anomaly, depth

accepted_data_types = ["MFL"]

def analyze(data):

    data_type = data.get("dataType", "")
    if data_type not in accepted_data_types:
        raise Exception("dataType: '%s' is not supported" % data_type)

    row_data = data["dataRow"]
    size_y = len(row_data[0])
    #raw_input("matrix size: %dx%d" % (size_x, size_y))

    # find line with maximum amplitude
    line_index = 0
    max_amplitude = anomaly.Item(line_index, row_data).amplitude
    for i in range(1, size_y):
        amplitude = anomaly.Item(i, row_data).amplitude
        if amplitude > max_amplitude:
            max_amplitude = amplitude
            line_index = i

    # defect sizes by x and y
    defect = anomaly.Item(line_index, row_data)
    x0, y0, x, y = defect.rectangle()

    return [
        [x0, y0, x, y, depth.calculate(x, defect.h0, defect.amplitude, False)],
    ]

if __name__ == "__main__":
    import json
    print analyze(json.loads(open("data01.json", "r").read()))
