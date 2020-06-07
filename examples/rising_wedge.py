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
    support_lines = ta.find_trendlines(df, clearance=2, what=ta.SUPPORTS)
    resist_lines = ta.find_trendlines(df, clearance=2, what=ta.RESISTS)

    # Is it a rising wedge?
    # Let's try all combinations between support and resist lines
    for s in support_lines:
        for r in resist_lines:
            # Support line
            x1, y1, x2, y2 = s                  # Extract the attributes of te line
            s_inclination = (y2-y1) / (x2-x1)   # Calculate the inclination per candle

            # Resist line
            x1, y1, x2, y2 = r
            r_inclination = (y2-y1) / (x2-x1)
            print(f'{s_inclination} over {r_inclination}')

            if s_inclination > 0:   # Support line is rising
                if r_inclination < s_inclination:   # Resist line is not rising as fast as support line
                    print("Found a rising wedge")
                    candle_graph.draw_lines(df, lines=[s])
                    candle_graph.draw_lines(df, lines=[r])

    # Uncomment these to show all trendlines
    #candle_graph.draw_lines(df, lines=support_lines)
    #candle_graph.draw_lines(df, lines=resist_lines)

    # Show the finished graph
    cv2.imshow('Technical analysis', graph.canvas)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()
