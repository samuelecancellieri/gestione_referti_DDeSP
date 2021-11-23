class documento_base:
    def __init__(self, unita_operativa='', n_modulo='', data_prelievo='', data_accettazione=''):
        # costruttore
        self.unita_operativa = unita_operativa
        self.n_modulo = n_modulo
        self.data_prelievo = data_prelievo
        self.data_accettazione = data_accettazione

    def scrivi_file(self, file_destinazione):
        # scrivi oggetto in file di testo
        for key in self.__dict__:
            file_destinazione.write(
                str(key)+':'+str(self.__dict__[key]).upper()+'\n')

    def leggi_file(self, file_da_leggere):
        # legge file di accettazione e ritorna l'oggetto
        file_letto = file_da_leggere.readlines()
        # print(file_letto)
        for elem in file_letto:
            if elem.strip().split(':')[0] in self.__dict__.keys():
                key = elem.strip().split(':')[0]
                self.__dict__[key] = elem.strip().split(':')[1]


class documento_accettazione(documento_base):
    def __init__(self, unita_operativa='', n_modulo='', data_prelievo='', data_accettazione='',
                 id_campione='', descrizione_campione='', operatore_prelievo_campione=''):
        super().__init__(unita_operativa='',
                         n_modulo='', data_prelievo='', data_accettazione='')
        self.unita_operativa = unita_operativa
        self.n_modulo = n_modulo
        self.data_prelievo = data_prelievo
        self.data_accettazione = data_accettazione
        self.id_campione = id_campione
        self.descrizione_campione = descrizione_campione
        self.operatore_prelievo_campione = operatore_prelievo_campione


class documento_referto(documento_base):
    def __init__(self, rapporto_di_prova='', unita_operativa='', n_modulo='', data_prelievo='', data_accettazione='',
                 id_campione='', descrizione_campione='', operatore_prelievo_campione='',
                 data_inizio_fine_analisi='', risultati=''):
        super().__init__(unita_operativa='',
                         n_modulo='', data_prelievo='', data_accettazione='')
        self.rapporto_di_prova = rapporto_di_prova
        self.unita_operativa = unita_operativa
        self.n_modulo = n_modulo
        self.data_prelievo = data_prelievo
        self.data_accettazione = data_accettazione
        self.id_campione = id_campione
        self.descrizione_campione = descrizione_campione
        self.operatore_prelievo_campione = operatore_prelievo_campione
        self.data_inizio_fine_analisi = data_inizio_fine_analisi
        self.risultati = risultati

    def set_data_analisi(self, data_inizio_fine_analisi):
        self.data_inizio_fine_analisi = data_inizio_fine_analisi

    def set_risultati(self, risultati):
        self.risultati = risultati
