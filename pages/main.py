import dash
from dash import html, dcc, Output, Input, callback, ctx
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import dash_mantine_components as dmc
from pages.funcs import human_format, create_main_df, create_summary_card, create_graph_card, create_summary_line_graph,\
    create_main_graph, create_main_top10_graph, create_map_graph, compute_difference
from datetime import datetime, timedelta, date
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
from utils.login_handler import require_login
import numpy as np



dash.register_page(__name__, title='summary', path='/summary')
require_login(__name__)


main_df = create_main_df()
df_2_years = main_df.copy()
main_df = main_df[main_df['order_year'] == 2017]


monthly_sales = main_df.groupby('order_month', as_index=False)['sales'].sum()
monthly_profits = main_df.groupby('order_month', as_index=False)['profit'].sum()
monthly_orders = main_df.groupby('order_month', as_index=False)['orders'].nunique()
monthly_customers = main_df.groupby('order_month', as_index=False)['customer_id'].nunique()
sales_fig = create_summary_line_graph(monthly_sales, 'sales')  # Making line chart from the above DFs
profits_fig = create_summary_line_graph(monthly_profits, 'profit')
orders_fig = create_summary_line_graph(monthly_orders, 'orders')
customers_fig = create_summary_line_graph(monthly_customers, 'customer_id')


sales = '$' + human_format(main_df['sales'].sum())
profit = '$' + human_format(main_df['profit'].sum())
orders = human_format(main_df['orders'].nunique())
customers = human_format(main_df['customer_id'].nunique())

sales_difference, sales_difference_style = compute_difference(df_2_years, 'sales', sum)
profit_difference, profit_difference_style = compute_difference(df_2_years, 'profit', sum)
orders_difference, orders_difference_style = compute_difference(df_2_years, 'orders', pd.Series.nunique)
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
                  {"value": "orders", "label": "Orders"}],
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
            style={"width": 300},
            className='mt-1'
        ),
    ]
)

# date_range = html.Div(
#     [
#         dmc.DateRangePicker(
#             id="date-range-picker",
#             minDate=date(2020, 8, 5),
#             value=[date(2022, 1, 1), date(2022, 12, 31)],
#             style={"width": "100%"},
#             class_name='mt-1'
#         ),
#         html.Div(
#             [
#                 DashIconify(icon="fontisto:date"),
#             ]
#         )
#     ],
#     style={'display': 'inline-block'}
# )


# regions = np.insert(main_df['region'].unique(), 0, 'All')
# ship_modes = main_df['ship_mode'].unique()
#
#
# popovers = html.Div(
#     [
#         # First example - using dbc.PopoverBody
#         dbc.Button(
#             id="popover-target", className="bi bi-funnel"
#         ),
#         dbc.Popover(
#             dbc.PopoverBody([
#             dbc.Label("Region"),
#             dmc.MultiSelect(
#                 placeholder="Select all you like!",
#                 id="regions",
#                 clearable=True,
#                 data=regions,
#                 value=[regions[0]],
#                 style={"width": '100%', "marginBottom": 10},
#         ),
#             html.Hr(),
#             dbc.Label("Ship mode"),
#             dbc.Checklist(
#                 id="ship_mode",
#                 options=ship_modes,
#                 value=ship_modes,
#                 label_checked_style={"color": "#2471a1"},
#                 input_checked_style={
#                     "backgroundColor": "#2471a1",
#                     "borderColor": "#2471a1",
#                 },
#                 className='mb-1'
#             )
#                              ],
# style={'width':'300px','height':'250px'}
#                             ),
#             target="popover-target",
#             trigger="click",
#         ),
#         ]
# )


layout = dbc.Container(
    [
        dbc.Row([dbc.Col(html.H5('Welcome, Mohamed'), width=3), dbc.Col(date_range, width={'offset': 1}), dbc.Col(choices, width={'offset': 2})]),
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
Output('regions', 'value')],
           [Input('segmented', 'value'), Input('ship_mode', 'value'), Input('regions', 'value'),  Input('by_category', 'selectedData'), Input('by_state', 'selectedData'), Input('by_sub_category', 'selectedData'),
           Input('by_segment', 'selectedData'), Input('by_customer', 'selectedData'), Input('by_manufacturer', 'selectedData')])
