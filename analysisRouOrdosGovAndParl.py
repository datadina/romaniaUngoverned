import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import matplotlib.dates as mdates
import re


from scrapRouOrdosAbrog import finalOrdos
roOrdo = finalOrdos


pd.set_option('display.width', 1000) 
pd.set_option('display.max_columns', 1000)  
# print(roOrdo.head())

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

### change months from romanian to english in date of ordonanta column
for monthro, montheng in monthsRom.items():
    roOrdo.date_ordo = roOrdo.date_ordo.str.replace(monthro, montheng)
    roOrdo.date_law = roOrdo.date_law.str.replace(monthro, montheng)


# print(roOrdo.head())

### turn date columns into time
roOrdo['date_ordo'] = pd.to_datetime(roOrdo['date_ordo'])
roOrdo['date_law'] = pd.to_datetime(roOrdo['date_law'], errors='coerce')

roOrdo['ones'] = 1

### create column of no of days between ordo and law. if no law, set date to end value date
end = pd.to_datetime('2020-12-01') ## to be changed with day doing the scrapping
roOrdo['date_law'] = roOrdo['date_law'].fillna(end)
roOrdo['zile efecte'] = (roOrdo['date_law'] - roOrdo['date_ordo']).dt.days
 
# print(roOrdo.head())

roOrdo['status'] = roOrdo['status'].str.replace("placeholder", "uitata")

# print(roOrdo.head())
# print(roOrdo.shape)


startORBAN = datetime.datetime(2019, 11, 4)
endORBAN = datetime.datetime(2020, 12, 7) ## https://www.gov.ro/ro/fosti%20ministri 

startDANCILA = datetime.datetime(2018, 1, 29)
endDANCILA = datetime.datetime(2019, 11, 4) ## https://www.gov.ro/ro/fosti%20ministri 

startFIFOR = datetime.datetime(2018, 1, 16)
endFIFOR = datetime.datetime(2018, 1, 29) ## https://www.gov.ro/ro/fosti%20ministri 

startTUDOSE = datetime.datetime(2017, 6, 29) ## https://www.presidency.ro/ro/media/decrete-si-acte-oficiale/decret-pentru-numirea-guvernului-romaniei1498751006
endTUDOSE = datetime.datetime(2018, 1, 16) ## https://lege5.ro/Gratuit/gi3dmmrygi2q/decretul-nr-49-2018-pentru-incetarea-functiei-de-prim-ministru-al-guvernului-romaniei 

startGRINDEANU = datetime.datetime(2017, 1, 4) ## https://lege5.ro/Gratuit/ge2dambsgm4a/decretul-nr-7-2017-pentru-numirea-guvernului-romaniei 
endGRINDEANU= datetime.datetime(2017, 6, 21) ## https://stirileprotv.ro/stiri/politic/motiunea-de-cenzura-impotriva-guvernului-grindeanu-decisa-azi-in-parlament-dragnea-sunt-realist-va-trece.html

startCIOLOS = datetime.datetime(2015, 11, 17)   ## https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjjg7rbhe_tAhWhx4UKHakkCnYQFjAAegQIBBAC&url=https%3A%2F%2Fwww.hotnews.ro%2Fstiri-politic-20599732-livetext-parlamentul-voteaza-guvernul-ciolos.htm&usg=AOvVaw1iycfnWfJxA6Rg-L9kzQKj
endCIOLOS = datetime.datetime(2017, 1, 4)  ## start grindeanu

startCIMPEANU = datetime.datetime(2015, 11, 5)  ## https://www.hotnews.ro/stiri-politic-20559991-cine-este-sorin-cimpeanu-cum-ajuns-noul-prim-ministru-interimar.htm
endCIMPEANU = datetime.datetime(2016, 11, 17)  ## start ciolos

startPONTA = datetime.datetime(2012, 5, 7)  ## https://www.digi24.ro/stiri/actualitate/politica/un-an-de-guvernare-usl-la-7-mai-2012-guvernul-condus-de-victor-ponta-a-depus-juramantul-71177 
endPONTA = datetime.datetime(2015, 11, 4)  ## https://www.digi24.ro/stiri/actualitate/politica/victor-ponta-a-demisionat-454264

startUNGUREANU = datetime.datetime(2012, 2, 9)
endUNGUREANU= datetime.datetime(2012, 4, 27) ## http://old.gov.ro

startBOC = datetime.datetime(2008, 12, 22)
endBOC = datetime.datetime(2012, 2, 6) ## http://old.gov.ro

startTARICEANU = datetime.datetime(2004, 12, 29)
endTARICEANU= datetime.datetime(2008, 12, 22) ## http://old.gov.ro

startBEJINARIU = datetime.datetime(2004, 12, 21)
endBEJINARIU= datetime.datetime(2004, 12, 28) ## http://old.gov.ro

startNASTASE = datetime.datetime(2000, 12, 28)   ## ihttp://arhiva.gov.ro/adrian-nastase__l1a121587.html
endNASTASE = datetime.datetime(2004, 12, 21)  ## http://arhiva.gov.ro/adrian-nastase__l1a121587.html

startISARESCU = datetime.datetime(1999, 12, 22)  ##
endISARESCU = datetime.datetime(2000, 12, 28)  ## https://www.capital.ro/adevarul-despre-mugur-isarescu-s-a-aflat-cum-a-ajuns-de-fapt-guvernator-la-bnr.html
  
startATHANASIU = datetime.datetime(1999, 12, 13)    ## no ordos passed in this timeframe
endATHANASIU= datetime.datetime(1999, 12, 22)  ##

startVASILE = datetime.datetime(1998, 4, 18)
endVASILE = datetime.datetime(1999, 12, 21)  ## https://www.gov.ro/ro/fosti%20ministri 

startDEJEU = datetime.datetime(1998, 3, 30)
endDEJEU = datetime.datetime(1998, 4, 17)  ## https://www.gov.ro/ro/fosti%20ministri 

startCIORBEA = datetime.datetime(1996, 12, 19)
endCIORBEA = datetime.datetime(1998, 3, 30) ## https://www.gov.ro/ro/fosti%20ministri 

startVACAROIU = datetime.datetime(1992, 11, 20)
endVACAROIU = datetime.datetime(1996, 12, 11) ## https://www.gov.ro/ro/fosti%20ministri 

