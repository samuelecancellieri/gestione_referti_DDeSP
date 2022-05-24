from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from numpy.lib.function_base import _diff_dispatcher
# from app import URL, app
# from app import app
import pandas as pd
# from datatable import dt, f, sort
from dash import html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table

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
