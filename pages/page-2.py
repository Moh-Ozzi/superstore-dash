import dash
from dash import html, dcc, Output, Input, callback
from flask_login import current_user
from utils.login_handler import require_login
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from datetime import date, datetime

dash.register_page(__name__, title='Category', path='/categories')
require_login(__name__)


ecom_sales = pd.read_excel('pages/ecom_sales.xlsx')

ecom_sales['InvoiceDate'] = ecom_sales['InvoiceDate'].dt.date

ecom_sales = ecom_sales.groupby(['InvoiceDate', 'Country', 'Major Category', 'Minor Category'], as_index=False)\
             ['OrderValue'].sum()


major_cats = ecom_sales['Major Category'].unique()
major_cats = np.insert(major_cats, 0, 'All')

def layout():
    if not current_user.is_authenticated:
        return html.Div(["Please ", dcc.Link("login", href="/login"), " to continue"])

    return html.Div(children=[
                        dcc.DatePickerRange(id='date_range', min_date_allowed=ecom_sales['InvoiceDate'].min(),
                                            max_date_allowed=ecom_sales['InvoiceDate'].max(),
                                            display_format='DD/MM/YYYY',
                                            start_date = ecom_sales['InvoiceDate'].min(),
                                            end_date = ecom_sales['InvoiceDate'].max()
                                            ),
                        html.Br(),
                        html.Hr(),
                        dbc.RadioItems(id='radio', options=major_cats, value=major_cats[0], inline=True),
                        html.Br(),
                        dbc.Checklist(id='checklist', persistence=True, persistence_type='local', inline=True),
                        dcc.Graph(id='bar_graph_2'),
                        # dcc.Graph(id='line_graph')
                        ])


@callback([
              Output('checklist', 'options'),
               Output('checklist', 'value')],
              Input('radio', 'value'))

def update_graph(value):
    if value == 'All':
        checklist_options = []
    else:
        checklist_options = ecom_sales[ecom_sales['Major Category'] == value]['Minor Category'].unique()
    checklist_value = checklist_options
    return checklist_options, checklist_value


@callback(Output('bar_graph_2', 'figure'),
              [Input('checklist', 'value'),
              Input('radio', 'value'),
              Input('date_range', 'start_date'),
              Input('date_range', 'end_date')]
              )
def update_checklist(value, options, start_date, end_date):

    startdate = pd.to_datetime(start_date).date()
    enddate = pd.to_datetime(end_date).date()
    if value == [] and options == 'All':
        df = ecom_sales[(ecom_sales['InvoiceDate'] >= startdate) & (ecom_sales['InvoiceDate'] <= enddate)]
    else:
        df = ecom_sales[(ecom_sales['Minor Category'].isin(value)) & (ecom_sales['InvoiceDate'] >= startdate) & (ecom_sales['InvoiceDate'] <= enddate)]

    fig = px.histogram(df, x='Country', y='OrderValue', text_auto=True)
    return fig

