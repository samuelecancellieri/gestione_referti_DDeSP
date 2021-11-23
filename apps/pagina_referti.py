from app import app
import os
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, dash_table
from dash.exceptions import PreventUpdate
import pandas as pd


# class documento_referto(documento_accettazione):
#     def __init__(self, codice='', nome_operatore_invio='', nome_operatore_esecutore='', analisi='', dipartimento_provenienza='', risultato=''):
#         # costruttore
#         super().__init__(codice, nome_operatore_invio,
#                          nome_operatore_esecutore, analisi, dipartimento_provenienza)
#         self.risultato = risultato

#     def scrivi_file(self, file_destinazione):
#         # scrivi oggetto in file di testo
#         for key in self.__dict__:
#             file_destinazione.write(
#                 str(key).upper()+':'+str(self.__dict__[key]).upper()+'\n')

#     def leggi_file(self, file_da_leggere):
#         # legge file di accettazione e ritorna l'oggetto
#         referto = file_da_leggere.readlines()
#         self.codice = referto[0].split(':')[1].strip()
#         self.nome_operatore_invio = referto[1].split(':')[1].strip()
#         self.nome_operatore_esecutore = referto[2].split(':')[1].strip()
#         self.analisi = referto[3].split(':')[1].strip()
#         self.dipartimento_provenienza = referto[4].split(':')[1].strip()
#         self.risultato = referto[4].split(':')[1].strip()


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
                                html.P('Inserire nome operatore invio'),
                                dcc.Textarea(id='text_nome_operatore_invio', placeholder='Mario Rossi', style={
                                    'width': '300px', 'height': '30px'}),
                                html.P('Inserire nome operatore esecutore'),
                                dcc.Textarea(id='text_nome_operatore_esecutore', placeholder='Mario Rossi', style={
                                    'width': '300px', 'height': '30px'}),
                                html.P('Inserire analisi da effettuare'),
                                dcc.Textarea(id='text_analisi', placeholder='Mario Rossi', style={
                                    'width': '300px', 'height': '30px'}),
                                html.P('Inserire dipartimento di provenienza'),
                                dcc.Textarea(id='text_dipartimento_provenienza', placeholder='Mario Rossi', style={
                                    'width': '300px', 'height': '30px'}),
                            ]
                        )
                    )
                ], style={'margin': '1%'}
            )
        ]
    )

    return layout
