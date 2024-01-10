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



# Unique subcategories
unique_subcats = main_df['sub_category'].unique()
print(unique_subcats)

# Symbol list (extend as needed)
symbols = ['circle', 'square', 'diamond', 'cross', 'x', 'triangle-up', 'triangle-down', 'triangle-left', 'triangle-right', 'hexagram', 'hexagon']


# for i, trace in enumerate(fig['data']):
#     trace['marker']['symbol'] = symbols[i % len(symbols)]


def layout():
    if not current_user.is_authenticated:
        return html.Div(["Please ", dcc.Link("login", href="/login"), " to continue"])

    return dbc.Container(children=[
        dcc.Dropdown(
            ['Product', 'City'], 'Product', id='dropdown'
        ),
        dcc.Graph(id='scatter', className='mt-4')
    ])

@callback(Output('scatter', 'figure'), Input('dropdown', 'value'))
def update_figure(input):
    main_df2 = main_df.copy()
    if input == 'Product':
        top_products = main_df2.groupby('product_name')['sales'].sum().sort_values(ascending=False).head(30).index
        df = main_df2[main_df2['product_name'].isin(top_products)]
        df = df.groupby(['category', 'sub_category', 'product_name'], as_index=False).agg(
            {'sales': 'sum', 'profit': 'sum'})
        fig = px.scatter(df, x="sales", y="profit", color='category', symbol='sub_category',
                         hover_data=['product_name']
                         ).update_traces(marker_size=13).update_layout(height=700)
    elif input == 'City':
        top_cities = main_df2.groupby('city')['sales'].sum().sort_values(ascending=False).head(30).index
        df = main_df2[main_df2['city'].isin(top_cities)]
        df = df.groupby(['region', 'state', 'city'], as_index=False).agg(
            {'sales': 'sum', 'profit': 'sum'})
        fig = px.scatter(df, x="sales", y="profit", color='region', symbol='state',
                         hover_data=['city']
                         ).update_traces(marker_size=13).update_layout(height=700)
    return fig