startSTOLOJAN = datetime.datetime(1991, 10, 16)
endSTOLOJAN = datetime.datetime(1992, 11, 19)  ## https://www.gov.ro/ro/fosti%20ministri 

 
ordoORBAN = roOrdo.loc[(roOrdo['date_ordo'] > startORBAN) & (roOrdo['date_ordo'] <= endORBAN)].reset_index()
ordoDANCILA = roOrdo.loc[(roOrdo['date_ordo'] > startDANCILA) & (roOrdo['date_ordo'] <= endDANCILA)].reset_index()
ordoFIFOR = roOrdo.loc[(roOrdo['date_ordo'] > startFIFOR) & (roOrdo['date_ordo'] <= endFIFOR)].reset_index()
ordoTUDOSE = roOrdo.loc[(roOrdo['date_ordo'] > startTUDOSE) & (roOrdo['date_ordo'] <= endTUDOSE)].reset_index()
ordoGRINDEANU = roOrdo.loc[(roOrdo['date_ordo'] > startGRINDEANU) & (roOrdo['date_ordo'] <= endGRINDEANU)].reset_index()
ordoCIOLOS = roOrdo.loc[(roOrdo['date_ordo'] > startCIOLOS) & (roOrdo['date_ordo'] <= endCIOLOS)].reset_index()
ordoCIMPEANU = roOrdo.loc[(roOrdo['date_ordo'] > startCIMPEANU) & (roOrdo['date_ordo'] <= endCIMPEANU)].reset_index()
ordoPONTA = roOrdo.loc[(roOrdo['date_ordo'] > startPONTA) & (roOrdo['date_ordo'] <= endPONTA)].reset_index()
ordoUNGUREANU = roOrdo.loc[(roOrdo['date_ordo'] > startUNGUREANU) & (roOrdo['date_ordo'] <= endUNGUREANU)].reset_index()
ordoBOC = roOrdo.loc[(roOrdo['date_ordo'] > startSTOLOJAN) & (roOrdo['date_ordo'] <= endSTOLOJAN)].reset_index()
ordoTARICEANU = roOrdo.loc[(roOrdo['date_ordo'] > startTARICEANU) & (roOrdo['date_ordo'] <= endTARICEANU)].reset_index()
ordoBEJINARIU = roOrdo.loc[(roOrdo['date_ordo'] > startBEJINARIU) & (roOrdo['date_ordo'] <= endBEJINARIU)].reset_index()
ordoNASTASE = roOrdo.loc[(roOrdo['date_ordo'] > startNASTASE) & (roOrdo['date_ordo'] <= endNASTASE)].reset_index()
ordoISARESCU = roOrdo.loc[(roOrdo['date_ordo'] > startISARESCU) & (roOrdo['date_ordo'] <= endISARESCU)].reset_index()
ordoATHANASIU = roOrdo.loc[(roOrdo['date_ordo'] > startATHANASIU) & (roOrdo['date_ordo'] <= endATHANASIU)].reset_index()
ordoVASILE = roOrdo.loc[(roOrdo['date_ordo'] > startVASILE) & (roOrdo['date_ordo'] <= endVASILE)].reset_index()
ordoDEJEU = roOrdo.loc[(roOrdo['date_ordo'] > startDEJEU) & (roOrdo['date_ordo'] <= endDEJEU)].reset_index()
ordoCIORBEA = roOrdo.loc[(roOrdo['date_ordo'] > startCIORBEA) & (roOrdo['date_ordo'] <= endCIORBEA)].reset_index()
ordoVACAROIU = roOrdo.loc[(roOrdo['date_ordo'] > startVACAROIU) & (roOrdo['date_ordo'] <= endVACAROIU)].reset_index()
ordoSTOLOJAN = roOrdo.loc[(roOrdo['date_ordo'] > startSTOLOJAN) & (roOrdo['date_ordo'] <= endSTOLOJAN)].reset_index()
 

# print('ordoORBAN')
# print(ordoORBAN.head())
# print('ordoFIFOR')
# print(ordoFIFOR.head())
# print('ordoTUDOSE')
# print(ordoTUDOSE.head())
# print('ordoGRINDEANU')
# print(ordoGRINDEANU.head())
# print('ordoCIMPEANU')
# print(ordoCIMPEANU.head())
# print('ordoPONTA')
# print(ordoPONTA.head())
# print('ordoUNGUREANU')
# print(ordoUNGUREANU.head())
# print('ordoBOC')
# print(ordoBOC.head())
# print('ordoTARICEANU')
# print(ordoTARICEANU.head())
# print('ordoBEJINARIU')
# print(ordoBEJINARIU.head())
# print('ordoNASTASE')
# print(ordoNASTASE.head())
# print('ordoISARESCU')
# print(ordoISARESCU.head())
# print('ordoATHANASIU')
# print(ordoATHANASIU.head())
# print('ordoVASILE')
# print(ordoVASILE.head())
# print('ordoDEJEU')
# print(ordoDEJEU.head())
# print('ordoCIORBEA')
# print(ordoCIORBEA.head())
# print('ordoVACAROIU')
# print(ordoVACAROIU.head())
# print('ordoSTOLOJAN')
# print(ordoSTOLOJAN.head()) 



### create df, by gov how many ordos of each kind

govs = [ordoORBAN, ordoDANCILA, ordoFIFOR, ordoTUDOSE, ordoGRINDEANU, ordoCIOLOS, ordoCIMPEANU, ordoPONTA, ordoUNGUREANU, ordoBOC, 
ordoTARICEANU, ordoBEJINARIU, ordoNASTASE, ordoISARESCU, ordoATHANASIU, ordoVASILE, ordoDEJEU, ordoCIORBEA, ordoVACAROIU, ordoSTOLOJAN]      

govSTARTS = [startORBAN, startDANCILA, startFIFOR, startTUDOSE, startGRINDEANU, startCIOLOS, startCIMPEANU, startPONTA,  
             startUNGUREANU, startBOC, startTARICEANU, startBEJINARIU, startNASTASE, startISARESCU, startATHANASIU,  
             startVASILE, startDEJEU, startCIORBEA, startVACAROIU, startSTOLOJAN]

govENDS = [endORBAN, endDANCILA, endFIFOR , endTUDOSE , endGRINDEANU, endCIOLOS , endCIMPEANU, 
           endPONTA , endUNGUREANU, endBOC, endTARICEANU, endBEJINARIU, endNASTASE, endISARESCU, 
           endATHANASIU, endVASILE, endDEJEU, endCIORBEA, endVACAROIU, endSTOLOJAN]

statsGOVS = pd.DataFrame(columns = ['total', "aprob", "resp", "abORDO", 'abLAW', 'uitate', 'days of gov', "aprobDAYS", "respDAYS", "abORDOdays", 'abLAWdays', 'uitateDAYS', 'totalDAYS'], 
                         index = ['Orban', 'Dancila', 'Fifor', 'Tudose', 'Grind', 'Ciolos', 'Cimp', 'Ponta', 'Ungur', 'Boc', 'Taric', 'Bejin', 'Nastase', 'Isar', 'Athan', 'Vasile', 'Dejeu', 'Ciorbea', 'Vacaroiu', 'Stolo'])

