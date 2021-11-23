from app import app
import os
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, dash_table
from dash.exceptions import PreventUpdate
import pandas as pd
from documenti import documento_accettazione, documento_referto


# class documento_accettazione:
#     def __init__(self, codice='', nome_operatore_invio='', nome_operatore_esecutore='', analisi='', dipartimento_provenienza='', campioni=''):
#         # costruttore
#         self.codice = codice
#         self.nome_operatore_invio = nome_operatore_invio
#         self.nome_operatore_esecutore = nome_operatore_esecutore
#         self.analisi = analisi
#         self.dipartimento_provenienza = dipartimento_provenienza
#         self.campioni = campioni

#     def scrivi_file(self, file_destinazione):
#         # scrivi oggetto in file di testo
#         for key in self.__dict__:
#             file_destinazione.write(
#                 str(key).upper()+':'+str(self.__dict__[key]).upper()+'\n')

#     def leggi_file(self, file_da_leggere):
#         # legge file di accettazione e ritorna l'oggetto
#         accettazione = file_da_leggere.readlines()
#         self.codice = accettazione[0].split(':')[1].strip()
#         self.nome_operatore_invio = accettazione[1].split(':')[1].strip()
#         self.nome_operatore_esecutore = accettazione[2].split(':')[1].strip()
#         self.analisi = accettazione[3].split(':')[1].strip()
#         self.dipartimento_provenienza = accettazione[4].split(':')[1].strip()
#         self.dipartimento_provenienza = accettazione[5].split(':')[1].strip()


def lista_documenti_accettazione():
    # ritorna la lista di documenti in cartella documenti_accettazione
    lista_documenti_accettazione = os.listdir('documenti_accettazione/')

    return lista_documenti_accettazione


def return_dizionario_accettazione():
    # ritorna il dizionario con i nomi dei file in cartella documenti_accettazione
    df = pd.DataFrame(lista_documenti_accettazione())
    df.set_axis(['Documento Accettazione'], axis=1, inplace=True)

    return df


def update_table_accettazione():
    # ritorna tabella contenente i link ai file in documenti_accettazione
    try:
        table = dash_table.DataTable(
            id='table_accettazione',
            columns=[{"name": i, "id": i}
                     for i in return_dizionario_accettazione().columns],
            data=return_dizionario_accettazione().to_dict('records'),
            virtualization=True,
            fixed_rows={'headers': True, 'data': 0},
            style_cell={'textAlign': 'left'},
            style_table={
                'max-height': '400px'},
            css=[{'selector': '.row',
                  'rule': 'margin: 0'}, {'selector': 'td.cell--selected, td.focused', 'rule': 'background-color: rgba(0, 0, 255,0.15) !important;'}, {
                'selector': 'td.cell--selected *, td.focused *', 'rule': 'background-color: rgba(0, 0, 255,0.15) !important;'}],
        )
    except:
        # se niente da mettere in tabella, fai tabella vuota
        table = dash_table.DataTable()

    return table


def return_layout():
    # ritorna il layout per la pagina accettazione
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
                                html.P('Inserire unità operativa invio'),
                                dcc.Textarea(id='text_unita_operativa', placeholder='Mario Rossi', style={
                                    'width': '300px', 'height': '30px'}),
                                html.P('Inserire numero modulo'),
                                dcc.Textarea(id='text_numero_modulo', placeholder='Mario Rossi', style={
                                    'width': '300px', 'height': '30px'}),
                                html.P('Inserire data prelievo'),
                                dcc.Textarea(id='text_data_prelievo', placeholder='Mario Rossi', style={
                                    'width': '300px', 'height': '30px'}),
                                html.P('Inserire data_accettazione'),
                                dcc.Textarea(id='text_data_accettazione', placeholder='Mario Rossi', style={
                                    'width': '300px', 'height': '30px'}),
                                html.P('Inserire id campione, uno per riga'),
                                dcc.Textarea(id='text_id_campione', placeholder='Mario Rossi', style={
                                    'width': '300px', 'height': '30px'}),
                                html.P(
                                    'Inserire descrizione campione, uno per riga'),
                                dcc.Textarea(id='text_descrizione_campione', placeholder='Mario Rossi', style={
                                    'width': '300px', 'height': '30px'}),
                                html.P(
                                    'Inserire operatore_prelievo_campione, uno per riga'),
                                dcc.Textarea(id='text_operatore_prelievo_campione', placeholder='Mario Rossi', style={
                                    'width': '300px', 'height': '30px'})
                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            update_table_accettazione(),
                            id='div_table_accettazione'
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
                                        id='div_modal', style={'white-space': 'pre'}
                                    )
                                )
                            ],
                            id="modal_accettazione",
                            centered=True,
                            is_open=False,
                        ),
                    ]
                )
            )
        ], style={'margin': '1%'}
    )

    return layout


