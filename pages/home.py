import dash, base64
from dash import html, dcc

dash.register_page(__name__, path="/")



layout = html.Div(
    [
        html.H1('DASH SUPERSTORE', className="text-center mt-3 fw-bolder", style={'color':'#2471a1'}),
        html.Img(src='assets/plotly_logo.png',style={'height':'500px', 'width':'60%'}, className="img-fluid mx-auto d-block img-responsive my-5")
    ]
)