i = 0
for gov in govs:
    statsGOVS['aprob'][i] = gov[gov['status'].str.contains('Aprobata')]['ones'].sum()
    statsGOVS['resp'][i] = gov[gov['status'].str.contains('Respinsa')]['ones'].sum()
    statsGOVS['abORDO'][i] = gov[gov['status'].str.contains('abrogata prin og')]['ones'].sum()
    statsGOVS['abLAW'][i] = gov[gov['status'].str.contains('abrogata prin lege')]['ones'].sum()
    statsGOVS['uitate'][i] = gov[gov['status'].str.contains('uitata')]['ones'].sum()
    statsGOVS['total'][i] = len(gov.index)

    statsGOVS['days of gov'][i] = (govENDS[i] - govSTARTS[i]).days
    
    i = i + 1


statsGOVS['aprobDAYS'] = statsGOVS['aprob'] / statsGOVS['days of gov']*100
statsGOVS['respDAYS'] =  statsGOVS['resp'] / statsGOVS['days of gov']*100
statsGOVS['abORDOdays'] = statsGOVS['abORDO'] / statsGOVS['days of gov']*100
statsGOVS['abLAWdays'] = statsGOVS['abLAW'] / statsGOVS['days of gov']*100
statsGOVS['uitateDAYS'] = statsGOVS['uitate'] / statsGOVS['days of gov']*100
statsGOVS['totalDAYS'] = statsGOVS['total'] / statsGOVS['days of gov']*100
      
    
# print(statsGOVS)


# fig, (ax1,ax2, ax3) = plt.subplots(nrows=3)#, sharex=True)

# ax1.grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.7)
# ax2.grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.7)
# ax3.grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.7)

# ax1.plot(statsGOVS['totalDAYS'], label='total no or ordos per day times 100', color='red')
# ax1.legend(frameon=False, loc=2)
# ax1.spines['top'].set_visible(False)
# ax1.spines['right'].set_visible(False)
# ax1.spines['bottom'].set_visible(False)
# ax1.spines['left'].set_visible(False)
# ax1.tick_params(bottom=False, left=False)
# ax1.tick_params(axis='x', rotation=30)

# ax2.plot(statsGOVS['aprobDAYS'], label='no of ordos approved per day times 100', color='darkolivegreen')
# ax2.legend(frameon=False, loc=2)
# ax2.spines['top'].set_visible(False)
# ax2.spines['right'].set_visible(False)
# ax2.spines['bottom'].set_visible(False)
# ax2.spines['left'].set_visible(False)
# ax2.tick_params(bottom=False, left=False)
# ax2.tick_params(axis='x', rotation=30)

# ax3.plot(statsGOVS['uitateDAYS'], label='no of ordos forgotten per day times 100', color='chocolate')
# ax3.legend(frameon=False, loc=2)
# ax3.spines['top'].set_visible(False)
# ax3.spines['right'].set_visible(False)
# ax3.spines['bottom'].set_visible(False)
# ax3.spines['left'].set_visible(False)
# ax3.tick_params(bottom=False, left=False)
# ax3.tick_params(axis='x', rotation=30)
              

# plt.tight_layout()
# plt.show()


# fig, (ax1,ax2) = plt.subplots(nrows=2)#, sharex=True)

# ax1.grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.7)
# ax2.grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.7)
# # ax3.grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.7)


# ax1.plot(statsGOVS['totalDAYS'], label='total no or ordos per day times 100', color='red')
# ax1.legend(frameon=False, loc=2)
# ax1.spines['top'].set_visible(False)
# ax1.spines['right'].set_visible(False)
# ax1.spines['bottom'].set_visible(False)
# ax1.spines['left'].set_visible(False)
# ax1.tick_params(bottom=False, left=False)
# ax1.tick_params(axis='x', rotation=30)
              
# ax2.plot(statsGOVS['respDAYS'], label='no of ordos rejected per day times 100', color='orchid')
# ax2.legend(frameon=False, loc=2)
# ax2.spines['top'].set_visible(False)
# ax2.spines['right'].set_visible(False)
# ax2.spines['bottom'].set_visible(False)
# ax2.spines['left'].set_visible(False)
# ax2.tick_params(bottom=False, left=False)
# ax2.tick_params(axis='x', rotation=30)

# plt.tight_layout()
# plt.show()

# fig, (ax1,ax2, ax3) = plt.subplots(nrows=3)#, sharex=True)

# ax1.grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.7)
# ax2.grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.7)
# ax3.grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.7)


# ax1.plot(statsGOVS['totalDAYS'], label='total no or ordos per day times 100', color='red')
# ax1.legend(frameon=False, loc=2)
# ax1.spines['top'].set_visible(False)
# ax1.spines['right'].set_visible(False)
# ax1.spines['bottom'].set_visible(False)
# ax1.spines['left'].set_visible(False)
# ax1.tick_params(bottom=False, left=False)
# ax1.tick_params(axis='x', rotation=30)

# ax2.plot(statsGOVS['abORDOdays'], label='no of ordos abrog through ordos per day times 100', color='darkcyan')
# ax2.legend(frameon=False, loc=2)
# ax2.spines['top'].set_visible(False)
# ax2.spines['right'].set_visible(False)
# ax2.spines['bottom'].set_visible(False)
# ax2.spines['left'].set_visible(False)
# ax2.tick_params(bottom=False, left=False)
# ax2.tick_params(axis='x', rotation=30)

# ax3.plot(statsGOVS['abLAWdays'], label='no of ordos abrog through laws per day times 100', color='seagreen')
# ax3.legend(frameon=False, loc=2)
# ax3.spines['top'].set_visible(False)
# ax3.spines['right'].set_visible(False)
# ax3.spines['bottom'].set_visible(False)
# ax3.spines['left'].set_visible(False)
# ax3.tick_params(bottom=False, left=False)
# ax3.tick_params(axis='x', rotation=30)


# plt.tight_layout()
# plt.show()


### add column stating the parl of each ordo

rouParl1990to1992start = pd.to_datetime('1992-01-01')
rouParl1990to1992end = pd.to_datetime('1992-10-16')

rouParl1992to1996start = pd.to_datetime('1992-10-16')
rouParl1992to1996end = pd.to_datetime('1996-11-22')

rouParl1996to2000start = pd.to_datetime('1996-11-22')
rouParl1996to2000end = pd.to_datetime('2000-12-11')

rouParl2000to2004start = pd.to_datetime('2000-12-11')
rouParl2000to2004end = pd.to_datetime('2004-12-13')

rouParl2004to2008start = pd.to_datetime('2004-12-13')
rouParl2004to2008end = pd.to_datetime('2008-12-15')

rouParl2008to2012start = pd.to_datetime('2008-12-15')
rouParl2008to2012end = pd.to_datetime('2012-12-19')

rouParl2012to2016start = pd.to_datetime('2012-12-19')
rouParl2012to2016end = pd.to_datetime('2016-12-20')

rouParl2016to2020start = pd.to_datetime('2016-12-20')
rouParl2016to2020end = pd.to_datetime('2020-12-21')


