from pythonta import utils

CLASSIC = 0
MODERN = 1

TOPS = 0
BOTTOMS = 1

SUPPORTS = 0
RESISTS = 1

trendline_reach = 2.0
def find_trendlines(dataframe,
                    clearance=5,
                    what=SUPPORTS):
    '''Calculates trendlines for the given dataframe.

    :param dataframe: Dataframe containing the price data.
    :param clearance: Nr of candles to clear on both sides of the peak
    :param what: Selects whether SUPPORTS or RESISTS will be returned.
    :type dataframe: pandas
    :type clearance: int
    :type what: const
    :returns: lines
    :rtype: array

    .. note:: The dataframe must contain the columns 'High' and 'Low'.
    .. note:: The returned array of lines are in the format (x1,y1,x2,y2) where x1 and x2 are indexes into the dataframe and Y1 and Y2 are actual price points.
    '''

    results = []

    if what == SUPPORTS:
        peaks = find_peaks(dataframe, clearance=clearance, method=MODERN, what=BOTTOMS)
    if what == RESISTS:
        peaks = find_peaks(dataframe, clearance=clearance, method=MODERN, what=TOPS)

    print(peaks)

    for i in range(0, len(peaks)):
        for j in range(0, len(peaks)):
            if j <= i:
                continue
            x1 = peaks[i]
            x2 = peaks[j]
            reach = int(x2 + ((x2-x1)*trendline_reach))
            if reach < len(dataframe):
                continue
            if what == SUPPORTS:
                y1 = dataframe['Low'].iloc[x1]
                y2 = dataframe['Low'].iloc[x2]
            if what == RESISTS:
                y1 = dataframe['High'].iloc[x1]
                y2 = dataframe['High'].iloc[x2]
            valid = True
            for k in range(i, len(dataframe)):
                y3 = utils.translate(k, x1, x2, y1, y2)
                if what == SUPPORTS:
                    if dataframe['Low'].iloc[k] < y3:
                        valid = False
                if what == RESISTS:
                    if dataframe['High'].iloc[k] > y3:
                        valid = False
            if valid is True:
                results.append((x1,
                                y1,
                                k,
                                y3))

    return results


def find_support_and_ressitance(dataframe,
                                clearance=5,
                                what=SUPPORTS):
    '''Calculates support or resistance levels for the given dataframe.

    :param dataframe: Dataframe containing the price data.
    :param clearance: Nr of candles to clear on both sides of the peak
    :param what: Selects whether SUPPORTS or RESISTS will be returned.
    :type dataframe: pandas
    :type clearance: int
    :type what: const
    :returns: lines
    :rtype: array

    .. note:: The dataframe must contain the columns 'High' and 'Low'.
    .. note:: The returned array of lines are in the format (x1,y1,x2,y2) where x1 and x2 are indexes into the dataframe and Y1 and Y2 are actual price points.
    '''

    results = []

    if what == SUPPORTS:
        peaks = find_peaks(dataframe, clearance=clearance, method=CLASSIC, what=BOTTOMS)
    if what == RESISTS:
        peaks = find_peaks(dataframe, clearance=clearance, method=CLASSIC, what=TOPS)

    while len(peaks):
        pp = peaks[-1]
        del peaks[-1]

        valid = True
        for i in range(pp, len(dataframe)):
            if what == SUPPORTS:
                y = dataframe['Low'].iloc[pp]
                if dataframe['Low'].iloc[i] < dataframe['Low'].iloc[pp]:
                    valid = False
                    break
            if what == RESISTS:
                y = dataframe['High'].iloc[pp]
                if dataframe['High'].iloc[i] > dataframe['High'].iloc[pp]:
                    valid = False
                    break

        if valid is True:
            results.append((pp,
                           y,
                           len(dataframe)-1,
                           y))

    return results


