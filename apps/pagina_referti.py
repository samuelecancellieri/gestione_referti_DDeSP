from optparse import check_choice
import sqlite3
from time import sleep
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
# from app import URL, app
from app import app
import pandas as pd
# from datatable import dt, f, sort
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash import dash_table
from documenti import elimina_documento,converti_pdf_to_pdfA
from db_manager import database, create_connection, insert_identificazione, insert_referto, get_id_last_row, delete_record_identificazione
from stampa_pdf import stampa_referto, stampa_referto_identificazione


def update_table_referti_identificazione(codice_accettazione):
    # ritorna tabella contenente i link ai file in documenti_accettazione
    # conn = sqlite3.connect(database)
    conn = create_connection(database)
    c = conn.cursor()
    tabella_referti = pd.read_sql_query(
        "SELECT * FROM referti_identificazione WHERE \"{}\"=\'{}\'".format('id_accettazione', codice_accettazione), conn)
    tabella_referti['index'] = tabella_referti['rapporto_di_prova_identificazione'].apply(
        lambda x: str(x).split('_')[0])
    tabella_referti['index'] = tabella_referti['index'].astype(int)
    tabella_referti.sort_values(
        'index', ascending=True, inplace=True)
    tabella_referti.drop(['index'], inplace=True, axis=1)
    conn.commit()
    conn.close()
    try:
        table = dash_table.DataTable(
            id='table_referti_identificazione',
            columns=[{"name": i, "id": i, 'hideable': False}
                     for i in tabella_referti.columns],
            data=tabella_referti.to_dict('records'),
            export_format="xlsx",
            style_data={
                'whiteSpace': 'pre-line',
                'height': 'auto',
                'lineHeight': '15px'
            },
            style_cell={
                "height": "auto",
                "textAlign": "left",
            },
            style_table={
                "overflowX": "scroll",
                "overflowY": "scroll",
                "max-height": "300px",
            },
            css=[{'selector': '.row',
                  'rule': 'margin: 0'}, {'selector': 'td.cell--selected, td.focused', 'rule': 'background-color: rgba(0, 0, 255,0.15) !important;'}, {
                'selector': 'td.cell--selected *, td.focused *', 'rule': 'background-color: rgba(0, 0, 255,0.15) !important;'}],
        )
    except:
        # se niente da mettere in tabella, fai tabella vuota
        table = dash_table.DataTable(id='table_referti_identificazione')

    return table


def update_table_referti(codice_accettazione):
    # ritorna tabella contenente i link ai file in documenti_accettazione
    # conn = sqlite3.connect(database)
    conn = create_connection(database)
    c = conn.cursor()
    tabella_referti = pd.read_sql_query(
        "SELECT * FROM referti WHERE \"{}\"=\'{}\'".format('id_accettazione', codice_accettazione), conn)
    tabella_referti['index'] = tabella_referti['rapporto_di_prova'].apply(
        lambda x: str(x).split('_')[0])
    tabella_referti['index'] = tabella_referti['index'].astype(int)
    tabella_referti.sort_values(
        'index', ascending=True, inplace=True)
    tabella_referti.drop(['index'], inplace=True, axis=1)
    conn.commit()
    conn.close()
    try:
        table = dash_table.DataTable(
            id='table_referti',
            columns=[{"name": i, "id": i, 'hideable': False}
                     for i in tabella_referti.columns],
            data=tabella_referti.to_dict('records'),
            export_format="xlsx",
            style_data={
                'whiteSpace': 'pre-line',
                'height': 'auto',
                'lineHeight': '15px'
            },
            style_cell={
                "height": "auto",
                "textAlign": "left",
            },
            style_table={
                "overflowX": "scroll",
                "overflowY": "scroll",
                "max-height": "300px",
            },
            css=[{'selector': '.row',
                  'rule': 'margin: 0'}, {'selector': 'td.cell--selected, td.focused', 'rule': 'background-color: rgba(0, 0, 255,0.15) !important;'}, {
                'selector': 'td.cell--selected *, td.focused *', 'rule': 'background-color: rgba(0, 0, 255,0.15) !important;'}],
        )
    except:
        # se niente da mettere in tabella, fai tabella vuota
        table = dash_table.DataTable(id='table_referti')

    return table