rouParl1990to1992 = roOrdo.loc[(roOrdo['date_law'] > rouParl1990to1992start) & (roOrdo['date_law'] <= rouParl1990to1992end)]#.reset_index()
rouParl1992to1996 = roOrdo.loc[(roOrdo['date_law'] > rouParl1992to1996start) & (roOrdo['date_law'] <= rouParl1992to1996end)]#.reset_index()
rouParl1996to2000 = roOrdo.loc[(roOrdo['date_law'] > rouParl1996to2000start) & (roOrdo['date_law'] <= rouParl1996to2000end)]#.reset_index()
rouParl2000to2004 = roOrdo.loc[(roOrdo['date_law'] > rouParl2000to2004start) & (roOrdo['date_law'] <= rouParl2000to2004end)]#.reset_index()
rouParl2004to2008 = roOrdo.loc[(roOrdo['date_law'] > rouParl2004to2008start) & (roOrdo['date_law'] <= rouParl2004to2008end)]#.reset_index()
rouParl2008to2012 = roOrdo.loc[(roOrdo['date_law'] > rouParl2008to2012start) & (roOrdo['date_law'] <= rouParl2008to2012end)]#.reset_index()
rouParl2012to2016 = roOrdo.loc[(roOrdo['date_law'] > rouParl2012to2016start) & (roOrdo['date_law'] <= rouParl2012to2016end)]#.reset_index()
rouParl2016to2020 = roOrdo.loc[(roOrdo['date_law'] > rouParl2016to2020start) & (roOrdo['date_law'] <= rouParl2016to2020end)]#.reset_index()

pd.options.mode.chained_assignment = None 

rouParl1990to1992['parl'] = 'parl 90 92'
rouParl1992to1996['parl'] = 'parl 92 96'
rouParl1996to2000['parl'] = 'parl 96 00'
rouParl2000to2004['parl'] = 'parl 00 04'
rouParl2004to2008['parl'] = 'parl 04 08'
rouParl2008to2012['parl'] = 'parl 08 12'
rouParl2012to2016['parl'] = 'parl 12 16'
rouParl2016to2020['parl'] = 'parl 16 20'



# print(rouParl1990to1992)
# print(rouParl1992to1996)
# print(rouParl1996to2000)
# print(rouParl2000to2004)
# print(rouParl2004to2008)
# print(rouParl2008to2012)
# print(rouParl2012to2016)
# print(rouParl2016to2020)

roOrdoNew = pd.concat([rouParl1990to1992, rouParl1992to1996, rouParl1996to2000, rouParl2000to2004, rouParl2004to2008, rouParl2008to2012, rouParl2012to2016, rouParl2016to2020], ignore_index=True) 

# print(roOrdoNew.head())

### add column stating the gov of each ordo

ordoORBAN = roOrdoNew.loc[(roOrdoNew['date_ordo'] > startORBAN) & (roOrdoNew['date_ordo'] <= endORBAN)] 
ordoDANCILA = roOrdoNew.loc[(roOrdoNew['date_ordo'] > startDANCILA) & (roOrdoNew['date_ordo'] <= endDANCILA)] 
ordoFIFOR = roOrdoNew.loc[(roOrdoNew['date_ordo'] > startFIFOR) & (roOrdoNew['date_ordo'] <= endFIFOR)] 
ordoTUDOSE = roOrdoNew.loc[(roOrdoNew['date_ordo'] > startTUDOSE) & (roOrdoNew['date_ordo'] <= endTUDOSE)] 
ordoGRINDEANU = roOrdoNew.loc[(roOrdoNew['date_ordo'] > startGRINDEANU) & (roOrdoNew['date_ordo'] <= endGRINDEANU)] 
ordoCIOLOS = roOrdoNew.loc[(roOrdoNew['date_ordo'] > startCIOLOS) & (roOrdoNew['date_ordo'] <= endCIOLOS)] 
ordoCIMPEANU = roOrdoNew.loc[(roOrdoNew['date_ordo'] > startCIMPEANU) & (roOrdoNew['date_ordo'] <= endCIMPEANU)] 
ordoPONTA = roOrdoNew.loc[(roOrdoNew['date_ordo'] > startPONTA) & (roOrdoNew['date_ordo'] <= endPONTA)] 
ordoUNGUREANU = roOrdoNew.loc[(roOrdoNew['date_ordo'] > startUNGUREANU) & (roOrdoNew['date_ordo'] <= endUNGUREANU)] 
ordoBOC = roOrdoNew.loc[(roOrdoNew['date_ordo'] > startSTOLOJAN) & (roOrdoNew['date_ordo'] <= endSTOLOJAN)] 
ordoTARICEANU = roOrdoNew.loc[(roOrdoNew['date_ordo'] > startTARICEANU) & (roOrdoNew['date_ordo'] <= endTARICEANU)] 
ordoBEJINARIU = roOrdoNew.loc[(roOrdoNew['date_ordo'] > startBEJINARIU) & (roOrdoNew['date_ordo'] <= endBEJINARIU)] 
ordoNASTASE = roOrdoNew.loc[(roOrdoNew['date_ordo'] > startNASTASE) & (roOrdoNew['date_ordo'] <= endNASTASE)] 
ordoISARESCU = roOrdoNew.loc[(roOrdoNew['date_ordo'] > startISARESCU) & (roOrdoNew['date_ordo'] <= endISARESCU)] 
ordoATHANASIU = roOrdoNew.loc[(roOrdoNew['date_ordo'] > startATHANASIU) & (roOrdoNew['date_ordo'] <= endATHANASIU)] 
ordoVASILE = roOrdoNew.loc[(roOrdoNew['date_ordo'] > startVASILE) & (roOrdoNew['date_ordo'] <= endVASILE)] 
ordoDEJEU = roOrdoNew.loc[(roOrdoNew['date_ordo'] > startDEJEU) & (roOrdoNew['date_ordo'] <= endDEJEU)] 
ordoCIORBEA = roOrdoNew.loc[(roOrdoNew['date_ordo'] > startCIORBEA) & (roOrdoNew['date_ordo'] <= endCIORBEA)] 
ordoVACAROIU = roOrdoNew.loc[(roOrdoNew['date_ordo'] > startVACAROIU) & (roOrdoNew['date_ordo'] <= endVACAROIU)] 
ordoSTOLOJAN = roOrdoNew.loc[(roOrdoNew['date_ordo'] > startSTOLOJAN) & (roOrdoNew['date_ordo'] <= endSTOLOJAN)] 

# print(ordoORBAN.shape)