def find_peaks(dataframe,
               clearance=5,
               method=CLASSIC,
               what=TOPS):
    '''Calculates peaks for the given dataframe.

    :param dataframe: Dataframe containing the price data.
    :param clearance: Nr of candles to clear on both sides of the peak
    :param method: User CLASSIC or MODERN style for peak detection
    :param what: Selects whether TOPS or BOTTOMS will be returned.
    :type dataframe: pandas
    :type clearance: int
    :type what: const
    :returns: indexes
    :rtype: array

    .. note:: The dataframe must contain the columns 'High' and 'Low'.
    .. note:: CLASSIC peak stick out on a horizontal level. MODERN peaks also consider the trend of surrounding candles.
    '''

    result = []

    if what == TOPS:
        element = 'High'
    if what == BOTTOMS:
        element = 'Low'

    for i in range(clearance, len(dataframe)-clearance):
        target = dataframe[element].iloc[i]
        isTop = True

        if method == CLASSIC:
            for j in range(1, clearance+1):
                left = dataframe[element].iloc[i-j]
                right = dataframe[element].iloc[i+j]
                if what == TOPS:
                    thresHold = max(left, right)
                    if target <= thresHold:
                        isTop = False
                        break
                if what == BOTTOMS:
                    thresHold = min(left, right)
                    if target >= thresHold:
                        isTop = False
                        break

        if method == MODERN:
            left = dataframe[element].iloc[i-1]
            right = dataframe[element].iloc[i+1]
            if what == TOPS:
                if target <= (left+right)/2:  # Quick optimization
                    continue
            if what == BOTTOMS:
                if target >= (left+right)/2:  # Quick optimization
                    continue
            for k in range(i - clearance, i + clearance + 1):
                if k == i:
                    continue
                elif k > i:
                    x = i
                    y = k
                elif k < i:
                    x = k
                    y = i
                isTop = True
                left = dataframe[element].iloc[x]
                right = dataframe[element].iloc[y]
                for l in range(i-clearance, i+clearance+1):
                    if l == i or l == k:
                        continue
                    pp = dataframe[element].iloc[l]
                    t = utils.translate(l, x, y, left, right)
                    if what == TOPS:
                        if pp >= t:
                            isTop = False
                            break
                    if what == BOTTOMS:
                        if pp <= t:
                            isTop = False
                            break
                if isTop is True:
                    break

        if isTop is True:
            result.append(i)

    return result


def find_regression_line(dataframe):
    '''Returns a regression line for the given dataframe.

    :param dataframe: Dataframe containing the price data.
    :type dataframe: pandas
    :returns: line
    :rtype: (x1, y1, x2, y2)

    '''
    delta = 0.001 * dataframe['Close'].iloc[-1]

    x1 = 0
    y1 = dataframe['Close'].mean()
    x2 = len(dataframe)
    y2 = y1

    score = utils.calc_dist_to_line(dataframe, (x1, y1, x2, y2))

    while True:
        old_score = score

        # Add delta to left side
        new_score = utils.calc_dist_to_line(dataframe, (x1, y1 + delta, x2, y2))
        if score > new_score:
            score = new_score
            y1 += delta

        # Substract delta to left side
        new_score = utils.calc_dist_to_line(dataframe, (x1, y1 - delta, x2, y2))
        if score > new_score:
            score = new_score
            y1 -= delta

        # Add delta to right side
        new_score = utils.calc_dist_to_line(dataframe, (x1, y1, x2, y2 + delta))
        if score > new_score:
            score = new_score
            y2 += delta

        # Subsctract delta to right side
        new_score = utils.calc_dist_to_line(dataframe, (x1, y1, x2, y2 - delta))
        if score > new_score:
            score = new_score
            y2 -= delta

        if score == old_score:
            break

    return (x1, y1, x2, y2)


def peak_sequence(dataframe):
    # Find tops and bottoms
    tops = find_peaks(dataframe, what=TOPS)
    bottoms = find_peaks(dataframe, what=BOTTOMS)

    arr_sequence = []
    str_sequence = ''

    # For all the tops, see if the next top is higher (HT) or lower (LT)
    if len(tops) > 1:
        for i in range(1, len(tops)):
            if dataframe['High'].iloc[tops[i]] > dataframe['High'].iloc[tops[i - 1]]:
                arr_sequence.append((tops[i], 'HT'))
            else:
                arr_sequence.append((tops[i], 'LT'))

    # For all the bottoms, see if the next bottom is higher (HB) or lower (LB)
    if len(bottoms) > 1:
        for i in range(1, len(bottoms)):
            if dataframe['Low'].iloc[bottoms[i]] > dataframe['Low'].iloc[bottoms[i - 1]]:
                arr_sequence.append((bottoms[i], 'HB'))
            else:
                arr_sequence.append((bottoms[i], 'LB'))

    # Last price would make for a higher top but is not yet confirmed as a top
    if dataframe['High'].iloc[-1] > dataframe['High'].iloc[tops[-1]]:
        arr_sequence.append((len(dataframe), 'HT'))

    # Last price would make for a lower bottom but is not yet confirmed as a bottom
    if dataframe['Low'].iloc[-1] < dataframe['Low'].iloc[bottoms[-1]]:
        arr_sequence.append((len(dataframe), 'LB'))

    # Sort the sequence by date (the dataframe index)
    arr_sequence = sorted(arr_sequence, key=utils.getKey)

    # Make it into a string, de indexes are no longer needed
    for k, v in arr_sequence:
        str_sequence += ' ' + v

    return str_sequence

