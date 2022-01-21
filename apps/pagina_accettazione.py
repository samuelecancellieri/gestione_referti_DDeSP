import sqlite3
from app import app
import os
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
import pandas as pd
from documenti import documento_accettazione, documento_referto
from db_manager import insert_accettazione, insert_referto, database


# def lista_documenti_referti():
#     # ritorna la lista di documenti in cartella documenti_accettazione
#     lista_documenti_referti = os.listdir('documenti_referti/')
#     return lista_documenti_referti


# def lista_documenti_accettazione():
#     # ritorna la lista di documenti in cartella documenti_accettazione
#     lista_documenti_accettazione = os.listdir('documenti_accettazione/')

#     return lista_documenti_accettazione


# def update_database_referti():
#     database_referti = open('database/database_referti.txt', 'r')
#     header_referti = database_referti.readline()

#     database_referti = open('database/database_referti.txt', 'w')
#     database_referti.write(header_referti)
#     lista_referti = lista_documenti_referti()

#     for file_referto in lista_referti:
#         # print(file_accettazione)
#         nome_file = file_referto
#         documento_referto_letto = documento_referto()
#         file_referto = open(
#             'documenti_referti/'+file_referto, 'r')
#         documento_referto_letto.leggi_file(
#             file_da_leggere=file_referto)
#         stringa_da_salvare = ';'.join(
#             documento_referto_letto.__dict__.values()).upper()
#         stringa_da_salvare += ';'+nome_file
#         database_referti.write(
#             stringa_da_salvare+'\n')


# def update_database_accettazioni():
#     # aggiorna file contenente tutte le accettazioni
#     database_accettazioni = open('database/database_accettazioni.txt', 'r')
#     header_accettazioni = database_accettazioni.readline()

#     database_accettazioni = open('database/database_accettazioni.txt', 'w')
#     database_accettazioni.write(header_accettazioni)
#     lista_accettazioni = lista_documenti_accettazione()

#     for file_accettazione in lista_accettazioni:
#         # print(file_accettazione)
#         documento_accettazione_letto = documento_accettazione()
#         file_accettazione = open(
#             'documenti_accettazione/'+file_accettazione, 'r')
#         documento_accettazione_letto.leggi_file(
#             file_da_leggere=file_accettazione)
#         stringa_da_salvare = ';'.join(
#             documento_accettazione_letto.__dict__.values()).upper()
#         stringa_da_salvare += ';'+'accettazione_' + \
#             str(documento_accettazione_letto.n_modulo)+'.txt'
#         database_accettazioni.write(
#             stringa_da_salvare+'\n')


def return_dizionario_accettazione():
    database_accettazioni = 'database/database_accettazioni.txt'
    # ritorna il dizionario con i dati dei file in cartella documenti_accettazione
    df_accettazioni = pd.read_csv(database_accettazioni, sep=';')

    return df_accettazioni


def update_table_accettazione():
    # ritorna tabella contenente i link ai file in documenti_accettazione
    conn = sqlite3.connect(database)
    c = conn.cursor()
    tabella_accettazione = pd.read_sql_query(
        "SELECT * FROM accettazioni", conn)
    # rows = c.execute(tabella_accettazione)
    # header = [description[0] for description in rows.description]
    conn.commit()
    conn.close()

    try:
        table = dash_table.DataTable(
            id='table_accettazione',
            columns=[{"name": i, "id": i, 'hideable': False}
                     for i in tabella_accettazione.columns],
            data=tabella_accettazione.to_dict('records'),
            # virtualization=True,
            # fixed_rows={'headers': True, 'data': 0},
            # style_cell={'textAlign': 'left'},
            # style_table={
            #     'max-height': '400px'},
            css=[{'selector': '.row',
                  'rule': 'margin: 0'}, {'selector': 'td.cell--selected, td.focused', 'rule': 'background-color: rgba(0, 0, 255,0.15) !important;'}, {
                'selector': 'td.cell--selected *, td.focused *', 'rule': 'background-color: rgba(0, 0, 255,0.15) !important;'}],
        )
    except:
        # se niente da mettere in tabella, fai tabella vuota
        table = dash_table.DataTable(id='table_accettazione')

    return table


