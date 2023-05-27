import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px


data = {"fruit": ["Apples", "Bananas", "Grapes"], "quantity": [5, 7, 3]}
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

fig = px.bar(data, x="fruit", y="quantity", title='This Title')
fig.update_layout(
    xaxis=dict(showticklabels=False, visible=False),
    yaxis=dict(showticklabels=False, visible=False),
    margin=dict(l=0, r=0, t=30, b=0),
)



card = dbc.Card(
    dbc.CardBody(
        [
            dcc.Graph(
                id="bar-chart",
                figure=fig,
            ),
        ],
        className='border border-1 border-danger'
    ),
)


app.layout = dbc.Container(
    [
        dbc.Row(dbc.Col(card, width=6)),
    ],
    fluid=True,
)


if __name__ == "__main__":
    app.run_server(debug=True)

