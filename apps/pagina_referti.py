from app import app
import os
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, dash_table
from dash.exceptions import PreventUpdate
import pandas as pd
from documenti import documento_accettazione, documento_referto


def lista_documenti_referti():
    # ritorna la lista di documenti in cartella documenti_accettazione
    lista_documenti_referti = os.listdir('documenti_referti/')

    return lista_documenti_referti


def return_dizionario_referti():
    df_referti = 'database/database_referti.txt'
    # ritorna il dizionario con i dati dei file in cartella documenti_accettazione
    df_referti = pd.read_csv(df_referti, sep=';')
    return df_referti


def return_dizionario_accettazione():
    database_accettazioni = 'database/database_accettazioni.txt'
    # ritorna il dizionario con i dati dei file in cartella documenti_accettazione
    df_accettazioni = pd.read_csv(database_accettazioni, sep=';')

    return df_accettazioni


def update_table_referti():
    # ritorna tabella contenente i link ai file in documenti_accettazione
    try:
        table = dash_table.DataTable(
            id='table_referti',
            columns=[{"name": i, "id": i}
                     for i in return_dizionario_referti().columns],
            data=return_dizionario_referti().to_dict('records'),
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
        table = dash_table.DataTable(id='table_referti')

    return table


def update_table_accettazione():
    # ritorna tabella contenente i link ai file in documenti_accettazione
    try:
        table = dash_table.DataTable(
            id='table_accettazione_in_referti',
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
        table = dash_table.DataTable(id='table_accettazione_in_referti')

    return table


def return_layout():
    # ritorna il layout per la pagina accettazione
    layout = html.Div(
        [
            dcc.Location(id='refresh_url', refresh=True),
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
                    update_table_referti(),
                    id='div_table_referti'
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
            )
        ], style={'margin': '1%'}
    )

    return layout


# @ app.callback(
#     Output('div_table_referti', 'children'),
#     Input('table_accettazione_in_referti', 'active_cell'),
# )
# def display_referti_by_accettazione(cella_selezionata_accettazione):
#     # ritorna tabella referti aggiornata con referti di doc_accettazione

#     if cella_selezionata_accettazione is None:
#         raise PreventUpdate

#     # ritorna dataframe per tabella di documenti_accettazione
#     df_accettazione = return_dizionario_accettazione()
#     row = cella_selezionata_accettazione['row']
#     codice_modulo_accettazione = df_accettazione.loc[row, 'n_modulo']

#     tabella_referti = update_table_referti(codice_modulo_accettazione)

#     return update_table_referti()
