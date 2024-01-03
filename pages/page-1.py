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


dash.register_page(__name__, title='regions', path='/regions')
require_login(__name__)

main_df = create_main_df()
main_df = main_df[main_df['order_date'].dt.year == 2017]
main_df['order_date'] = pd.to_datetime(main_df['order_date']).dt.date


sales_by_region_df = main_df.groupby(['region', 'order_date'], as_index=False)['sales'].sum()
sales_region_bar_graph = px.histogram(sales_by_region_df, x='region', y='sales', text_auto=True).update_layout(
    margin=dict(l=0, r=0, t=30, b=0),
)


def layout():
    if not current_user.is_authenticated:
        return html.Div(["Please ", dcc.Link("login", href="/login"), " to continue"])

    return dbc.Container(children=[
        dbc.Row(dmc.DateRangePicker(
                            id="date-range-picker",
                            minDate=sales_by_region_df['order_date'].min(),
                            value=[sales_by_region_df['order_date'].min(), sales_by_region_df['order_date'].max()],
                            style={"width": 300},
                        ), className='m-2',  style={'height': '10vh'}),

        dbc.Row([dbc.Col(dcc.Graph(id='bar_graph', style={'height': '80%'}), width=4),
                 dbc.Col(dcc.Graph(id='line_graph', style={'height': '80%'}), width=8)], style={'height': '90vh'}),
                        ])

@callback(Output('bar_graph', 'figure'),
              Input('date-range-picker', 'value'))
def update_graph(value):
    if value:
        startdate = pd.to_datetime(value[0]).date()
        enddate = pd.to_datetime(value[1]).date()
        df = sales_by_region_df[(sales_by_region_df['order_date'] >= startdate) & (sales_by_region_df['order_date'] <= enddate)]
        updated_figure = px.histogram(df, x='region', y='sales', text_auto='0.2s', title='Sales by region').update_layout(clickmode="event+select",
    margin=dict(l=10, r=10, t=60, b=10))
        return updated_figure
    else:
        raise PreventUpdate

@callback(Output('line_graph', 'figure'),
Input('bar_graph', 'selectedData'),
              Input('date-range-picker', 'value'),
   )
def update_line(selectedData, value):

    if value:
        start_date = pd.to_datetime(value[0]).date()
        end_date = pd.to_datetime(value[1]).date()
        if selectedData is None:
            df = main_df[(main_df['order_date'] >= start_date) & (main_df['order_date'] <= end_date)]
            df = df.groupby('order_date', as_index=False)['sales'].sum()
            return px.line(df, x='order_date', y='sales', markers=True, title='daily sales').update_layout(margin=dict(l=10, r=10, t=60, b=10))
        else:
            country = selectedData['points'][0]['x']
            single_country_time_series_df = main_df[(main_df['region'] == country) & (main_df['order_date'] >= start_date) & (main_df['order_date'] <= end_date)]
            ecom_sales_line_country = single_country_time_series_df.groupby('order_date', as_index=False)['sales'].sum()
            fig = px.line(ecom_sales_line_country, x='order_date', y='sales', title=f'Sales for {country}', markers=True).update_layout(margin=dict(l=10, r=10, t=60, b=10))
            fig.update_traces(textposition="bottom right")
            return fig
    else:
        raise PreventUpdate

# dcc.DatePickerRange(id='date_range', min_date_allowed=sales_by_region_df['order_date'].min(),
#                     max_date_allowed=sales_by_region_df['order_date'].max(),
#                     display_format='DD/MM/YYYY',
#                     start_date = sales_by_region_df['order_date'].min(),
#                     end_date = sales_by_region_df['order_date'].max()
#                     ),