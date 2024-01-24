import dash
from dash import html, dcc, Output, Input, callback
from flask_login import current_user
from utils.login_handler import require_login
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from pages.funcs import create_main_df
from datetime import date, datetime
import random

dash.register_page(__name__, title='time', path='/time')
require_login(__name__)


df = create_main_df()

weekday_order = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
               'August', 'September', 'October', 'November', 'December']

df['order_day'] = pd.Categorical(df['order_day'], categories=weekday_order, ordered=True)
df['order_month'] = pd.Categorical(df['order_month'], categories=month_order, ordered=True)

numbers = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
weights = [1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 4, 4, 2, 2]
num_rows = df.shape[0]
random_numbers = random.choices(numbers, weights, k=num_rows)
df['hour'] = random_numbers


# MATRIX GRAPH & DATAFRAME
count_matrix = pd.crosstab(index=df['hour'], columns=df['order_day'], normalize=True)
count_matrix = count_matrix.div(count_matrix.sum().sum()).multiply(100).round(2)
fig = px.imshow(count_matrix, color_continuous_scale=px.colors.sequential.Blues, text_auto=True, labels=dict(x="Day",
                                    y="Hour",
                                    color="No of Orders"))
fig.update(layout_coloraxis_showscale=False).update_layout(hoverlabel=dict(
        bgcolor="#2471a1",
    ))

fig.layout.height = 600
fig.layout.width = 1200

# CATEGORICAL MONTH GRAPH & DATAFRAME

monthly_sales = df.groupby('order_month', as_index=False)['order_id'].nunique()
monthly_sales.rename(columns = {'order_id':'no_orders'}, inplace = True)
monthly_sales['Difference'] = monthly_sales['no_orders'].pct_change() * 100
fig2 = px.bar(monthly_sales, x='order_month', y='no_orders')
fig2.update_traces(texttemplate='%{y}', textposition='inside', insidetextanchor='middle')
for i in range(1, len(monthly_sales)):
    diff = monthly_sales.loc[i, 'Difference']
    if diff > 0:
        color = 'green'
    else:
        color = 'red'
    fig2.add_annotation(
        x=monthly_sales.loc[i, 'order_month'],
        y=monthly_sales.loc[i, 'no_orders'],
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
