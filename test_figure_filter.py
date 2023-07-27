import dash
from dash import Dash, html, dcc, Output, Input, callback, ctx
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from funcs2 import  create_main_df, create_graph_card, create_main_graph


app = Dash(__name__)


main_df = create_main_df()
df_2_years = main_df.copy()
main_df = main_df[main_df['order_year'] == 2017]




height = "100%"

by_category = create_graph_card('by_category')
by_segment = create_graph_card('by_segment')
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




app.layout = dbc.Container(
    [
        dbc.Row(dbc.Col(choices, width=6)),
        dbc.Row([dbc.Col(by_segment, width=4, style={'height': height})], className='mb-4', justify='around',
                style={"height": '30vh'}),
        dbc.Row([dbc.Col(by_category, width=4, style={'height': height}),
                 dbc.Col(by_sub_category, width=4, style={'height': height})], className='mb-4', justify='around',
                style={"height": '30vh'}),
    ],
    fluid=True,
)


inputs = []



@callback([
Output('by_category', 'figure'), Output('by_sub_category', 'figure'),
Output('by_segment', 'figure')
],
           [Input('segmented', 'value'), Input('by_category', 'selectedData'), Input('by_sub_category', 'selectedData'),
           Input('by_segment', 'selectedData')])
def update_graphs(value, selected_category, selected_subcategory, selected_segment):
    # Initiate a copy of main_df for each graph
    category_df = main_df.copy()
    segment_df = main_df.copy()
    sub_cat_df = main_df.copy()

    # Check which graph was clicked
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print(triggered_id)

    if selected_category is not None:
        cat_selected = selected_category['points'][0]['x']

        # Filter the data for segment and sub-category graphs
        if triggered_id != 'by_category':
            segment_df = segment_df[segment_df['category'] == cat_selected]
            sub_cat_df = sub_cat_df[sub_cat_df['category'] == cat_selected]

    if selected_subcategory is not None:
        subcat_selected = selected_subcategory['points'][0]['x']

        # Filter the data for category and segment graphs
        if triggered_id != 'by_sub_category':
            category_df = category_df[category_df['sub_category'] == subcat_selected]
            segment_df = segment_df[segment_df['sub_category'] == subcat_selected]

    if selected_segment is not None:
        segment_selected = selected_segment['points'][0]['x']

        # Filter the data for category and sub-category graphs
        if triggered_id != 'by_segment':
            category_df = category_df[category_df['segment'] == segment_selected]
            sub_cat_df = sub_cat_df[sub_cat_df['segment'] == segment_selected]

    # Create graphs with respective dataframes
    category_bar_graph = create_main_graph(category_df, x='category', y=value, title='Category', value=value)
    segment_bar_graph = create_main_graph(segment_df, x='segment', y=value, title='Segment', value=value)
    sub_category_bar_graph = create_main_graph(sub_cat_df, x='sub_category', y=value, title='Sub-Category', value=value)

    return category_bar_graph, sub_category_bar_graph, segment_bar_graph




if __name__ == '__main__':
    app.run(debug=True)




# def update_graphs(value, selected_category, selected_subcategory, selected_segment):
#     main_copy_df = main_df.copy()
#
#     category_df = main_copy_df.copy()
#     segment_df = main_copy_df.copy()
#     sub_cat_df = main_copy_df.copy()
#
#     print('category: ' + str(selected_category))
#     # print('sub_category: ' + str(selected_subcategory))
#     # print('segment: ' + str(selected_segment))
#
#
#     if selected_category is not None:
#        cat_selected = selected_category['points'][0]['x']
#        segment_df = main_copy_df[main_copy_df['category'] == cat_selected]
#        sub_cat_df = main_copy_df[main_copy_df['category'] == cat_selected]
#
#     if selected_subcategory is not None:
#        subcat_selected = selected_subcategory['points'][0]['x']
#        category_df = main_copy_df[main_copy_df['sub_category'] == subcat_selected]
#        segment_df = main_copy_df[main_copy_df['sub_category'] == subcat_selected]
#
#     if selected_segment is not None:
#        segment_selected = selected_segment['points'][0]['x']
#        category_df = main_copy_df[main_copy_df['segment'] == segment_selected]
#        sub_cat_df = main_copy_df[main_copy_df['segment'] == segment_selected]
#
#
#     category_bar_graph = create_main_graph(category_df, x='category', y=value, title='Category', value=value)
#     segment_bar_graph = create_main_graph(segment_df, x='segment', y=value, title='Segment', value=value)
#     print('category: ' + str(selected_category))
#     sub_category_bar_graph = create_main_graph(sub_cat_df, x='sub_category', y=value, title='Sub-Category', value=value)
#
#     dic = {}
#     if ctx.triggered_id == 'by_category' or ctx.triggered_id == 'by_segment' or ctx.triggered_id == 'by_sub_category':
#         if ctx.triggered[0]['value'] is not None:
#             dic = {'input': ctx.triggered[0]['prop_id'].split('.')[0], 'value':ctx.triggered[0]['value']['points'][0]['x']}
#         else:
#             dic = {'input': ctx.triggered[0]['prop_id'].split('.')[0], 'value':ctx.triggered[0]['value']}
#     # elif ctx.triggered_id == 'segmented':
#     #     if len(ctx.triggered) > 1:
#     #         print('All')
#     #     else:
#     #         print(ctx.triggered)
#
#     inputs.append(dic)
#     # print(inputs)
#
#     #
#     # if ctx.triggered_id == 'by_category':
#     #     return category_bar_graph, sub_category_bar_graph, segment_bar_graph
#     # elif ctx.triggered_id == 'by_segment':
#     #     return category_bar_graph, sub_category_bar_graph, segment_bar_graph
#     # else:
#     return category_bar_graph, sub_category_bar_graph, segment_bar_graph
