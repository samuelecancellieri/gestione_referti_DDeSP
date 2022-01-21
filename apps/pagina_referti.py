import os
import sqlite3
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from numpy.lib.function_base import _diff_dispatcher
# from app import URL, app
from app import app
import pandas as pd
# from datatable import dt, f, sort
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
from documenti import documento_accettazione, documento_referto
from db_manager import insert_referto, database


# def lista_documenti_referti():
#     # ritorna la lista di documenti in cartella documenti_accettazione
#     lista_documenti_referti = os.listdir('documenti_referti/')

#     return lista_documenti_referti


# def return_dizionario_referti(codice_accettazione):
#     # print('entro diz')
#     df_referti = 'database/database_referti.txt'
#     # ritorna il dizionario con i dati dei file in cartella documenti_accettazione
#     df_referti = pd.read_csv(df_referti, sep=';')
#     df_referti = df_referti.loc[(
#         df_referti['n_modulo'] == codice_accettazione)]
#     # print(df_referti)
#     return df_referti


# def return_dizionario_accettazione():
#     database_accettazioni = 'database/database_accettazioni.txt'
#     # ritorna il dizionario con i dati dei file in cartella documenti_accettazione
#     df_accettazioni = pd.read_csv(database_accettazioni, sep=';')
#     return df_accettazioni


def update_table_referti(codice_accettazione):
    # ritorna tabella contenente i link ai file in documenti_accettazione
    conn = sqlite3.connect(database)
    c = conn.cursor()
    tabella_referti = pd.read_sql_query(
        "SELECT * FROM referti WHERE \"{}\"=\'{}\'".format('id_accettazione', codice_accettazione), conn)
    # rows = c.execute(tabella_accettazione)
    # header = [description[0] for description in rows.description]
    conn.commit()
    conn.close()
    try:
        table = dash_table.DataTable(
            id='table_referti',
            columns=[{"name": i, "id": i, 'hideable': False}
                     for i in tabella_referti.columns],
            data=tabella_referti.to_dict('records'),
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
        table = dash_table.DataTable(id='table_referti')

    return table


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
            id='table_accettazione_in_referti',
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
                html.Div(
                    html.H4('Tabella Accettazioni')
                )
            ),
            dbc.Row(
                html.Div(
                    update_table_accettazione(),
                    id='div_table_accettazione_in_referti'
                )
            ),
            html.Br(),
            dbc.Row(
                html.Div(
                    html.H4('Tabella Referti')
                )
            ),
            dbc.Row(
                html.Div(
                    # update_table_referti(),
                    id='div_table_referti'
                )
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.P('unità operativa invio'),
                                dcc.Textarea(id='text_unita_operativa_referti', placeholder='Neurologia', style={
                                    'width': '300px', 'height': '30px'})
                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('numero modulo'),
                                dcc.Textarea(id='text_numero_modulo_referti', placeholder='ABC123', style={
                                    'width': '300px', 'height': '30px'}),
                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('data prelievo'),
                                dcc.Textarea(id='text_data_prelievo_referti', placeholder='13/10/2021', style={
                                    'width': '300px', 'height': '30px'}),
                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('data_accettazione'),
                                dcc.Textarea(id='text_data_accettazione_referti', placeholder='13/10/2021', style={
                                    'width': '300px', 'height': '30px'}),

                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('Inserire rapporto di prova'),
                                dcc.Textarea(id='text_rapporto_di_prova_referti', placeholder='x/2021', style={
                                    'width': '300px', 'height': '30px'}),

                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('id campione analizzato'),
                                dcc.Textarea(id='text_id_campione_referti', placeholder='id123', style={
                                    'width': '300px', 'height': '30px'}),
                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('descrizione campione'),
                                dcc.Textarea(id='text_descrizione_campione_referti', placeholder='prelievo_cappa', style={
                                    'width': '300px', 'height': '30px'}),
                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('operatore_prelievo_campione'),
                                dcc.Textarea(id='text_operatore_prelievo_campione_referti', placeholder='Mario Rossi', style={
                                    'width': '300px', 'height': '30px'})
                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('Inserire data inizio analisi'),
                                dcc.Textarea(id='text_data_inizio_analisi_referti', placeholder='10/12/2021', style={
                                    'width': '300px', 'height': '30px'})
                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('Inserire data fine analisi'),
                                dcc.Textarea(id='text_data_fine_analisi_referti', placeholder='11/12/2021', style={
                                    'width': '300px', 'height': '30px'})
                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.P('Inserire risultati'),
                                dcc.Textarea(id='text_risultati_referti', placeholder='E. Coli', style={
                                    'width': '300px', 'height': '30px'})
                            ]
                        )
                    )
                ]
            ),
            dbc.Row(
                html.Div(
                    [
                        html.Button(
                            'Submit', id='submit_referto'),
                        html.Div(id='alert_submission')
                    ]
                )
            )
        ], style={'margin-left': '2%', 'margin-top': '2%'}
    )

    return layout


