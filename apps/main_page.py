#dash import
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

layout = html.Div(
    [
        html.H3('Seleziona la pagina dalla barra di navigazione'),
        dbc.Row(
            [
                dcc.Link('Apri pagina accettazione',
                         href='/apps/pagina_accettazione')
            ]
        ),
        dbc.Row(
            [
                dcc.Link('Apri pagina referti', href='/apps/pagina_referti')
            ]
        )
    ], style={'margin-left': '2%', 'margin-top': '2%'}
)