def update_table_accettazione():
    # ritorna tabella contenente i link ai file in documenti_accettazione
    # conn = sqlite3.connect(database)
    conn = create_connection(database)
    c = conn.cursor()
    tabella_accettazione = pd.read_sql_query(
        "SELECT * FROM accettazioni", conn)
    tabella_accettazione['index'] = tabella_accettazione['id'].apply(
        lambda x: str(x).split('_')[0])
    tabella_accettazione['index'] = tabella_accettazione['index'].astype(int)
    tabella_accettazione.sort_values(
        'index', ascending=True, inplace=True)
    tabella_accettazione.drop(['index'], inplace=True, axis=1)
    conn.commit()
    conn.close()
    try:
        table = dash_table.DataTable(
            id='table_accettazione_in_referti',
            columns=[{"name": i, "id": i, 'hideable': False}
                     for i in tabella_accettazione.columns],
            data=tabella_accettazione.to_dict('records'),
            export_format="xlsx",
            style_data={
                'whiteSpace': 'pre-line',
                'height': 'auto',
                'lineHeight': '15px'
            },
            style_cell={
                "height": "auto",
                "textAlign": "left",
            },
            style_table={
                "overflowX": "scroll",
                "overflowY": "scroll",
                "max-height": "300px",
            },
            css=[{'selector': '.row',
                  'rule': 'margin: 0'}, {'selector': 'td.cell--selected, td.focused', 'rule': 'background-color: rgba(0, 0, 255,0.15) !important;'}, {
                'selector': 'td.cell--selected *, td.focused *', 'rule': 'background-color: rgba(0, 0, 255,0.15) !important;'}],
        )
    except:
        # se niente da mettere in tabella, fai tabella vuota
        table = dash_table.DataTable(id='table_accettazione_in_referti')

    return table


