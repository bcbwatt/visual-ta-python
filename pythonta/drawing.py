import cv2
import numpy as np

from pythonta import utils


class Graph:
    canvas = None
    top = 0
    left = 0
    bottom = 0
    right = 0

    heightmargin = 0.10
    candlesmargin = 0.5
    candlesrightfree = 10

    def clear(self):
        cv2.rectangle(self.canvas,
                      (self.left, self.top),
                      (self.right, self.bottom),
                      (0, 0, 0),
                      -1)

    def split_vertical(self, left, right):
        left_graph = Graph(0, 0)
        left_graph.canvas = self.canvas
        left_graph.top = self.top
        left_graph.bottom = self.bottom
        left_graph.left = self.left
        left_graph.right = int(self.right*left/(left+right))

        right_graph = Graph(0, 0)
        right_graph.canvas = self.canvas
        right_graph.top = self.top
        right_graph.bottom = self.bottom
        right_graph.left = left_graph.right+1
        right_graph.right = self.right

        return (left_graph, right_graph)

    def split_horizontal(self, top, bottom):
        top_graph = Graph(0, 0)
        top_graph.canvas = self.canvas
        top_graph.top = self.top
        top_graph.bottom = int(self.bottom*top/(top+bottom))
        top_graph.left = self.left
        top_graph.right = self.right

        bottom_graph = Graph(0, 0)
        bottom_graph.canvas = self.canvas
        bottom_graph.top = top_graph.bottom+1
        bottom_graph.bottom = self.bottom
        bottom_graph.left = self.left
        bottom_graph.right = self.right

        return (top_graph, bottom_graph)

    def get_width(self):
        return self.right-self.left

    def get_height(self):
        return self.bottom-self.top

    def __init__(self, width=0, height=0):
        if width == 0:
            return
        if height == 0:
            return

        self.right = width
        self.bottom = height
        self.canvas = np.zeros(shape=[height, width, 3], dtype=np.uint8)

    def draw_bars(self, dataframe):
        what = 'Volume'
        vmax = dataframe[what].max()
        if vmax == 0:
            return

        candle_left = 0
        candle_right = len(dataframe)+self.candlesrightfree
        color = (192, 192, 192)

        for index in range(0, len(dataframe)):
            row = dataframe.iloc[index]

            # Draw body
            x1 = index
            x2 = index + (1 - self.candlesmargin)
            start_point = (int(utils.translate(x1, candle_left, candle_right, self.left, self.right)),
                           int(utils.translate(row[what], 0, vmax, self.bottom, self.top)))
            end_point = (int(utils.translate(x2, candle_left, candle_right, self.left, self.right)),
                         self.bottom)
            thickness = -1

            cv2.rectangle(self.canvas,
                     start_point,
                     end_point,
                     color,
                     thickness)



    def draw_lines(self, dataframe, lines=[]):
        if len(lines) == 0:
            return
        candle_bottom = dataframe['Low'].min()
        candle_top = dataframe['High'].max()
        height_diff = (candle_top - candle_bottom) * self.heightmargin
        candle_bottom -= height_diff
        candle_top += height_diff

        candle_left = 0
        candle_right = len(dataframe)+self.candlesrightfree

        color = (192, 192, 192)

        for x1, y1, x2, y2 in lines:
            # Draw line
            start_point = (int(utils.translate(x1, candle_left, candle_right, self.left, self.right)),
                           int(utils.translate(y1, candle_bottom, candle_top, self.bottom, self.top)))
            end_point = (int(utils.translate(x2, candle_left, candle_right, self.left, self.right)),
                         int(utils.translate(y2, candle_bottom, candle_top, self.bottom, self.top)))
            thickness = 1

            cv2.line(self.canvas,
                     start_point,
                     end_point,
                     color,
                     thickness)

            lable = str(y2)[:7]
            end_point = (int(utils.translate(x2+1, candle_left, candle_right, self.left, self.right)),
                         int(utils.translate(y2, candle_bottom, candle_top, self.bottom, self.top))+3)
            cv2.putText(self.canvas,
                        lable,
                        end_point,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.35,
                        (255, 255, 255),
                        1,
                        cv2.LINE_AA)

    def draw_candles(self, dataframe, greens=[], reds=[]):
        candle_bottom = dataframe['Low'].min()
        candle_top = dataframe['High'].max()
        height_diff = (candle_top - candle_bottom) * self.heightmargin
        candle_bottom -= height_diff
        candle_top += height_diff

        candle_left = 0
        candle_right = len(dataframe)+self.candlesrightfree

        # Draw candles
        for index in range(0, len(dataframe)):
            row = dataframe.iloc[index]

            # Color
            color = (192, 192, 192)
            if index in greens:
                color = (0, 192, 0)
            if index in reds:
                color = (0, 0, 192)

            # Body high and low
            if row['Open'] > row['Close']:
                body_high = row['Open']
                body_low = row['Close']
            else:
                body_high = row['Close']
                body_low = row['Open']

            # Draw body top line
            x1 = index + (1-self.candlesmargin) / 2
            x2 = x1
            start_point = (int(utils.translate(x1, candle_left, candle_right, self.left, self.right)),
                           int(utils.translate(row['High'], candle_bottom, candle_top, self.bottom, self.top)))
            end_point = (int(utils.translate(x2, candle_left, candle_right, self.left, self.right)),
                         int(utils.translate(body_high, candle_bottom, candle_top, self.bottom, self.top)))
            thickness = 1

            cv2.line(self.canvas,
                     start_point,
                     end_point,
                     color,
                     thickness)

            # Draw body bottom line
            x1 = index + (1 - self.candlesmargin) / 2
            x2 = x1
            start_point = (int(utils.translate(x1, candle_left, candle_right, self.left, self.right)),
                           int(utils.translate(body_low, candle_bottom, candle_top, self.bottom, self.top)))
            end_point = (int(utils.translate(x2, candle_left, candle_right, self.left, self.right)),
                         int(utils.translate(row['Low'], candle_bottom, candle_top, self.bottom, self.top)))
            thickness = 1

            cv2.line(self.canvas,
                     start_point,
                     end_point,
                     color,
                     thickness)

            # Draw body
            x1 = index
            x2 = index + (1 - self.candlesmargin)
            start_point = (int(utils.translate(x1, candle_left, candle_right, self.left, self.right)),
                           int(utils.translate(row['Open'], candle_bottom, candle_top, self.bottom, self.top)))
            end_point = (int(utils.translate(x2, candle_left, candle_right, self.left, self.right)),
                         int(utils.translate(row['Close'], candle_bottom, candle_top, self.bottom, self.top)))
            thickness = -1

            cv2.rectangle(self.canvas,
                     start_point,
                     end_point,
                     color,
                     thickness)



