import dash
from dash import html, dcc, Output, Input, callback, ctx, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import dash_mantine_components as dmc
from pages.funcs import human_format, create_main_df, create_summary_card, create_graph_card, create_summary_line_graph,\
    create_main_graph, create_main_top10_graph, create_map_graph, compute_difference, graph_highlight, filter_regions

from datetime import datetime, timedelta, date
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
from utils.login_handler import require_login


dash.register_page(__name__, title='summary', path='/summary')
require_login(__name__)


main_df = create_main_df()
df_2_years = main_df.copy()
main_df = main_df[main_df['order_year'] == 2017]


monthly_sales = main_df.groupby('order_month', as_index=False)['sales'].sum()
monthly_profits = main_df.groupby('order_month', as_index=False)['profit'].sum()
monthly_orders = main_df.groupby('order_month', as_index=False)['order_id'].nunique()
monthly_customers = main_df.groupby('order_month', as_index=False)['customer_id'].nunique()

sales_fig = create_summary_line_graph(monthly_sales, 'sales')  # Making line chart from the above DFs
profits_fig = create_summary_line_graph(monthly_profits, 'profit')
orders_fig = create_summary_line_graph(monthly_orders, 'order_id')
customers_fig = create_summary_line_graph(monthly_customers, 'customer_id')


sales = '$' + human_format(main_df['sales'].sum())
profit = '$' + human_format(main_df['profit'].sum())
orders = human_format(main_df['order_id'].nunique())
customers = human_format(main_df['customer_id'].nunique())

sales_difference, sales_difference_style = compute_difference(df_2_years, 'sales', sum)
profit_difference, profit_difference_style = compute_difference(df_2_years, 'profit', sum)
orders_difference, orders_difference_style = compute_difference(df_2_years, 'order_id', pd.Series.nunique)
customers_difference, customers_difference_style = compute_difference(df_2_years, 'customer_id', pd.Series.nunique)


card_sales = create_summary_card("Sales", sales, sales_fig, 'sales_card_output', 'sales_line', sales_difference, sales_difference_style, 'sales_difference')
card_profit = create_summary_card("Profit", profit, profits_fig, 'profit_card_output', 'profit_line', profit_difference, profit_difference_style, 'profit_difference')
card_orders = create_summary_card("Orders", orders, orders_fig, 'orders_card_output', 'orders_line', orders_difference, orders_difference_style, 'orders_difference')
card_customers = create_summary_card("Customers", customers, customers_fig, 'customer_card_output', 'customers_line', customers_difference, customers_difference_style, 'customers_difference')

height = "100%"

by_category = create_graph_card('by_category')
by_segment = create_graph_card('by_segment')
by_manufacturer = create_graph_card('by_manufacturer')
by_state = create_graph_card('by_state')
by_customer = create_graph_card('by_customer')
by_sub_category = create_graph_card('by_sub_category')

choices = html.Div(
    [
        dmc.SegmentedControl(
            id="segmented",
            value="sales",
            data=[{"value": "sales", "label": "Sales"},
                  {"value": "profit", "label": "Profit"},
                  {"value": "order_id", "label": "Orders"}],
            color='blue.9',
            fullWidth=True,
            className='fw-bold me-4 shadow-sm',
            # style={'color':'black'}
        ),
    ]
)


date_range = html.Div(
    [
        dmc.DateRangePicker(
            id="date-range-picker",
            minDate=date(2020, 8, 5),
            value=[date(2022, 1, 1), date(2022, 12, 31)],
            icon=DashIconify(icon="fontisto:date"),
            clearable=False,
            disabled=True,
            style={"width": 300},
            className='mt-1'
        ),
    ]
)

