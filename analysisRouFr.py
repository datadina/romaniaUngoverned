#### !!!! change "end" with date of scrapping line 10

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import matplotlib.dates as mdates
import re

end = pd.to_datetime('2021-01-3') ## to be changed with day doing the scrapping

### clean the scrapped data

roLaws = pd.read_csv("rouLaws3jan.csv", index_col=False) ### read laws
roLaws = roLaws[roLaws.law != 'law']
roLaws['date_law'] = roLaws['date_law'].str.replace("(\d{1,3})(\/)", "").str.replace(".", "-")

### turn date columns into time
roLaws['date_law'] = pd.to_datetime(roLaws['date_law'], format='%d-%m-%Y')#.dt.strftime('%d-%m-%Y'))
# print(roLaws.head())

#### laws devided into 8 parliaments
 
### get df containing laws passed until the end of the 1990-1992 rouParliament
rouParl1990to1992start = pd.to_datetime('1992-01-01')
rouParl1990to1992end = pd.to_datetime('1992-10-16')
mask1990to1992 = (roLaws['date_law'] > rouParl1990to1992start) & (roLaws['date_law'] <= rouParl1990to1992end)
rouParl1990to1992 = roLaws.loc[mask1990to1992].reset_index(drop=True)

# print('rouParl1990to1992')
# print(rouParl1990to1992.head())

### get df containing laws passed in the 1992-1996 rouParliament
rouParl1992to1996start = pd.to_datetime('1992-10-16')
rouParl1992to1996end = pd.to_datetime('1996-11-22')
mask1992to1996 = (roLaws['date_law'] > rouParl1992to1996start) & (roLaws['date_law'] <= rouParl1992to1996end)
rouParl1992to1996 = roLaws.loc[mask1992to1996].reset_index(drop=True)

# print(rouParl1992to1996)

### get df containing laws passed in the 1996-2000 rouParliament
rouParl1996to2000start = pd.to_datetime('1996-11-22')
rouParl1996to2000end = pd.to_datetime('2000-12-11')
mask1996to2000 = (roLaws['date_law'] > rouParl1996to2000start) & (roLaws['date_law'] <= rouParl1996to2000end)
rouParl1996to2000 = roLaws.loc[mask1996to2000].reset_index(drop=True)

# print(rouParl1996to2000)

### get df containing laws passed in the 2000 - 2004 rouParliament
rouParl2000to2004start = pd.to_datetime('2000-12-11')
rouParl2000to2004end = pd.to_datetime('2004-12-13')
mask2000to2004 = (roLaws['date_law'] > rouParl2000to2004start) & (roLaws['date_law'] <= rouParl2000to2004end)
rouParl2000to2004 = roLaws.loc[mask2000to2004].reset_index(drop=True)

# # print(rouParl2000to2004)

### get df containing laws passed in the 2004 - 2008 rouParliament
rouParl2004to2008start = pd.to_datetime('2004-12-13')
rouParl2004to2008end = pd.to_datetime('2008-12-15')
mask2004to2008 = (roLaws['date_law'] > rouParl2004to2008start) & (roLaws['date_law'] <= rouParl2004to2008end)
rouParl2004to2008 = roLaws.loc[mask2004to2008].reset_index(drop=True)

# print(rouParl2004to2008)

### get df containing laws passed in the 2008 - 2012 rouParliament
rouParl2008to2012start = pd.to_datetime('2008-12-15')
rouParl2008to2012end = pd.to_datetime('2012-12-19')
mask2008to2012 = (roLaws['date_law'] > rouParl2008to2012start) & (roLaws['date_law'] <= rouParl2008to2012end)
rouParl2008to2012 = roLaws.loc[mask2008to2012].reset_index(drop=True)

# print(rouParl2008to2012)

### get df containing laws passed in the 2012 - 2016 rouParliament
rouParl2012to2016start = pd.to_datetime('2012-12-19')
rouParl2012to2016end = pd.to_datetime('2016-12-20')
mask2012to2016 = (roLaws['date_law'] > rouParl2012to2016start) & (roLaws['date_law'] <= rouParl2012to2016end)
rouParl2012to2016 = roLaws.loc[mask2012to2016].reset_index(drop=True)

# print(rouParl2012to2016)

