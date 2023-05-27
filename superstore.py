from sqlalchemy import create_engine
import pandas as pd
import socket


server = socket.gethostname()
database = 'Super Store'
engine = create_engine('mssql+pyodbc://' + server + '/' + database + '?driver=SQL+Server')
query = 'SELECT * FROM orders'
main_df = pd.read_sql(query, engine)

# main_df = pd.read_csv('pages/superstore.csv')
main_df.columns = ['row_id', 'orders', 'order_date', 'ship_date', 'ship_mode', 'customer_id', 'customer_name',
                   'segment',
                   'country', 'city', 'state', 'postal_code', 'region', 'product_id', 'category', 'sub_category',
                   'prodcut_name',
                   'sales', 'quantity', 'discount', 'profit']
main_df['manufacturer'] = main_df['prodcut_name'].str.partition(' ')[0]
main_df['order_date'] = pd.to_datetime(main_df.order_date)
main_df['ship_date'] = pd.to_datetime(main_df.ship_date)
main_df['order_year'] = main_df.order_date.dt.year
main_df['order_day'] = main_df.order_date.dt.day_name()
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
               'August', 'September', 'October', 'November', 'December']
main_df['order_month'] = pd.Categorical(main_df['order_date'].dt.month_name(), categories=month_order, ordered=True)
code = {'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
        'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
        'District of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI',
        'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
        'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME',
        'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
        'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE',
        'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
        'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
        'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI',
        'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX',
        'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
        'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'}
main_df['state_code'] = main_df['state'].map(code)

# df = main_df[main_df['order_year'] == 2016]
# print(df['sales'].sum())
#
# sales_2017 = sales_2017_total = main_df.loc[main_df['order_year'] == 2017, 'sales'].sum()
# print(sales_2017)


def compute_difference(df, measure, func):
    num = (df.loc[df['order_year'] == 2017, measure].agg(func) - \
                   df.loc[df['order_year'] == 2016, measure].agg(func)) / \
                   df.loc[df['order_year'] == 2016, measure].agg(func) * 100

    if num > 0:
        style = "bi bi-caret-up-fill text-success text-nowrap"
    else:
        style = "bi bi-caret-down-fill text-danger text-nowrap"
        num = human_format(abs(num))
    return num, style

value, style = compute_difference(main_df, 'customer_id', pd.Series.nunique)

print(compute_difference(main_df, 'customer_id', pd.Series.nunique))




#
# sales_difference = (main_df.loc[main_df['order_year'] == 2017, 'orders'].nunique() - \
#                    main_df.loc[main_df['order_year'] == 2016, 'orders'].nunique()) / \
#                    main_df.loc[main_df['order_year'] == 2016, 'orders'].nunique() * 100
#
#
# print(sales_difference)

