### when running,change name of the  csv where the data will be scrapped in line 28

import requests
from bs4 import BeautifulSoup
import csv

def getordodata(sourcePath):
    """
    scrap the romanian parliament website for laws passed 1992-2020 and writes to csv
    """
    baseUrl = 'http://www.cdep.ro/pls/dic/legis_acte_parlam2015?cam=0&tip=1&an='
    res = requests.get(f'{baseUrl}{sourcePath}')
    soup = BeautifulSoup(res.text, features="html")
    body = soup.find('tbody')
    trs = body.find_all('tr')
    
    laws = []
    date_laws = []    
    for tr in trs:
        laws.append(tr.find_all("td")[2].text)
        date_laws.append(tr.find_all("td")[1].text)
        

    ### write scrapped data to csv as dict
    rows = zip(laws, date_laws)
    headers = ['law', 'date_law']

    with open('rouLaws3jan.csv', "a") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([header for header in headers])
        for row in rows:
            writer.writerow(row)


sourcePaths = [1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

def finalfunc():
    for page in sourcePaths:
        print(page)
        getordodata(page)
finalfunc()

