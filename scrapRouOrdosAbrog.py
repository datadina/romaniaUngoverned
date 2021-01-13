### when running,change name of the  csv files 

### clean the scrapped data and get list of ordos not approved, rejected or forgotten ("uitata")

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd 
import re
import requests
from bs4 import BeautifulSoup
from csv import DictWriter
import matplotlib.dates as mdates
from datetime import datetime
 

pd.set_option("display.max_rows", None, "display.max_columns", 1000, 'max_colwidth', 30, 'display.width', 1000)
df = pd.read_csv("rouOrdos3jan.csv", index_col=False)
# print(df.head())

## delete rows with only title, law, date
df = df[df.title != 'title']
df = df[~df['title'].str.contains('ORDONANŢE DE URGENŢĂ emise în anul')]
df = df[~df['title'].str.contains('ORDONANŢE emise în anul')]
# print(df.head())

## cleaning on title column, date column, law column, status column (delete spaces, brackets, other symbols)
df['title'] = df['title'].str.replace("\('", "").str.replace("',\)", "").str.replace(r"(\\t)", "").str.replace(r'\("', '').str.replace("\s\s+", " ") 
df['date_ordo'] = df['date_ordo'].str.replace("\[<b>", "").str.replace("<\/b>\]", "")   
df['law'] = df['law'].str.replace("\s\s+", " ") ## extra spaces
df['status'] = df['status'].str.replace("\\n", "").str.replace('Aprobatacu modificariprin:', "Aprobata").str.replace('Aprobataprin:', "Aprobata").str.replace('Respinsaprin:', 'Respinsa')
# print(df.head())

### split df (all the ordonances) into 1. respAprobUitate (those either aprobate/approved or respinse/rejected) and 
### 2. notRespAprobUitate to be further scrapped for status (abrogate prin oug/abrogated through another ordonance or abrogate prin lege / abrogated through law)
statusnot = ['Respinsa', 'Aprobata', 'Uitata']
respAprobUitate = df[df.status.isin(statusnot)]
notRespAprobUitate = df[~df.status.isin(statusnot)]

### ordonante further to be scrapped, made to list for func below doing the scrapping 
listnotRespAprobUitate = notRespAprobUitate['date_ordo'].tolist()
# print(listnotRespAprobUitate)

def getordodataABROG(sourcePath):

    """
    for every page containing ordonances ("sourcePaths"), check every ordonance if
    is included in listnotRespAprobUitate (ordonances not approved, rejected, or forgotten)
    scrap again for data (the pages for this ordonances do not have the same headers as 
    the approved/rejected/forgotten ordonances, though some might still be forgotten) 

    append scrapped data to list and writes list to roOrdosAbrog3jan.csv
    
    """

    baseUrl = 'http://www.cdep.ro/pls/legis/'


    res = requests.get(f'{baseUrl}{sourcePath}')
    soup = BeautifulSoup(res.text, features="lxml")
    print('inside getordodata')
    
    abrogLawOrdin = []

  
    for a in soup.find_all('a', href=True):
        link_ordo = a['href']
        res_ordo = requests.get(f'{baseUrl}{link_ordo}')
        soup_ordo = BeautifulSoup(res_ordo.text, 'html.parser')


        for elem in listnotRespAprobUitate: ## for each ordo in the list created above, check for status 
            if soup_ordo.find_all(lambda e: e.name == 'b' and elem in e.text):
                
                title = soup_ordo.find('title').get_text()
                date_ordo = soup_ordo.find_all(lambda e: e.name == 'b' and 'Ordonanţă' in e.text)
                
                title_law = 'placeholder'
                date_law = 'placeholder'
                status = 'placeholder'
            
                if soup_ordo.find(lambda e: e.name == 'tr' and 'Modificată' in e.text): ## if "modificata" means the parliament did not consider it, the gov did not yet take it back
                    status = 'uitata'

                trs = soup_ordo.find(lambda e: e.name == 'tr' and 'Abrogată' in e.text) ## if "abrogata" in the page, can either be through law or another ordonanta
                if trs:
                    tdlawordi = trs.find_all('td')[1].text ## location of text indicating if abrogata through law or another ordonanta
                 
                    if 'L.' in tdlawordi:
                        linkToLawAbrogata = trs.find_all('td')[1].find('a')['href']
                        res_law = requests.get(f'{baseUrl}{linkToLawAbrogata}')
                        soup_law = BeautifulSoup(res_law.text, 'html.parser')

                        title_law = soup_law.find('title').get_text()
                        date_law = soup_law.find(lambda e: e.name == 'b' and 'Lege' in e.text)
                        status = 'abrogata prin lege'

                    
                    if 'O.U.G.' in tdlawordi or 'O.G.' in tdlawordi:
                        linkToLawAbrogata = trs.find_all('td')[1].find('a')['href']
                        res_law = requests.get(f'{baseUrl}{linkToLawAbrogata}')
                        soup_law = BeautifulSoup(res_law.text, 'html.parser')
                        
                        title_law = soup_law.find('title').get_text()
                        date_law = soup_law.find(lambda e: e.name == 'b' and ('O.U.G.' in e.text or 'O.G.' in e.text or 'Ordonanţă' in e.text))
                        status = 'abrogata prin og'
                        

                abrogLawOrdin.append({'title':title, 'date_ordo':date_ordo, 'status':status, 'law':title_law, 'date_law':date_law})
               

    with open('roOrdosAbrog3jan.csv', 'a') as csv_file:
        headers = ['title', 'date_ordo', 'status', 'law', 'date_law']
        csv_writer = DictWriter(csv_file, fieldnames=headers)
        csv_writer.writeheader()
        for law in abrogLawOrdin:
            csv_writer.writerow(law)

    return abrogLawOrdin

from scrapRouOrdos import getAllLinks

def finalfunc():

    """
    for every page containing ordonances, rescraps  
    
    """

    # for page in getAllLinks():
    for page in getAllLinks():
        print(page) ## for debugging when one page would be slightly different and break the code
        print(getordodataABROG(page))
    
# finalfunc()

## reads the roOrdosAbrog3jan.csv file as dataframe "abrog" and 
## concatenates it with the existing respAprobUitate into final
# finalOrdos = contains all romanian ordonances

# pd.set_option("display.max_rows", None, "display.max_columns", None, 'max_colwidth', 45)
abrog = pd.read_csv("roOrdosAbrog3jan.csv", index_col=False) ### read re-scrapped ordonante
abrog = abrog[abrog.title != 'title']

# print(abrog.head())

finalOrdos = pd.concat([respAprobUitate, abrog], ignore_index=True) ### merge the 2 dataframes, aprobate, respinse, uitate, re scrapped

finalOrdos['law'] = finalOrdos['law'].str.replace("\s\s+", " ") ### extra spaces
finalOrdos['date_law'] = finalOrdos['date_law'].str.replace("<b>", "").str.replace("<\/b>", "").str.replace("(Ordonanţă nr.)(\d{1,3})( din )", "").str.replace("(Ordonanţă de Urgenţă nr.)(\d{1,3})( din )", "").str.replace("(Lege nr.)(\d{1,3})( din )", "").str.replace("\s\s+", " ") 
finalOrdos['date_ordo'] = finalOrdos['date_ordo'].str.replace("\[<b>", "").str.replace("<\/b>\]", "").str.replace("(Ordonanţă nr.)(\d{1,3})( din )", "").str.replace("(Ordonanţă de Urgenţă nr.)(\d{1,3})( din )", "").str.replace("\s\s+", " ") 

# print(finalOrdos.head())