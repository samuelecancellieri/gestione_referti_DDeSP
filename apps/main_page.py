from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc


layout = html.Div(
    [
        html.H3('Main page'),
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
    ], style={'margin': '1%'}
)
