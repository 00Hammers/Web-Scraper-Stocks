from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs
import copy

def cutStrHead(str):
    return str[0:-1]

class Stock:
    azienda = ""
    nome = ""
    url = ""
    url_statements = ""
    prezzo = ""
    revenue = ""
    pe = ""
    ps = ""
    roa = ""
    roe = ""
    roi = ""
    deb_eq = ""
    growth_5y = ""
    dividend = ""
    beta = ""
    clean = False
    vincoli = {}
    
    def __init__(this,nome):
        vincoli = {"roa" : 0.0,
                   "roe" : 0.0,
                   "roi" : 0.0,
                   "den_eq" : 0.0,
                   "revenue" : 0.0}
        
        fp = open("vincoli.txt","r")
        
        for riga in fp:
            a = riga.split()
            vincoli[a[0]] = a[1]
            
        fp.close()
        
        this.vincoli = vincoli
        this.nome = nome
        this.url = "https://finviz.com/quote.ashx?t=" + nome
        this.url_statements = "https://finviz.com/quote.ashx?t=" + nome + "/financials"
    
    def stampaInfo(this):
        print("Azienda:             ",this.azienda)
        print("Prezzo:              ",this.prezzo)
        print("Fatturato:           ",this.revenue)
        print("P/E:                 ",this.pe)
        print("P/S:                 ",this.ps)
        print("ROA:                 ",this.roa)
        print("ROE:                 ",this.roe)
        print("ROI:                 ",this.roi)
        print("Debt/Eq:             ",this.deb_eq)
        print("EPS past 5 Years:    ",this.growth_5y)
        print("Dividend:            ",this.dividend)
        print("Beta:                ",this.beta)
        print()
    
    def getRecord(this):
        return (this.azienda,
                this.nome,
                this.url,
                this.url_statements,
                this.vincoli,
                this.prezzo,
                this.revenue,
                this.pe,
                this.ps,
                this.roa,
                this.roe,
                this.roi,
                this.deb_eq,
                this.growth_5y,
                this.dividend,
                this.beta)
    
    def getCSV(this):
        stringa = ""
        for item in this.getDatiPuliti().getRecord():
            if (type(item) is str and item[0:5] != "https") or type(item) is float:
                stringa += str(item) + ";"
        
        return stringa[:-1]
    
    def setStockFromList(azione,lista):
        azione.azienda = lista[0]
        azione.prezzo = lista[1]
        azione.revenue = lista[2]
        azione.pe = lista[3]
        azione.ps = lista[4]
        azione.roa = lista[5]
        azione.roe = lista[6]
        azione.roi = lista[7]
        azione.deb_eq = lista[8]
        azione.growth_5y = lista[9]
        azione.dividend = lista[10]
        azione.beta = lista[11]
    
    def getDatiPuliti(this):
        azione = copy.deepcopy(this)
        
        vals = [azione.azienda]
        x = ""
        for val in this.getRecord()[5:]:
            if val == "-":
                val = 0.0
            else:
                x = val[-1]
                if x == "B" or x == "M" or x == "%":
                    val = cutStrHead(val)
            
            val = float(val)
            
            if x == "M":
                val *= 0.001
            
            vals.append(val)
       
        azione.setStockFromList(vals)
        azione.clean = True

        return azione
    
    def isClean(this):
        return this.clean
    
    def isGoodStock(this):
        if this.isClean():
            azione = this
        else:
            azione = this.getDatiPuliti()
        
        flag = (azione.roa>=float(this.vincoli["roa"]))
        flag *= (azione.roe>=float(this.vincoli["roe"]))
        flag *= (azione.roi>=float(this.vincoli["roi"]))
        flag *= (azione.deb_eq<float(this.vincoli["deb_eq"]))
        flag *= (azione.revenue>=float(this.vincoli["revenue"]))

        return flag
    
    def setStockFromSoup(azione,soup):
        table_elements = ("Price","Sales","P/E","P/S","ROA","ROE","ROI","Debt/Eq","EPS past 5Y","Dividend","Beta")

        val = soup.find(id="ticker").findNext("b").text
        table_vals = [val]
        for key in table_elements:
            val = soup.find(text=key).findNext("b").text
            table_vals.append(val)
        
        azione.setStockFromList(table_vals)

    def getZuppa(azione):
        browser = wd.Chrome()
        browser.get(azione.url)
       
        content = browser.page_source
        
        browser.close()
        
        return bs(content,'html.parser')