ordoORBAN['guv'] = 'ordoORBAN'
ordoDANCILA['guv'] = 'ordoDANCILA'
ordoFIFOR['guv'] = 'ordoFIFOR'
ordoTUDOSE['guv'] = 'ordoTUDOSE'
ordoGRINDEANU['guv'] = 'ordoGRINDEANU'
ordoCIOLOS['guv'] = 'ordoCIOLOS'
ordoCIMPEANU['guv'] = 'ordoCIMPEANU'
ordoPONTA['guv'] = 'ordoPONTA'
ordoUNGUREANU['guv'] = 'ordoUNGUREANU'
ordoBOC['guv'] = 'ordoBOC'
ordoTARICEANU['guv'] = 'ordoTARICEANU'
ordoBEJINARIU['guv'] = 'ordoBEJINARIU'
ordoNASTASE['guv'] = 'ordoNASTASE'
ordoISARESCU['guv'] = 'ordoISARESCU'
ordoATHANASIU['guv'] = 'ordoATHANASIU'
ordoVASILE['guv'] = 'ordoVASILE'
ordoDEJEU['guv'] = 'ordoDEJEU'
ordoCIORBEA['guv'] = 'ordoCIORBEA'
ordoVACAROIU['guv'] = 'ordoVACAROIU'
ordoSTOLOJAN['guv'] = 'ordoSTOLOJAN'

# print(ordoSTOLOJAN)

statusnot = ['uitata', 'abrogata prin og']

ordoORBAN = ordoORBAN[~ordoORBAN.status.isin(statusnot)]
ordoDANCILA = ordoDANCILA[~ordoDANCILA.status.isin(statusnot)]
ordoFIFOR = ordoFIFOR[~ordoFIFOR.status.isin(statusnot)]
ordoTUDOSE = ordoTUDOSE[~ordoTUDOSE.status.isin(statusnot)]
ordoGRINDEANU = ordoGRINDEANU[~ordoGRINDEANU.status.isin(statusnot)]
ordoCIOLOS = ordoCIOLOS[~ordoCIOLOS.status.isin(statusnot)]
ordoCIMPEANU = ordoCIMPEANU[~ordoCIMPEANU.status.isin(statusnot)]
ordoPONTA = ordoPONTA[~ordoPONTA.status.isin(statusnot)]
ordoUNGUREANU = ordoUNGUREANU[~ordoUNGUREANU.status.isin(statusnot)]
ordoBOC = ordoBOC[~ordoBOC.status.isin(statusnot)]
ordoTARICEANU = ordoTARICEANU[~ordoTARICEANU.status.isin(statusnot)]
ordoBEJINARIU = ordoBEJINARIU[~ordoBEJINARIU.status.isin(statusnot)]
ordoNASTASE = ordoNASTASE[~ordoNASTASE.status.isin(statusnot)]
ordoISARESCU = ordoISARESCU[~ordoISARESCU.status.isin(statusnot)]
ordoATHANASIU = ordoATHANASIU[~ordoATHANASIU.status.isin(statusnot)]
ordoVASILE = ordoVASILE[~ordoVASILE.status.isin(statusnot)]
ordoDEJEU = ordoDEJEU[~ordoDEJEU.status.isin(statusnot)]
ordoCIORBEA = ordoCIORBEA[~ordoCIORBEA.status.isin(statusnot)]
ordoVACAROIU = ordoVACAROIU[~ordoVACAROIU.status.isin(statusnot)]
ordoSTOLOJAN = ordoSTOLOJAN[~ordoSTOLOJAN.status.isin(statusnot)]

# print(ordoSTOLOJAN)

### create df calculating how many ordos for each gov were approved, 
### rejected or abrogated through law by own parl, parl after, 2 parl after 

# govs = [ordoORBAN, ordoDANCILA, ordoFIFOR, ordoTUDOSE, ordoGRINDEANU, ordoCIOLOS, ordoCIMPEANU, ordoPONTA, ordoUNGUREANU, ordoBOC, 
# ordoTARICEANU, ordoBEJINARIU, ordoNASTASE, ordoISARESCU, ordoATHANASIU, ordoVASILE, ordoDEJEU, ordoCIORBEA, ordoVACAROIU, ordoSTOLOJAN]      

govParls = pd.DataFrame(columns = ['own parl', "parl after", "two parls later", 'total', 'own parl percent', 'parl after percent', 'two parls later percent'], 
                         index = ['Orban', 'Dancila', 'Fifor', 'Tudose', 'Grind', 'Ciolos', 'Cimp', 'Ponta', 'Ungur', 'Boc', 'Taric', 'Bejin', 'Nastase', 'Isar', 'Athan', 'Vasile', 'Dejeu', 'Ciorbea', 'Vacaroiu', 'Stolo'])


govParls.loc['Orban', 'own parl'] = ordoORBAN[ordoORBAN['parl'].str.contains('parl 16 20')]['ones'].sum()
govParls.loc['Dancila', 'own parl'] = ordoDANCILA[ordoDANCILA['parl'].str.contains('parl 16 20')]['ones'].sum()

govParls.loc['Fifor', 'own parl'] = ordoFIFOR[ordoFIFOR['parl'].str.contains('parl 16 20')]['ones'].sum()
govParls.loc['Tudose', 'own parl'] = ordoTUDOSE[ordoTUDOSE['parl'].str.contains('parl 16 20')]['ones'].sum()
govParls.loc['Grind', 'own parl'] = ordoGRINDEANU[ordoGRINDEANU['parl'].str.contains('parl 16 20')]['ones'].sum()


govParls.loc['Ciolos', 'own parl'] = ordoCIOLOS[ordoCIOLOS['parl'].str.contains('parl 12 16')]['ones'].sum()
govParls.loc['Ciolos', 'parl after'] = ordoCIOLOS[ordoCIOLOS['parl'].str.contains('parl 16 20')]['ones'].sum()

govParls.loc['Cimp', 'own parl'] = ordoCIMPEANU[ordoCIMPEANU['parl'].str.contains('parl 12 16')]['ones'].sum()
govParls.loc['Cimp', 'parl after'] = ordoCIMPEANU[ordoCIMPEANU['parl'].str.contains('parl 16 20')]['ones'].sum()

govParls.loc['Ponta', 'own parl'] = ordoPONTA[ordoPONTA['parl'].str.contains('parl 12 16')]['ones'].sum()
govParls.loc['Ponta', 'parl after'] = ordoPONTA[ordoPONTA['parl'].str.contains('parl 16 20')]['ones'].sum()

govParls.loc['Ungur', 'own parl'] = ordoUNGUREANU[ordoUNGUREANU['parl'].str.contains('parl 12 16')]['ones'].sum()
govParls.loc['Ungur', 'parl after'] = ordoUNGUREANU[ordoUNGUREANU['parl'].str.contains('parl 16 20')]['ones'].sum()

govParls.loc['Boc', 'own parl'] = ordoBOC[ordoBOC['parl'].str.contains('parl 08 12')]['ones'].sum()
govParls.loc['Boc', 'parl after'] = ordoBOC[ordoBOC['parl'].str.contains('parl 12 16')]['ones'].sum()
govParls.loc['Boc', 'two parls later'] = ordoBOC[ordoBOC['parl'].str.contains('parl 16 20')]['ones'].sum()

