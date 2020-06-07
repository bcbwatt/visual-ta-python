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

    # Show the finished graph
    cv2.imshow('Technical analysis', graph.canvas)
    cv2.waitKey(0)

    return


if __name__ == '__main__':
    main()