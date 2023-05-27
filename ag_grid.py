import dash
import dash_html_components as html
import dash_ag_grid as dag

app = dash.Dash(__name__)

app.layout = html.Div([
    dag.AgGrid(
        id='my-grid',
        rowData=[
            {'name': 'Alice', 'age': 30},
            {'name': 'Bob', 'age': 25},
            {'name': 'Eve', 'age': 35}
        ],
        columnDefs=[
            {'headerName': 'Name', 'field': 'name'},
            {'headerName': 'Age', 'field': 'age'}
        ],
        defaultColDef={'sortable': True, 'filter': True}
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