@ app.callback(
    Output('div_table_referti', 'children'),
    [Input('table_accettazione_in_referti', 'active_cell'),
     Input('table_accettazione_in_referti', 'derived_virtual_data')]
)
def display_referti_by_accettazione(cella_selezionata_accettazione, table_virtual_data):
    # ritorna tabella referti aggiornata con referti di doc_accettazione
    if cella_selezionata_accettazione is None:
        raise PreventUpdate

    # ritorna codice modulo accettazione per aprire referti correlati
    codice_modulo_accettazione = table_virtual_data[cella_selezionata_accettazione['row']
                                                    ]['id']
    tabella_referti = update_table_referti(codice_modulo_accettazione)

    return tabella_referti


@ app.callback(
    [Output('text_unita_operativa_referti', 'value'),
     Output('text_numero_modulo_referti', 'value'),
     Output('text_data_prelievo_referti', 'value'),
     Output('text_data_accettazione_referti', 'value'),
     Output('text_rapporto_di_prova_referti', 'value'),
     Output('text_id_campione_referti', 'value'),
     Output('text_descrizione_campione_referti', 'value'),
     Output('text_operatore_prelievo_campione_referti', 'value'),
     Output('text_data_inizio_analisi_referti', 'value'),
     Output('text_data_fine_analisi_referti', 'value'),
     Output('text_risultati_referti', 'value')],
    [Input('table_referti', 'active_cell'),
     Input('table_referti', "derived_virtual_data")]
)
def apri_referto(cella_selezionata_referto, table_virtual_data):
    if cella_selezionata_referto is None:
        raise PreventUpdate

    # documento_referto_id = table_virtual_data[cella_selezionata_referto['row']]['id']
    # file referto selezionato nella tabella
    # referto_da_leggere = open(
    #     'documenti_referti/referto_'+documento_referto_id+'.txt', 'r')
    # # crea doc referto vuoto e poi assegna membri dopo lettura
    # documento_referto_letto = documento_referto()
    # documento_referto_letto.leggi_file(
    #     file_da_leggere=referto_da_leggere)
    # referto_da_leggere.close()

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
        table_virtual_data[cella_selezionata_referto['row']]['data_inizio_analisi'])
    out_list.append(
        table_virtual_data[cella_selezionata_referto['row']]['data_fine_analisi'])
    out_list.append(
        table_virtual_data[cella_selezionata_referto['row']]['risultato'])

    return out_list


@ app.callback(
    Output('refresh_url_referti', 'href'),
    [Input('submit_referto', 'n_clicks')],
    [State('text_unita_operativa_referti', 'value'),
     State('text_numero_modulo_referti', 'value'),
     State('text_data_prelievo_referti', 'value'),
     State('text_data_accettazione_referti', 'value'),
     State('text_rapporto_di_prova_referti', 'value'),
     State('text_id_campione_referti', 'value'),
     State('text_descrizione_campione_referti', 'value'),
     State('text_operatore_prelievo_campione_referti', 'value'),
     State('text_data_inizio_fine_analisi_referti', 'value'),
     State('text_risultati_referti', 'value')]
)
def modifica_e_scrittura_referto(submit_referto_click, text_unita_operativa_referti,
                                 text_numero_modulo_referti, text_data_prelievo_referti,
                                 text_data_accettazione_referti, text_rapporto_di_prova_referti, text_id_campione_referti,
                                 text_descrizione_campione_referti, text_operatore_prelievo_campione_referti,
                                 text_data_inizio_fine_analisi_referti, text_risultati_referti):
    if None in locals().values() or '' in locals().values():
        raise PreventUpdate

    # modifica file di referto con nuovi dati, procedi solo se ogni campo è scritto
    file_referto_da_scrivere = open(
        'documenti_referti/referto_'+text_numero_modulo_referti.upper()+'_'+str(text_id_campione_referti).upper()+'.txt', 'w')
    new_doc_referto = documento_referto(unita_operativa=text_unita_operativa_referti, n_modulo=text_numero_modulo_referti,
                                        data_prelievo=text_data_prelievo_referti, data_accettazione=text_data_accettazione_referti,
                                        id_campione=text_id_campione_referti, descrizione_campione=text_descrizione_campione_referti,
                                        operatore_prelievo_campione=text_operatore_prelievo_campione_referti,
                                        rapporto_di_prova=text_rapporto_di_prova_referti,
                                        data_inizio_fine_analisi=text_data_inizio_fine_analisi_referti, risultati=text_risultati_referti)
    new_doc_referto.scrivi_file(file_destinazione=file_referto_da_scrivere)
    file_referto_da_scrivere.close()

    return '/apps/pagina_referti'
