import dash
from dash import html, dcc, Output, Input, callback
from flask_login import current_user
from utils.login_handler import require_login
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from pages.funcs import create_main_df
from datetime import date, datetime



dash.register_page(__name__, title='time', path='/time')
require_login(__name__)

df1 = create_main_df()




df = pd.read_excel('pages/ecom_sales.xlsx')

# MATRIX GRAPH & DATAFRAME
df['InvoiceTime'] = pd.to_datetime(df['InvoiceTime'], format='%H:%M:%S')
df['InvoiceHour'] = df['InvoiceTime'].dt.hour
df['WeekDay'] = df['InvoiceDate'].dt.day_name()
count_matrix = pd.crosstab(index=df['InvoiceHour'], columns=df['WeekDay'])
fig = px.imshow(count_matrix, color_continuous_scale=px.colors.sequential.Blues, text_auto=True, labels=dict(x="WeekDay",
                                    y="Hour",
                                    color="No of Orders"))
fig.update(layout_coloraxis_showscale=False).update_layout(hoverlabel=dict(
        bgcolor="#2471a1",
    ))

# CATEGORICAL MONTH GRAPH & DATAFRAME
df['MonthName'] = df['InvoiceDate'].dt.month_name()
df['MonthName'] = df['MonthName'].astype('category')
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
               'August', 'September', 'October', 'November', 'December']
df['MonthName'] = pd.Categorical(df['InvoiceDate'].dt.month_name(), categories=month_order, ordered=True)
monthly_sales = df.groupby('MonthName', as_index=False)['InvoiceNo'].nunique()
monthly_sales['InvoiceNo'] = monthly_sales['InvoiceNo'] * 4
monthly_sales.rename(columns = {'InvoiceNo':'Orders'}, inplace = True)
monthly_sales['Difference'] = monthly_sales['Orders'].pct_change() * 100
fig2 = px.bar(monthly_sales, x='MonthName', y='Orders')
fig2.update_traces(texttemplate='%{y}', textposition='inside', insidetextanchor='middle')
for i in range(1, len(monthly_sales)):
    diff = monthly_sales.loc[i, 'Difference']
    if diff > 0:
        color = 'green'
    else:
        color = 'red'
    fig2.add_annotation(
        x=monthly_sales.loc[i, 'MonthName'],
        y=monthly_sales.loc[i, 'Orders'],
        text=f'{diff:.1f}%',
        showarrow=False,
        font=dict(color=color),
        xshift=0,
        yshift=10
    )
fig2.update_layout(
    xaxis_title='Month',
    yaxis_title='Orders',
    yaxis=dict(showgrid=False),
    hoverlabel=dict(
        bgcolor="#2471a1",
    )
)



tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("Orders by Weekday and Hour", className="card.py-text"),
            dcc.Graph(id='heatmap', figure=fig)
        ]
    ),
    className="mt-3 p-6",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("Orders by Categorical Month", className="card.py-text"),
            dcc.Graph(id='bar', figure=fig2),
        ]
    ),
    className="mt-3",
)

tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Matrix"),
        dbc.Tab(tab2_content, label="Month"),
    ]
)

def layout():
    if not current_user.is_authenticated:
        return html.Div(["Please ", dcc.Link("login", href="/login"), " to continue"])

    return html.Div(children=[
        tabs
                        ])
