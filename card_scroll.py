import dash_bootstrap_components as dbc
from dash import Dash, html
from pandas.util.testing import makeDataFrame

df = makeDataFrame()

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    dbc.Card(
        html.Div(
            dbc.Table.from_dataframe(df),
            style={"maxHeight": "200px", "overflow": "scroll"},
        ),
        body=True,
    ),
    className="p-5",
)

if __name__ == "__main__":
    app.run_server(debug=True)