layout = dbc.Container(
    [
        dcc.Store(id='store', data={'last_category': None, 'last_segment': None, 'last_subcategory': None,
                                    'last_state': None, 'category_filtered': False, 'segment_filtered': False,
                                    'sub_category_filtered': False, 'state_filtered': False, 'inputs': []}),
        dbc.Row([dbc.Col(html.H5(id='username'), width=3), dbc.Col(date_range, width={'offset': 1}), dbc.Col(choices, width={'offset': 2})]),
        dbc.Row([dbc.Col(card_sales), dbc.Col(card_profit), dbc.Col(card_orders), dbc.Col(card_customers)]),
        dbc.Row([dbc.Col(by_state, width=4, style={'height': height}),
                 dbc.Col(by_segment, width=4, style={'height': height}),
                 dbc.Col(by_manufacturer, width=4, style={'height': height})], className='mb-4', justify='around',
                style={"height": '35vh'}),
        dbc.Row([dbc.Col(by_category, width=4, style={'height': height}),
                 dbc.Col(by_sub_category, width=4, style={'height': height}),
                 dbc.Col(by_customer, width=4, style={'height': height})], className='mb-4', justify='around',
                style={"height": '35vh'}),
    ],
    fluid=True,
)


inputs = []
@callback([
Output('by_category', 'figure'), Output('by_state', 'figure'), Output('by_sub_category', 'figure'),
Output('by_segment', 'figure'), Output('by_customer', 'figure'), Output('by_manufacturer', 'figure'),
Output('sales_card_output', 'children'), Output('profit_card_output', 'children'), Output('orders_card_output', 'children'), Output('customer_card_output', 'children'),
Output('sales_line', 'figure'), Output('profit_line', 'figure'), Output('orders_line', 'figure'), Output('customers_line', 'figure'),
Output('sales_difference', 'children'), Output('profit_difference', 'children'), Output('orders_difference', 'children'), Output('customers_difference', 'children'),
Output('sales_difference', 'className'), Output('profit_difference', 'className'), Output('orders_difference', 'className'), Output('customers_difference', 'className'),
Output('regions', 'value'), Output('by_category', 'clickData'),
Output('by_sub_category', 'clickData'),  Output('by_segment', 'clickData'), Output('by_state', 'clickData'), Output('store', 'data')],
 [Input('segmented', 'value'), Input('ship_mode', 'value'), Input('regions', 'value'),  Input('by_category', 'clickData'),
  Input('by_state', 'clickData'), Input('by_sub_category', 'clickData'),
Input('by_segment', 'clickData')],
    State('store', 'data'),
    prevent_initial_call=True)
