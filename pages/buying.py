import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = dbc.Container([
    html.Br(),

    html.Br(),
    html.Br(),
    html.Br(),

    # TRIAL ENDED MESSAGE (YOUR TRAIL HAS ENDED. IF YOU WANT TO BUY PLEASE PRESS THE BUTTON)

    # BUTTON TO PRESS

    # MESSAGE CONFIRMING THAT THE REQUEST HAS BEEN RECEIVED AND THAT THEY WILL BE CONTACTED WITH THE OTP



    # MESSAGE TELLING THEM TO ENTER THE OTP BELOW

    # INPUT FIELD FOR INTERING THE OTP

    # MESSAGE FOR SUCCESS OF STATUS UPDATE

    # REDIRECT TO LOGIN PAGE

    dbc.Row(dbc.Col(html.H3('الفترة التجريبية انتهت. لشراء رخصة البرنامج انقر على الزر في الأسفل', className='ms-6'))) ,
    dbc.Row(dbc.Col(html.Div(
        dbc.Button('موافق', id='buy_button', type='submit', n_clicks=0),
        className="mb-3 form-group className='ms-6'"
    ))) ,
    dbc.Row(dbc.Col(html.Div(id='buying_message', className='ms-6'))),
    html.Br(),
    html.Br(),
    dbc.Row(dbc.Col(dcc.Input(id='otp-input', debounce=True, className='ms-6')))
], className='ms-6', fluid=True
)
