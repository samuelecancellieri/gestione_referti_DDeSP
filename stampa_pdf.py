from sys import excepthook
from fpdf import FPDF


def stampa_referto_identificazione(id_accettazione, id_campione, unita_operativa, data_prelievo, data_accettazione, rapporto_di_prova, descrizione_campione, operatore_prelievo_campione, operatore_analisi, data_inizio_analisi, data_fine_analisi, identificazione, note):
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.set_margins(10, 10, 10)
    pdf.image('assets/logo-univr.png', w=70, x=10)
    # pdf.image('assets/logo-dip-diagnostica.png', type='PNG', w=100, x=120)
    # pdf.ln(2)
    # set color and for grey titles
    # set color and for grey titles
    pdf.set_font('arial', 'I', 12)
    pdf.cell(0, 0, '', 0, 1, 'C')
    pdf.set_font('arial', 'I', 12)
    pdf.set_text_color(220, 220, 220)  # grey
    # pdf.cell(12)
    pdf.cell(0, 10, "STRUTTURA", 0, 0, 'L')
    pdf.ln(5)
    # set color and for for main text
    pdf.set_text_color(0, 0, 0)  # black
    pdf.set_font('arial', '', 12)
    pdf.cell(150, 10, "LABORATORIO DI IGIENE", 0, 0, 'L')
    pdf.cell(20, 10, 'MR49', 0, 0, 'L')
    pdf.ln(6)
    # set color for documento
    pdf.set_font('arial', 'I', 12)
    pdf.set_text_color(220, 220, 220)  # grey
    pdf.cell(140, 10, "DOCUMENTO", 0, 0, 'L')
    pdf.set_font('arial', 'I', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, 'Data di Emissione 03.04.2020', 0, 0, 'L')
    pdf.ln(5)
    pdf.set_text_color(0, 0, 0)  # black
    pdf.set_font('arial', '', 12)
    pdf.cell(140, 10, "REFERTO IDENTIFICAZIONE MICROBICA PO28", 0, 0, 'L')
    pdf.set_font('arial', 'I', 10)
    pdf.cell(0, 10, 'Indice di Revisione 1', 0, 0, 'L')
    pdf.ln(8)
    pdf.set_font('arial', '', 12)
    pdf.cell(140, 10, 'Rif. PO28 "Identificazione microbica"', 0, 0, 'L')
    pdf.ln(10)

    # tabella prova
    pdf.set_text_color(0, 0, 0)  # black
    pdf.set_font('arial', '', 10)
    pdf.cell(90, 10, 'Rapporto di prova n°:', 0, 0, 'L')
    pdf.cell(120, 10, str(rapporto_di_prova), 0, 0, 'L')
    pdf.ln(5)
    pdf.cell(90, 10, 'Modulo campionamento-accettazione n°:', 0, 0, 'L')
    pdf.cell(120, 10, str(id_accettazione), 0, 0, 'L')
    pdf.ln(5)
    pdf.cell(90, 10, 'Codice ID campione/punto campionamento:', 0, 0, 'L')
    pdf.cell(120, 10, str(id_campione), 0, 0, 'L')
    pdf.ln(5)
    pdf.cell(90, 10, 'Descrizione campione analizzato:', 0, 0, 'L')
    pdf.cell(120, 10, str(descrizione_campione), 0, 0, 'L')
    pdf.ln(5)
    pdf.cell(90, 10, 'Data prelievo:', 0, 0, 'L')
    pdf.cell(120, 10, str(data_prelievo), 0, 0, 'L')
    pdf.cell(90, 10, 'Data ricevimento campione:', 0, 0, 'L')
    pdf.cell(120, 10, str(data_accettazione), 0, 0, 'L')
    pdf.ln(5)
    pdf.cell(90, 10, 'Operatore:', 0, 0, 'L')
    pdf.cell(120, 10, str(operatore_analisi), 0, 0, 'L')
    pdf.ln(5)
    pdf.cell(90, 10, 'Data inizio-fine analisi:', 0, 0, 'L')
    pdf.cell(120, 10, str(data_inizio_analisi) +
             '-'+str(data_fine_analisi), 0, 0, 'L')
    pdf.ln(5)
    pdf.cell(120, 10, 'Risultati:', 0, 0, 'L')
    pdf.ln(10)

    # header table risultati
    pdf.set_left_margin(20)
    pdf.set_text_color(0, 0, 0)  # black
    pdf.set_font('arial', '', 8)
    pdf.cell(60, 10, 'ID CAMPIONE', 1, 0, 'C')
    pdf.cell(60, 10, 'IDENTIFICAZIONE*', 1, 1, 'C')
    pdf.cell(60, 10, str(id_campione), 1, 0, 'C')
    pdf.cell(60, 10, str(identificazione), 1, 1, 'C')
    pdf.set_font('arial', 'I', 8)
    pdf.cell(60, 10, '* Mediante VITEK® 2 Compact, bioMérieux')

    # nota post tabella classe
    pdf.set_left_margin(10)
    pdf.set_font('arial', '', 10)
    pdf.cell(0, 0, '', 0, 1, 'C')
    pdf.ln(20)
    pdf.cell(
        0, 10, 'Note: '+note, 0, 1, 'L')
    pdf.ln(20)
    pdf.cell(
        0, 10, 'prof. Stefano Tardivo', 0, 0, 'R')
    pdf.ln(3)
    pdf.set_font('arial', 'I', 8)
    pdf.cell(0, 10, 'il presente documento è firmato digitalmente', 0, 1, 'R')

    # firma e terminazione documento
    # pdf.ln(9)
    pdf.set_text_color(0, 0, 0)  # black
    pdf.set_font('arial', 'I', 10)
    pdf.cell(
        0, 10, "________________________________________________________________________________________________", 0, 1, 'L')
    pdf.cell(0, 10, 'MR 32 rev. 1 - Pag 1 a 1', 0, 1, 'R')
    pdf.set_font('arial', '', 10)
    pdf.cell(0, 10, 'Laboratorio di Igiene', 0, 0, 'L')
    pdf.ln(4)
    pdf.cell(0, 10, 'Responsabile: prof. Stefano Tardivo', 0, 0, 'L')
    pdf.ln(4)
    pdf.set_font('arial', 'I', 10)
    pdf.cell(0, 10, 'Istituti Biologici - Blocco B - Strade le Grazie, 8 - 37134 Verona | T: +39 045 802 7659-7631', 0, 0, 'L')
    pdf.ln(4)
    pdf.cell(0, 10, 'laboratiorio.igiene@ateneo.univr.it | silvia.sembeni@univr.it | morena.nicolis@univr.it', 0, 0, 'L')

    pdf.output('documenti_referti/referto_' +
               str(id_accettazione).upper()+'_' +
               str(id_campione).upper()+'_identificazione.pdf', 'F')

    return('referto_'+str(id_accettazione).upper()+'_' +
           str(id_campione).upper()+' stampato con successo')


