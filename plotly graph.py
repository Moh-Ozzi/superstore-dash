import dash
from dash import html, dcc, Output, Input, callback
import numpy as np
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import dash_mantine_components as dmc
import pycountry

# Radio constants
radio_categories = ["UMTS", "LTE", "GSM", "CDMA"]
radio_colors_list = ["green", "red", "blue", "orange"]
radio_colors = {cat: color for cat, color in zip(radio_categories, radio_colors_list)}

# Colors
bgcolor = "#f3f3f1"  # mapbox light map land color
bar_bgcolor = "#b0bec5"  # material blue-gray 200
bar_unselected_color = "#78909c"  # material blue-gray 400
bar_color = "#546e7a"  # material blue-gray 600
bar_selected_color = "#37474f"  # material blue-gray 800
bar_unselected_opacity = 0.8

# Figure template
row_heights = [150, 500, 300]
template = {"layout": {"paper_bgcolor": bgcolor, "plot_bgcolor": bgcolor}}



    # total_radio_counts = get_dataset(client, "total_radio_counts")

    fig = {
        "data": [
            {
                "type": "bar",
                "x": ['Apples', 'Oranges', 'Bananas'],
                "y": [10, 8, 12],
                "marker": {"color": bar_bgcolor},
                "orientation": "h",
                "selectedpoints": selectedpoints,
                "unselected": {"marker": {"opacity": 0.2}},
                "selected": {"marker": {"opacity": 1, "color": bar_bgcolor}},
                "showlegend": False,
                "hovertemplate": hovertemplate,
            },
        ],
        "layout": {
            "barmode": "overlay",
            "dragmode": "select",
            "selectdirection": "v",
            "clickmode": "event+select",
            "selectionrevision": True,
            "height": 150,
            "margin": {"l": 10, "r": 80, "t": 10, "b": 10},
            "xaxis": {
                "type": "log",
                "title": {"text": "Count"},
                # "range": [-1, np.log10(total_radio_counts.max() * 2)],
                "automargin": True,
            },
            "yaxis": {
                "type": "category",
                "categoryorder": "array",
                "categoryarray": radio_categories,
                "side": "left",
                "automargin": True,
            },
        },
    }

    # # Add selected bars in color
    # fig["data"].append(
    #     {
    #         "type": "bar",
    #         # "x": selected_radio_counts.loc[total_radio_counts.index],
    #         # "y": total_radio_counts.index,
    #         "orientation": "h",
    #         "marker": {
    #             "color": [radio_colors[cat] for cat in total_radio_counts.index]
    #         },

    #         "hovertemplate": hovertemplate,
    #         "showlegend": False,
    #     }
    # )

    return fig
selection_cleared = None
fig = build_radio_histogram(selection_cleared)


app = dash.Dash()

app.layout = html.Div(
    children=[
        html.H1('Fruit Sales Dashboard'),
        dcc.Graph(
            id='fruit-sales-chart',
            figure=fig
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)