def return_layout():
    # ritorna il layout per la pagina accettazione
    layout = html.Div(
        [
            dcc.Location(id='refresh_url_referti', refresh=True),
            dbc.Row(
                dbc.Col(
                    html.Div(
                        html.H3('Pagina Referti')
                    )
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.Div(
                        html.H4('Tabella Accettazioni')
                    )
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.Div(
                        update_table_accettazione(),
                        id='div_table_accettazione_in_referti'
                    )
                )
            ),
            html.Br(),
            dbc.Row(
                dbc.Col(
                    html.Div(
                        html.H4('Tabella Referti')
                    )
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.Div(
                        id='div_table_referti'
                    )
                )
            ),
            html.Br(),
            dbc.Row(
                dbc.Col(
                    html.Div(
                        html.H4('Tabella Referti Identificazione')
                    )
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.Div(
                        id='div_table_referti_identificazione'
                    )
                )
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.P('ID Accettazione'),
                                dcc.Textarea(id='text_id_accettazione_referti', disabled=True, placeholder='1_2021', style={
                                    'width': '300px', 'height': '30px'}),
                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('Rapporto di Prova'),
                                dcc.Textarea(id='text_rapporto_di_prova_referti', disabled=True, placeholder='2_2021', style={
                                    'width': '300px', 'height': '30px'}),

                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('Unità Operativa'),
                                dcc.Textarea(id='text_unita_operativa_referti', disabled=True, placeholder='B. CELL/TESS', style={
                                    'width': '300px', 'height': '30px'})
                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('Data Prelievo'),
                                dcc.Textarea(id='text_data_prelievo_referti', disabled=True, placeholder='13/10/2021', style={
                                    'width': '300px', 'height': '30px'}),
                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('Data Accettazione'),
                                dcc.Textarea(id='text_data_accettazione_referti', disabled=True, placeholder='13/10/2021', style={
                                    'width': '300px', 'height': '30px'}),

                            ]
                        )
                    ),

                    dbc.Col(
                        html.Div(
                            [
                                html.P('ID Campione Analizzato'),
                                dcc.Textarea(id='text_id_campione_referti', disabled=True, placeholder='id123', style={
                                    'width': '300px', 'height': '30px'}),
                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('Descrizione Campione'),
                                dcc.Textarea(id='text_descrizione_campione_referti', disabled=True, placeholder='prelievo_cappa', style={
                                    'width': '300px', 'height': '30px'}),
                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('Operatore Prelievo Campione'),
                                dcc.Textarea(id='text_operatore_prelievo_campione_referti', disabled=True, placeholder='Mario Rossi', style={
                                    'width': '300px', 'height': '30px'})
                            ]
                        )
                    ),
                    dbc.Col(html.Div())
                ]
            ),
            dbc.Row(
                [
                dbc.Col(html.Div()),
                dbc.Col(
                    html.Div(
                        html.H4('CAMPI DA COMPILARE OBBLIGATORIAMENTE')
                    )
                ),
                dbc.Col(html.Div())
                ]
            ),
            dbc.Row(
                dbc.Col(
                    html.Div(
                        html.H5('INSERIRE DATI GENERALI ANALISI')
                    )
                )
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.P('Inserire Operatore Analisi'),
                                dcc.Textarea(id='text_operatore_analisi_referti', placeholder='Silvia Sembeni', style={
                                    'width': '300px', 'height': '30px'})
                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('Inserire data inizio Analisi'),
                                dcc.Textarea(id='text_data_inizio_analisi_referti', placeholder='10/12/2021', style={
                                    'width': '300px', 'height': '30px'})
                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('Inserire data fine Analisi'),
                                dcc.Textarea(id='text_data_fine_analisi_referti', placeholder='11/12/2021', style={
                                    'width': '300px', 'height': '30px'})
                            ]
                        )
                    )
                ]
            ),
            dbc.Row(
                dbc.Col(
                    html.Div(
                        html.H5('INSERIRE RISULTATI ANALISI')
                    )
                )
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.P('UFC Batteri'),
                                dcc.Textarea(id='text_risultati_UFC_batteri', value='n.r.', style={
                                    'width': '300px', 'height': '30px'})
                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('UFC Miceti'),
                                dcc.Textarea(id='text_risultati_UFC_miceti', value='n.r.', style={
                                    'width': '300px', 'height': '30px'}),
                            ],style={'display':'none'},id='div_miceti'
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('Note'),
                                dcc.Textarea(id='text_risultati_note', value='Nessuna nota', style={
                                    'width': '300px', 'height': '30px'})
                            ]
                        )
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.P('Esame microscopico (colorazione di Kinyoun)'),
                                dcc.Textarea(id='text_colorazione', value='NEGATIVO', style={
                                    'width': '300px', 'height': '30px'}),
                            ],style={'display':'none'},id='div_colorazione'
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('Coltura su terreno liquido/solido'),
                                dcc.Textarea(id='text_coltura', value='NEGATIVO/NEGATIVO', style={
                                    'width': '300px', 'height': '30px'}),
                            ],style={'display':'none'},id='div_coltura'
                        )
                    ),
                    dbc.Col()
                ]
            ),
            dbc.Row(
                dbc.Col(
                    html.Div(
                        html.H5('INSERIRE RISULTATI IDENTIFICAZIONE [NON OBBLIGATORI]')
                    )
                )
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.P('Identificazione'),
                                dcc.Textarea(id='text_risultati_identificazione', value='n.r.', style={
                                    'width': '300px', 'height': '30px'})
                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('Note'),
                                dcc.Textarea(id='text_risultati_note_identificazione', value='n.r.', style={
                                    'width': '300px', 'height': '30px'})
                            ]
                        )
                    ),
                    dbc.Col(html.Div())
                ]
            ),
            dbc.Row(
                html.Div(
                    [
                        html.Br(),
                        html.Button(
                            'AGGIORNA REFERTO', id='aggiorna_referto_button'),
                        html.Button('SCARICA REFERTO',
                                    id='download_referti_button'),
                        html.Button('ELIMINA IDENTIFICAZIONE',
                                    id='elimina_identificazione_button'),
                        html.Div(id='alert_submission_referti'),
                        html.Div(id='alert_eliminazione_identificazione'),
                        dcc.Download(id="download_referto"),
                        dcc.Download(id="download_referto_identificazione")
                    ]
                )
            )
        ], style={'margin-left': '2%', 'margin-top': '2%'}
    )

    return layout


