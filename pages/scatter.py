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
from plotly.validators.scatter.marker import SymbolValidator
from dash.exceptions import PreventUpdate


dash.register_page(__name__, title='scatter', path='/scatter')
require_login(__name__)


main_df = create_main_df()
main_df = main_df[main_df['order_date'].dt.year == 2017]


raw_symbols = SymbolValidator().values
namestems = []
for i in range(0,len(raw_symbols),3):
    name = raw_symbols[i+2]
    namestems.append(name.replace("-open", "").replace("-dot", ""))

unique_symbols = sorted(list(set(namestems)))
filtered_symbols_list = [item for item in unique_symbols if '-' not in item]


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
        value = 'product_name'
        level1 = 'category'
        level2 = 'sub_category'
    else:
        value = 'city'
        level1 = 'region'
        level2 = 'state'

    top_30 = main_df2.groupby(value)['sales'].sum().sort_values(ascending=False).head(30).index
    df1 = main_df2[main_df2[value].isin(top_30)]
    df1 = df1.groupby([level1, level2, value], as_index=False).agg({'sales': 'sum', 'profit': 'sum'})
    fig = px.scatter(df1, x="sales", y="profit", color=level1, symbol=level2,
                          title=f'Sales VS Profit of {input}', hover_name=value
                         ).update_traces(marker_size=13).update_layout(height=600, yaxis_title='Profit', xaxis_title='Sales').update_yaxes(
            zeroline=True,
            visible=True,
            zerolinecolor='black',
            zerolinewidth=1).update_xaxes(
            range=[-1, max(df1['sales']) + (max(df1['sales']) * 0.01)],
            zeroline=True,
            visible=True,
            zerolinecolor='black',
            zerolinewidth=1)
    # for i, trace in enumerate(fig['data']):
    #     trace['marker']['symbol'] = filtered_symbols_list[i % len(filtered_symbols_list)]
    return fig

