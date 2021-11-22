from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc


from app import app

layout = html.Div(
    [
        dbc.Row(
            [
                html.H3('Pagina Accettazione')
            ]
        ),
        dbc.Row(
            [
                html.P('Inserire codice accettazione'),
                dcc.Textarea(id='codice_accettazione', placeholder='1234ABC', style={
                    'width': '300px', 'height': '30px'}),
                html.P('Inserire nome'),
                dcc.Textarea(id='nome_accettazione', placeholder='Mario Rossi', style={
                    'width': '300px', 'height': '30px'}),
            ]
        )
    ]
)
