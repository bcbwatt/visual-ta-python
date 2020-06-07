import cv2
import yfinance as yf

from pythonta import drawing as dt
from pythonta import technical as ta
from pythonta import utils as ut


def main():
    # We download the S&P 500
    df = yf.download('^GSPC',
                     start='2019-06-01',
                     end='2020-01-01',
                     progress=False)

    # Create a graph and clear it
    graph = dt.Graph(width=1280, height=1280)
    graph.clear()
    graph.draw_candles(df)

    lines = []
    lines += [ta.find_regression_line(df)]

    # This wil be all values above and below the regression line
    above = []
    below = []

    # Extract the parameters of the regression line
    x1, y1, x2, y2 = lines[0]
    for x in range(x1, x2):     # Go through the entire dataframe
        y = ut.translate(x, x1, x2, y1, y2)     # Get the current height of the regression line
        above.append(df['High'].iloc[x] - y)
        below.append(df['Low'].iloc[x] - y)

    above.sort(reverse=True)
    below.sort(reverse=False)

    top_max_line = (x1, y1+above[0], x2, y2+above[0])
    bottom_max_line = (x1, y1+below[0], x2, y2+below[0])
    lines += [top_max_line, bottom_max_line]

    # Method 1, have 20% of candles in top zone and 20% in bottom zone
    # nr_candles = int(len(df)*0.2)
    # top_safe_line = (x1, y1+above[nr_candles], x2, y2+above[nr_candles])
    # top_bottom_line = (x1, y1+below[nr_candles], x2, y2+below[nr_candles])
    # lines += [top_safe_line, top_bottom_line]

    # Method 2, have 30% of price in top zone and 30% in bottom zone
    # top_safe_line = (x1, y1+above[0]*0.7, x2, y2+above[0]*0.7)
    # top_bottom_line = (x1, y1+below[0]*0.7, x2, y2+below[0]*0.7)
    # lines += [top_safe_line, top_bottom_line]

    # Draw the lines
    graph.draw_lines(df, lines)         # Draw the line

    # Show the finished graph
    cv2.imshow('Technical analysis', graph.canvas)
    cv2.waitKey(0)

    return


if __name__ == '__main__':
    main()