@ app.callback(
    Output('alert_eliminazione_identificazione', 'children'),
    Input('elimina_identificazione_button', 'n_clicks'),
    [State('table_referti_identificazione', 'active_cell'),
     State('table_referti_identificazione', 'derived_virtual_data')]
)
def elimina_identificazione(elimina_button_click, cella_selezionata_identificazione, tabella_identificazione):
    if cella_selezionata_identificazione is None:
        raise PreventUpdate

    id_accettazione = tabella_identificazione[cella_selezionata_identificazione['row']
                                              ]['id_accettazione']
    id_campione = tabella_identificazione[cella_selezionata_identificazione['row']]['id_campione']

    status = delete_record_identificazione(id_accettazione, id_campione)

    alert_eliminazione = dbc.Alert("Modulo di identificazione eliminato correttamente",
                                   is_open=True, duration=5000, color='success')

    if status:
        nome_documento = tabella_identificazione[cella_selezionata_identificazione['row']
                                                 ]['documento_identificazione']
        check_eliminazione = elimina_documento(
            'documenti_referti/'+nome_documento)
        if check_eliminazione:
            return alert_eliminazione


@ app.callback(
    [Output('div_table_referti', 'children'),
     Output('div_table_referti_identificazione', 'children'),
     Output('div_colorazione', 'style'),
     Output('div_coltura', 'style'),
     Output('div_miceti', 'style')],
    [Input('aggiorna_referto_button', 'n_clicks'),
     Input('elimina_identificazione_button', 'n_clicks'),
     Input('table_accettazione_in_referti', 'active_cell'),
     Input('table_accettazione_in_referti', 'derived_virtual_data')]
)
def display_referti_by_accettazione(aggiorna_referto_click, elimina_identificazione_click, cella_selezionata_accettazione, table_virtual_data):
    # ritorna tabella referti aggiornata con referti di doc_accettazione
    if cella_selezionata_accettazione is None:
        raise PreventUpdate

    # ritorna codice modulo accettazione per aprire referti correlati
    codice_modulo_accettazione = table_virtual_data[cella_selezionata_accettazione['row']
                                                    ]['id']
    modulo_referto=table_virtual_data[cella_selezionata_accettazione['row']
                                                    ]['modulo_referto']
    
    # sleep(1)  # necessario per attendere update della tabella a db
    tabella_referti = update_table_referti(codice_modulo_accettazione)

    # sleep(1)  # necessario per attendere update della tabella a db
    tabella_referti_identificazione = update_table_referti_identificazione(
        codice_modulo_accettazione)

    out_list = list()
    out_list.append(tabella_referti)
    out_list.append(tabella_referti_identificazione)
    
    #check if referto richiede input più specifico (MR43/44)
    if modulo_referto=='MR43':
        out_list.append({'display':''})
        out_list.append({'display':''})
        out_list.append({'display':'none'})
    else:
        out_list.append({'display':'none'})
        out_list.append({'display':'none'})
        if modulo_referto=='MR44':
            out_list.append({'display':''})
        else:
            out_list.append({'display':'none'})

    return out_list


@ app.callback(
    Output("download_referto_identificazione", "data"),
    Input('download_referti_button', 'n_clicks'),
    [State('table_referti_identificazione', 'active_cell'),
     State('table_referti_identificazione', 'derived_virtual_data')]
)
def download_identificazione(download_click, cella_selezionata_identificazione, tabella_identificazione):
    if download_click is None or download_click == 0:
        raise PreventUpdate

    file_identificazione = ''
    if cella_selezionata_identificazione is not None and tabella_identificazione is not None:
        file_identificazione = str(tabella_identificazione[cella_selezionata_identificazione['row']
                                                           ]['documento_identificazione'])
        return dcc.send_file(
            'documenti_referti/'+file_identificazione)


@ app.callback(
    Output("download_referto", "data"),
    Input('download_referti_button', 'n_clicks'),
    [State('table_referti', 'active_cell'),
     State('table_referti', 'derived_virtual_data')]
)
def download_referto(download_click, cella_selezionata_referto, tabella_referti):
    if download_click is None or download_click == 0:
        raise PreventUpdate

    file_referto = ''
    if cella_selezionata_referto is not None and tabella_referti is not None:
        file_referto = str(tabella_referti[cella_selezionata_referto['row']
                                           ]['documento_referto'])
        return dcc.send_file(
            'documenti_referti/'+file_referto)