@ app.callback(
    [Output('modal_accettazione', 'is_open'),
     Output('div_modal', 'children')],
    Input('table_accettazione', 'active_cell')
)
def apri_file_accettazione(cella_selezionata):
    # apre modal con lettura file di accettazione selezionato in table_accettazione
    if cella_selezionata is None:
        raise PreventUpdate

    # ritorna dataframe per tabella di documenti_accettazione
    df_accettazione = return_dizionario_accettazione()
    row = cella_selezionata['row']
    col = cella_selezionata['column']

    # file accettazione selezionato nella tabella
    accettazione_da_leggere = open('documenti_accettazione/' +
                                   str(df_accettazione.iloc[row, col]), 'r')

    # crea doc accettazione vuoto e poi assegna membri dopo lettura
    documento_accettazione_letto = documento_accettazione()
    documento_accettazione_letto.leggi_file(
        file_da_leggere=accettazione_da_leggere)

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
    [Output('alert_submission', 'children'),
     Output('div_table_accettazione', 'children')],
    Input('submit_accettazione', 'n_clicks'),
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

    # estrae codice ultima accettazione
    try:
        last_code = int(lista_documenti_accettazione()
                        [-1].split('_')[1].replace('.txt', ''))
    except:
        last_code = 0
    # codice ultima accettazione+1
    current_code = str(last_code + 1)

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
        out_list.append(alert_submit)
        out_list.append(table_accettazione)

        return out_list

    # crea oggetto documento_accettazione
    new_doc_accettazione = documento_accettazione(unita_operativa=text_unita_operativa, n_modulo=text_numero_modulo,
                                                  data_prelievo=text_data_prelievo, data_accettazione=text_data_accettazione,
                                                  id_campione=text_id_campione.replace('\n', ','), descrizione_campione=text_descrizione_campione.replace('\n', ','),
                                                  operatore_prelievo_campione=text_operatore_prelievo_campione.replace('\n', ','))

    file_accettazione_da_scrivere = open('documenti_accettazione/accettazione_' +
                                         current_code+'.txt', 'w')
    # scrivi file di testo con dati del documento_accettazione
    new_doc_accettazione.scrivi_file(
        file_destinazione=file_accettazione_da_scrivere)

    for index, id_campione in enumerate(campioni_id_list):
        file_referto_da_scrivere = open(
            'documenti_referti/referto'+current_code+'_'+str(id_campione)+'.txt', 'w')
        new_doc_referto = documento_referto(unita_operativa=text_unita_operativa, n_modulo=text_numero_modulo,
                                            data_prelievo=text_data_prelievo, data_accettazione=text_data_accettazione,
                                            id_campione=id_campione, descrizione_campione=campioni_descrizione_list[
                                                index],
                                            operatore_prelievo_campione=campioni_operatori_list[index])
        new_doc_referto.scrivi_file(file_destinazione=file_referto_da_scrivere)

    # print('new doc', new_doc_accettazione.__dict__.values())

    # output list
    out_list = list()
    alert_submit = dbc.Alert("Modulo di accettazione inserito correttamente",
                             is_open=True, duration=5000, color='success')
    table_accettazione = update_table_accettazione()
    out_list.append(alert_submit)
    out_list.append(table_accettazione)

    return out_list
