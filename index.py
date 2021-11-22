from dash import dcc, html, Input, Output

from app import app
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
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/pagina_accettazione':
        return pagina_accettazione.layout
    elif pathname == '/apps/pagina_referti':
        return pagina_referti.layout
    else:
        return main_page.layout


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True,
                   dev_tools_ui=True, dev_tools_props_check=True)