### get df containing laws passed in the 2016 - 2020 rouParliament
rouParl2016to2020start = pd.to_datetime('2016-12-20')
rouParl2016to2020end = end
mask2016to2020 = (roLaws['date_law'] > rouParl2016to2020start) & (roLaws['date_law'] <= rouParl2016to2020end)
rouParl2016to2020 = roLaws.loc[mask2016to2020].reset_index(drop=True)

# print(rouParl2016to2020)

### ROU ordos

from scrapRouOrdosAbrog import finalOrdos
roOrdo = finalOrdos

monthsRom = {'ianuarie':'January', 
             'februarie':'February',
             'martie':'March',
             'aprilie':'April',
             'mai':'May',
             'iunie':'June',
             'iulie':'July',
             'august':'August',
             'septembrie':'September',
             'octombrie':'October',
             'noiembrie':'November',
             'decembrie':'December'}

### change months from romanian to english in date of ordonanta column and date of law column
for monthro, montheng in monthsRom.items():
    roOrdo.date_ordo = roOrdo.date_ordo.str.replace(monthro, montheng)
    roOrdo.date_law = roOrdo.date_law.str.replace(monthro, montheng)

### turn date columns into time
roOrdo['date_ordo'] = pd.to_datetime(roOrdo['date_ordo'])
roOrdo['date_law'] = pd.to_datetime(roOrdo['date_law'], errors='coerce')

# print(roOrdo.head())

roOrdo['status'] = roOrdo['status'].str.replace("placeholder", "uitata")
roLaws['ones'] = 1
roOrdo['ones'] = 1

# print(roOrdo.head())

### FR ORDOS AND LAWS

frenchLaws = pd.read_csv("french laws as of 3 jan.csv", index_col=False) ### read french laws
frenchOrdo = pd.read_csv("french ordos as of 3 jan.csv", index_col=False) ### read french ordos

### a bunch of laws cleaning
frenchLaws['frlaw_date'] = frenchLaws['frlaw_date'].str.findall('( du )(1er )(\w* )(\d{4})|( du )(\d{1,2} )(\w* )(\d{4})')
frenchLaws['frlaw_date'] = frenchLaws['frlaw_date'].astype(str)
frenchLaws['frlaw_date'] = frenchLaws['frlaw_date'].str.replace('\[\(\'', '').str.replace(',', '').str.replace('\'', '').str.replace('\)', '').str.replace('\]', '').str.replace('du', '').str.replace("\s\s+", " ")
frenchLaws['frlaw_date'] = frenchLaws['frlaw_date'].str.replace('(\([\s\d\w]*)|( \( 1er[\s\w\d]*)', '')
frenchLaws['frlaw_date'] = frenchLaws['frlaw_date'].str.lstrip().str.rstrip().str.replace('1er', '1')
### a bunch of ordos cleaning
frenchOrdo['ordo_date'] = frenchOrdo['ordo_date'].str.findall('( du )(1er )(\w* )(\d{4})|( du )(\d{1,2} )(\w* )(\d{4})')
frenchOrdo['ordo_date'] = frenchOrdo['ordo_date'].astype(str)
frenchOrdo['ordo_date'] = frenchOrdo['ordo_date'].str.replace('\[\(\'', '').str.replace(',', '').str.replace('\'', '').str.replace('\)', '').str.replace('\]', '').str.replace('du', '').str.replace("\s\s+", " ")
frenchOrdo['ordo_date'] = frenchOrdo['ordo_date'].str.replace('(\([\s\d\w]*)|( \( 1er[\s\w\d]*)', '')
frenchOrdo['ordo_date'] = frenchOrdo['ordo_date'].str.lstrip().str.rstrip().str.replace('1er', '1')

frenchOrdo['ordo'] = frenchOrdo['ordo'].str.replace('n °', 'no').str.replace('n°', 'no')


### change months from fr to english and change column to date
months = {'janvier': 'January', 'février': 'February', 'mars': 'March', 'avril': 'April', 'mai': 'May', 'juin': 'June', 'juillet': 'July', 'août': 'August', 'septembre': 'September', 'octobre': 'October', 'novembre': 'November', 'décembre': 'December'}

for monthfr, montheng in months.items():
    frenchLaws.frlaw_date = frenchLaws.frlaw_date.str.replace(monthfr, montheng)
    frenchOrdo.ordo_date = frenchOrdo.ordo_date.str.replace(monthfr, montheng)
    
frenchLaws['frlaw_date'] = pd.to_datetime(frenchLaws['frlaw_date'])
frenchOrdo['ordo_date'] = pd.to_datetime(frenchOrdo['ordo_date'])

