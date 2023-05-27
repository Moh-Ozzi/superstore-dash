import dash
from dash import html, dcc, Output, Input, callback
from flask_login import current_user
from utils.login_handler import require_login
import plotly.express as px
import pandas as pd
from datetime import date, datetime


dash.register_page(__name__, title='countries', path='/countries')
require_login(__name__)

ecom_sales = pd.read_excel('pages/ecom_sales.xlsx')
ecom_sales['InvoiceDate'] = ecom_sales['InvoiceDate'].dt.date
sales_by_country_df = ecom_sales.groupby(['Country', 'InvoiceDate'], as_index=False)['OrderValue'].sum()
sales_country_bar_graph = px.histogram(sales_by_country_df, x='Country', y='OrderValue', text_auto=True)


def layout():
    if not current_user.is_authenticated:
        return html.Div(["Please ", dcc.Link("login", href="/login"), " to continue"])

    return html.Div(children=[
                        dcc.DatePickerRange(id='date_range', min_date_allowed=sales_by_country_df['InvoiceDate'].min(),
                                            max_date_allowed=sales_by_country_df['InvoiceDate'].max(),
                                            display_format='DD/MM/YYYY',
                                            start_date = sales_by_country_df['InvoiceDate'].min(),
                                            end_date = sales_by_country_df['InvoiceDate'].max()
                                            ),
                        dcc.Graph(id='bar_graph', figure=sales_country_bar_graph, clear_on_unhover=True),
                        dcc.Graph(id='line_graph')
                        ])

@callback(Output('bar_graph', 'figure'),
              Input('date_range', 'start_date'),
              Input('date_range', 'end_date'))
def update_graph(start_date, end_date):

    startdate = pd.to_datetime(start_date).date()
    enddate = pd.to_datetime(end_date).date()
    df = sales_by_country_df[(sales_by_country_df['InvoiceDate'] >= startdate) & (sales_by_country_df['InvoiceDate'] <= enddate)]
    updated_figure = px.histogram(df, x='Country', y='OrderValue', text_auto=True, title='Sales by country').update_layout(clickmode="event+select")
    return updated_figure


selected_country = None

@callback(Output('line_graph', 'figure'),
Input('bar_graph', 'selectedData'),
              Input('date_range', 'start_date'),
              Input('date_range', 'end_date'))
def update_line(selectedData, start_date, end_date):

    global selected_country
    startdate = pd.to_datetime(start_date).date()
    enddate = pd.to_datetime(end_date).date()

    if selectedData is None:
        df = ecom_sales[(ecom_sales['InvoiceDate'] >= startdate) & (ecom_sales['InvoiceDate'] <= enddate)]
        df = df.groupby('InvoiceDate', as_index=False)['OrderValue'].sum()
        return px.line(df, x='InvoiceDate', y='OrderValue', markers=True)
    else:
        country = selectedData['points'][0]['x']
        # selected_country = selectedData['points'][0]['x']
        single_country_time_series_df = ecom_sales[(ecom_sales['Country']== country) & (ecom_sales['InvoiceDate'] >= startdate) & (ecom_sales['InvoiceDate'] <= enddate)]
        ecom_sales_line_country = single_country_time_series_df.groupby('InvoiceDate', as_index=False)['OrderValue'].sum()
        fig = px.line(ecom_sales_line_country, x='InvoiceDate', y='OrderValue', title=f'Sales for {country}', markers=True)
        fig.update_traces(textposition="bottom right")
        return fig
