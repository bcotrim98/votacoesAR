# This Python project obtains, processes and publishes on social media (BlueSky,
# in this case) the various votes casted for the different proposals on the
# Portuguese Assembly by the different elected parties and deputees
# 
# Bruno Cotrim, 24/02/2026

import readPDF

fname = 'documentos/XVII_1_48_2026-01-23_ResultadoVotacoes_2026-01-23 - Versao 3.pdf'
# fname = 'documentos/XVII_1_51_2026-02-03_ResultadoVotacoes_2026-01-30.pdf'

props = readPDF.readFile(fname)