def stampa_referto(id_accettazione, id_campione, unita_operativa, data_prelievo, data_accettazione, rapporto_di_prova, descrizione_campione, operatore_prelievo_campione, operatore_analisi, data_inizio_analisi, data_fine_analisi, ufc_batteri, ufc_miceti, identificazione, note):
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.set_margins(10, 10, 10)
    pdf.image('assets/logo-univr.png', w=70, x=10)
    # pdf.image('assets/logo-dip-diagnostica.png', type='PNG', w=100, x=120)
    # pdf.ln(2)
    # set color and for grey titles
    # set color and for grey titles
    pdf.set_font('arial', 'I', 12)
    pdf.cell(0, 0, '', 0, 1, 'C')
    pdf.set_font('arial', 'I', 12)
    pdf.set_text_color(220, 220, 220)  # grey
    # pdf.cell(12)
    pdf.cell(0, 10, "STRUTTURA", 0, 0, 'L')
    pdf.ln(5)
    # set color and for for main text
    pdf.set_text_color(0, 0, 0)  # black
    pdf.set_font('arial', '', 12)
    pdf.cell(150, 10, "LABORATORIO DI IGIENE", 0, 0, 'L')
    pdf.cell(20, 10, 'MR44', 0, 0, 'L')
    pdf.ln(6)
    # set color for documento
    pdf.set_font('arial', 'I', 12)
    pdf.set_text_color(220, 220, 220)  # grey
    pdf.cell(140, 10, "DOCUMENTO", 0, 0, 'L')
    pdf.set_font('arial', 'I', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, 'Data di Emissione 03.04.2020', 0, 0, 'L')
    pdf.ln(5)
    pdf.set_text_color(0, 0, 0)  # black
    pdf.set_font('arial', '', 12)
    pdf.cell(140, 10, "REFERTO CONTROLLO MICROBIOLOGICO PO25", 0, 0, 'L')
    pdf.set_font('arial', 'I', 10)
    pdf.cell(0, 10, 'Indice di Revisione 1', 0, 0, 'L')
    pdf.ln(10)
    pdf.set_font('arial', '', 12)
    stringa_campionamento = "Controllo microbiologico dell'aria e delle superfici di laboratorio\nsoggetti a lavorazioni speciali (banca del cordone-lab. procreazione assistita, farmacia)"
    pdf.write(5, 'Rif. PO25'+' "'+stringa_campionamento+'"')
    pdf.ln(10)

    # tabella prova
    pdf.set_text_color(0, 0, 0)  # black
    pdf.set_font('arial', '', 10)
    pdf.cell(90, 10, 'Rapporto di prova n°:', 0, 0, 'L')
    pdf.cell(120, 10, str(rapporto_di_prova), 0, 0, 'L')
    pdf.ln(5)
    pdf.cell(90, 10, 'Modulo campionamento-accettazione n°:', 0, 0, 'L')
    pdf.cell(120, 10, str(id_accettazione), 0, 0, 'L')
    pdf.ln(5)
    pdf.cell(90, 10, 'Codice ID campione/punto campionamento:', 0, 0, 'L')
    pdf.cell(120, 10, str(id_campione), 0, 0, 'L')
    pdf.ln(5)
    pdf.cell(90, 10, 'Descrizione campione analizzato:', 0, 0, 'L')
    pdf.cell(120, 10, str(descrizione_campione), 0, 0, 'L')
    pdf.ln(5)
    pdf.cell(90, 10, 'Data prelievo:', 0, 0, 'L')
    pdf.cell(120, 10, str(data_prelievo), 0, 0, 'L')
    pdf.cell(90, 10, 'Data ricevimento campione:', 0, 0, 'L')
    pdf.cell(120, 10, str(data_accettazione), 0, 0, 'L')
    pdf.ln(5)
    pdf.cell(90, 10, 'Prelevatore:', 0, 0, 'L')
    pdf.cell(120, 10, str(operatore_prelievo_campione), 0, 0, 'L')
    pdf.ln(5)
    pdf.cell(90, 10, 'Data inizio-fine analisi:', 0, 0, 'L')
    pdf.cell(120, 10, str(data_inizio_analisi) +
             '-'+str(data_fine_analisi), 0, 0, 'L')
    pdf.ln(5)
    pdf.cell(120, 10, 'Risultati:', 0, 0, 'L')
    pdf.ln(10)

    # header table risultati
    pdf.set_left_margin(20)
    pdf.set_text_color(0, 0, 0)  # black
    pdf.set_font('arial', '', 10)
    pdf.cell(60, 10, 'ID CAMPIONE', 1, 0, 'C')
    pdf.cell(50, 5, 'UFC ', 'TLR', 0, 'C')
    pdf.cell(50, 5, 'UFC ', 'TLR', 1, 'C')
    pdf.cell(60, 5, '', 0, 0)
    pdf.set_font('arial', 'I', 6)
    pdf.cell(50, 5, 'piastra 90 Ø 90mm / <4 ore (batteri)', 'LR', 0, 'C')
    pdf.cell(50, 5, 'piastra 90 Ø 90mm / <4 ore (miceti)', 'LR', 1, 'C')
    # risultati
    pdf.set_font('arial', '', 8)
    pdf.cell(60, 10, str(id_campione), 1, 0, 'C')
    pdf.cell(50, 10, str(ufc_batteri), 1, 0, 'C')
    pdf.cell(50, 10, str(ufc_miceti), 1, 0, 'C')
    pdf.ln(7)
    pdf.set_font('arial', '', 8)
    pdf.cell(0, 10, 'n.r.*: non rivelato, nessun sviluppo o < 1 UFC', 0, 0, 'L')

    pdf.set_left_margin(10)
    pdf.ln(9)
    pdf.set_font('arial', '', 10)
    pdf.cell(
        0, 10, 'Valori di riferimento secondo doc. ANNEX 1 2008 (e successive edizioni):', 0, 1, 'L')
    pdf.set_left_margin(20)
    pdf.cell(30, 10, 'CLASSE', 1, 0, 'C')
    pdf.cell(30, 5, 'ARIA', 'LRT', 0, 'C')
    pdf.cell(30, 5, 'ARIA', 'LRT', 0, 'C')
    pdf.cell(30, 5, 'SUPERFICI', 'LRT', 0, 'C')
    pdf.cell(30, 5, 'IMPRONTE', 'LRT', 1, 'C')
    pdf.set_font('arial', 'I', 6)
    pdf.cell(30, 5, '', 0, 0, 'C')
    pdf.cell(30, 5, '(UFC/m³)', 'LR', 0, 'C')
    pdf.cell(30, 5, 'UFC/piastra Ø 90mm / <4 ore', 'LR', 0, 'C')
    pdf.cell(30, 5, 'UFC/piastra Ø 55mm', 'LR', 0, 'C')
    pdf.cell(30, 5, 'UFC/guanto', 'LR', 1, 'C')

    # classe A
    pdf.set_font('arial', 'I', 10)
    pdf.cell(30, 5, 'A', 1, 0, 'C')
    pdf.cell(30, 5, '<1', 1, 0, 'C')
    pdf.cell(30, 5, '<1', 1, 0, 'C')
    pdf.cell(30, 5, '<1', 1, 0, 'C')
    pdf.cell(30, 5, '<1', 1, 1, 'C')
    # classe B
    pdf.set_font('arial', 'I', 10)
    pdf.cell(30, 5, 'B', 1, 0, 'C')
    pdf.cell(30, 5, '10', 1, 0, 'C')
    pdf.cell(30, 5, '5', 1, 0, 'C')
    pdf.cell(30, 5, '5', 1, 0, 'C')
    pdf.cell(30, 5, '5', 1, 1, 'C')
    # classe C
    pdf.set_font('arial', 'I', 10)
    pdf.cell(30, 5, 'C', 1, 0, 'C')
    pdf.cell(30, 5, '100', 1, 0, 'C')
    pdf.cell(30, 5, '25', 1, 0, 'C')
    pdf.cell(30, 5, '25', 1, 0, 'C')
    pdf.cell(30, 5, '', 1, 1, 'C')
    # classe D
    pdf.set_font('arial', 'I', 10)
    pdf.cell(30, 5, 'D', 1, 0, 'C')
    pdf.cell(30, 5, '200', 1, 0, 'C')
    pdf.cell(30, 5, '100', 1, 0, 'C')
    pdf.cell(30, 5, '50', 1, 0, 'C')
    pdf.cell(30, 5, '', 1, 1, 'C')

    # nota post tabella classe
    pdf.set_left_margin(10)
    pdf.set_font('arial', '', 10)
    pdf.cell(0, 0, '', 0, 1, 'C')
    pdf.cell(
        0, 10, 'Osservazione microscopica:', 0, 0, 'L')
    pdf.ln(12)
    pdf.cell(
        0, 10, 'Note: '+note, 0, 1, 'L')
    pdf.ln(20)
    pdf.cell(
        0, 10, 'prof. Stefano Tardivo', 0, 0, 'R')
    pdf.ln(3)
    pdf.set_font('arial', 'I', 8)
    pdf.cell(0, 10, 'il presente documento è firmato digitalmente', 0, 1, 'R')

    # firma e terminazione documento
    # pdf.ln(9)
    pdf.set_text_color(0, 0, 0)  # black
    pdf.set_font('arial', 'I', 10)
    pdf.cell(
        0, 10, "________________________________________________________________________________________________", 0, 1, 'L')
    pdf.cell(0, 10, 'MR 32 rev. 1 - Pag 1 a 1', 0, 1, 'R')
    pdf.set_font('arial', '', 10)
    pdf.cell(0, 10, 'Laboratorio di Igiene', 0, 0, 'L')
    pdf.ln(4)
    pdf.cell(0, 10, 'Responsabile: prof. Stefano Tardivo', 0, 0, 'L')
    pdf.ln(4)
    pdf.set_font('arial', 'I', 10)
    pdf.cell(0, 10, 'Istituti Biologici - Blocco B - Strade le Grazie, 8 - 37134 Verona | T: +39 045 802 7659-7631', 0, 0, 'L')
    pdf.ln(4)
    pdf.cell(0, 10, 'laboratiorio.igiene@ateneo.univr.it | silvia.sembeni@univr.it | morena.nicolis@univr.it', 0, 0, 'L')

    pdf.output('documenti_referti/referto_' +
               str(id_accettazione).upper()+'_' +
               str(id_campione).upper()+'.pdf', 'F')

    stampa_referto_identificazione(id_accettazione, id_campione, unita_operativa, data_prelievo, data_accettazione, rapporto_di_prova,
                                   descrizione_campione, operatore_prelievo_campione, operatore_analisi, data_inizio_analisi, data_fine_analisi, identificazione, note)

    return('referto_'+str(id_accettazione).upper()+'_' +
           str(id_campione).upper()+' stampato con successo')