frenchLaws = frenchLaws[(frenchLaws['frlaw_date'] > '1991-12-31')].reset_index()
frenchLaws = frenchLaws.drop(['index'], axis=1)

frenchLaws['ones'] = 1
frenchOrdo['ones'] = 1

# print(frenchLaws.head())
# print(frenchOrdo.head())


### plotYears = df contains nr of fr and rou laws and ordos by year

plotYears = pd.DataFrame(columns = ["ro laws", "ro ordos", "fr laws", 'fr ordos'], index = [1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020])

plotYears['ro laws'] = roLaws.groupby(roLaws['date_law'].dt.year).sum()
plotYears['ro ordos'] = roOrdo.groupby(roOrdo['date_ordo'].dt.year).sum()
plotYears['fr laws'] = frenchLaws.groupby(frenchLaws['frlaw_date'].dt.year).sum()
plotYears['fr ordos'] = frenchOrdo.groupby(frenchOrdo['ordo_date'].dt.year).sum()
plotYears = plotYears.fillna({'fr ordos' : 0})
# print(plotYears)


# fig, (ax1,ax2, ax3) = plt.subplots(nrows=3)#, sharex=True)

# ax1.grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.7)
# ax2.grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.7)
# ax3.grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.7)

# ax1.plot(plotYears['ro laws'], label='Rou Laws', color='blue')
# ax1.plot(plotYears['fr laws'], label='French Laws', color='red')
# ax1.legend(frameon=False, loc=2)
# ax1.title.set_text('number of ROU laws and FR laws 1992 - 2020')
# ax1.spines['top'].set_visible(False)
# ax1.spines['right'].set_visible(False)
# ax1.spines['bottom'].set_visible(False)
# ax1.spines['left'].set_visible(False)
# ax1.tick_params(bottom=False, left=False)
              
# ax2.plot(plotYears['ro ordos'], label='Rou Ordos', color='cornflowerblue')
# ax2.plot(plotYears['fr ordos'], label='Fench Ordos', color='black')
# ax2.legend(frameon=False, loc=2)
# ax2.title.set_text('number of ROU ordos and FR ordos 1992 - 2020')
# ax2.spines['top'].set_visible(False)
# ax2.spines['right'].set_visible(False)
# ax2.spines['bottom'].set_visible(False)
# ax2.spines['left'].set_visible(False)
# ax2.tick_params(bottom=False, left=False)

# ax3.plot(plotYears['ro laws'], label='Rou laws', color='blue')
# ax3.plot(plotYears['ro ordos'], label='Rou ordos', color='cornflowerblue')
# ax3.legend(frameon=False, loc=2)
# ax3.title.set_text('number of ROU laws and ordinances 1992 - 2020')
# ax3.spines['top'].set_visible(False)
# ax3.spines['right'].set_visible(False)
# ax3.spines['bottom'].set_visible(False)
# ax3.spines['left'].set_visible(False)
# ax3.tick_params(bottom=False, left=False)

# plt.tight_layout()
# plt.show()


##### analysis on months

### plotMonths = df contains nr of fr and rou laws and ordos by month

plotMonths = pd.DataFrame(columns = ["ro laws", "ro ordos", "fr laws", 'fr ordos'], index = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])

plotMonths['ro laws'] = roLaws.groupby(roLaws['date_law'].dt.strftime('%B')).sum()
                    
plotMonths['ro ordos'] = roOrdo.groupby(roOrdo['date_ordo'].dt.strftime('%B')).sum()   
plotMonths['fr laws'] = frenchLaws.groupby(frenchLaws['frlaw_date'].dt.strftime('%B')).sum()
plotMonths['fr ordos'] = frenchOrdo.groupby(frenchOrdo['ordo_date'].dt.strftime('%B')).sum()

# print(plotMonths)


# fig, (ax1,ax2) = plt.subplots(nrows=2)#, sharex=True)
# ax1.grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.7)
# ax2.grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.7)


# ax1.plot(plotMonths['fr ordos'], label='Fench Ordos', color='black')
# ax1.plot(plotMonths['fr laws'], label='French Laws', color='red')
# ax1.legend(frameon=False, loc=2)
# ax1.title.set_text('number of fr laws and fr ordos per month, shadded = outside parliament session')
# ax1.spines['top'].set_visible(False)
# ax1.spines['right'].set_visible(False)
# ax1.spines['bottom'].set_visible(False)
# ax1.spines['left'].set_visible(False)
# ax1.tick_params(bottom=False, left=False)
              
