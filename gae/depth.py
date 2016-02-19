def calculate(diam, h0, amplitude, isInternal):
    # size 60mm: prcnt = dltH / h0 * 40 + 5
    # size 70mm: prcnt = dltH / h0 * 32 + 5
    k1 = 32 if diam > 6 else 40
    prcnt = float(amplitude) / float(h0) * k1 + 5
    if isInternal:
        prcnt = prcnt * 0.8

    if prcnt > 85.0:
        prcnt = 85

    return int(prcnt)
