import pandas as pd
import matplotlib
from pylab import title, figure, xlabel, ylabel, xticks, bar, legend, axis, savefig
from fpdf import FPDF

matplotlib.use('Agg')


pdf = FPDF('P', 'mm', 'A4')
pdf.add_page()
pdf.set_xy(0, 0)
# set color and for grey titles
pdf.set_font('arial', 'I', 12)
pdf.set_text_color(220, 220, 220)  # grey
pdf.cell(200, 10, "Struttura", 0, 0, 'C')
pdf.ln(5)
pdf.cell(-10)
# set color and for for main text
pdf.set_text_color(0, 0, 0)  # black
pdf.set_font('arial', 'B', 12)
pdf.cell(200, 10, "Laboratorio di Igiene", 0, 2, 'C')
pdf.cell(10)
pdf.cell(50, 10, 'Numero Modulo', 1, 0, 'C')
pdf.cell(100, 10, '', 1, 1, 'C')
pdf.cell(50, 10, 'Unità Operativa', 1, 0, 'C')
pdf.cell(100, 10, '', 1, 1, 'C')
pdf.cell(50, 10, 'Data Prelievo', 1, 0, 'C')
pdf.cell(100, 10, '', 1, 1, 'C')
pdf.cell(50, 10, 'Data Accettazione', 1, 0, 'C')
pdf.cell(100, 10, '', 1, 1, 'C')
pdf.ln(5)
pdf.cell(60, 10, 'ID CAMPIONE', 1, 0, 'C')
pdf.cell(60, 10, 'DESCRIZIONE CAMPIONE', 1, 0, 'C')
pdf.cell(60, 10, 'OPERATORE PRELIEVO', 1, 1, 'C')
for i in range(9):
    pdf.cell(60, 10, '', 1, 0, 'C')
    pdf.cell(60, 10, '', 1, 0, 'C')
    pdf.cell(60, 10, '', 1, 1, 'C')

pdf.output('test.pdf', 'F')