def return_layout():
    # ritorna il layout per la pagina accettazione
    layout = html.Div(
        [
            dcc.Location(id='refresh_url', refresh=True),
            dbc.Row(
                dbc.Col(
                    html.Div(
                        html.H3('Pagina Accettazione')
                    )
                )
            ),
            dbc.Row(
                html.Div(
                    html.H4('Tabella Accettazioni')
                )
            ),
            dbc.Row(
                html.Div(
                    update_table_accettazione(),
                    id='div_table_accettazione'
                )
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.P('Inserire unità operativa invio'),
                                dcc.Textarea(id='text_unita_operativa', placeholder='Neurologia', style={
                                    'width': '300px', 'height': '30px'})
                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('Inserire numero modulo'),
                                dcc.Textarea(id='text_numero_modulo', placeholder='ABC123', style={
                                    'width': '300px', 'height': '30px'}),
                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('Inserire data prelievo'),
                                dcc.Textarea(id='text_data_prelievo', placeholder='13/10/2021', style={
                                    'width': '300px', 'height': '30px'}),
                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('Inserire data_accettazione'),
                                dcc.Textarea(id='text_data_accettazione', placeholder='13/10/2021', style={
                                    'width': '300px', 'height': '30px'}),

                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('Inserire id campione, uno per riga'),
                                dcc.Textarea(id='text_id_campione', placeholder='id123', style={
                                    'width': '300px', 'height': '30px'}),
                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P(
                                    'Inserire descrizione campione, uno per riga'),
                                dcc.Textarea(id='text_descrizione_campione', placeholder='prelievo_cappa', style={
                                    'width': '300px', 'height': '30px'}),
                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P(
                                    'Inserire operatore_prelievo_campione, uno per riga'),
                                dcc.Textarea(id='text_operatore_prelievo_campione', placeholder='Mario Rossi', style={
                                    'width': '300px', 'height': '30px'})
                            ]
                        )
                    )
                ]
            ),
            dbc.Row(
                html.Div(
                    [
                        html.Button('Submit', id='submit_accettazione'),
                        html.Div(id='alert_submission')
                    ]
                )
            ),
            # dbc.Row(
            #     html.Div(
            #         [
            #             # dbc.Button("Open", id="open-centered"),
            #             dbc.Modal(
            #                 [
            #                     # dbc.ModalHeader(dbc.ModalTitle(
            #                     #     "Documento Accettazione"), close_button=True),
            #                     dbc.ModalBody(
            #                         html.Div(
            #                             id='div_modal', style={'white-space': 'pre'}
            #                         )
            #                     ),
            #                     dbc.ModalFooter(
            #                         dbc.Button(
            #                             "Modifica modulo accettazione", id="button_modifica_accettazione", className="ms-auto", n_clicks=0
            #                         )
            #                     )
            #                 ],
            #                 id="modal_accettazione",
            #                 centered=True,
            #                 is_open=False,
            #             ),
            #         ]
            #     )
            # )
        ], style={'margin-left': '2%', 'margin-top': '2%'}
    )

    return layout


