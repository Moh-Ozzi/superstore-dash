import dash, base64
from dash import html, dcc

dash.register_page(__name__, path="/")



layout = html.Div(
    [
        html.H1('Dash Plotly Superstore', className="text-center mt-3 fw-bolder", style={'color':'#1F618D'}),
        html.Img(src='assets/plotly_logo.png',style={'height':'50%', 'width':'50%'}, className="img-fluid mx-auto d-block img-responsive my-5")
        # dcc.Link("Go to Page 1", href="/page-1"),
        # html.Br(),
        # dcc.Link("Go to Page 2", href="/page-2"),
    ]
)