def stampa_accettazione(numero_modulo, unita_operativa, data_prelievo, data_accettazione, lista_id_campione, lista_descrizione_campione, operatore_prelievo):
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.set_margins(10, 10, 10)
    pdf.image('assets/logo-univr.png', w=70, x=10)
    # pdf.image('assets/logo-dip-diagnostica.png', type='PNG', w=100, x=120)
    # pdf.ln(2)
    # set color and for grey titles
    pdf.set_font('arial', 'I', 12)
    pdf.cell(0, 0, '', 0, 1, 'C')
    pdf.set_font('arial', 'I', 12)
    pdf.set_text_color(220, 220, 220)  # grey
    # pdf.cell(12)
    pdf.cell(0, 10, "STRUTTURA", 0, 0, 'L')
    pdf.ln(5)
    # set color and for for main text
    pdf.set_text_color(0, 0, 0)  # black
    pdf.set_font('arial', '', 12)
    pdf.cell(150, 10, "LABORATORIO DI IGIENE", 0, 0, 'L')
    pdf.cell(20, 10, 'MR32', 0, 0, 'L')
    pdf.ln(6)
    # set color for documento
    pdf.set_font('arial', 'I', 12)
    pdf.set_text_color(220, 220, 220)  # grey
    pdf.cell(140, 10, "DOCUMENTO", 0, 0, 'L')
    pdf.set_font('arial', 'I', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, 'Data di Emissione 01.10.2018', 0, 0, 'L')
    pdf.ln(5)
    pdf.set_text_color(0, 0, 0)  # black
    pdf.set_font('arial', '', 12)
    pdf.cell(140, 10, "MODULO CAMPIONAMENTO - ACCETTAZIONE CAMPIONE PO19", 0, 0, 'L')
    pdf.set_font('arial', 'I', 10)
    pdf.cell(0, 10, 'Indice di Revisione 1', 0, 0, 'L')
    pdf.ln(8)
    pdf.set_font('arial', '', 12)
    pdf.cell(140, 10, 'Rif. PO19 "Gestione dei campioni e delle prove"', 0, 0, 'L')
    pdf.ln(10)

    # text unità operativa
    pdf.set_text_color(0, 0, 0)  # black
    pdf.set_font('arial', '', 14)
    pdf.cell(0, 10, 'Unità Operativa: '+str(unita_operativa), 0, 1, 'L')
    pdf.ln(2)

    # tabella accettazione
    pdf.set_text_color(0, 0, 0)  # black
    pdf.set_font('arial', '', 12)
    pdf.cell(70, 10, 'Numero Modulo', 'LTB', 0, 'L')
    pdf.set_font('arial', '', 12)
    pdf.cell(120, 10, str(numero_modulo), 'LTB', 0, 'C')
    pdf.set_font('arial', 'I', 6)
    pdf.cell(0, 10, '(compila LAB IGIENE)', 'TRB', 1, 'R')
    pdf.set_font('arial', '', 12)
    pdf.cell(70, 10, 'Data Prelievo/Accettazione', 1, 0, 'L')
    pdf.cell(60, 10, str(data_prelievo), 'LTB', 0, 'L')
    pdf.cell(60, 10, str(data_accettazione), 'LTB', 0, 'L')
    pdf.set_font('arial', 'I', 6)
    pdf.cell(0, 10, '(compila LAB IGIENE)', 'TRB', 1, 'R')
    pdf.set_font('arial', '', 12)
    pdf.cell(70, 10, 'Firma consegna/ricezione', 1, 0, 'L')
    pdf.cell(60, 10, '', 'LTB', 0, 'C')
    pdf.cell(60, 10, '', 'LTB', 0, 'C')
    pdf.set_font('arial', 'I', 6)
    pdf.cell(0, 10, '(compila LAB IGIENE)', 'RB', 1, 'R')
    pdf.ln(5)

    # tabella campionamento
    pdf.set_font('arial', 'I', 8)
    pdf.cell(80, 10, 'ID CAMPIONE', 1, 0, 'C')
    pdf.cell(50, 10, 'DESCRIZIONE CAMPIONE', 1, 0, 'C')
    pdf.cell(60, 5, 'OPERATORE PRELIEVO', 'LRT', 1, 'C')
    pdf.set_font('arial', 'I', 6)
    pdf.cell(130, 10, '', 0, 0, 'C')
    pdf.cell(60, 5, '(NOME e COGNOME)', 'R', 1, 'C')
    # creazione tabella accettazione campioni
    pdf.set_font('arial', 'I', 7)
    for i in range(10):
        try:
            pdf.cell(80, 10, str(lista_id_campione[i]), 1, 0, 'C')
            pdf.cell(50, 10, str(lista_descrizione_campione[i]), 1, 0, 'C')
            pdf.cell(60, 10, operatore_prelievo, 1, 1, 'C')
        except:
            pdf.cell(80, 10, '', 1, 0, 'C')
            pdf.cell(50, 10, '', 1, 0, 'C')
            pdf.cell(60, 10, '', 1, 1, 'C')

    # firma e terminazione documento
    pdf.ln(5)
    pdf.set_text_color(0, 0, 0)  # black
    pdf.set_font('arial', '', 12)
    pdf.cell(0, 10, "Note:", 0, 1, 'L')
    pdf.set_text_color(0, 0, 0)  # black
    pdf.set_font('arial', 'I', 8)
    pdf.cell(
        0, 10, "________________________________________________________________________________________________", 0, 1, 'L')
    pdf.cell(0, 10, 'MR 32 rev. 1 - Pag 1 a 1', 0, 1, 'R')
    pdf.set_font('arial', '', 8)
    pdf.cell(0, 10, 'Laboratorio di Igiene', 0, 0, 'L')
    pdf.ln(4)
    pdf.cell(0, 10, 'Responsabile: prof. Stefano Tardivo', 0, 0, 'L')
    pdf.ln(4)
    pdf.set_font('arial', 'I', 8)
    pdf.cell(0, 10, 'Istituti Biologici - Blocco B - Strade le Grazie, 8 - 37134 Verona | T: +39 045 802 7659-7631', 0, 0, 'L')
    pdf.ln(4)
    pdf.cell(0, 10, 'laboratorio.igiene@ateneo.univr.it | silvia.sembeni@univr.it | morena.nicolis@univr.it', 0, 0, 'L')

    # save pdf to accettazione directory
    pdf.output('documenti_accettazione/accettazione_' +
               str(numero_modulo).upper()+'.pdf', 'F')

    return('accettazione_'+str(numero_modulo)+' stampata con successo')