@ app.callback(
    [Output('text_unita_operativa', 'value'),
     Output('text_numero_modulo', 'value'),
     Output('text_data_prelievo', 'value'),
     Output('text_data_accettazione', 'value'),
     Output('text_id_campione', 'value'),
     Output('text_descrizione_campione', 'value'),
     Output('text_operatore_prelievo_campione', 'value')],
    [Input('table_accettazione', 'active_cell'),
     Input('table_accettazione', 'derived_virtual_data')]
)
def modifica_accettazione(cella_selezionata_accettazione, table_virtual_data):
    if cella_selezionata_accettazione is None:
        raise PreventUpdate

    # ritorna documento accettazione da leggere
    documento_accettazione_path = table_virtual_data[cella_selezionata_accettazione['row']
                                                     ]['documento_accettazione']
    # file accettazione selezionato nella tabella
    accettazione_da_leggere = open(
        'documenti_accettazione/' + documento_accettazione_path, 'r')
    # crea doc accettazione vuoto e poi assegna membri dopo lettura
    documento_accettazione_letto = documento_accettazione()
    documento_accettazione_letto.leggi_file(
        file_da_leggere=accettazione_da_leggere)
    accettazione_da_leggere.close()

    # stringhe per popolare textarea pagina
    text_unita_operativa = str(documento_accettazione_letto.unita_operativa)
    text_numero_modulo = str(documento_accettazione_letto.n_modulo)
    text_data_prelievo = str(documento_accettazione_letto.data_prelievo)
    text_data_accettazione = str(
        documento_accettazione_letto.data_accettazione)
    text_id_campione = str(documento_accettazione_letto.id_campione)
    text_descrizione_campione = str(
        documento_accettazione_letto.descrizione_campione)
    text_operatore_prelievo_campione = str(
        documento_accettazione_letto.operatore_prelievo_campione)

    # output list
    out_list = list()
    # reset click_count button di modifica del file accettazione
    # out_list.append(0)
    out_list.append(text_unita_operativa)
    out_list.append(text_numero_modulo)
    out_list.append(text_data_prelievo)
    out_list.append(text_data_accettazione)
    out_list.append(text_id_campione.replace(',', '\n'))
    out_list.append(text_descrizione_campione.replace(',', '\n'))
    out_list.append(text_operatore_prelievo_campione.replace(',', '\n'))

    return out_list


@ app.callback(
    [Output('modal_accettazione', 'is_open'),
     Output('div_modal', 'children')],
    [Input('table_accettazione', 'active_cell'),
     Input('table_accettazione', 'derived_virtual_data')]
)
def apri_file_accettazione(cella_selezionata_accettazione, table_virtual_data):
    # apre modal con lettura file di accettazione selezionato in table_accettazione
    if cella_selezionata_accettazione is None:
        raise PreventUpdate

    # ritorna documento accettazione da leggere
    documento_accettazione_path = table_virtual_data[cella_selezionata_accettazione['row']
                                                     ]['documento_accettazione']
    # file accettazione selezionato nella tabella
    accettazione_da_leggere = open(
        'documenti_accettazione/' + documento_accettazione_path, 'r')
    # crea doc accettazione vuoto e poi assegna membri dopo lettura
    documento_accettazione_letto = documento_accettazione()
    documento_accettazione_letto.leggi_file(
        file_da_leggere=accettazione_da_leggere)
    accettazione_da_leggere.close()

    # stringa da inviare al div del modal per printare a schermo il doc accettazione selezionato
    documento_letto_da_modal = str()
    for key in documento_accettazione_letto.__dict__.keys():
        documento_letto_da_modal += str(key).upper() + ': ' + \
            str(documento_accettazione_letto.__dict__[key])+'\n'

    # out list
    out_list = list()
    out_list.append(True)
    out_list.append(documento_letto_da_modal)

    return out_list