@ app.callback(
    [Output('text_unita_operativa_referti', 'value'),
     Output('text_id_accettazione_referti', 'value'),
     Output('text_data_prelievo_referti', 'value'),
     Output('text_data_accettazione_referti', 'value'),
     Output('text_rapporto_di_prova_referti', 'value'),
     Output('text_id_campione_referti', 'value'),
     Output('text_descrizione_campione_referti', 'value'),
     Output('text_operatore_prelievo_campione_referti', 'value'),
     Output('text_operatore_analisi_referti', 'value'),
     Output('text_data_inizio_analisi_referti', 'value'),
     Output('text_data_fine_analisi_referti', 'value'),
     Output('text_risultati_UFC_batteri', 'value'),
     Output('text_risultati_UFC_miceti', 'value'),
     Output('text_risultati_note', 'value'),
     Output('text_colorazione', 'value'),
     Output('text_coltura', 'value'),
     Output('text_risultati_identificazione', 'value'),
     Output('text_risultati_note_identificazione', 'value')],
    [Input('table_referti', 'active_cell'),
     Input('table_referti', 'derived_virtual_data'),
     Input('table_referti_identificazione', 'active_cell'),
     Input('table_referti_identificazione', 'derived_virtual_data')]
)
def apri_referto(cella_selezionata_referto, table_virtual_data,cella_selezionata_identificazione,table_identificazione):
    if cella_selezionata_referto is None:
        raise PreventUpdate

    print('entro nel apri referto')
    out_list = list()
    out_list.append(
        table_virtual_data[cella_selezionata_referto['row']]['unita_operativa'])
    out_list.append(
        table_virtual_data[cella_selezionata_referto['row']]['id_accettazione'])
    out_list.append(
        table_virtual_data[cella_selezionata_referto['row']]['data_prelievo'])
    out_list.append(
        table_virtual_data[cella_selezionata_referto['row']]['data_accettazione'])
    out_list.append(
        table_virtual_data[cella_selezionata_referto['row']]['rapporto_di_prova'])
    out_list.append(
        table_virtual_data[cella_selezionata_referto['row']]['id_campione'])
    out_list.append(
        table_virtual_data[cella_selezionata_referto['row']]['descrizione_campione'])
    out_list.append(
        table_virtual_data[cella_selezionata_referto['row']]['operatore_prelievo_campione'])
    out_list.append(
        table_virtual_data[cella_selezionata_referto['row']]['operatore_analisi'])
    out_list.append(
        table_virtual_data[cella_selezionata_referto['row']]['data_inizio_analisi'])
    out_list.append(
        table_virtual_data[cella_selezionata_referto['row']]['data_fine_analisi'])
    out_list.append(
        table_virtual_data[cella_selezionata_referto['row']]['UFC_batteri'])
    out_list.append(
        table_virtual_data[cella_selezionata_referto['row']]['UFC_miceti'])
    out_list.append(
        table_virtual_data[cella_selezionata_referto['row']]['note'])
    out_list.append(
        table_virtual_data[cella_selezionata_referto['row']]['esame_microscopico'])
    out_list.append(
        table_virtual_data[cella_selezionata_referto['row']]['coltura_su_terreno'])
    
    if cella_selezionata_identificazione:
        out_list.append(table_identificazione[cella_selezionata_identificazione['row']]['identificazione'])
        out_list.append(table_identificazione[cella_selezionata_identificazione['row']]['note'])
    else:
        out_list.append('n.r.')
        out_list.append('n.r.')

    return out_list