# ax1.fill_between(x = plotMonths.index,
#                 y1 = plotMonths['fr laws'],
#                 y2 = plotMonths['fr ordos'],
#                 where = plotMonths.index.isin(['October', 'November', 'December', 'January', "February", 'March', 'April', 'May', 'June']),
#                 facecolor = 'lightskyblue',
#                 alpha = 0.2)

# ax2.plot(plotMonths['ro laws'], label='Rou laws', color='blue')
# ax2.plot(plotMonths['ro ordos'], label='Rou Ordos', color='cornflowerblue')
# ax2.legend(frameon=False, loc=2)
# ax2.title.set_text('number of ROU laws and ROU ordos per month shadded = outside parliament session')
# ax2.spines['top'].set_visible(False)
# ax2.spines['right'].set_visible(False)
# ax2.spines['bottom'].set_visible(False)
# ax2.spines['left'].set_visible(False)
# ax2.tick_params(bottom=False, left=False)

# ax2.fill_between(x = plotMonths.index,
#                 y1 = plotMonths['ro laws'],
#                 y2 = plotMonths['ro ordos'],
#                 where = plotMonths.index.isin(["February", 'March', 'April', 'May', 'June', 'September', 'October', 'November', 'December']),
#                 facecolor = 'lightskyblue',
#                 alpha = 0.2)

# plt.tight_layout()
# plt.show()

### create column of no of days between ordo and law. if no law, set date to end value 
roOrdo['date_law'] = roOrdo['date_law'].fillna(end)
roOrdo['zile efecte'] = (roOrdo['date_law'] - roOrdo['date_ordo']).dt.days

print(roOrdo.head())

pd.set_option('display.max_colwidth', None)
### out of all ordos, regardless of status, 1992-2020, which is the oldest by zile efecte
zileEfecteFaraParlMAX = roOrdo.loc[[roOrdo['zile efecte'].idxmax()]]

print("'zile efecte' = no of days between ordo and law. if no law, set law date to date of last scrapping")
print('out of all ordos 1992 to 2020, regardless of status the oldest by zile efecte is:')
print(zileEfecteFaraParlMAX.to_string(header=False, index=False))

### out of all ordos, 1992-2020, which is the youngest by zile efecte 
### (without uitata status. there are ordos given right before scrapping, considering them would distort the result)
zileEfecteFaraParlMIN = roOrdo.loc[[roOrdo[~roOrdo['status'].str.contains('uitata')]['zile efecte'].idxmin()]]

print('out of all ordos, 1992-2020, the youngest by zile efecte, "uitata" not included is:')
print(zileEfecteFaraParlMIN.to_string(header=False, index=False))

### for all ordos, regardless of status, 1992-2020, what is the mean of zile efecte
zileEfecteFaraParlAVERAGE = roOrdo['zile efecte'].mean()

print('out of all ordos 1992-2020, regardless of status, the mean of zile efecte is:')
print(zileEfecteFaraParlAVERAGE)


### for all APROBATE ordos, 1992-2020, the fastest and slowest approved, and the mean of approving
stats92to20APROB = roOrdo[roOrdo['status'].str.contains('Aprobata')]['zile efecte'].agg(['min', 'max','mean'])

print('for all APROBATE ordos, 1992-2020, the fastest and the slowest approved, and the mean of approving')
print(stats92to20APROB.to_string(header=False, index=False))

### for all APROBATE ordos, 1992-2020, which is the fastest approved
stats92to20AprobFAST = roOrdo.loc[[roOrdo[roOrdo['status'].str.contains('Aprobata')]['zile efecte'].idxmin()]]

print('for all APROBATE ordos, 1992-2020, the fastest approved is:')
print(stats92to20AprobFAST.to_string(header=False, index=False))

### for all APROBATE ordos, 1992-2020, which is the slowest approved
stats92to20AprobSLOW = roOrdo.loc[[roOrdo[roOrdo['status'].str.contains('Aprobata')]['zile efecte'].idxmax()]]

print('for all APROBATE ordos, 1992-2020, the slowest approved is:')
print(stats92to20AprobSLOW.to_string(header=False, index=False))


### for all RESPINSE ordos, 1992-2020, the fastest and slowest rejected, and the mean of rejecting
stats92to20RESP = roOrdo[roOrdo['status'].str.contains('Respinsa')]['zile efecte'].agg(['min', 'max','mean'])

