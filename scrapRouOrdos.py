### when running,change name of the two csv where the data will be scrapped in line 10 and 64

import requests
from bs4 import BeautifulSoup
from csv import DictWriter

def getordodata(sourcePath):
    """
    scrap for tile or ordonance, date or ordonance, status ordo, law and date of law that approves/rejects the oroance
    Appends data to list and writes list to .csv (ordos3jan.csv)

    """

    baseUrl = 'http://www.cdep.ro/pls/legis/'

    all_laws = []

    res = requests.get(f'{baseUrl}{sourcePath}')
    soup = BeautifulSoup(res.text, features="html")
    print('inside getordodata')
    for a in soup.find_all('a', href=True):
        link_ordo = a['href']
        res_ordo = requests.get(f'{baseUrl}{link_ordo}')
        soup_ordo = BeautifulSoup(res_ordo.text, 'html.parser')

        title = soup_ordo.find('title').get_text() ## title of the ordonanta
        date_ordo = soup_ordo.find_all(lambda e: e.name == 'b' and 'Ordonanţă' in e.text) ## date of the ordonanta

        def getStatus():
            if 'Functie pasiva:' not in soup_ordo.get_text():
                status1 = "uitata"
            else:
                statusTable = soup_ordo.find(attrs={'border':'0', 'cellspacing':'0', 'cellpadding':'2', 'width':"100%"})
                if statusTable:
                    status1 = statusTable.find_all(attrs={'align':"right", 'bgcolor':"#e0e0e0"})[2].get_text()
               
            return status1

        ## get name of law approving the ordo
        def getLawApprov():
            for tr in soup_ordo.find_all(lambda e: e.name == 'tr' and ('Aprobata' in e.text or 'Respinsa' in e.text)):
                linkToLawApproving = tr.find('a')['href']
                res_law = requests.get(f'{baseUrl}{linkToLawApproving}')
                soup_law = BeautifulSoup(res_law.text, 'html.parser')
                title_law = soup_law.find('title').get_text()
                
                return title_law

        def getDateLawApprov():
            for tr in soup_ordo.find_all(lambda e: e.name == 'tr' and ('Aprobata' in e.text or 'Respinsa' in e.text)):
                linkToLawApproving = tr.find('a')['href']
                res_law = requests.get(f'{baseUrl}{linkToLawApproving}')
                soup_law = BeautifulSoup(res_law.text, 'html.parser')
                date_law = soup_law.find(lambda e: e.name == 'b' and 'Lege' in e.text)
               
                return date_law

        all_laws.append({'title':title, 'date_ordo':date_ordo, 'status':getStatus(), 'law':getLawApprov(), 'date_law':getDateLawApprov()})
   
    print(len(all_laws))

    ## write scrapped data to csv as dict

    with open('rouOrdos3jan.csv', 'a') as csv_file:
        headers = ['title', 'date_ordo', 'status', 'law', 'date_law']
        csv_writer = DictWriter(csv_file, fieldnames=headers)
        csv_writer.writeheader()
        for law in all_laws:
            csv_writer.writerow(law)


def getAllLinks():
    
    """
    get all "next" pages starting from the main ordonante pages ("sourcePathsMAIN")
    add "next pages" to the list of pages ("sourcePathsMAIN") to be subsequently scrapped

    """

    baseUrl = 'http://www.cdep.ro/pls/legis/'
   
    sourcePaths = ['legis_pck.lista_anuala?an=1992&emi=3&tip=18&rep=0', 
                       'legis_pck.lista_anuala?an=1993&emi=3&tip=18&rep=0', 
                       'legis_pck.lista_anuala?an=1994&emi=3&tip=18&rep=0', 
                       'legis_pck.lista_anuala?an=1995&emi=3&tip=18&rep=0', 
                       'legis_pck.lista_anuala?an=1996&emi=3&tip=18&rep=0', 
                       'legis_pck.lista_anuala?an=1997&emi=3&tip=18&rep=0', 
                       'legis_pck.lista_anuala?an=1998&emi=3&tip=18&rep=0', 
                       'legis_pck.lista_anuala?an=1999&emi=3&tip=18&rep=0&nrc=1', 
                       'legis_pck.lista_anuala?an=2000&emi=3&tip=18&rep=0&nrc=1',
                       'legis_pck.lista_anuala?an=2001&emi=3&tip=18&rep=0&nrc=1', 
                       'legis_pck.lista_anuala?an=2002&emi=3&tip=18&rep=0&nrc=1', 
                       'legis_pck.lista_anuala?an=2003&emi=3&tip=18&rep=0&nrc=1', 
                       'legis_pck.lista_anuala?an=2004&emi=3&tip=18&rep=0&nrc=1',
                       'legis_pck.lista_anuala?an=2005&emi=3&tip=18&rep=0&nrc=1', 
                       'legis_pck.lista_anuala?an=2006&emi=3&tip=18&rep=0&nrc=1', 
                       'legis_pck.lista_anuala?an=2007&emi=3&tip=18&rep=0&nrc=1',
                       'legis_pck.lista_anuala?an=2008&emi=3&tip=18&rep=0&nrc=1', 
                       'legis_pck.lista_anuala?an=2009&emi=3&tip=18&rep=0&nrc=1', 
                       'legis_pck.lista_anuala?an=2010&emi=3&tip=18&rep=0&nrc=1', 
                       'legis_pck.lista_anuala?an=2011&emi=3&tip=18&rep=0&nrc=1', 
                       'legis_pck.lista_anuala?an=2012&emi=3&tip=18&rep=0', 
                       'legis_pck.lista_anuala?an=2013&emi=3&tip=18&rep=0&nrc=1',
                       'legis_pck.lista_anuala?an=2014&emi=3&tip=18&rep=0', 
                       'legis_pck.lista_anuala?an=2015&emi=3&tip=18&rep=0', 
                       'legis_pck.lista_anuala?an=2016&emi=3&tip=18&rep=0', 
                       'legis_pck.lista_anuala?an=2017&emi=3&tip=18&rep=0', 
                       'legis_pck.lista_anuala?an=2018&emi=3&tip=18&rep=0&nrc=1', 
                       'legis_pck.lista_anuala?an=2019&emi=3&tip=18&rep=0', 
                       'legis_pck.lista_anuala?an=2020&emi=3&tip=18&rep=0&nrc=1', 
                       'legis_pck.lista_anuala?an=1992&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=1993&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=1994&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=1995&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=1996&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=1997&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=1998&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=1999&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=2000&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=2001&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=2002&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=2003&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=2004&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=2005&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=2006&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=2007&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=2008&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=2009&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=2010&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=2011&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=2012&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=2013&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=2014&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=2015&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=2016&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=2017&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=2018&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=2019&emi=3&tip=13&rep=0', 
                       'legis_pck.lista_anuala?an=2020&emi=3&tip=13&rep=0']  


    print('getting page links')
    for path in sourcePaths:
        res = requests.get(f'{baseUrl}{path}')
        soup = BeautifulSoup(res.text, "html.parser")

        next_btn = soup.find("p",class_="headline").find("table", {"align":"center"})
        if next_btn:
            anchor = next_btn.find_all("td")[-1].find("a")
            if anchor: 
                ordo100to199 = anchor['href']
                sourcePaths.append(ordo100to199)

    return sourcePaths

def finalfunc():
    """
    
    scrap each page in the sourcePaths list
    
    """

    for page in getAllLinks():
        getordodata(page)
        print(page)
    print('end')
# finalfunc()