govParls.loc['Taric', 'own parl'] = ordoTARICEANU[ordoTARICEANU['parl'].str.contains('parl 04 08')]['ones'].sum()
govParls.loc['Taric', 'parl after'] = ordoTARICEANU[ordoTARICEANU['parl'].str.contains('parl 08 12')]['ones'].sum()
govParls.loc['Taric', 'two parls later'] = ordoTARICEANU[ordoTARICEANU['parl'].str.contains('parl 12 16')]['ones'].sum()

govParls.loc['Bejin', 'own parl'] = ordoBEJINARIU[ordoBEJINARIU['parl'].str.contains('parl 04 08')]['ones'].sum()
govParls.loc['Bejin', 'parl after'] = ordoBEJINARIU[ordoBEJINARIU['parl'].str.contains('parl 08 12')]['ones'].sum()
govParls.loc['Bejin', 'two parls later'] = ordoBEJINARIU[ordoBEJINARIU['parl'].str.contains('parl 12 16')]['ones'].sum()

govParls.loc['Nastase', 'own parl'] = ordoNASTASE[ordoNASTASE['parl'].str.contains('parl 00 04')]['ones'].sum()
govParls.loc['Nastase', 'parl after'] = ordoNASTASE[ordoNASTASE['parl'].str.contains('parl 04 08')]['ones'].sum()
govParls.loc['Nastase', 'two parls later'] = ordoNASTASE[ordoNASTASE['parl'].str.contains('parl 08 12')]['ones'].sum()

govParls.loc['Isar', 'own parl'] = ordoISARESCU[ordoISARESCU['parl'].str.contains('parl 96 00')]['ones'].sum()
govParls.loc['Isar', 'parl after'] = ordoISARESCU[ordoISARESCU['parl'].str.contains('parl 00 04')]['ones'].sum()
govParls.loc['Isar', 'two parls later'] = ordoISARESCU[ordoISARESCU['parl'].str.contains('parl 04 08')]['ones'].sum()

govParls.loc['Athan', 'own parl'] = ordoATHANASIU[ordoATHANASIU['parl'].str.contains('parl 96 00')]['ones'].sum()
govParls.loc['Athan', 'parl after'] = ordoATHANASIU[ordoATHANASIU['parl'].str.contains('parl 00 04')]['ones'].sum()
govParls.loc['Athan', 'two parls later'] = ordoATHANASIU[ordoATHANASIU['parl'].str.contains('parl 04 08')]['ones'].sum()

govParls.loc['Vasile', 'own parl'] = ordoVASILE[ordoVASILE['parl'].str.contains('parl 96 00')]['ones'].sum()
govParls.loc['Vasile', 'parl after'] = ordoVASILE[ordoVASILE['parl'].str.contains('parl 00 04')]['ones'].sum()
govParls.loc['Vasile', 'two parls later'] = ordoVASILE[ordoVASILE['parl'].str.contains('parl 04 08')]['ones'].sum()

govParls.loc['Dejeu', 'own parl'] = ordoDEJEU[ordoDEJEU['parl'].str.contains('parl 96 00')]['ones'].sum()
govParls.loc['Dejeu', 'parl after'] = ordoDEJEU[ordoDEJEU['parl'].str.contains('parl 00 04')]['ones'].sum()
govParls.loc['Dejeu', 'two parls later'] = ordoDEJEU[ordoDEJEU['parl'].str.contains('parl 04 08')]['ones'].sum()

govParls.loc['Ciorbea', 'own parl'] = ordoCIORBEA[ordoCIORBEA['parl'].str.contains('parl 96 00')]['ones'].sum()
govParls.loc['Ciorbea', 'parl after'] = ordoCIORBEA[ordoCIORBEA['parl'].str.contains('parl 00 04')]['ones'].sum()
govParls.loc['Ciorbea', 'two parls later'] = ordoCIORBEA[ordoCIORBEA['parl'].str.contains('parl 04 08')]['ones'].sum()

govParls.loc['Vacaroiu', 'own parl'] = ordoVACAROIU[ordoVACAROIU['parl'].str.contains('parl 92 96')]['ones'].sum()
govParls.loc['Vacaroiu', 'parl after'] = ordoVACAROIU[ordoVACAROIU['parl'].str.contains('96 00')]['ones'].sum()
govParls.loc['Vacaroiu', 'two parls later'] = ordoVACAROIU[ordoVACAROIU['parl'].str.contains('parl 00 04')]['ones'].sum()

govParls.loc['Stolo', 'own parl'] = ordoSTOLOJAN[ordoSTOLOJAN['parl'].str.contains('parl 90 92')]['ones'].sum()
govParls.loc['Stolo', 'parl after'] = ordoSTOLOJAN[ordoSTOLOJAN['parl'].str.contains('parl 92 96')]['ones'].sum()
govParls.loc['Stolo', 'two parls later'] = ordoSTOLOJAN[ordoSTOLOJAN['parl'].str.contains('parl 96 00')]['ones'].sum()

govParls.loc['Orban', 'total'] = ordoORBAN.shape[0]
govParls.loc['Dancila', 'total'] = ordoDANCILA.shape[0]
govParls.loc['Fifor', 'total'] = ordoFIFOR.shape[0]
govParls.loc['Tudose', 'total'] = ordoTUDOSE.shape[0]
govParls.loc['Grind', 'total'] = ordoGRINDEANU.shape[0]
govParls.loc['Ciolos', 'total'] = ordoCIOLOS.shape[0]
govParls.loc['Cimp', 'total'] = ordoCIMPEANU.shape[0]
govParls.loc['Ponta', 'total'] = ordoPONTA.shape[0]
govParls.loc['Ungur', 'total'] = ordoUNGUREANU.shape[0]
govParls.loc['Boc', 'total'] = ordoBOC.shape[0]
govParls.loc['Taric', 'total'] = ordoTARICEANU.shape[0]
govParls.loc['Bejin', 'total'] = ordoBEJINARIU.shape[0]
govParls.loc['Nastase', 'total'] = ordoNASTASE.shape[0]
govParls.loc['Isar', 'total'] = ordoISARESCU.shape[0]
govParls.loc['Athan', 'total'] = ordoATHANASIU.shape[0]
govParls.loc['Vasile', 'total'] = ordoVASILE.shape[0]
govParls.loc['Dejeu', 'total'] = ordoDEJEU.shape[0]
govParls.loc['Ciorbea', 'total'] = ordoCIORBEA.shape[0]
govParls.loc['Vacaroiu', 'total'] = ordoVACAROIU.shape[0]
govParls.loc['Stolo', 'total'] = ordoSTOLOJAN.shape[0]


# print(govParls)

