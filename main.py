# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 23:17:10 2020

@author: Christian
"""
"""
da fare:
    -inserisci EBIT/(Interest Expense), the bigger the better, ma sicuramente 
     non minore di 2
    -integrare Pandas
    -FARE MENU, PRIORITA ASSOLUTA
    -capire cosa puoi metterci di analisi dati
idee:
    -metterci qualche ordinamento
    -la possibilità di aggiungere su file un record con una nuova azione
        -mantenere l'ordine alfabetico
"""

from azioni_test import Stock

def stampaAzioni(azioni):
    for azione in azioni:
        azione.stampaInfo()

def stampaAzioniSuFile(azioni,file_path):
    str_parametri = "Azienda;nome;Prezzo;Fatturato (B);P/E;P/S;"
    str_parametri += "ROA (%);ROE (%);ROI (%);Debt/Eq;EPS past 5Y (%);Dividend;Beta\n"
    
    stringa = str_parametri
    for azione in azioni:
        stringa += azione.getCSV()
        stringa += "\n"

    fp = open(file_path,"w")
    fp.write(stringa)
    fp.close()

aziende = []
f = open("azioni.txt","r")
for azione in f:
    if azione[-1] == '\n':
        azione = azione[:-1]
    aziende.append(["",azione])
f.close()

azioni = []
for azienda in aziende:
    azioni.append(Stock(azienda[1]))
    azienda[0] = azioni[-1].azienda

for azione in azioni:
    soup = azione.getZuppa()
    azione.setStockFromSoup(soup)

good_stocks = []
for azione in azioni:
    if azione.isGoodStock():
        good_stocks.append(azione)

stampaAzioni(good_stocks)
stampaAzioni(azioni)

# stampaAzioniSuFile(azioni,"C:/Users/Christian/Desktop/prova.txt")
stampaAzioniSuFile(azioni,"C:/Users/Christian/Desktop/Azioni/fogli/stocks.csv")
stampaAzioniSuFile(good_stocks,"C:/Users/Christian/Desktop/Azioni/fogli/good_stocks.csv")
print("FINITO")
#https://finviz.com/quote.ashx?t=GOOGL
