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

    # Get str_sequence from dataframe
    str_sequence = ta.peak_sequence(df)

    # Recognize some standard patterns
    if str_sequence[-6:] in [' HT HB', ' HB HT']:  # Higher tops and higher bottoms
        print('Uptrend!')

    if str_sequence[-6:] in [' LT LB', ' LB LT']:  # Lower tops and lower bottoms
        print('Downtrend!')

    return


if __name__ == '__main__':
    main()