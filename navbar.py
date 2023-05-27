import dash
from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

navbar = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Link 1", href="#")),
        dbc.NavItem(dbc.NavLink("Link 2", href="#")),
        dbc.NavItem(dbc.NavLink("Link 3", href="#")),
    ],
    vertical=True,
)

collapse = dbc.Collapse(navbar, id="navbar-collapse", is_open=True)

toggle_button = dbc.Button(
    id="navbar-toggle",
)

app.layout = html.Div(
    [
        toggle_button,
        collapse,
    ]
)

@app.callback(
    Output("navbar-collapse", "is_open"),
    Output("navbar-toggle", "className"),
    [Input("navbar-toggle", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_collapse(n_clicks, is_open):
    if n_clicks is None:
        return is_open, "bi bi-arrow-left"
    if n_clicks and n_clicks % 2 == 0:
        return not is_open, "bi bi-arrow-left"
    else:
        return not is_open, "bi bi-arrow-right"

if __name__ == "__main__":
    app.run_server(debug=True)
