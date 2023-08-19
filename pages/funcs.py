import pandas as pd
import plotly.express as px
import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine
import plotly.express as px
import pandas as pd
import socket

# FORMAT THE NUMBERS IN CARDS
def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


## CREATE THE MAIN DATAFRAME
def create_main_df():
    # server = socket.gethostname()
    # database = 'Super Store'
    # engine = create_engine('mssql+pyodbc://' + server + '/' + database + '?driver=SQL+Server')
    # query = 'SELECT * FROM orders'
    # main_df = pd.read_sql(query, engine)

    main_df = pd.read_csv('pages/cleaned_superstore.csv', engine='pyarrow', dtype_backend='pyarrow')
    # main_df[['ship_mode', 'segment', 'category', 'sub_category', 'region', 'country', 'state']] = main_df[['ship_mode', 'segment', 'category', 'sub_category', 'region', 'country', 'state']].astype('category')


    # main_df.columns = ['row_id', 'orders', 'order_date', 'ship_date', 'ship_mode', 'customer_id', 'customer_name',
    #                    'segment',
    #                    'country', 'city', 'state', 'postal_code', 'region', 'product_id', 'category', 'sub_category',
    #                    'prodcut_name',
    #                    'sales', 'quantity', 'discount', 'profit']
    # main_df['manufacturer'] = main_df['prodcut_name'].str.partition(' ')[0]
    # main_df['order_date'] = pd.to_datetime(main_df.order_date)
    # main_df['ship_date'] = pd.to_datetime(main_df.ship_date)
    # main_df['order_year'] = main_df.order_date.dt.year
    # main_df['order_day'] = main_df.order_date.dt.day_name()
    # month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
    #                'August', 'September', 'October', 'November', 'December']
    # main_df['order_month'] = pd.Categorical(main_df['order_date'].dt.month_name(), categories=month_order, ordered=True)
    # code = {'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    #         'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    #         'District of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI',
    #         'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    #         'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME',
    #         'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
    #         'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE',
    #         'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
    #         'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    #         'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI',
    #         'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX',
    #         'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
    #         'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'}
    # main_df['state_code'] = main_df['state'].map(code)
    # main_df['customer_name'] = main_df['customer_name'].apply(lambda x: x[0] + ', ' + x.split(' ')[-1])
    # main_df = main_df[main_df['order_year'].isin([2016, 2017])]
    # main_df.to_csv('pages/cleaned_superstore.csv', index=False)
    return main_df


# CREATE THE 4 MAIN CARDS   , difference, difference_style
def create_summary_card(card_title, value, fig, id, line_id, difference, difference_style, difference_id):
    card = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                [
                 dbc.Col(html.H6(card_title, className="text-nowrap")),
                 dbc.Col(html.Div([html.I(id=difference_id, children=difference, className=difference_style), " vs LY"], className="text-nowrap"), width={'offset':1})
                 ], style={'height': '50%'}, className='my-1'),

            dbc.Row(
                [
                dbc.Col(html.H4(children=value, id=id, className='text-nowrap text-center fw-bolder'), width=2),
                dbc.Col(dcc.Graph(id=line_id, figure=fig,
                        style={"height": "100%"},
                        config={'displayModeBar': False}
                    ),
                    width={'size':8, 'offset':2},)], style={'height': '50%'})
        ], className="border rounded border-white ps-2 pt-1"
    ),
    className='my-4 mx-1',
)
    return card

# Difference Style
def compute_difference(df, measure, func):
    num = (df.loc[df['order_year'] == 2017, measure].agg(func) - \
                   df.loc[df['order_year'] == 2016, measure].agg(func)) / \
                   df.loc[df['order_year'] == 2016, measure].agg(func) * 100
    if num > 0:
        style = "bi bi-caret-up-fill text-success text-nowrap"
    else:
        style = "bi bi-caret-down-fill text-danger text-nowrap"
    num = str(human_format(abs(num))) + '%'
    return num, style

##############
def create_graph_card(id, className='p-2'):
    height = "100%"
    card = dbc.Card(
    [dcc.Graph(id=id, style={'height': height})],
    style={'height': height},
    className=className
)
    return card


############

def create_summary_line_graph(df, y):
    fig = px.line(df, x='order_month', y=y, markers=True) \
        .update_xaxes(visible=False, fixedrange=True). \
        update_yaxes(visible=False, fixedrange=True). \
        update_layout(
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        autosize=True,
        showlegend=False,
        plot_bgcolor="white",
    ).update_traces(hovertemplate="<br>%{x}: %{y}</br>", marker=dict(size=4))
    return fig


def create_main_graph(df, x, y, title, value):
    if value == 'order_id':
        df = df.groupby(x, as_index=False)[y].nunique().sort_values(by=value, ascending=False)
    else:
        df = df.groupby(x, as_index=False)[y].sum().sort_values(by=value, ascending=False)
    fig = px.bar(df, x=x, y=y, text_auto='0.2s',
                 title=f'<b>{value.capitalize()}</b> by {title}').update_layout(yaxis_title=None,
                 xaxis_title=None, margin=dict(l=0, r=0, t=30, b=0), yaxis=dict(showticklabels=False, visible=False),
                 title=dict(font=dict(family='Arial', size=14), x=0.5))
    return fig


