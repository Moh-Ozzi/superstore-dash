import dash, base64
from dash import html, dcc

dash.register_page(__name__, path="/")



layout = html.Div(
    [
        html.H1('MEDAD SOFT', className="text-center mt-3 fw-bolder", style={'color':'#2471a1'}),
        html.Img(src='assets/midad.png',style={'height':'500px', 'width':'60%'}, className="img-fluid mx-auto d-block img-responsive my-5")
        # dcc.Link("Go to Page 1", href="/page-1"),
        # html.Br(),
        # dcc.Link("Go to Page 2", href="/page-2"),
    ]
)