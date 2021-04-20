"""This module takes a dataframe and converts it into encoded PNG"""

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigCanvas
import base64
from io import BytesIO


def create_plot(dataframe, x_values, y_values):
    """Return a plot by given data and axis"""
    fig = Figure(figsize=(7, 7), tight_layout=True)
    ax = fig.subplots()
    xs = dataframe[x_values].tolist()
    ys = dataframe[y_values].tolist()
    ax.plot(xs, ys)
    return fig


def encode_fig(fig):
    """Return encoded png by given figure plot."""
    png_image = BytesIO()
    FigCanvas(fig).print_png(png_image)
    png_b64 = "data:image/png;base64,"
    png_b64 += base64.b64encode(png_image.getvalue()).decode('utf8')
    return png_b64