def create_main_top10_graph(df, x, y, title, value):
    if value == 'order_id':
        df = df.groupby(y, as_index=False)[value].nunique().nlargest(10, value).sort_values(by=value)
    else:
        df = df.groupby(y, as_index=False)[value].sum().nlargest(10, value).sort_values(by=value)
    fig = px.histogram(df, x=x, y=y, text_auto='0.2s',
                      title=f'<b>{value.capitalize()}</b> by {title}').update_layout(yaxis_title=None,
                      xaxis_title=None, margin=dict(l=0, r=0, t=30, b=0),
                      title=dict(font=dict(family='Arial', size=14), x=0.5))
    return fig

def create_map_graph(df, value):
    if value == 'order_id':
        grouped_by_state = df.groupby(['state', 'state_code'], as_index=False)[value].nunique()
    else:
        grouped_by_state = df.groupby(['state', 'state_code'], as_index=False)[value].sum()
    fig = px.choropleth(
        data_frame=grouped_by_state,
        locationmode='USA-states',
        locations='state_code',
        color=value,
        scope='usa',
        # custom_data=value,
        hover_name='state',
        # hover_data={'state': True, 'state_code': False, value:':.0f'},
        color_continuous_scale=px.colors.sequential.Blues,
        range_color=[grouped_by_state[value].min(), grouped_by_state[value].max()],
        title=f'<b>{value.capitalize()}</b> by State',
        labels={value: value},
    ).update_layout(margin=dict(l=0, r=0, t=30, b=0), coloraxis_showscale=True, coloraxis_colorbar_x=0.9,
                    title=dict(font=dict(family='Arial', size=16), x=0.5), hoverlabel=dict(bgcolor="#2471a1"))\
        .update_traces(marker_line_color='lightgrey')

    return fig


#
# def create_map_graph(df, value):
#     if value == 'orders':
#         grouped_by_state = df.groupby(['state', 'state_code'], as_index=False)[value].nunique()
#     else:
#         grouped_by_state = df.groupby(['state', 'state_code'], as_index=False)[value].sum()
#     fig = px.choropleth(
#         data_frame=grouped_by_state,
#         locationmode='USA-states',
#         locations='state_code',
#         color=value,
#         scope='usa',
#         hover_data=['state', value],
#         color_continuous_scale=px.colors.sequential.Blues,
#         range_color=[grouped_by_state[value].min(), grouped_by_state[value].max()],
#         title=f'<b>{value.capitalize()}</b> by State',
#         labels={'Sales': 'Sales'},
#     ).update_layout(margin=dict(l=0, r=0, t=30, b=0), coloraxis_showscale=False, clickmode="event+select",
#                     uirevision='dataset', title=dict(font=dict(family='Arial', size=14), x=0.5), hoverlabel=dict(
#         bgcolor="#2471a1"))
#
#     return fig

def graph_highlight(graph, selected_mark):
    if 'bar' in graph.data[0].type:
        graph["data"][0]["marker"]["opacity"] = [1 if c == selected_mark else 0.2 for c in graph["data"][0]["x"]]
        graph["data"][0]["marker"]["line"]['color'] = ['black' if c == selected_mark else 'grey' for c in graph["data"][0]["x"]]
        graph["data"][0]["marker"]["line"]['width'] = [2 if c == selected_mark else 1 for c in graph["data"][0]["x"]]
    elif 'choropleth' in graph.data[0].type:
        graph["data"][0]["marker"]["line"]['color'] = ['black' if c == selected_mark else 'lavender' for c in graph["data"][0]['locations']]
        graph["data"][0]["marker"]["line"]['width'] = [3 if c == selected_mark else 0.2 for c in graph["data"][0]['locations']]
        graph['data'][0]['z'] = [max(graph['data'][0]['z'] / 1.5) if c == selected_mark else 0 for c in graph["data"][0]['locations']]
    return graph

def filter_regions(main_copy_df, df_2_years_copy, category_df, segment_df, sub_cat_df, state_df, manufacturer_df, customer_df, regions):
    main_copy_df = main_copy_df[main_copy_df['region'].isin(regions)]
    df_2_years_copy = df_2_years_copy[df_2_years_copy['region'].isin(regions)]
    category_df = category_df[category_df['region'].isin(regions)]
    segment_df = segment_df[segment_df['region'].isin(regions)]
    sub_cat_df = sub_cat_df[sub_cat_df['region'].isin(regions)]
    state_df = state_df[state_df['region'].isin(regions)]
    manufacturer_df = manufacturer_df[manufacturer_df['region'].isin(regions)]
    customer_df = customer_df[customer_df['region'].isin(regions)]
    return main_copy_df, df_2_years_copy, category_df, segment_df, sub_cat_df, state_df, manufacturer_df, customer_df