@ app.callback(
    [Output("refresh_url", "href"),
     Output('alert_submission', 'children'),
     Output('div_table_accettazione', 'children')],
    [Input('submit_accettazione', 'n_clicks')],
    [State('text_unita_operativa', 'value'),
     State('text_numero_modulo', 'value'),
     State('text_data_prelievo', 'value'),
     State('text_data_accettazione', 'value'),
     State('text_id_campione', 'value'),
     State('text_descrizione_campione', 'value'),
     State('text_operatore_prelievo_campione', 'value')]
)
def crea_nuova_accettazione(submit_accettazione_click, text_unita_operativa,
                            text_numero_modulo, text_data_prelievo,
                            text_data_accettazione, text_id_campione, text_descrizione_campione, text_operatore_prelievo_campione):
    # inserire nuova accettazione in elenco, conferma inserimento e aggiorna tabella accettazione
    # print(locals().values())
    if None in locals().values():
        raise PreventUpdate

    # check validità numero di campioni/descrizione/operatore prelievo
    campioni_id_list = text_id_campione.split('\n')
    campioni_descrizione_list = text_descrizione_campione.split('\n')
    campioni_operatori_list = text_operatore_prelievo_campione.split('\n')
    check_len_set = set()
    check_len_set.add(len(campioni_id_list))
    check_len_set.add(len(campioni_descrizione_list))
    check_len_set.add(len(campioni_operatori_list))
    if len(check_len_set) > 1:
        print('non corrispondenza campioni/descrizione/operatori prelievo')
        alert_submit = dbc.Alert("ERRORE IN INSERIMENTO CAMPIONI",
                                 is_open=True, duration=5000, color='danger')
        table_accettazione = dash_table.DataTable()

        out_list = list()
        out_list.append('/')
        out_list.append(alert_submit)
        out_list.append(table_accettazione)

        return out_list

    # crea oggetto documento_accettazione
    new_doc_accettazione = documento_accettazione(unita_operativa=text_unita_operativa, n_modulo=text_numero_modulo,
                                                  data_prelievo=text_data_prelievo, data_accettazione=text_data_accettazione,
                                                  id_campione=text_id_campione.replace('\n', ','), descrizione_campione=text_descrizione_campione.replace('\n', ','),
                                                  operatore_prelievo_campione=text_operatore_prelievo_campione.replace('\n', ','))
    # codice della corrente accettazione
    current_code = text_numero_modulo

    file_accettazione_da_scrivere = open('documenti_accettazione/accettazione_' +
                                         current_code.upper()+'.txt', 'w')
    # scrivi file di testo con dati del documento_accettazione
    new_doc_accettazione.scrivi_file(
        file_destinazione=file_accettazione_da_scrivere)
    file_accettazione_da_scrivere.close()

    accettazione_to_db = (text_numero_modulo, text_unita_operativa, text_data_prelievo, text_data_accettazione, text_id_campione.replace('\n', ','),
                          text_descrizione_campione.replace('\n', ','), text_operatore_prelievo_campione.replace('\n', ','), 'accettazione_'+current_code.upper()+'.txt')
    insert_accettazione(accettazione_to_db)

    for index, id_campione in enumerate(campioni_id_list):
        file_referto_da_scrivere = open(
            'documenti_referti/referto_'+current_code.upper()+'_'+str(id_campione).upper()+'.txt', 'w')
        new_doc_referto = documento_referto(unita_operativa=text_unita_operativa, n_modulo=text_numero_modulo,
                                            data_prelievo=text_data_prelievo, data_accettazione=text_data_accettazione,
                                            id_campione=id_campione, descrizione_campione=campioni_descrizione_list[
                                                index],
                                            operatore_prelievo_campione=campioni_operatori_list[index])
        new_doc_referto.scrivi_file(file_destinazione=file_referto_da_scrivere)
        file_referto_da_scrivere.close()

        referto_to_db = (text_numero_modulo+'_'+id_campione,
                         text_numero_modulo, id_campione, text_unita_operativa, text_data_prelievo, text_data_accettazione, '', campioni_descrizione_list[index], campioni_operatori_list[index], '', '', '')
        insert_referto(referto_to_db)
    # update file con accettazioni
    # update_database_accettazioni()

    # update file con accettazioni
    # update_database_referti()

    # output list
    out_list = list()
    alert_submit = dbc.Alert("Modulo di accettazione inserito correttamente",
                             is_open=True, duration=5000, color='success')
    table_accettazione = update_table_accettazione()

    out_list.append('/apps/pagina_accettazione')
    out_list.append(alert_submit)
    out_list.append(table_accettazione)

    return out_list
