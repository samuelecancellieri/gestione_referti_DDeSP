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
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
from db_manager import database


# def update_dropdown_unita_operativa():
#     # ritorna tabella contenente i link ai file in documenti_accettazione
#     conn = sqlite3.connect(database)
#     c = conn.cursor()
#     tabella_referti = pd.read_sql_query(
#         "SELECT * FROM referti", conn)

#     return list(tabella_referti['unita_operativa'].unique())


def update_table_referti():
    conn = sqlite3.connect(database)
    tabella_referti = pd.read_sql_query("SELECT * FROM referti", conn)
    # tabella_referti = pd.read_sql_query(
    #     "SELECT * FROM referti WHERE \"{}\"=\'{}\'".format('unita_operativa', unita_operativa), conn)
    tabella_referti['index'] = tabella_referti['rapporto_di_prova'].apply(
        lambda x: str(x).split('_')[0])
    tabella_referti['index'] = tabella_referti['index'].astype(int)
    tabella_referti.sort_values(
        'index', ascending=True, inplace=True)
    tabella_referti.drop(['index'], inplace=True, axis=1)
    conn.commit()
    conn.close()
    tabella_referti = tabella_referti.loc[(tabella_referti['UFC_batteri']
                                          != '') & (tabella_referti['UFC_miceti'] != '')]
    tabella_referti['UFC_batteri'] = tabella_referti['UFC_batteri'].astype(int)
    tabella_referti['UFC_miceti'] = tabella_referti['UFC_miceti'].astype(int)
    tabella_referti['strumento'] = tabella_referti['id_campione'].apply(
        lambda x: str(x).split('-')[0])
    tabella_referti['anno'] = tabella_referti['rapporto_di_prova'].apply(
        lambda x: str(x).split('_')[1])

    lista_tabella_consultiva_unita_operative = list()
    for unita_operativa in tabella_referti['unita_operativa'].unique():
        temp_list = list()
        temp_list.append(unita_operativa)
        for anno in tabella_referti['anno'].unique():
            tabella_anno = tabella_referti.loc[(
                tabella_referti['anno'] == anno) & (tabella_referti['unita_operativa'] == unita_operativa)]
            tabella_anno = tabella_anno[(tabella_anno['UFC_batteri'] >= 1) | (
                tabella_anno['UFC_miceti'] >= 1)]
            tabella_anno.drop_duplicates('strumento', inplace=True)
            temp_list.append(len(tabella_anno.index))
        lista_tabella_consultiva_unita_operative.append(temp_list)

    colonne = ['Unità_Operativa']
    for anno in tabella_referti['anno'].unique():
        colonne.append('Strumenti_positivi_'+str(anno))
    # colonne.append('Numero positivi con enterobatteri')
    tabella_consultiva_unita_operative = pd.DataFrame(
        data=lista_tabella_consultiva_unita_operative, columns=colonne)

    try:
        table = dash_table.DataTable(
            id='table_referti',
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
        table = dash_table.DataTable(id='table_referti')

    return table


def return_layout():
    # ritorna il layout per la pagina accettazione
    layout = html.Div(
        [
            dcc.Location(id='refresh_url_consuntivo', refresh=True),
            dbc.Row(
                html.Div(
                    html.H4('Tabella Consuntivo con strumenti positivi per anno e unità operativa'))
            ),
            # dbc.Row(
            #     dbc.Col(
            #         html.Div(
            #             [
            #                 html.P('Seleziona una unità operativa'),
            #                 dcc.Dropdown(
            #                     options=update_dropdown_unita_operativa(), id='dropdown_unita_operativa', style={'width': '300px'})
            #             ]
            #         )
            #     )
            # ),
            html.Br(),
            dbc.Row(
                dbc.Col(
                    html.Div(update_table_referti(),
                             id='div_table_consuntivo'
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
#     return update_table_referti(unita_operativa)
