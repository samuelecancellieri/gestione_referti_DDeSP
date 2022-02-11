from faulthandler import disable
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
from db_manager import insert_accettazione, insert_referto, database, get_id_last_row
from stampa_pdf import stampa_accettazione, stampa_referto


def update_table_accettazione():
    # ritorna tabella contenente i link ai file in documenti_accettazione
    conn = sqlite3.connect(database)
    tabella_accettazione = pd.read_sql_query(
        "SELECT * FROM accettazioni", conn)
    tabella_accettazione.sort_values('id', ascending=True, inplace=True)
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
                dbc.Col(
                    html.Div(
                        update_table_accettazione(),
                        id='div_table_accettazione'
                    )
                )
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.P('ID accettazione '),
                                dcc.Textarea(id='text_id_accettazione', disabled=True, value='nuova_accettazione', style={
                                    'width': '300px', 'height': '30px'}),
                            ]
                        )
                    ),
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
                        html.Button('INVIO', id='submit_accettazione'),
                        html.Div(id='alert_submission'),
                        dcc.Download(id="download_accettazione")
                    ]
                )
            ),
        ], style={'margin-left': '2%', 'margin-top': '2%'}
    )

    return layout


def get_id_referti(id_accettazione):
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        sql_select_query = """SELECT id from referti where id_accettazione = ?"""
        cursor.execute(sql_select_query, (id_accettazione,))
        records = cursor.fetchall()
        records.sort()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print('record id referti', records)
            return records  # return list of ids


