from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from numpy.lib.function_base import _diff_dispatcher
# from app import URL, app
# from app import app
import pandas as pd
# from datatable import dt, f, sort
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
from app import URL
# from index import DISPLAY_HISTORY
# PLOTLY_LOGO = 'assets/favicon.png'

# DISPLAY_OFFLINE = ''
DISPLAY_HISTORY = ''
search_bar = dbc.Row(
    [
        # dbc.Col(dbc.Input(type="search", placeholder="Search")),
        # dbc.Col(dbc.NavLink(
        #     html.A('Home', href=URL + '/index', target='', style={
        #            'text-decoration': 'none', 'color': 'white'}),
        #     active=True,
        #     className='testHover', style={'text-decoration': 'none', 'color': 'white', 'font-size': '1.5rem'})),
        dbc.Col(dbc.NavLink(
            html.A('Pagina Accettazione', href=URL + '/apps/pagina_accettazione', target='', style={
                   'text-decoration': 'none', 'color': 'white'}),
            active=True,
            className='testHover', style={'text-decoration': 'none', 'color': 'white', 'font-size': '1.5rem'})),
        dbc.Col(dbc.NavLink(
            html.A('Pagina Referti', href=URL + '/apps/pagina_referti', target='', style={
                   'text-decoration': 'none', 'color': 'white'}),
            active=True,
            className='testHover', style={'text-decoration': 'none', 'color': 'white', 'font-size': '1.5rem'})),
        # dbc.Col(dbc.NavLink(
        #     html.A('PERSONAL_DATA_MANAGEMENT', href=URL + '/genome-dictionary-management', target='',
        #            style={'text-decoration': 'none', 'color': 'white'}),
        #     active=True,
        #     className='testHover', style={'text-decoration': 'none', 'color': 'white', 'font-size': '1.5rem', 'display': DISPLAY_OFFLINE})),
        # dbc.Col(dbc.NavLink(
        #     html.A('MANUAL', href=URL + '/user-guide', target='',
        #            style={'text-decoration': 'none', 'color': 'white'}),
        #     active=True,
        #     className='testHover', style={'text-decoration': 'none', 'color': 'white', 'font-size': '1.5rem'})),
        # dbc.Col(dbc.NavLink(
        #     html.A('CONTACTS', href=URL + '/contacts', target='',
        #            style={'text-decoration': 'none', 'color': 'white'}),
        #     active=True,
        #     className='testHover', style={'text-decoration': 'none', 'color': 'white', 'font-size': '1.5rem'})),
        # dbc.Col(dbc.NavLink(
        #     html.A('HISTORY', href=URL + '/history', target='',
        #            style={'text-decoration': 'none', 'color': 'white'}),
        #     active=True,
        #     className='testHover', style={'text-decoration': 'none', 'color': 'white', 'font-size': '1.5rem', 'display': 'none'}))
    ],
    # no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = html.Div(dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                  [
                      # dbc.Col(html.Img(src=PLOTLY_LOGO, height="60px")),
                      dbc.Col(dbc.NavbarBrand(
                          "Gestione Accettazione e Referti Sezione Igiene", className="ml-2", style={'font-size': '20px'}))
                  ],
                  align="center",
                  # no_gutters=True,
                  ),
            href=URL + '/index',
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
    ],
    color="dark",
    dark=True,
)
)
