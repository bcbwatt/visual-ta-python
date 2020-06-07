import datetime
import decimal

def translate(value, fromBegin, fromEnd, toBegin, toEnd):
    '''Translates a point from one system to the other. A system is defined (but
     not limited) by a begin- and end-value.
    Parameters:
        value               : The point to be transformed
        fromBegin, fromEnd  : System in which the value parameter is now
        toBegin, toEnd      : System to which value is to be translated

    Returns:
        translated value in the new system

    Notes:
    1. For examele; if you wanted 10 on a scale of 1-10 to be translated to a
       scale of 20-40 you would do:
           v_new = translate(10, 1, 10, 20, 40)
    '''
    leftSpan = fromEnd - fromBegin
    rightSpan = toEnd - toBegin

    valueScaled = float(value - fromBegin) / float(leftSpan)

    return toBegin + (valueScaled * rightSpan)


# Obsolete function
def df_from_yfinance(df):
    result = df.rename(columns={'High': 'High',
                                'Low': 'Low',
                                'Open': 'Open',
                                'Close': 'Close',
                                'Volume': 'Volume'})
    return result


# Decimals -> dataframe gives roundin isues so this function is not to usefull yet
def decimals(nr):
    arr = str(nr).split('.')
    return len(arr[1])


def ztime_to_time(time):
    return time[:10] + ' ' + time[11:-4]


def time_to_ztime(time):
    return time[:10] + 'T' + time[11:19] + '.000000Z'


def str_to_ns(time_str):
     dt = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')
     ms = int(dt.timestamp() * 10**6)
     return ms


def calc_dist_to_line(df, line):
    result = 0
    x1, y1, x2, y2 = line           # Unpack the line
    for x in range(0, len(df)):     # Go through all the data points
        y = translate(x, x1, x2, y1, y2)     # Get height of the trendline
        d = abs(y - df['Close'].iloc[x])        # Get the absulute distance to the line
        result += d                             # Add this to the total distance
    return result


def getKey(item):
    return item[0]