### create df calculating how many (as percentage) ordos for each gov were approved, 
### rejected or abrogated through law by own parl parl after, 2 parl after 

govParls['own parl percent'] = (100*govParls['own parl']).div(govParls['total'].where((govParls['own parl'] != 0) & (govParls['total'] != 0 ), np.nan)) 
govParls['parl after percent'] = (100*govParls['parl after']).div(govParls['total'].where((govParls['parl after'] != 0) & (govParls['total'] != 0 ), np.nan)) 
govParls['two parls later percent'] = (100*govParls['two parls later']).div(govParls['total'].where((govParls['two parls later'] != 0) & (govParls['total'] != 0 ), np.nan))

# print(govParls)


# fig, (ax1,ax2, ax3) = plt.subplots(3,1)

# govParls.plot(y='own parl percent', kind='bar', ax=ax1, color='#005f81')
# govParls.plot(y='parl after percent', kind='bar', ax=ax2, color='#009abc')
# govParls.plot(y='two parls later percent', kind='bar', ax=ax3, sharex=True, color='#00dbf0')

# ax1.spines['top'].set_visible(False)
# ax1.spines['right'].set_visible(False)
# ax1.spines['left'].set_visible(False)
# ax1.tick_params(bottom=False, left=False)
# ax1.set_axisbelow(True)

# ax2.spines['top'].set_visible(False)
# ax2.spines['right'].set_visible(False)
# ax2.spines['left'].set_visible(False)
# ax2.tick_params(bottom=False, left=False)
# ax2.set_axisbelow(True)

# ax3.spines['top'].set_visible(False)
# ax3.spines['right'].set_visible(False)
# ax3.spines['left'].set_visible(False)
# ax3.tick_params(bottom=False, left=False)

# ax1.grid(axis='y', color='gainsboro', linestyle='-', linewidth=1)
# ax2.grid(axis='y', color='gainsboro', linestyle='-', linewidth=1)
# ax3.grid(axis='y', color='gainsboro', linestyle='-', linewidth=1)
# ax3.set_axisbelow(True)
# ax3.tick_params(axis='x', rotation=30)

# plt.tight_layout()
# plt.show()


from datetime import timedelta

hundredDayOrdos = roOrdoNew.copy()

hunDayordoORBAN = hundredDayOrdos.loc[(hundredDayOrdos['date_ordo'] > startORBAN) & (hundredDayOrdos['date_ordo'] <= (startORBAN + timedelta(days=100)))] 
hunDayordoDANCILA = hundredDayOrdos.loc[(hundredDayOrdos['date_ordo'] > startDANCILA) & (hundredDayOrdos['date_ordo'] <= (startDANCILA + timedelta(days=100)))]
hunDayordoFIFOR = hundredDayOrdos.loc[(hundredDayOrdos['date_ordo'] > startFIFOR) & (hundredDayOrdos['date_ordo'] <= (startFIFOR + timedelta(days=100)))]
hunDayordoTUDOSE = hundredDayOrdos.loc[(hundredDayOrdos['date_ordo'] > startTUDOSE) & (hundredDayOrdos['date_ordo'] <= (startTUDOSE + timedelta(days=100)))]
hunDayordoGRINDEANU = hundredDayOrdos.loc[(hundredDayOrdos['date_ordo'] > startGRINDEANU) & (hundredDayOrdos['date_ordo'] <= (startGRINDEANU + timedelta(days=100)))] 
hunDayordoCIOLOS = hundredDayOrdos.loc[(hundredDayOrdos['date_ordo'] > startCIOLOS) & (hundredDayOrdos['date_ordo'] <= (startCIOLOS + timedelta(days=100)))]
hunDayordoCIMPEANU = hundredDayOrdos.loc[(hundredDayOrdos['date_ordo'] > startCIMPEANU) & (hundredDayOrdos['date_ordo'] <= (startCIMPEANU + timedelta(days=100)))]
hunDayordoPONTA = hundredDayOrdos.loc[(hundredDayOrdos['date_ordo'] > startPONTA) & (hundredDayOrdos['date_ordo'] <= (startPONTA + timedelta(days=100)))]
hunDayordoUNGUREANU = hundredDayOrdos.loc[(hundredDayOrdos['date_ordo'] > startUNGUREANU) & (hundredDayOrdos['date_ordo'] <= (startUNGUREANU + timedelta(days=100)))]
hunDayordoBOC = hundredDayOrdos.loc[(hundredDayOrdos['date_ordo'] > startBOC) & (hundredDayOrdos['date_ordo'] <= (startBOC + timedelta(days=100)))]
hunDayordoTARICEANU = hundredDayOrdos.loc[(hundredDayOrdos['date_ordo'] > startTARICEANU) & (hundredDayOrdos['date_ordo'] <= (startTARICEANU + timedelta(days=100)))]
hunDayordoBEJINARIU = hundredDayOrdos.loc[(hundredDayOrdos['date_ordo'] > startBEJINARIU) & (hundredDayOrdos['date_ordo'] <= (startBEJINARIU + timedelta(days=100)))]
hunDayordoNASTASE = hundredDayOrdos.loc[(hundredDayOrdos['date_ordo'] > startNASTASE) & (hundredDayOrdos['date_ordo'] <= (startNASTASE + timedelta(days=100)))]
hunDayordoISARESCU = hundredDayOrdos.loc[(hundredDayOrdos['date_ordo'] > startISARESCU) & (hundredDayOrdos['date_ordo'] <= (startISARESCU + timedelta(days=100)))]
hunDayordoATHANASIU = hundredDayOrdos.loc[(hundredDayOrdos['date_ordo'] > startATHANASIU) & (hundredDayOrdos['date_ordo'] <= (startATHANASIU + timedelta(days=100)))]
hunDayordoVASILE = hundredDayOrdos.loc[(hundredDayOrdos['date_ordo'] > startVASILE) & (hundredDayOrdos['date_ordo'] <= (startVASILE + timedelta(days=100)))]
hunDayordoDEJEU = hundredDayOrdos.loc[(hundredDayOrdos['date_ordo'] > startDEJEU) & (hundredDayOrdos['date_ordo'] <= (startDEJEU + timedelta(days=100)))]
hunDayordoCIORBEA = hundredDayOrdos.loc[(hundredDayOrdos['date_ordo'] > startCIORBEA) & (hundredDayOrdos['date_ordo'] <= (startCIORBEA + timedelta(days=100)))]
hunDayordoVACAROIU = hundredDayOrdos.loc[(hundredDayOrdos['date_ordo'] > startVACAROIU) & (hundredDayOrdos['date_ordo'] <= (startVACAROIU + timedelta(days=100)))]
hunDayordoSTOLOJAN = hundredDayOrdos.loc[(hundredDayOrdos['date_ordo'] > startSTOLOJAN) & (hundredDayOrdos['date_ordo'] <= (startSTOLOJAN + timedelta(days=100)))]