def update_graphs(value, ship_mode, regions, selected_category, selected_state, selected_subcategory, selected_segment,selected_customer, selected_manufacturer):

    # global sales, profit, customers, orders
    main_copy_df = main_df.copy()
    df_2_years_copy = df_2_years.copy()

    if selected_category is not None:
       cat_selected = selected_category['points'][0]['x']
       main_copy_df = main_copy_df[main_copy_df['category'] == cat_selected]
       df_2_years_copy = df_2_years_copy[df_2_years_copy['category'] == cat_selected]

    if selected_state is not None:
       state_selected = selected_state['points'][0]['location']
       main_copy_df = main_copy_df[main_copy_df['state_code'] == state_selected]
       df_2_years_copy = df_2_years_copy[df_2_years_copy['state_code'] == state_selected]

    print(selected_state)
    if selected_subcategory is not None:
       subcat_selected = selected_subcategory['points'][0]['x']
       main_copy_df = main_copy_df[main_copy_df['sub_category'] == subcat_selected]
       df_2_years_copy = df_2_years_copy[df_2_years_copy['sub_category'] == subcat_selected]

    if selected_segment is not None:
       segment_selected = selected_segment['points'][0]['x']
       main_copy_df = main_copy_df[main_copy_df['segment'] == segment_selected]
       df_2_years_copy = df_2_years_copy[df_2_years_copy['segment'] == segment_selected]

    if ship_mode:
        main_copy_df = main_copy_df[main_copy_df['ship_mode'].isin(ship_mode)]
        df_2_years_copy = df_2_years_copy[df_2_years_copy['ship_mode'].isin(ship_mode)]

    if regions[-1] == 'All':
        all_regions = ['South', 'West', 'Central', 'East']
        main_copy_df = main_copy_df[main_copy_df['region'].isin(all_regions)]
        df_2_years_copy = df_2_years_copy[df_2_years_copy['region'].isin(all_regions)]
        regions = ['All']
    elif len(regions) > 1 and 'All' in regions and regions[-1] != 'All':
        regions.remove('All')
        main_copy_df = main_copy_df[main_copy_df['region'].isin(regions)]
        df_2_years_copy = df_2_years_copy[df_2_years_copy['region'].isin(regions)]
    else:
        main_copy_df = main_copy_df[main_copy_df['region'].isin(regions)]
        df_2_years_copy = df_2_years_copy[df_2_years_copy['region'].isin(regions)]




    # if selected_manufacturer is not None:
    #    manufacturer_selected = selected_manufacturer['points'][0]['x']
    #    main_copy_df = main_copy_df[main_copy_df['manufacturer'] == manufacturer_selected]

    state_map = create_map_graph(main_copy_df, value=value)
    category_bar_graph = create_main_graph(main_copy_df, x='category', y=value, title='Category', value=value)
    segment_bar_graph = create_main_graph(main_copy_df, x='segment', y=value, title='Segment', value=value)
    sub_category_bar_graph = create_main_graph(main_copy_df, x='sub_category', y=value, title='Sub-Category', value=value)
    manufacturer_bar_graph = create_main_top10_graph(main_copy_df, x=value, y='manufacturer', title='Manufacturer', value=value)
    customer_bar_graph = create_main_top10_graph(main_copy_df, x=value, y='customer_name', title='Customer', value=value)

    dic = {}
    if ctx.triggered_id == 'by_category' or ctx.triggered_id == 'by_segment' or ctx.triggered_id == 'by_sub_category':
        if ctx.triggered[0]['value'] is not None:
            dic = {'input': ctx.triggered[0]['prop_id'].split('.')[0], 'value':ctx.triggered[0]['value']['points'][0]['x']}
        else:
            dic = {'input': ctx.triggered[0]['prop_id'].split('.')[0], 'value':ctx.triggered[0]['value']}
    elif ctx.triggered_id == 'by_state':
        if ctx.triggered[0]['value'] is not None:
            dic = {'input': ctx.triggered[0]['prop_id'].split('.')[0], 'value':ctx.triggered[0]['value']['points'][0]['location']}
        else:
            dic = {'input': ctx.triggered[0]['prop_id'].split('.')[0], 'value': ctx.triggered[0]['value']}
    elif ctx.triggered_id == 'by_manufacturer':
        if ctx.triggered[0]['value'] is not None:
            dic = {'input': ctx.triggered[0]['prop_id'].split('.')[0], 'value':ctx.triggered[0]['value']['points'][0]['y']}
        else:
            dic = {'input': ctx.triggered[0]['prop_id'].split('.')[0], 'value': ctx.triggered[0]['value']}

    inputs.append(dic)
    print(inputs)
    # print(ctx.triggered)

    sales = '$' + human_format(main_copy_df['sales'].sum())
    profit = '$' + human_format(main_copy_df['profit'].sum())
    orders = human_format(main_copy_df['orders'].nunique())
    customers = human_format(main_copy_df['customer_id'].nunique())

    monthly_sales = main_copy_df.groupby('order_month', as_index=False)['sales'].sum()
    monthly_profits = main_copy_df.groupby('order_month', as_index=False)['profit'].sum()
    monthly_orders = main_copy_df.groupby('order_month', as_index=False)['orders'].nunique()
    monthly_customers = main_copy_df.groupby('order_month', as_index=False)['customer_id'].nunique()

    sales_fig = create_summary_line_graph(monthly_sales, 'sales')
    profits_fig = create_summary_line_graph(monthly_profits, 'profit')
    orders_fig = create_summary_line_graph(monthly_orders, 'orders')
    customers_fig = create_summary_line_graph(monthly_customers, 'customer_id')

    sales_difference, sales_difference_style = compute_difference(df_2_years_copy, 'sales', sum)
    profit_difference, profit_difference_style = compute_difference(df_2_years_copy, 'profit', sum)
    orders_difference, orders_difference_style = compute_difference(df_2_years_copy, 'orders', pd.Series.nunique)
    customers_difference, customers_difference_style = compute_difference(df_2_years_copy, 'customer_id', pd.Series.nunique)

    # if (ctx.triggered_id == 'by_category' or selected_category is not None) and selected_segment is None:
    #     return dash.no_update, state_map, sub_category_bar_graph, segment_bar_graph, customer_bar_graph, manufacturer_bar_graph, sales, profit, orders, customers, sales_fig, profits_fig, orders_fig, customers_fig
    # elif ctx.triggered_id == 'by_segment' or selected_segment is not None:
    #     return category_bar_graph, state_map, sub_category_bar_graph, dash.no_update, customer_bar_graph, manufacturer_bar_graph, sales, profit, orders, customers, sales_fig, profits_fig, orders_fig, customers_fig
    # else:
    #     return category_bar_graph, state_map, sub_category_bar_graph, segment_bar_graph, customer_bar_graph, manufacturer_bar_graph, sales, profit, orders, customers, sales_fig, profits_fig, orders_fig, customers_fig

    if ctx.triggered_id != 'regions':
        regions = dash.no_update

    if (ctx.triggered_id == 'by_category' or selected_category is not None) and selected_segment is None:
        return dash.no_update, state_map, sub_category_bar_graph, segment_bar_graph, customer_bar_graph, manufacturer_bar_graph, sales, profit, orders, customers, sales_fig, profits_fig, orders_fig, customers_fig, sales_difference, profit_difference, orders_difference, customers_difference, sales_difference_style, profit_difference_style, orders_difference_style, customers_difference_style, regions
    elif ctx.triggered_id == 'by_segment' or selected_segment is not None:
        return category_bar_graph, state_map, sub_category_bar_graph, dash.no_update, customer_bar_graph, manufacturer_bar_graph, sales, profit, orders, customers, sales_fig, profits_fig, orders_fig, customers_fig, sales_difference, profit_difference, orders_difference, customers_difference, sales_difference_style, profit_difference_style, orders_difference_style, customers_difference_style, regions
    else:
        return category_bar_graph, state_map, sub_category_bar_graph, segment_bar_graph, customer_bar_graph, manufacturer_bar_graph, sales, profit, orders, customers, sales_fig, profits_fig, orders_fig, customers_fig, sales_difference, profit_difference, orders_difference, customers_difference, sales_difference_style, profit_difference_style, orders_difference_style, customers_difference_style, regions

    # elif ctx.triggered_id == 'by_state' or selected_state is not None:
    #     return category_bar_graph, dash.no_update, sub_category_bar_graph, segment_bar_graph, customer_bar_graph, manufacturer_bar_graph
    # elif ctx.triggered_id == 'by_manufacturer' or selected_manufacturer is not None:
    #     return category_bar_graph, state_map, sub_category_bar_graph, segment_bar_graph, customer_bar_graph, dash.no_update
    # elif ctx.triggered_id == 'by_sub_category' or selected_subcategory is not None:
    #     return category_bar_graph, state_map, dash.no_update, segment_bar_graph, customer_bar_graph, manufacturer_bar_graph

    # @callback(Output("regions", "error"), Input("regions", "value"))
    # def select_value(value):
    #     return "Select at least 1." if len(value) < 1 else ""



# @callback(
#     Output("selected-date-date-range-picker", "children"),
#     Input("date-range-picker", "value"),
# )
# def update_output(dates):
#     prefix = "You have selected: "
#     if dates:
#         return prefix + "   -   ".join(dates)
#     else:
#         raise PreventUpdate

# MAKING GROUPED DATAFRAMES FOR THE FIGURES
# grouped_dataframe = main_df.groupby(['category', 'sub_category', 'segment', 'customer_id', 'customer_name', 'state', 'state_code',
#                                     'manufacturer'], as_index=False) \
#     .agg({'sales': 'sum', 'profit': 'sum', 'orders': 'nunique'})