@ app.callback(
    [Output('text_unita_operativa', 'value'),
     Output('text_id_accettazione', 'value'),
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

    # output list
    out_list = list()
    out_list.append(table_virtual_data[cella_selezionata_accettazione['row']
                                       ]['unita_operativa'])
    out_list.append(table_virtual_data[cella_selezionata_accettazione['row']
                                       ]['id'])
    out_list.append(table_virtual_data[cella_selezionata_accettazione['row']
                                       ]['data_prelievo'])
    out_list.append(table_virtual_data[cella_selezionata_accettazione['row']
                                       ]['data_accettazione'])
    out_list.append(table_virtual_data[cella_selezionata_accettazione['row']
                                       ]['id_campioni'].replace(',', '\n'))
    out_list.append(table_virtual_data[cella_selezionata_accettazione['row']
                                       ]['descrizione_campioni'].replace(',', '\n'))
    out_list.append(table_virtual_data[cella_selezionata_accettazione['row']
                                       ]['operatore_prelievo_campioni'].replace(',', '\n'))

    return out_list


@ app.callback(
    [Output("refresh_url", "href"),
     Output('alert_submission', 'children'),
     Output('div_table_accettazione', 'children'),
     Output('download_accettazione', 'data')],
    [Input('submit_accettazione', 'n_clicks')],
    [State('text_id_accettazione', 'value'),
     State('text_unita_operativa', 'value'),
     State('text_data_prelievo', 'value'),
     State('text_data_accettazione', 'value'),
     State('text_id_campione', 'value'),
     State('text_descrizione_campione', 'value'),
     State('text_operatore_prelievo_campione', 'value')]
)
def crea_nuova_accettazione(submit_accettazione_click, text_id_accettazione, text_unita_operativa, text_data_prelievo,
                            text_data_accettazione, text_id_campione, text_descrizione_campione, text_operatore_prelievo_campione):
    # inserire nuova accettazione in elenco, conferma inserimento e aggiorna tabella accettazione
    if None in locals().values() or '' in locals().values():
        raise PreventUpdate

    # check validità numero di campioni/descrizione/operatore prelievo
    campioni_id_list = text_id_campione.strip().split('\n')
    campioni_descrizione_list = text_descrizione_campione.strip().split('\n')
    campioni_operatori_list = text_operatore_prelievo_campione.strip().split('\n')
    check_len_set = set()
    check_len_set.add(len(campioni_id_list))
    check_len_set.add(len(campioni_descrizione_list))
    check_len_set.add(len(campioni_operatori_list))
    if len(check_len_set) > 1:
        print('non corrispondenza numero campioni/descrizione/operatori prelievo')
        alert_submit = dbc.Alert("ERRORE IN INSERIMENTO CAMPIONI, CONTROLLARE CORRISPONDENZA #CAMPIONI = #DESCRIZIONI = #OPERATORI",
                                 is_open=True, duration=5000, color='danger')
        table_accettazione = dash_table.DataTable()

        out_list = list()
        out_list.append('/')
        out_list.append(alert_submit)
        out_list.append(table_accettazione)
        out_list.append(dcc.send_file(''))

        return out_list

    if text_id_accettazione == 'nuova_accettazione':  # se nuova accettazione crea nuova accettazione in db
        new_id_accettazione = str(get_id_last_row(
            'accettazioni')+1) + '_' + text_data_accettazione.strip().split('/')[-1]
    else:  # altrimenti modifica quella presente (update)
        new_id_accettazione = text_id_accettazione

    accettazione_to_db = (new_id_accettazione, text_unita_operativa, text_data_prelievo, text_data_accettazione, text_id_campione,
                          text_descrizione_campione, text_operatore_prelievo_campione, 'accettazione_'+new_id_accettazione+'.pdf')
    check_insert_accettazione = insert_accettazione(accettazione_to_db)

    if check_insert_accettazione:
        stampa_accettazione(new_id_accettazione, text_unita_operativa, text_data_prelievo, text_data_accettazione, str(text_id_campione).strip(
        ).split('\n'), str(text_descrizione_campione).strip().split('\n'), str(text_operatore_prelievo_campione).strip().split('\n'))

    if check_insert_accettazione:
        # usa id referto ordinato per campione inserito in accettazione
        id_referti = get_id_referti(text_id_accettazione)
        for index, id_campione in enumerate(campioni_id_list):
            if text_id_accettazione == 'nuova_accettazione':  # se nuova accettazione, crea nuovi referti correlati
                new_id_referto = str(get_id_last_row('referti')+1) + \
                    '_' + text_data_accettazione.strip().split('/')[-1]
                referto_to_db = (new_id_referto, new_id_accettazione, id_campione, text_unita_operativa, text_data_prelievo, text_data_accettazione, '',
                                 campioni_descrizione_list[index], campioni_operatori_list[index], '', '', '', '', '', '', 'referto_'+str(new_id_accettazione).upper()+'_'+str(id_campione).upper()+'.pdf')
                insert_referto(referto_to_db)
            else:
                new_id_referto = id_referti[index][0]
                # print('id referto estratto', new_id_referto)
                referto_to_db = (new_id_referto, new_id_accettazione, id_campione, text_unita_operativa, text_data_prelievo, text_data_accettazione, '',
                                 campioni_descrizione_list[index], campioni_operatori_list[index], '', '', '', '', '', '', 'referto_'+str(new_id_accettazione).upper()+'_'+str(id_campione).upper()+'.pdf')
                insert_referto(referto_to_db)

    if check_insert_accettazione:
        # output list
        out_list = list()
        alert_submit = dbc.Alert("Modulo di accettazione inserito correttamente",
                                 is_open=True, duration=5000, color='success')
        table_accettazione = update_table_accettazione()

        out_list.append('/apps/pagina_accettazione')
        out_list.append(alert_submit)
        out_list.append(table_accettazione)
        out_list.append(dcc.send_file(
            'documenti_accettazione/accettazione_'+str(new_id_accettazione).upper()+'.pdf'))
    else:
        print('errore inserimento database')
        alert_submit = dbc.Alert("ERRORE IN INSERIMENTO DATABASE, ATTNDERE QUALCHE SECONDO E RIPROVARE",
                                 is_open=True, duration=5000, color='danger')
        table_accettazione = dash_table.DataTable()

        out_list = list()
        out_list.append('/')
        out_list.append(alert_submit)
        out_list.append(table_accettazione)
        out_list.append(dcc.send_file(''))

    return out_list