hunDayordoORBAN['guv'] = 'ordoORBAN'
hunDayordoDANCILA['guv'] = 'ordoDANCILA'
hunDayordoFIFOR['guv'] = 'ordoFIFOR'
hunDayordoTUDOSE['guv'] = 'ordoTUDOSE'
hunDayordoGRINDEANU['guv'] = 'ordoGRINDEANU'
hunDayordoCIOLOS['guv'] = 'ordoCIOLOS'
hunDayordoCIMPEANU['guv'] = 'ordoCIMPEANU'
hunDayordoPONTA['guv'] = 'ordoPONTA'
hunDayordoUNGUREANU['guv'] = 'ordoUNGUREANU'
hunDayordoBOC['guv'] = 'ordoBOC'
hunDayordoTARICEANU['guv'] = 'ordoTARICEANU'
hunDayordoBEJINARIU['guv'] = 'ordoBEJINARIU'
hunDayordoNASTASE['guv'] = 'ordoNASTASE'
hunDayordoISARESCU['guv'] = 'ordoISARESCU'
hunDayordoATHANASIU['guv'] = 'ordoATHANASIU'
hunDayordoVASILE['guv'] = 'ordoVASILE'
hunDayordoDEJEU['guv'] = 'ordoDEJEU'
hunDayordoCIORBEA['guv'] = 'ordoCIORBEA'
hunDayordoVACAROIU['guv'] = 'ordoVACAROIU'
hunDayordoSTOLOJAN['guv'] = 'ordoSTOLOJAN'

hundredDayOrdosConcat = pd.concat([hunDayordoORBAN, hunDayordoDANCILA, hunDayordoFIFOR, hunDayordoTUDOSE, 
                                   hunDayordoGRINDEANU, hunDayordoCIOLOS, hunDayordoCIMPEANU, hunDayordoPONTA, 
                                   hunDayordoUNGUREANU, hunDayordoBOC, hunDayordoTARICEANU, hunDayordoBEJINARIU, 
                                   hunDayordoNASTASE, hunDayordoISARESCU, hunDayordoATHANASIU, hunDayordoVASILE, 
                                   hunDayordoDEJEU, hunDayordoCIORBEA, hunDayordoVACAROIU, hunDayordoSTOLOJAN], ignore_index=True) 
 

# print(hundredDayOrdosConcat.head())


hundredDayGovs = [hunDayordoORBAN, hunDayordoDANCILA, hunDayordoFIFOR, hunDayordoTUDOSE, 
                  hunDayordoGRINDEANU, hunDayordoCIOLOS, hunDayordoCIMPEANU, hunDayordoPONTA, 
                  hunDayordoUNGUREANU, hunDayordoBOC, hunDayordoTARICEANU, hunDayordoBEJINARIU, 
                  hunDayordoNASTASE, hunDayordoISARESCU, hunDayordoATHANASIU, hunDayordoVASILE, 
                  hunDayordoDEJEU, hunDayordoCIORBEA, hunDayordoVACAROIU, hunDayordoSTOLOJAN] 


hunDaygovParls = pd.DataFrame(columns = ["aprob", "resp", "abORDO", 'abLAW', 'uitate', 'total'],  
                         index = ['Orban', 'Dancila', 'Fifor', 'Tudose', 'Grind', 'Ciolos', 'Cimp', 'Ponta', 'Ungur', 'Boc', 'Taric', 'Bejin', 'Nastase', 'Isar', 'Athan', 'Vasile', 'Dejeu', 'Ciorbea', 'Vacaroiu', 'Stolo'])

i = 0
for gov in hundredDayGovs:
    hunDaygovParls['aprob'][i] = gov[gov['status'].str.contains('Aprobata')]['ones'].sum()
    hunDaygovParls['resp'][i] = gov[gov['status'].str.contains('Respinsa')]['ones'].sum()
    hunDaygovParls['abORDO'][i] = gov[gov['status'].str.contains('abrogata prin og')]['ones'].sum()
    hunDaygovParls['abLAW'][i] = gov[gov['status'].str.contains('abrogata prin lege')]['ones'].sum()
    hunDaygovParls['uitate'][i] = gov[gov['status'].str.contains('uitata')]['ones'].sum()
    hunDaygovParls['total'][i] = len(gov.index)
    
    i = i + 1

# print(hunDaygovParls)

fig, (ax1,ax2, ax3, ax4,ax5, ax6) = plt.subplots(nrows=6, sharex=True)

ax1.grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.7)
ax2.grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.7)
ax3.grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.7)
ax4.grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.7)
ax5.grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.7)
ax6.grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.7)

ax1.plot(hunDaygovParls['aprob'], label='# ordos that were approved', color='#67ac74')
ax1.legend(frameon=False, loc=1)
ax1.title.set_text('no of ordos issued in first 100 days in office that were...')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.tick_params(bottom=False, left=False)
ax1.tick_params(axis='x', rotation=30)
              
ax2.plot(hunDaygovParls['resp'], label='# ordos that were rejected', color='#b8c49e')
ax2.legend(frameon=False, loc=1)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.tick_params(bottom=False, left=False)
ax2.tick_params(axis='x', rotation=30)

ax3.plot(hunDaygovParls['abORDO'], label='# ordos that were abrog through ordos', color='#ec7d52')
ax3.legend(frameon=False, loc=1)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.spines['bottom'].set_visible(False)
ax3.spines['left'].set_visible(False)
ax3.tick_params(bottom=False, left=False)
ax3.tick_params(axis='x', rotation=30)

ax4.plot(hunDaygovParls['abLAW'], label='# ordos that were abrog through laws', color='#3d996e')
ax4.legend(frameon=False, loc=1)
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)
ax4.spines['bottom'].set_visible(False)
ax4.spines['left'].set_visible(False)
ax4.tick_params(bottom=False, left=False)
ax4.tick_params(axis='x', rotation=30)

ax5.plot(hunDaygovParls['uitate'], label='# ordos that were forgotten', color='#f89758')
ax5.legend(frameon=False, loc=1)
ax5.spines['top'].set_visible(False)
ax5.spines['right'].set_visible(False)
ax5.spines['bottom'].set_visible(False)
ax5.spines['left'].set_visible(False)
ax5.tick_params(bottom=False, left=False)
ax5.tick_params(axis='x', rotation=30)

ax6.plot(hunDaygovParls['total'], label='total ordos in first 100 days', color='#de425b')
ax6.legend(frameon=False, loc=1)
ax6.spines['top'].set_visible(False)
ax6.spines['right'].set_visible(False)
ax6.spines['bottom'].set_visible(False)
ax6.spines['left'].set_visible(False)
ax6.tick_params(bottom=False, left=False)
ax6.tick_params(axis='x', rotation=30)

plt.tight_layout()
plt.show()
