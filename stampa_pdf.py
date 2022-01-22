from fpdf import FPDF


def stampa_referto(id_accettazione, id_campione, unita_operativa, data_prelievo, data_accettazione, rapporto_di_prova, descrizione_campione, operatore_prelievo_campione, data_inizio_analisi, data_fine_analisi, risultato):
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.image('assets/logo-univr.png', w=70, x=10)
    # pdf.image('assets/logo-dip-diagnostica.png', type='PNG', w=100, x=120)
    # pdf.ln(2)
    # set color and for grey titles
    pdf.set_font('arial', 'I', 12)
    pdf.set_text_color(220, 220, 220)  # grey
    pdf.cell(12)
    pdf.cell(0, 10, "Struttura", 0, 0, 'C')
    pdf.ln(5)
    # set color and for for main text
    pdf.set_text_color(0, 0, 0)  # black
    pdf.set_font('arial', 'B', 12)
    pdf.cell(0, 10, "Laboratorio di Igiene", 0, 1, 'C')

    # tabella referto
    pdf.cell(50, 10, 'Rapporto di Prova', 1, 0, 'C')
    pdf.cell(100, 10, str(rapporto_di_prova), 1, 1, 'C')
    pdf.cell(50, 10, 'Numero Modulo', 1, 0, 'C')
    pdf.cell(100, 10, str(id_accettazione), 1, 1, 'C')
    pdf.cell(50, 10, 'Unità Operativa', 1, 0, 'C')
    pdf.cell(100, 10, str(unita_operativa), 1, 1, 'C')
    pdf.cell(50, 10, 'Data Prelievo', 1, 0, 'C')
    pdf.cell(100, 10, str(data_prelievo), 1, 1, 'C')
    pdf.cell(50, 10, 'Data Accettazione', 1, 0, 'C')
    pdf.cell(100, 10, str(data_accettazione), 1, 1, 'C')
    pdf.ln(5)

    # tabella campionamento
    pdf.cell(60, 10, 'ID CAMPIONE', 1, 0, 'C')
    pdf.cell(60, 10, 'DESCRIZIONE CAMPIONE', 1, 0, 'C')
    pdf.cell(60, 10, 'RISULTATO', 1, 1, 'C')
    # for i in range(len(lista_id_campione)):
    pdf.cell(60, 10, str(id_campione), 1, 0, 'C')
    pdf.cell(60, 10, str(descrizione_campione), 1, 0, 'C')
    pdf.cell(60, 10, str(risultato), 1, 1, 'C')

    # firma e terminazione documento
    pdf.ln(5)
    pdf.cell(60, 10, "Firma responsabile", 0, 1, 'C')
    # pdf.cell(-10)
    pdf.cell(100, 10, "________________________", 0, 0, 'L')

    pdf.output('documenti_referti/referto' +
               str(id_accettazione).upper()+'_' +
               str(id_campione).upper()+'.pdf', 'F')

    return('referto_'+str(id_accettazione).upper()+'_' +
           str(id_campione).upper()+' stampato con successo')


def stampa_accettazione(numero_modulo, unita_operativa, data_prelievo, data_accettazione, lista_id_campione, lista_descrizione_campione, lista_operatore_prelievo):
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.image('assets/logo-univr.png', w=70, x=10)
    # pdf.image('assets/logo-dip-diagnostica.png', type='PNG', w=100, x=120)
    # pdf.ln(2)
    # set color and for grey titles
    pdf.set_font('arial', 'I', 12)
    pdf.set_text_color(220, 220, 220)  # grey
    pdf.cell(12)
    pdf.cell(0, 10, "Struttura", 0, 0, 'C')
    pdf.ln(5)
    # set color and for for main text
    pdf.set_text_color(0, 0, 0)  # black
    pdf.set_font('arial', 'B', 12)
    pdf.cell(0, 10, "Laboratorio di Igiene", 0, 1, 'C')

    # tabella accettazione
    pdf.cell(50, 10, 'Numero Modulo', 1, 0, 'C')
    pdf.cell(100, 10, str(numero_modulo), 1, 1, 'C')
    pdf.cell(50, 10, 'Unità Operativa', 1, 0, 'C')
    pdf.cell(100, 10, str(unita_operativa), 1, 1, 'C')
    pdf.cell(50, 10, 'Data Prelievo', 1, 0, 'C')
    pdf.cell(100, 10, str(data_prelievo), 1, 1, 'C')
    pdf.cell(50, 10, 'Data Accettazione', 1, 0, 'C')
    pdf.cell(100, 10, str(data_accettazione), 1, 1, 'C')
    pdf.ln(5)

    # tabella campionamento
    pdf.cell(60, 10, 'ID CAMPIONE', 1, 0, 'C')
    pdf.cell(60, 10, 'DESCRIZIONE CAMPIONE', 1, 0, 'C')
    pdf.cell(60, 10, 'OPERATORE PRELIEVO', 1, 1, 'C')
    for i in range(len(lista_id_campione)):
        pdf.cell(60, 10, str(lista_id_campione[i]), 1, 0, 'C')
        pdf.cell(60, 10, str(lista_descrizione_campione[i]), 1, 0, 'C')
        pdf.cell(60, 10, str(lista_operatore_prelievo[i]), 1, 1, 'C')

    # firma e terminazione documento
    pdf.ln(5)
    pdf.cell(60, 10, "Firma responsabile", 0, 1, 'C')
    # pdf.cell(-10)
    pdf.cell(100, 10, "________________________", 0, 0, 'L')

    pdf.output('documenti_accettazione/accettazione_' +
               str(numero_modulo).upper()+'.pdf', 'F')

    return('accettazione_'+str(numero_modulo)+' stampata con successo')