def update_graphs(value, ship_mode, regions, selected_category, selected_state, selected_subcategory, selected_segment
                  , app_state):
    df_2_years_copy = df_2_years.copy()
    print(df_2_years_copy.info())
    main_copy_df = main_df.copy()
    category_df = main_df.copy()
    segment_df = main_df.copy()
    sub_cat_df = main_df.copy()
    state_df = main_df.copy()
    manufacturer_df = main_df.copy()
    customer_df = main_df.copy()
    # get the values of the 'global variables' from the dcc.Store input
    last_category = app_state['last_category']
    last_segment = app_state['last_segment']
    last_subcategory = app_state['last_subcategory']
    last_state = app_state['last_state']
    category_filtered = app_state['category_filtered']
    segment_filtered = app_state['segment_filtered']
    sub_category_filtered = app_state['sub_category_filtered']
    state_filtered = app_state['state_filtered']
    inputs = app_state['inputs']
    graph_trigger = ctx.triggered_id  # get which figure triggered the callback

    dict = {}
    if graph_trigger == 'by_category' or graph_trigger == 'by_segment' or graph_trigger == 'by_sub_category':
        dict = {'input': ctx.triggered[0]['prop_id'].split('.')[0],
                'value': ctx.triggered[0]['value']['points'][0]['x']}
        inputs.append(dict)

    if graph_trigger == 'by_state':
        dict = {'input': ctx.triggered[0]['prop_id'].split('.')[0],
                'value': ctx.triggered[0]['value']['points'][0]['location']}
        inputs.append(dict)


    caetgoy_list = [d.get('value') for d in inputs if d.get('input') == 'by_category']
    segment_list = [d.get('value') for d in inputs if d.get('input') == 'by_segment']
    subcat_list = [d.get('value') for d in inputs if d.get('input') == 'by_sub_category']
    state_list = [d.get('value') for d in inputs if d.get('input') == 'by_state']

    # get the current selected value for each figure
    selected_category = caetgoy_list[-1] if len(caetgoy_list) >= 1 else None
    selected_segment = segment_list[-1] if len(segment_list) >= 1 else None
    selected_sub_category = subcat_list[-1] if len(subcat_list) >= 1 else None
    selected_state = state_list[-1] if len(state_list) >= 1 else None



    if selected_category is not None:
        if category_filtered and selected_category == last_category and graph_trigger == 'by_category':
            category_filtered = False
        elif category_filtered == False and graph_trigger != 'by_category':
            category_filtered = False
        else:
            segment_df = segment_df[segment_df['category'] == selected_category]
            sub_cat_df = sub_cat_df[sub_cat_df['category'] == selected_category]
            state_df = state_df[state_df['category'] == selected_category]
            manufacturer_df = manufacturer_df[manufacturer_df['category'] == selected_category]
            customer_df = customer_df[customer_df['category'] == selected_category]
            main_copy_df = main_copy_df[main_copy_df['category'] == selected_category]
            last_category = selected_category
            category_filtered = True
    else:
        category_filtered = False

    if selected_segment is not None:
        if segment_filtered and selected_segment == last_segment and graph_trigger == 'by_segment':
            segment_filtered = False
        elif segment_filtered == False and graph_trigger != 'by_segment':
            segment_filtered = False
        else:
            category_df = category_df[category_df['segment'] == selected_segment]
            sub_cat_df = sub_cat_df[sub_cat_df['segment'] == selected_segment]
            state_df = state_df[state_df['segment'] == selected_segment]
            manufacturer_df = manufacturer_df[manufacturer_df['segment'] == selected_segment]
            customer_df = customer_df[customer_df['segment'] == selected_segment]
            main_copy_df = main_copy_df[main_copy_df['segment'] == selected_segment]
            last_segment = selected_segment
            segment_filtered = True
    else:
        segment_filtered = False

    if selected_sub_category is not None:
        if sub_category_filtered and selected_sub_category == last_subcategory and graph_trigger == 'by_sub_category':
            sub_category_filtered = False
        elif sub_category_filtered == False and graph_trigger != 'by_sub_category':
            sub_category_filtered = False
        else:
            category_df = category_df[category_df['sub_category'] == selected_sub_category]
            segment_df = segment_df[segment_df['sub_category'] == selected_sub_category]
            state_df = state_df[state_df['sub_category'] == selected_sub_category]
            manufacturer_df = manufacturer_df[manufacturer_df['sub_category'] == selected_sub_category]
            customer_df = customer_df[customer_df['sub_category'] == selected_sub_category]
            main_copy_df = main_copy_df[main_copy_df['sub_category'] == selected_sub_category]
            last_subcategory = selected_sub_category
            sub_category_filtered = True
    else:
        sub_category_filtered = False

    if selected_state is not None:
        if state_filtered and selected_state == last_state and graph_trigger == 'by_state':
            state_filtered = False
        elif state_filtered == False and graph_trigger != 'by_state':
            state_filtered = False
        else:
            category_df = category_df[category_df['state_code'] == selected_state]
            segment_df = segment_df[segment_df['state_code'] == selected_state]
            sub_cat_df = sub_cat_df[sub_cat_df['state_code'] == selected_state]
            manufacturer_df = manufacturer_df[manufacturer_df['state_code'] == selected_state]
            customer_df = customer_df[customer_df['state_code'] == selected_state]
            main_copy_df = main_copy_df[main_copy_df['state_code'] == selected_state]
            last_state = selected_state
            state_filtered = True
    else:
        state_filtered = False

    if ship_mode:
        main_copy_df = main_copy_df[main_copy_df['ship_mode'].isin(ship_mode)]
        df_2_years_copy = df_2_years_copy[df_2_years_copy['ship_mode'].isin(ship_mode)]
        category_df = category_df[category_df['ship_mode'].isin(ship_mode)]
        segment_df = segment_df[segment_df['ship_mode'].isin(ship_mode)]
        sub_cat_df = sub_cat_df[sub_cat_df['ship_mode'].isin(ship_mode)]
        state_df = state_df[state_df['ship_mode'].isin(ship_mode)]
        manufacturer_df = manufacturer_df[manufacturer_df['ship_mode'].isin(ship_mode)]
        customer_df = customer_df[customer_df['ship_mode'].isin(ship_mode)]

    if regions[-1] == 'All':
        regions = ['South', 'West', 'Central', 'East']
        main_copy_df, df_2_years_copy, category_df, segment_df, sub_cat_df, state_df, manufacturer_df, customer_df \
        = filter_regions(main_copy_df, df_2_years_copy, category_df, segment_df, sub_cat_df, state_df, manufacturer_df, customer_df,regions)
        regions = ['All']
    elif len(regions) > 1 and 'All' in regions and regions[-1] != 'All':
        regions.remove('All')
        main_copy_df, df_2_years_copy, category_df, segment_df, sub_cat_df, state_df, manufacturer_df, customer_df = filter_regions(
            main_copy_df, df_2_years_copy, category_df, segment_df, sub_cat_df, state_df, manufacturer_df, customer_df,
            regions)
    else:
        main_copy_df, df_2_years_copy, category_df, segment_df, sub_cat_df, state_df, manufacturer_df, customer_df = filter_regions(
            main_copy_df, df_2_years_copy, category_df, segment_df, sub_cat_df, state_df, manufacturer_df, customer_df,
            regions)

    category_bar_graph = create_main_graph(category_df, x='category', y=value, title='Category', value=value)
    if selected_category is not None and category_filtered:
        graph_highlight(category_bar_graph, selected_category)

    segment_bar_graph = create_main_graph(segment_df, x='segment', y=value, title='Segment', value=value)
    if selected_segment is not None and segment_filtered:
        graph_highlight(segment_bar_graph, selected_segment)

    sub_category_bar_graph = create_main_graph(sub_cat_df, x='sub_category', y=value, title='Sub-Category', value=value)
    if selected_sub_category is not None and sub_category_filtered:
        graph_highlight(sub_category_bar_graph, selected_sub_category)

    state_map = create_map_graph(state_df, value)
    if selected_state is not None and state_filtered:
        graph_highlight(state_map, selected_state)

    manufacturer_bar_graph = create_main_top10_graph(manufacturer_df, x=value, y='manufacturer', title='Manufacturer', value=value)
    customer_bar_graph = create_main_top10_graph(customer_df, x=value, y='customer_name', title='Customer', value=value)

    app_state['last_category'] = last_category
    app_state['last_segment'] = last_segment
    app_state['last_subcategory'] = last_subcategory
    app_state['last_state'] = last_state
    app_state['category_filtered'] = category_filtered
    app_state['segment_filtered'] = segment_filtered
    app_state['sub_category_filtered'] = sub_category_filtered
    app_state['state_filtered'] = state_filtered
    app_state['inputs'] = inputs



    sales = '$' + human_format(main_copy_df['sales'].sum())
    profit = '$' + human_format(main_copy_df['profit'].sum())
    orders = human_format(main_copy_df['order_id'].nunique())
    customers = human_format(main_copy_df['customer_id'].nunique())

    monthly_sales = main_copy_df.groupby('order_month', as_index=False)['sales'].sum()
    monthly_profits = main_copy_df.groupby('order_month', as_index=False)['profit'].sum()
    monthly_orders = main_copy_df.groupby('order_month', as_index=False)['order_id'].nunique()
    monthly_customers = main_copy_df.groupby('order_month', as_index=False)['customer_id'].nunique()

    sales_fig = create_summary_line_graph(monthly_sales, 'sales')
    profits_fig = create_summary_line_graph(monthly_profits, 'profit')
    orders_fig = create_summary_line_graph(monthly_orders, 'order_id')
    customers_fig = create_summary_line_graph(monthly_customers, 'customer_id')

    sales_difference, sales_difference_style = compute_difference(df_2_years_copy, 'sales', sum)
    profit_difference, profit_difference_style = compute_difference(df_2_years_copy, 'profit', sum)
    orders_difference, orders_difference_style = compute_difference(df_2_years_copy, 'order_id', pd.Series.nunique)
    customers_difference, customers_difference_style = compute_difference(df_2_years_copy, 'customer_id', pd.Series.nunique)

    if ctx.triggered_id != 'regions':
        regions = dash.no_update

    return category_bar_graph, state_map, sub_category_bar_graph, segment_bar_graph, customer_bar_graph, manufacturer_bar_graph, sales, profit, orders, customers, sales_fig, profits_fig, orders_fig, customers_fig, sales_difference, profit_difference, orders_difference, customers_difference, sales_difference_style, profit_difference_style, orders_difference_style, customers_difference_style, regions, None, None, None,None, app_state


