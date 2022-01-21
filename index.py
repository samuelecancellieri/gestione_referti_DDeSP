# from dash import dcc, html, Input, Output

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

from app import app
from db_manager import generate_tables
from apps import main_page, navbar_page, pagina_accettazione, pagina_referti

# navbar = navbar_page.navbar
app.layout = html.Div(
    [
        navbar_page.navbar,
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content'),
        html.P(id='signal', style={'visibility': 'hidden'})
    ]
)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/pagina_accettazione':
        return pagina_accettazione.return_layout()
    elif pathname == '/apps/pagina_referti':
        return pagina_referti.return_layout()
    else:
        return main_page.layout


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True,
                   dev_tools_ui=True, dev_tools_props_check=True)
    # regenerate tables if not existent in db
    generate_tables()
