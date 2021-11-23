from app import app
import os
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, dash_table
from dash.exceptions import PreventUpdate
# import dash_table
import pandas as pd


def lista_documenti_accettazione():
    return os.listdir('documenti_accettazione/')


def return_dizionario_accettazione():
    df = pd.DataFrame(lista_documenti_accettazione())
    df.set_axis(['Numero_accettazione'], axis=1, inplace=True)
    # df['Codice_accettazione'] = 0
    # print(df)
    # for index, row in df.iterrows():
    #     row['Codice_accettazione'] = str(row['Numero_accettazione']).split('_')[
    #         1].replace('.txt', '')

    # df = df[['Codice_accettazione', 'Numero_accettazione']]
    return df


def update_tabella_accettazione():
    return dash_table.DataTable(
        # TABLE that represent the files in documenti_accettazione/
        id='tabella_accettazione',
        # columns=[nome, cognome],
        columns=[{"name": i, "id": i}
                 for i in return_dizionario_accettazione().columns],
        data=return_dizionario_accettazione().to_dict('records'),
        virtualization=True,
        fixed_rows={'headers': True, 'data': 0},
        style_cell={'textAlign': 'left'},
        # fixed_columns = {'headers': True, 'data':1},
        # style_cell={'width': '150px'},
        # page_current=0,
        # page_action='custom',
        # sort_action='custom',
        # sort_mode='multi',
        # sort_by=[],
        # filter_action='custom',
        # filter_query='',
        style_table={
            'max-height': '200px'},
        css=[{'selector': '.row',
              'rule': 'margin: 0'}, {'selector': 'td.cell--selected, td.focused', 'rule': 'background-color: rgba(0, 0, 255,0.15) !important;'}, {
            'selector': 'td.cell--selected *, td.focused *', 'rule': 'background-color: rgba(0, 0, 255,0.15) !important;'}],
    )


layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                html.Div(
                    html.H3('Pagina Accettazione')
                )
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.P('Inserire nome'),
                            dcc.Textarea(id='nome_accettazione', placeholder='Mario Rossi', style={
                                'width': '300px', 'height': '30px'}),
                        ]
                    )
                ),
                dbc.Col(
                    html.Div(
                        update_tabella_accettazione(),
                        id='div_tabella_accettazione'
                    )
                )
            ]
        ),
        dbc.Row(
            html.Div(
                [
                    html.Button('Submit', id='submit_accettazione'),
                    html.Div(id='submission_alert')
                ]
            )
        ),
        dbc.Row(
            html.Div(
                [
                    # dbc.Button("Open", id="open-centered"),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle(
                                "Documento Accettazione"), close_button=True),
                            dbc.ModalBody(
                                html.Div(
                                    id='modal_div'
                                )
                            ),
                            # dbc.ModalFooter(
                            #     dbc.Button(
                            #         "Close",
                            #         id="close-centered",
                            #         className="ms-auto",
                            #         n_clicks=0,
                            #     )
                            # ),
                        ],
                        id="modal_centered",
                        centered=True,
                        is_open=False,
                    ),
                ]
            )
        )
    ], style={'margin': '1%'}
)


@app.callback(
    [Output('modal_centered', 'is_open'),
     Output('modal_div', 'children')],
    Input('tabella_accettazione', 'active_cell')
)
def apri_file_accettazione(cella_selezionata):
    # print(cella_selezionata)
    if cella_selezionata is None:
        raise PreventUpdate
    df_accettazione = return_dizionario_accettazione()
    row = cella_selezionata['row']
    col = cella_selezionata['column']
    documento_accettazione = open('documenti_accettazione/' +
                                  str(df_accettazione.iloc[row, col]), 'r').read()
    # print(file)
    # documento_accettazione = str()
    # for line in file:
    #     documento_accettazione += line
    # print(documento_accettazione)

    out_list = list()
    out_list.append(True)
    out_list.append(documento_accettazione)

    return out_list


@ app.callback(
    [Output('submission_alert', 'children'),
     Output('div_tabella_accettazione', 'children')],
    Input('submit_accettazione', 'n_clicks'),
    State('nome_accettazione', 'value')
)
def crea_nuova_accettazione(submit_click, nome_accettazione):
    if submit_click is None or nome_accettazione is None:
        raise PreventUpdate
    print('entro in new_accettazione')
    try:
        prevo_code = int(lista_documenti_accettazione()
                         [-1].split('_')[1].replace('.txt', ''))
    except:
        prevo_code = 100
    current_code = str(prevo_code+1)
    file = open('documenti_accettazione/accettazione_' +
                current_code+'.txt', 'w')
    file.write('codice:'+current_code+'\n')
    file.write('nome:'+str(nome_accettazione))
    file.close()
    # output list
    out_list = list()
    alert = dbc.Alert("Modulo di accettazione inserito correttamente",
                      is_open=True, duration=5000, color='success')
    tabella_accettazione = update_tabella_accettazione()
    out_list.append(alert)
    out_list.append(tabella_accettazione)

    return out_list
