from dash import dcc, html, Input, Output
from app import app

layout = html.Div(
    [
        html.H3('Pagina Referti'),
    ], style={'margin': '1%'}
)


# @app.callback(
#     Output('app-1-display-value', 'children'),
#     Input('app-1-dropdown', 'value'))
# def display_value(value):
#     return 'You have selected "{}"'.format(value)