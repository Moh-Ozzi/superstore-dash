import dash
from dash import html, dcc, Output, Input, callback
from flask_login import current_user
from utils.login_handler import require_login
import plotly.express as px
import pandas as pd
from pages.funcs import create_main_df
from datetime import date, datetime
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate


dash.register_page(__name__, title='scatter', path='/scatter')
require_login(__name__)

main_df = create_main_df()
main_df = main_df[main_df['order_date'].dt.year == 2017]

top_products = main_df.groupby('product_name')['sales'].sum().sort_values(ascending=False).head(30).index
main_df = main_df[main_df['product_name'].isin(top_products)]


# Unique subcategories
unique_subcats = main_df['sub_category'].unique()

# Symbol list (extend as needed)
symbols = ['circle', 'square', 'diamond', 'cross', 'x', 'triangle-up', 'triangle-down', 'triangle-left', 'triangle-right', 'hexagram', 'hexagon']

fig = px.scatter(main_df, x="sales", y="profit", color='category', symbol='sub_category',
                 hover_data=['product_name']
                  ).update_traces(marker_size=13).update_layout(height=700)
for i, trace in enumerate(fig['data']):
    trace['marker']['symbol'] = symbols[i % len(symbols)]


def layout():
    if not current_user.is_authenticated:
        return html.Div(["Please ", dcc.Link("login", href="/login"), " to continue"])

    return dbc.Container(children=[
        dcc.Dropdown(
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': 'Montreal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'},
            ],
            value='MTL'
        ),
        dcc.Graph(id='scatter', figure=fig, className='mt-4')
    ])