@ app.callback(
    [Output('alert_submission_referti', 'children')],
    [Input('aggiorna_referto_button', 'n_clicks')],
    [State('text_unita_operativa_referti', 'value'),
     State('text_id_accettazione_referti', 'value'),
     State('text_data_prelievo_referti', 'value'),
     State('text_data_accettazione_referti', 'value'),
     State('text_rapporto_di_prova_referti', 'value'),
     State('text_id_campione_referti', 'value'),
     State('text_descrizione_campione_referti', 'value'),
     State('text_operatore_prelievo_campione_referti', 'value'),
     State('text_operatore_analisi_referti', 'value'),
     State('text_data_inizio_analisi_referti', 'value'),
     State('text_data_fine_analisi_referti', 'value'),
     State('text_risultati_UFC_batteri', 'value'),
     State('text_risultati_UFC_miceti', 'value'),
     State('text_risultati_note', 'value'),
     State('text_colorazione', 'value'),
     State('text_coltura', 'value'),
     State('text_risultati_identificazione', 'value'),
     State('text_risultati_note_identificazione', 'value')]
)
def modifica_e_scrittura_referto(aggiorna_referto_click, text_unita_operativa_referti,
                                 text_id_accettazione_referti, text_data_prelievo_referti,
                                 text_data_accettazione_referti, text_rapporto_di_prova_referti, text_id_campione_referti,
                                 text_descrizione_campione_referti, text_operatore_prelievo_campione_referti, text_operatore_analisi_referti,
                                 text_data_inizio_analisi_referti, text_data_fine_analisi_referti,
                                 text_risultati_UFC_batteri, text_risultati_UFC_miceti, text_risultati_note,text_colorazione,text_coltura,
                                 text_risultati_identificazione, text_risultati_note_identificazione):
    if None in locals().values():
        # print('sto bloccando update',locals().values())
        raise PreventUpdate

    # crea query di inserimento a db
    referto_to_db = (text_rapporto_di_prova_referti, text_id_accettazione_referti, text_id_campione_referti, text_unita_operativa_referti, text_data_prelievo_referti, text_data_accettazione_referti, text_descrizione_campione_referti, text_operatore_prelievo_campione_referti,
                     text_operatore_analisi_referti, text_data_inizio_analisi_referti, text_data_fine_analisi_referti, text_risultati_UFC_batteri, text_risultati_UFC_miceti, text_risultati_note, text_colorazione, text_coltura, 'referto_'+str(text_id_accettazione_referti).upper()+'_'+str(text_id_campione_referti).upper()+'.pdf')
    # inserisci a db
    insert_referto(referto_to_db)

    # crea pdf
    stampa_referto(text_id_accettazione_referti, text_id_campione_referti, text_unita_operativa_referti,
                   text_data_prelievo_referti, text_data_accettazione_referti, text_rapporto_di_prova_referti,
                   text_descrizione_campione_referti,
                   text_operatore_prelievo_campione_referti,
                   text_operatore_analisi_referti, text_data_inizio_analisi_referti,
                   text_data_fine_analisi_referti, text_risultati_UFC_batteri,
                   text_risultati_UFC_miceti, text_risultati_note)
    # converti_pdf_to_pdfA('documenti_referti/referto_'+str(text_id_accettazione_referti).upper()+'_'+str(text_id_campione_referti).upper()+'.pdf')

    if text_risultati_identificazione != 'n.r.':
        new_id_referto_identificazione = str(get_id_last_row('referti_identificazione')+1) + \
            '_' + text_data_accettazione_referti.strip().split('/')[-1]
        referto_identificazione_to_db = (new_id_referto_identificazione, text_id_accettazione_referti, text_id_campione_referti, text_unita_operativa_referti, text_data_prelievo_referti, text_data_accettazione_referti, text_descrizione_campione_referti,
                                         text_operatore_prelievo_campione_referti, text_operatore_analisi_referti, text_data_inizio_analisi_referti, text_data_fine_analisi_referti, text_risultati_identificazione, text_risultati_note_identificazione, 'referto_identificazione_'+str(text_id_accettazione_referti).upper()+'_'+str(text_id_campione_referti).upper()+'.pdf')
        insert_identificazione(referto_identificazione_to_db)
        stampa_referto_identificazione(text_id_accettazione_referti, text_id_campione_referti, text_unita_operativa_referti,
                                       text_data_prelievo_referti, text_data_accettazione_referti, new_id_referto_identificazione,
                                       text_descrizione_campione_referti, text_operatore_prelievo_campione_referti,
                                       text_operatore_analisi_referti, text_data_inizio_analisi_referti, text_data_fine_analisi_referti,
                                       text_risultati_identificazione, text_risultati_note_identificazione)
        # converti_pdf_to_pdfA('documenti_referti/referto_identificazione_'+str(text_id_accettazione_referti).upper()+'_'+str(text_id_campione_referti).upper()+'.pdf')


    out_list = list()
    alert_submit = dbc.Alert("Modulo di referto aggiornato correttamente",
                             is_open=True, duration=5000, color='success')
    out_list.append(alert_submit)

    return out_list
