from faulthandler import disable
import os
import re
import sqlite3
from time import sleep
from traceback import print_tb
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from numpy.lib.function_base import _diff_dispatcher
# from app import URL, app
from app import app
import pandas as pd
# from datatable import dt, f, sort
from dash import html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
from db_manager import database, create_connection

def update_table_consultivo_strumenti():
    conn = create_connection(database)
    tabella_referti = pd.read_sql_query("SELECT * FROM referti", conn)
    tabella_identificazione=pd.read_sql_query("SELECT * FROM referti_identificazione", conn)
    conn.commit()
    conn.close()

    #ordina per indice usando il rapporto di prova
    tabella_referti['index'] = tabella_referti['rapporto_di_prova'].apply(
        lambda x: str(x).strip().split('_')[0])
    tabella_referti['index'] = tabella_referti['index'].astype(int)
    tabella_referti.sort_values(
        'index', ascending=True, inplace=True)
    tabella_referti.drop(['index'], inplace=True, axis=1)
    
    tabella_identificazione['index'] = tabella_identificazione['rapporto_di_prova_identificazione'].apply(
        lambda x: str(x).strip().split('_')[0])
    tabella_identificazione['index'] = tabella_identificazione['index'].astype(int)
    tabella_identificazione.sort_values(
        'index', ascending=True, inplace=True)
    tabella_identificazione.drop(['index'], inplace=True, axis=1)

    #estrai ID strumento e anno da tabella
    tabella_referti['strumento'] = tabella_referti['id_campione'].apply(
        lambda x: str(x).strip().split('-')[0])
    tabella_referti['anno'] = tabella_referti['rapporto_di_prova'].apply(
        lambda x: str(x).strip().split('_')[1])
    
    tabella_identificazione['strumento'] = tabella_identificazione['id_campione'].apply(
        lambda x: str(x).strip().split('-')[0])
    tabella_identificazione['anno'] = tabella_identificazione['rapporto_di_prova_identificazione'].apply(
        lambda x: str(x).strip().split('_')[1])
    
    lista_tabella_consultiva_strumenti = list()
    for strumento in tabella_referti['strumento'].unique():
        lista_prelievi = list()
        lista_microrganimsi_trovati = list()
        #append di nome strumento univoco
        lista_prelievi.append(strumento)
        #estrai dati solo per strumento cosi da ottenere la sua unità operativa
        tabella_strumento = tabella_referti.loc[(tabella_referti['strumento'] == strumento)]
        lista_prelievi.append(tabella_strumento.iloc[0]['unita_operativa'])
        for anno in sorted(tabella_referti['anno'].unique()):
            #estrai dati per anno e strumento da referti
            tabella_anno = tabella_referti.loc[(
                tabella_referti['anno'] == anno) & (tabella_referti['strumento'] == strumento)]
            #estrai dati per anno e strumento da identificazione
            tabella_anno_identificazione=tabella_identificazione.loc[(
                tabella_identificazione['anno'] == anno) & (tabella_identificazione['strumento'] == strumento)]
            lista_prelievi.append(len(tabella_anno.index))
            #salva identificazione se trovata altrimenti n.r.
            stringa_identificazione='n.r.'
            if tabella_anno_identificazione['identificazione'].to_list():
                stringa_identificazione=','.join(tabella_anno_identificazione['identificazione'].to_list())
            lista_microrganimsi_trovati.append(stringa_identificazione)
            lista_totale = list(lista_prelievi+lista_microrganimsi_trovati)
        lista_tabella_consultiva_strumenti.append(lista_totale)
    
    colonne = ['Strumento','Unità Operativa']
    for anno in sorted(tabella_referti['anno'].unique()):
        colonne.append('Prelievi strumento '+str(anno))
    for anno in sorted(tabella_referti['anno'].unique()):
        colonne.append('Microrganismi rilevati '+str(anno))
    tabella_consultiva_strumenti = pd.DataFrame(
        data=lista_tabella_consultiva_strumenti, columns=colonne)

    try:
        table = dash_table.DataTable(
            id='table_consultivo_strumenti',
            columns=[{"name": i, "id": i, 'hideable': False}
                     for i in tabella_consultiva_strumenti.columns],
            data=tabella_consultiva_strumenti.to_dict('records'),
            export_format="xlsx",
            filter_action='native',
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
        table = dash_table.DataTable(id='table_consultivo_strumenti')

    return table


def update_table_consultivo_unita_operative():
    conn = create_connection(database)
    tabella_referti = pd.read_sql_query("SELECT * FROM referti", conn)
    tabella_identificazione=pd.read_sql_query("SELECT * FROM referti_identificazione", conn)
    conn.commit()
    conn.close()

    # rapporto di prova usato per ottenere l'id della tabella senza l'anno ed ordinare la tabella
    tabella_referti['index'] = tabella_referti['rapporto_di_prova'].apply(
        lambda x: str(x).strip().split('_')[0])
    tabella_referti['index'] = tabella_referti['index'].astype(int)
    tabella_referti.sort_values(
        'index', ascending=True, inplace=True)
    tabella_referti.drop(['index'], inplace=True, axis=1)
    
    #stesso fatto su tabella identificazione
    tabella_identificazione['index'] = tabella_identificazione['rapporto_di_prova_identificazione'].apply(
        lambda x: str(x).strip().split('_')[0])
    tabella_identificazione['index'] = tabella_identificazione['index'].astype(int)
    tabella_identificazione.sort_values(
        'index', ascending=True, inplace=True)
    tabella_identificazione.drop(['index'], inplace=True, axis=1)

    # estraggo solo i referti completi e converto ad int tutti i valori
    tabella_referti = tabella_referti.loc[(tabella_referti['UFC_batteri']
                                          != '') & (tabella_referti['UFC_miceti'] != '')]
    tabella_referti['UFC_batteri'] = tabella_referti['UFC_batteri'].astype(int)
    tabella_referti['UFC_miceti'] = tabella_referti['UFC_miceti'].astype(int)
    # estraggo id strumento da id campione
    tabella_referti['strumento'] = tabella_referti['id_campione'].apply(
        lambda x: str(x).strip().split('-')[0])
    # estraggo anno da rapporto di prova
    tabella_referti['anno'] = tabella_referti['rapporto_di_prova'].apply(
        lambda x: str(x).strip().split('_')[1])
    
    # estraggo anno da rapporto di prova
    tabella_identificazione['anno'] = tabella_identificazione['rapporto_di_prova_identificazione'].apply(
        lambda x: str(x).strip().split('_')[1])

    # ciclo sul dataframe per unità operativa e anno, cosi da ottenere il conto specifico per unità operativa/anno dei positivi
    lista_tabella_consultiva_unita_operative = list()
    for unita_operativa in tabella_referti['unita_operativa'].unique():
        lista_strumenti_positivi = list()
        conta_strumenti_per_micro=list()
        lista_strumenti_positivi.append(unita_operativa)
        for anno in sorted(tabella_referti['anno'].unique()):
            tabella_anno = tabella_referti.loc[(
                tabella_referti['anno'] == anno) & (tabella_referti['unita_operativa'] == unita_operativa)]
            tabella_anno = tabella_anno[(tabella_anno['UFC_batteri'] >= 1) | (
                tabella_anno['UFC_miceti'] >= 1)]
            tabella_anno.drop_duplicates('strumento', inplace=True)
            lista_strumenti_positivi.append(len(tabella_anno.index))
        for micro in sorted(tabella_identificazione['identificazione'].unique()):
            tabella_identificazione_unita_operativa=tabella_identificazione.loc[(tabella_identificazione['unita_operativa'] == unita_operativa)]
            tabella_identificazione_unita_operativa=tabella_identificazione_unita_operativa[tabella_identificazione_unita_operativa['identificazione']==micro]
            conta_strumenti_per_micro.append(len(tabella_identificazione_unita_operativa.index))
        lista_totale=list(lista_strumenti_positivi+conta_strumenti_per_micro)
        lista_tabella_consultiva_unita_operative.append(lista_totale)

    # popolo il df finale con le info raccolte nel passo precedente, le colonne sono generate per ogni anno contenuto nel db
    colonne = ['Unità Operativa']
    for anno in sorted(tabella_referti['anno'].unique()):
        colonne.append('Strumenti Positivi '+str(anno))
    for  micro in sorted(tabella_identificazione['identificazione'].unique()):
        colonne.append('Numero Strumenti con positivà a '+str(micro))
    tabella_consultiva_unita_operative = pd.DataFrame(
        data=lista_tabella_consultiva_unita_operative, columns=colonne)

    try:
        table = dash_table.DataTable(
            id='table_consultivo_unita_operative',
            columns=[{"name": i, "id": i, 'hideable': False}
                     for i in tabella_consultiva_unita_operative.columns],
            data=tabella_consultiva_unita_operative.to_dict('records'),
            export_format="xlsx",
            filter_action='native',
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
        table = dash_table.DataTable(id='table_consultivo_unita_operative')

    return table


def return_layout():
    # ritorna il layout per la pagina accettazione
    layout = html.Div(
        [
            dcc.Location(id='refresh_url_consuntivo', refresh=True),
            dbc.Row(
                html.Div(
                    html.H4('Tabella Consuntivo con positività per Unità Operativa'))
            ),
            dbc.Row(
                dbc.Col(
                    html.Div(update_table_consultivo_unita_operative(),
                             id='div_table_consuntivo_unita_operative'
                             )
                )
            ),
            dbc.Row(html.Br()),
            dbc.Row(
                html.Div(
                    html.H4('Tabella Consuntivo con prelievi per Strumento'))
            ),
            dbc.Row(
                dbc.Col(
                    html.Div(update_table_consultivo_strumenti(),
                             id='div_table_consuntivo_strumenti'
                             )
                )
            ),
        ], style={'margin-left': '2%', 'margin-top': '2%'}
    )

    return layout


# @ app.callback(
#     Output('div_table_consuntivo', 'children'),
#     Input('dropdown_unita_operativa', 'value')


# )
# def update_tabella_consuntivo_unita_operativa(unita_operativa):
#     return update_table_consultivo_unita_operative(unita_operativa)
