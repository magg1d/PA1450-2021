"""Module for serving an API."""

from flask import Flask, render_template, request
from ..data.data_filterer import compare_data, data_over_time, filter_data
from ..data.plotter import create_plot, encode_fig
from pandas import to_datetime, unique
from ..data.json_loader import load_json
from datetime import datetime as dt

FILTER_TYPES = ["Country_Region", "Province_State", "Admin2"]

def serve(options):
    """Serve an API."""

    # Create a Flask application
    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    @app.route("/")
    def home():
        """Return the index page of the website."""
        return render_template("index.html", show_fig=False, filter_types=FILTER_TYPES)

    @app.route("/plot", methods=['POST', 'GET'])
    def figure():
        if request.method == "POST":
            # Get form values
            filter_type = request.form.get('filter-type')
            filter_value = request.form.get('filter-value')
            data_type = request.form.get('data-type')
            start_date_form = request.form.get('start-date')
            end_date_form = request.form.get('end-date')
            start_date = to_datetime(start_date_form, format='%Y-%m-%d')
            end_date = to_datetime(end_date_form, format='%Y-%m-%d')
            show_by = request.form.get('choose-data')

            if data_type == "n_total":
                data = load_json()
                data = filter_data(data, filter_type, filter_value)
                secondary_y = "n_full"
            else:
                secondary_y = None
                if show_by == "delta":
                    interval = int(request.form.get('interval'))
                    data = data_over_time(filter_type, filter_value, data_type, start_date, end_date, interval)
                elif show_by == "total":
                    data = compare_data(filter_type, filter_value, start_date, end_date, "plot")
                else:
                    return render_template("index.html", errormsg="Please input valid options", filter_types=FILTER_TYPES)

            plot = create_plot(data, "Last_Update", data_type, secondary_y)
            fig_b64 = encode_fig(plot)
            return render_template("index.html", showFig=True, fig=fig_b64, filter_types=FILTER_TYPES)
        render_template("index.html", show_fig=False, filter_types=FILTER_TYPES)

    @app.route("/api/<filter>/<key>")
    def api(filter, key):
        data = compare_data(filter, key, dt(2021,1,1), dt(2021,4,1), "local", "api")
        json = data.to_json(orient='split')
        return render_template("api.html", json=json)

    app.run(host=options.address, port=options.port, debug=True)


def create_parser(subparsers):
    """Create an argument parser for the "serve" command."""
    parser = subparsers.add_parser("serve")
    parser.set_defaults(command=serve)
    # Add optional parameters to control the server configuration
    parser.add_argument("-p", "--port", default=8080, type=int, help="The port to listen on")
    parser.add_argument("--address", default="0.0.0.0", help="The address to listen on")
