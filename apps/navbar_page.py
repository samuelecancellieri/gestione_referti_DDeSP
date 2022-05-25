#dash import
from dash import html
import dash_bootstrap_components as dbc
from app import URL

search_bar = dbc.Row(
    [
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
        dbc.Col(dbc.NavLink(
            html.A('Pagina Consuntivo', href=URL + '/apps/pagina_consuntivo', target='', style={
                   'text-decoration': 'none', 'color': 'white'}),
            active=True,
            className='testHover', style={'text-decoration': 'none', 'color': 'white', 'font-size': '1.5rem'})),
    ],
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = html.Div(dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                  [
                      dbc.Col(dbc.NavbarBrand(
                          "Gestione Accettazione e Referti Sezione Igiene", className="ml-2", style={'margin-left': '1%', 'font-size': '20px'}))
                  ],
                  align="center",
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