print('for all RESPINSE ordos, 1992-2020, the fastest and slowest rejected, and the mean of rejecting')
print(stats92to20RESP.to_string(header=False, index=False))

### for all RESPINSE ordos, 1992-2020, which is the slowest rejected
stats92to20RespSLOW = roOrdo.loc[[roOrdo[roOrdo['status'].str.contains('Respinsa')]['zile efecte'].idxmax()]]

print('out of all RESPINSE ordos, 1992-2020, the slowest rejected is:')
print(stats92to20RespSLOW.to_string(header=False, index=False))

### for all RESPINSE ordos, 1992-2020, which is the fastest rejected
stats92to20RespFAST = roOrdo.loc[[roOrdo[roOrdo['status'].str.contains('Respinsa')]['zile efecte'].idxmin()]]

print('out of all RESPINSE ordos, 1992-2020, the fastest rejected is:')
print(stats92to20RespFAST.to_string(header=False, index=False))


### for all ABROG OUG ordos, 1992-2020, the fastest and slowest abrogata prin og, and the mean of doing so
stats92to20AbrogOUG = roOrdo[roOrdo['status'].str.contains('abrogata prin og')]['zile efecte'].agg(['min', 'max','mean'])

print('for all ABROG OUG ordos, 1992-2020, the fastest and slowest abrogata prin og, and the mean of doing so')
print(stats92to20AbrogOUG.to_string(header=False, index=False))

### for all abrogata prin og ordos, 1992-2020, which is the slowest abrogate
stats92to20OUGabrogSLOW = roOrdo.loc[[roOrdo[roOrdo['status'].str.contains('abrogata prin og')]['zile efecte'].idxmax()]]
print('or all abrogata prin og ordos, 1992-2020, which is the slowest abrogate')
print(stats92to20OUGabrogSLOW.to_string(header=False, index=False))


### for all abrogata prin og ordos, 1992-2020, which is the fastest abrogate
stats92to20OUGabrogFAST = roOrdo.loc[[roOrdo[roOrdo['status'].str.contains('abrogata prin og')]['zile efecte'].idxmin()]]
print('or all abrogata prin og ordos, 1992-2020, which is the fastest abrogate')
print(stats92to20OUGabrogFAST.to_string(header=False, index=False))


### for all ABROG LEGE ordos, 1992-2020, the fastest and slowest abrog lege, and the mean of doing so
stats92to20AbrogLEGE = roOrdo[roOrdo['status'].str.contains('abrogata prin lege')]['zile efecte'].agg(['min', 'max','mean'])

print('for all ABROG LEGE ordos, 1992-2020, the fastest and slowest abrog lege, and the mean of doing so')
print(stats92to20AbrogLEGE.to_string(header=False, index=False))

### for all abrogata prin og ordos, 1992-2020, which is the slowest abrogate
stats92to20LEGEabrogSLOW = roOrdo.loc[[roOrdo[roOrdo['status'].str.contains('abrogata prin lege')]['zile efecte'].idxmax()]]
print('for all abrogata prin og ordos, 1992-2020, which is the slowest abrogate')
print(stats92to20LEGEabrogSLOW.to_string(header=False, index=False))

### for all abrogata prin og ordos, 1992-2020, which is the fastest abrogate
stats92to20LEGEabrogFAST = roOrdo.loc[[roOrdo[roOrdo['status'].str.contains('abrogata prin lege')]['zile efecte'].idxmin()]]
print('for all abrogata prin og ordos, 1992-2020, which is the fastest abrogate')
print(stats92to20LEGEabrogFAST.to_string(header=False, index=False))


### for all uitate ordos, 1992-2020, the max, min, mean of days of forgetfulness
stats92to20Uitata = roOrdo[roOrdo['status'].str.contains('uitata')]['zile efecte'].agg(['min', 'max','mean'])

print('for all uitate ordos, 1992-2020, the max, min, mean of days of forgetfulness')
print(stats92to20Uitata.to_string(header=False, index=False))

### for all uitate, 1992-2020, which is the oldest
stats92to20uitataOLD = roOrdo.loc[[roOrdo[roOrdo['status'].str.contains('uitata')]['zile efecte'].idxmax()]]

print('for all uitate, 1992-2020, the oldest is:')
print(stats92to20uitataOLD.to_string(header=False, index=False))