from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import os

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
                # html.P('Inserire codice accettazione'),
                # dcc.Textarea(id='codice_accettazione', placeholder='1234ABC', style={
                #     'width': '300px', 'height': '30px'}),
                html.P('Inserire nome'),
                dcc.Textarea(id='nome_accettazione', placeholder='Mario Rossi', style={
                    'width': '300px', 'height': '30px'}),
            ]
        ),
        dbc.Row(
            [
                # html.Button('Submit', id='check_job',
                #             style={'background-color': '#E6E6E6'}),
                html.Button('Submit', id='submit_accettazione')
            ]
        ),
        dbc.Row(html.Div(id='submission_alert'))
    ], style={'margin': '1%'}
)


def last_code_accettazione():
    # print(os.listdir('documenti_accettazione/'))
    return os.listdir('documenti_accettazione/')[-1].split('_')[1].replace('.txt', '')


@app.callback(
    Output('submission_alert', 'children'),
    [Input('submit_accettazione', 'n_clicks')],
    [State('nome_accettazione', 'value')]
)
def new_accettazione(submit_click, nome_accettazione):
    if submit_click is None or nome_accettazione is None:
        raise PreventUpdate
    print('entro in new_accettazione')
    try:
        prevo_code = int(last_code_accettazione())
    except:
        prevo_code = 100
    current_code = str(prevo_code+1)
    file = open('documenti_accettazione/accettazione_' +
                current_code+'.txt', 'w')
    file.write('codice:'+current_code+'\n')
    file.write('nome:'+str(nome_accettazione))
    file.close()
    return dbc.Alert("Modulo di accettazione inserito correttamente", is_open=True, duration=5000, color='warning')
