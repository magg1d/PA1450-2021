"""This module takes a dataframe and converts it into encoded PNG"""

from matplotlib.figure import Figure
from pandas import date_range, Timestamp
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigCanvas
from datetime import datetime
import base64
from io import BytesIO


def create_plot(dataframe, x_values, y_values, secondary_y=None):
    """Return a plot by given data and axis"""
    fig = Figure(figsize=(7, 7), tight_layout=True)
    ax = fig.subplots()
    dataframe['Last_Update'] = dataframe['Last_Update'].apply(lambda x: Timestamp(x).strftime('%Y-%m-%d'))
    xs = dataframe[x_values].tolist()
    ys = dataframe[y_values].tolist()
    if secondary_y is not None:
        y2s = dataframe[secondary_y].tolist()
        line1, = ax.plot(xs, ys, label="Two Doses")
        line2, = ax.plot(xs, y2s, label="One Dose")
        ax.legend(handles=[line1, line2])
        days_elapsed = len(date_range(xs[0], xs[-1], freq='D'))
        ax.set_xticks(range(0, days_elapsed, 7))
    else:
        line1, = ax.plot(xs, ys, label=y_values)
        ax.legend(handles=[line1])

    fig.autofmt_xdate()

    return fig


def encode_fig(fig):
    """Return encoded png by given figure plot."""
    png_image = BytesIO()
    FigCanvas(fig).print_png(png_image)
    png_b64 = "data:image/png;base64,"
    png_b64 += base64.b64encode(png_image.getvalue()).decode('utf8')
    return png_b64
