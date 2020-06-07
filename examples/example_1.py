import cv2
import yfinance as yf

from pythonta import technical as ta
from pythonta import drawing as dt


def main():
    # Something to choose from
    # ^GSPC TSLA BTC-INR ^AEX ^AMX MSFT IWO BTC-USD

    # Download a pandas dataframe containing stock data
    df = yf.download('^GSPC',
                     start='2019-06-01',
                     end='2020-01-01',
                     progress=False)

    # Create a graph and clear it
    graph = dt.Graph(width=1280, height=1280)
    graph.clear()

    # Split it into two graphs with a ratio of 5 to 1
    candle_graph, volume_graph = graph.split_horizontal(5, 1)

    # Find tops and bottoms
    tops = ta.find_peaks(df, method=ta.CLASSIC, what=ta.TOPS)       # ta.CLASSIC or ta.MODERN
    bottoms = ta.find_peaks(df, method=ta.CLASSIC, what=ta.BOTTOMS)

    # Draw candles and volume
    candle_graph.draw_candles(df, greens=tops, reds=bottoms)
    volume_graph.draw_bars(df)

    # Find all trendlines
    lines = []
    lines += ta.find_support_and_ressitance(df, clearance=5, what=ta.SUPPORTS)
    lines += ta.find_support_and_ressitance(df, clearance=5, what=ta.RESISTS)

    lines += ta.find_trendlines(df, clearance=2, what=ta.SUPPORTS)
    lines += ta.find_trendlines(df, clearance=2, what=ta.RESISTS)

    # Draw them
    candle_graph.draw_lines(df, lines=lines)

    # Show the finished graph
    cv2.imshow('Technical analysis', graph.canvas)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()
